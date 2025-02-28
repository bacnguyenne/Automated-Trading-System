# Automated Trading Data Platform

Welcome to the Automated Trading System repository! This project is designed to facilitate automated trading by providing tools for data streaming, analysis, and execution of trading strategies.

## Installation

To set up the Automated Trading System locally, follow these steps:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/bacnguyenne/Automated-Trading-System.git
   cd Automated-Trading-System
   ```

2. **Install Dependencies**:
   Ensure you have [Python](https://www.python.org/downloads/) installed.

   ```bash
   pip install -r requirements.txt
   ```
2. **Setup [Fast Connect API](https://www.ssi.com.vn/khach-hang-ca-nhan/fast-connect-api) follow guideline.**

## Usage

1. **Data Streaming**:
   - Edit your API infomation in file `api_fc_data.txt` and `config.py` 
    
   - Navigate to the `StreamingData` directory and run the data collection script:
     ```bash
     cd StreamingData
     docker compose up -d --build
     ```

2. **Running the Django Web Application**

To run the Django web application in the `AutomatedTradingSystem` directory, follow these steps:

- **Navigate to the Project Directory**  
   ```bash
   cd AutomatedTradingSystem
   ```

- **Ensure Dependencies are Installed**  
   Before starting the server, make sure all necessary dependencies are installed and database migrations are applied:
   ```bash
   python manage.py migrate
   ```

- **Start the Django Development Server**  
   ```bash
   python manage.py runserver
   ```

   This command will start the Django development server at `http://127.0.0.1:8000/`.

## If you have any questions, concerns or contributions, please contact me via:
- email: nguyendinhnguyenbac@gmail.com
- facebook: https://www.facebook.com/bac2012.dz

