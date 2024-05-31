# import config
import json
from ssi_fc_data.fc_md_stream import MarketDataStream
from ssi_fc_data.fc_md_client import MarketDataClient

import time
from threading import Thread, Event

class Config():
    auth_type = 'Bearer'

    consumerID = 'a14ee41b0b6d4eb8990d8a17215151d4'
    consumerSecret = '590b66ec64e947ea92afb799de009efb'

    url = 'https://fc-data.ssi.com.vn/'  
    stream_url = 'https://fc-data.ssi.com.vn/'

config = Config()

class MarketDataHandler:
    def __init__(self, channel) -> None:
        self.source = None
        self.data_received_event = Event()
        self.channel = channel

    def get_market_data(self, message):
        self.source = json.loads(message['Content'])
        self.data_received_event.set()

    def get_error(self, error):
        print(error)

    def main(self):
        self.source = None
        selected_channel = self.channel
        mm = MarketDataStream(config, MarketDataClient(config))
        mm.start(self.get_market_data, self.get_error, selected_channel)
        self.data_received_event.wait(timeout=1)

