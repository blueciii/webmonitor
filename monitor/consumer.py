import os
import sys
import ujson
import threading
from datetime import datetime
from kafka import KafkaConsumer


CWD = os.getcwd()
        

class Consumer(threading.Thread):
    daemon = True

    def __init__(self, kafka_host, kafka_port, database, access_key, access_cert, ca_cert):
        super(Consumer, self).__init__()
        self.kafka_host = kafka_host
        self.kafka_port = kafka_port
        self.database = database
        self.access_key = access_key
        self.access_cert = access_cert
        self.ca_cert = ca_cert
        self.consumer = self.get_consumer()

    def get_uri(self):
        return '{0}:{1}'.format(self.kafka_host, self.kafka_port)

    def get_consumer(self):
        return KafkaConsumer(
            auto_offset_reset='earliest',
            bootstrap_servers=self.get_uri(),
            client_id='website-monitor-client',
            group_id='website-monitor-group',
            security_protocol='SSL',
            ssl_cafile=self.ca_cert,
            ssl_certfile=self.access_cert,
            ssl_keyfile=self.access_key
        )


    def consumer_process(self):
        self.consumer.subscribe(['site_status'])

        for message in self.consumer:
            data = ujson.loads(message.value)
            self.database.write_data(
                data.get('site', None), 
                data.get('httpcode'), 
                data.get('duration', None), 
                data.get('pattern', None), 
                data.get('error', None), 
                data.get('history', None), 
                datetime.now()
            )


    def run(self):       
        self.consumer_process()        
