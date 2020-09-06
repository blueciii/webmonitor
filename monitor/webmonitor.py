import click
import ujson
from time import sleep
from producer import Producer
from consumer import Consumer
from database import Database


needed_files = ['service.cert', 'ca.pem', 'service.key']


def monitor(
    db_name, 
    db_host, 
    db_port, 
    db_user, 
    db_password, 
    kafka_host, 
    kafka_port, 
    sites, 
    interval, 
    access_key, 
    access_cert, 
    ca_cert):
    
    database = Database(
        db_host, 
        db_port, 
        db_name, 
        db_user, 
        db_password
    )

    if database is None:
        print('error setting up the database')
    else:
        threads = [
            Producer(
                sites=sites, 
                interval=interval, 
                kafka_host=kafka_host, 
                kafka_port=kafka_port, 
                access_key=access_key, 
                access_cert=access_cert, 
                ca_cert=ca_cert
            ),
            Consumer(
                kafka_host=kafka_host, 
                kafka_port=kafka_port, 
                database=database, 
                access_key=access_key, 
                access_cert=access_cert, 
                ca_cert=ca_cert
            )
        ]

        for thread in threads:
            thread.start()

        print('running site monitor')
        while True:
            sleep(60)


@click.command()
@click.option('--db_name', required=True)
@click.option('--db_host', required=True)
@click.option('--db_port', required=True, type=int)
@click.option('--db_user', required=True)
@click.option('--db_password', required=True)
@click.option('--kafka_host', required=True)
@click.option('--kafka_port', required=True, type=int)
@click.argument('sites', type=click.File('r'), required=True)
@click.option('--interval', default=30, help='check interval', type=int)
@click.option('--access_key', required=True, type=click.Path(exists=True))
@click.option('--access_cert', required=True, type=click.Path(exists=True))
@click.option('--ca_cert', required=True, type=click.Path(exists=True))
def run(db_name, db_host, db_port, db_user, db_password, kafka_host, kafka_port, interval, sites, access_key, access_cert, ca_cert):
    file_data = sites.read()
    sites_to_monitor = ujson.loads(file_data)
    monitor(
        db_name=db_name, 
        db_host=db_host, 
        db_port=db_port, 
        db_user=db_user, 
        db_password=db_password, 
        kafka_host=kafka_host, 
        kafka_port=kafka_port, 
        interval=interval, 
        sites=sites_to_monitor,
        access_key=access_key,
        access_cert=access_cert,
        ca_cert=ca_cert
    )


if __name__ == '__main__':
    run()
