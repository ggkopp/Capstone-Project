import pika
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def callback(ch, method, properties, body):
    message_time, message_data = body.decode().split(',', 1)
    logging.info(f" [x] Received '{message_data}' from {method.routing_key} at {message_time}")

def main(hn: str = "localhost"):
    try:
        credentials = pika.PlainCredentials('guest', '12121212')
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=hn, credentials=credentials)
        )
        channel = connection.channel()

        # Declare the queues to consume from
        channel.queue_declare(queue='buoy_data', durable=True)
        channel.queue_declare(queue='buoy_data_alerts', durable=True)

        # Set up the callback function for message processing
        channel.basic_consume(queue='buoy_data', on_message_callback=callback, auto_ack=True)
        channel.basic_consume(queue='buoy_data_alerts', on_message_callback=callback, auto_ack=True)

        logging.info(' [*] Waiting for messages. To exit press CTRL+C')
        channel.start_consuming()

    except KeyboardInterrupt:
        logging.info("KeyboardInterrupt. Stopping the listener.")
    except Exception as e:
        logging.error("An unexpected error occurred: {}".format(e))
    finally:
        logging.info("\nClosing connection. Goodbye.\n")
        connection.close()

if __name__ == "__main__":
    main("localhost")
