import os
import ujson
from time import sleep
from utils import check_sites
import threading
from kafka import KafkaProducer
from kafka.admin import NewTopic, KafkaAdminClient
from kafka.errors import TopicAlreadyExistsError


CWD = os.getcwd()


class Producer(threading.Thread):
    daemon = True

    def __init__(self, sites, interval, kafka_host, kafka_port, access_key, access_cert, ca_cert):        
        super(Producer, self).__init__()        
        self.sites = sites
        self.interval = interval
        self.kafka_host = kafka_host
        self.kafka_port = kafka_port
        self.access_key = access_key
        self.access_cert = access_cert
        self.ca_cert = ca_cert
        self.producer = self.get_producer()

    def get_uri(self):
        return '{0}:{1}'.format(self.kafka_host, self.kafka_port)

    def get_producer(self):   
        return KafkaProducer(
            bootstrap_servers=self.get_uri(),
            security_protocol='SSL',
            ssl_cafile=self.ca_cert,
            ssl_certfile=self.access_cert,
            ssl_keyfile=self.access_key,
            value_serializer=lambda v: ujson.dumps(v).encode('utf-8')
        )


    def get_admin_client(self):
        client = KafkaAdminClient(
            bootstrap_servers=self.get_uri(),
            security_protocol='SSL',
            ssl_cafile=self.ca_cert,
            ssl_certfile=self.access_cert,
            ssl_keyfile=self.access_key
        )


    def create_topic(self, topic):
        topics = []
        topics.append(NewTopic(name=topic, num_partitions=1, replication_factor=3))
        try:
            get_admin_client().create_topics(new_topics=topics, validate_only=False)        
            return True
        except TopicAlreadyExistsError:
            return False


    def delete_topics(self, topics):
        try:
            get_admin_client().delete_topics(topics)
            return True
        except UnknownTopicOrPartitionError:
            return False

    def producer_process(self):
        if len(self.sites) > 0:
            while True:
                status_list = check_sites(self.sites)
                if len(status_list) > 0:
                    for status in status_list:
                        self.producer.send('site_status', status)        

                sleep(self.interval)

    def run(self):
        self.producer_process()