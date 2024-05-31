import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM, Dropout
from sklearn.model_selection import train_test_split
from dateutil.rrule import rrule, DAILY
from matplotlib.pylab import rcParams
import warnings
warnings.filterwarnings('ignore')

data = pd.read_csv('FPT.csv')

def preprocess_data(data, symbol):
    df = data[data['symbol'] == symbol]
    df["tradingdate"] = pd.to_datetime(df["tradingdate"]).dt.date
    df["tradingdate"] = pd.to_datetime(df["tradingdate"])

    start_date = df['tradingdate'].min()
    end_date = df['tradingdate'].max()
    records = []

    for d in rrule(DAILY, dtstart=start_date, until=end_date):
        date_check = pd.to_datetime(d.strftime("%Y-%m-%d"))
        if date_check in df['tradingdate'].values:
            df_sub = df[df['tradingdate'].dt.strftime('%Y-%m-%d') == d.strftime("%Y-%m-%d")]
            record = {
                'symbol': df['symbol'].iloc[0],
                'Date': d.strftime("%Y-%m-%d"),
                'Open': df_sub['open'].values[0],
                'High': df_sub['high'].max(),
                'Low': df_sub['low'].min(),
                'Close': df_sub['close'].values[-1],
                'EstMatchedPrice': df_sub['estmatchedprice'].sum()
            }
            records.append(record)

    close_df = pd.DataFrame(records).sort_index(ascending=True)
    close_df.set_index('Date', inplace=True)
    return close_df[['Close']]

def create_train_test_data(close_df, test_size=0.2):
    train_data, test_data = train_test_split(close_df, test_size=test_size, shuffle=False)
    
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(close_df.values)
    
    x_train = np.array([scaled_data[i - 30:i, 0] for i in range(30, len(train_data))])
    y_train = np.array([scaled_data[i, 0] for i in range(30, len(train_data))])
    
    x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))
    
    return x_train, y_train, test_data, scaler

def train_model(x_train, y_train):
    model = Sequential()
    model.add(LSTM(units=50, return_sequences=True, input_shape=(x_train.shape[1], 1)))
    model.add(Dropout(0.1))
    model.add(LSTM(units=50))
    model.add(Dense(1))
    model.compile(optimizer='adam', loss='mse')
    model.fit(x_train, y_train, epochs=1, validation_split=0.2, verbose=1, batch_size=50)
    return model

def predict_next_days(model, last_data, scaler, days=2):
    last_data_scaled = scaler.transform(last_data.reshape(-1, 1))
    
    X_predict = last_data_scaled[-30:].reshape(1, 30, 1)
    predictions = []
    
    for _ in range(days):
        predicted_price = model.predict(X_predict)
        predictions.append(predicted_price[0, 0])
        
        X_predict = np.append(X_predict[:, 1:, :], predicted_price.reshape(1, 1, 1), axis=1)
    
    predictions = scaler.inverse_transform(np.array(predictions).reshape(-1, 1))
    return predictions

def calculate_percentage_change(predictions, current_price):
    percentage_changes = [(pred[0] - current_price) / current_price * 100 for pred in predictions]
    return percentage_changes

symbols = data['symbol'].unique()

def main():
    for symbol in symbols:
        print(symbol)
        close_df = preprocess_data(data, symbol)
        x_train, y_train, test_data, scaler = create_train_test_data(close_df)
        model = train_model(x_train, y_train)
        
        last_data = close_df.values[-30:]
        current_price = close_df.values[-1, 0]
        predictions = predict_next_days(model, last_data, scaler, days=2)
        
        percentage_changes = calculate_percentage_change(predictions, current_price)
        
        for i, (pred, change) in enumerate(zip(predictions, percentage_changes), 1):
            print(f'Predicted close price for {symbol} day {i}: {pred[0]:.2f} ({change:.2f}%)')
        print(symbol, close_df.index[-1], current_price, predictions[0][0], predictions[1][0])
        # thêm dữ liệu vào bảng predict_price
        insert_query = """
        INSERT INTO predict_price (symbol, date, close_price, next_day_price, next_2_day_price)
        VALUES (%s, %s, %s, %s, %s)
        """
        conn = psycopg2.connect(
            host="54.254.170.147",
            database="postgres",
            user="dbmasteruser",
            password="ZinNopassword"
        )

        cur = conn.cursor()
        try:
            cur.execute(insert_query, (symbol, close_df.index[-1], float(current_price), float(predictions[0][0]), float(predictions[1][0])))
        except Exception as e:
            print("Failed to insert data:", e)
        conn.commit()
        cur.close()
        conn.close()
        print("Data inserted successfully")

