# import config
import json
from ssi_fc_data.fc_md_stream import MarketDataStream
from ssi_fc_data.fc_md_client import MarketDataClient
import time
from threading import Thread, Event
import config

class Config():
    auth_type = config.auth_type
    consumerID = config.consumerID
    consumerSecret = config.consumerSecret
    url = config.url
    stream_url = config.stream_url

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

