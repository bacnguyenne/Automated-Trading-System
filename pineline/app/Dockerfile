FROM python:3.9.11
WORKDIR /app
COPY . .
RUN pip install --upgrade pip
RUN pip install requests kafka-python schedule psycopg2-binary
RUN pip install dist/ssi_fc_data-2.2.1.tar.gz
CMD ["python", "./pineline_stock.py"]