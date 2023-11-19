import pika
import csv
import time
import logging
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def clean_wave_height(wave_height_str):
    cleaned_str = ''.join(c if c.isdigit() or c in ('.', ',') else ' ' for c in wave_height_str)
    parts = cleaned_str.split('.')
    if len(parts) > 2:
        cleaned_str = '.'.join(parts[:-1]) + '.' + parts[-1]
    cleaned_str = cleaned_str.replace(',', '.')
    return float(cleaned_str.strip())

def send_data_to_queue(channel, queue_name, data):
    try:
        # Declare a durable queue named 'buoy_data'
        channel.queue_declare(queue=queue_name, durable=True)

        # Convert the data to a string
        message = f"{datetime.now().strftime('%m/%d/%y %H:%M:%S')},{data}"

        # Publish the message to the 'buoy_data' queue
        channel.basic_publish(
            exchange='',
            routing_key=queue_name,
            body=message,
            properties=pika.BasicProperties(
                delivery_mode=2,  # Make the message persistent
            )
        )

        logging.info(f" [x] Sent '{message}' to {queue_name}")

    except Exception as e:
        logging.error("Error sending data to {} queue: {}".format(queue_name, e))

def send_email(subject, body):
    # Email configuration
    sender_email = "sclarrettsklopp@gmail.com"
    receiver_email = "sclarrettsklopp@gmail.com"
    password = "ogwz fcfb ywkq dscp"  

    # Setup the MIME
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = "Severe Wave Warning"

    # Attach the body to the email
    message.attach(MIMEText(body, "plain"))

    # Connect to the Gmail server and send the email
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())
        logging.info("Email notification sent.")
    except smtplib.SMTPException as smtp_exc:
        logging.error(f"SMTP Exception: {smtp_exc}")
    except Exception as e:
        logging.error(f"Error sending email: {e}")

def main(hn: str = "localhost"):
    try:
        credentials = pika.PlainCredentials('guest', '12121212')
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=hn, credentials=credentials)
        )
        channel = connection.channel()

        # Move queue declaration outside the loop to avoid redeclaration
        channel.queue_declare(queue='buoy_data', durable=True)
        channel.queue_declare(queue='buoy_data_alerts', durable=True)

        while True:
            with open('Buoydata_modified.csv', 'r') as file:
                reader = csv.reader(file)
                header = next(reader)  # Get header row

                if 'time_UTC' in header:
                    time_utc_index = header.index('time_UTC')  # Find the index of time_utc column

                    for row in reader:
                        try:
                            station_id = row[0]  # Assuming station_id is at index 0
                            wave_height = clean_wave_height(row[6])
                            wind_speed = float(row[4])  # Assuming wind_speed is at index 6
                            wind_gust = float(row[5])   # Assuming wind_gust is at index 7

                            # Check for severe weather conditions
                            if wave_height * wind_gust > 95 or wave_height * wind_speed > 95:
                                warning_message = f"SEVERE WEATHER WARNING AT STATION {station_id}"
                                send_data_to_queue(channel, 'buoy_data_alerts', warning_message)
                                send_email("Severe Weather Alert", "{}\nSevere weather conditions detected.".format(warning_message))

                            # Send the result of the parameter equation to the 'buoy_data' queue
                            send_data_to_queue(channel, 'buoy_data', wave_height * wind_gust)
                        except ValueError as ve:
                            logging.error("Error processing row {}: {}".format(row, ve))
                        except Exception as e:
                            logging.error("An unexpected error occurred: {}".format(e))

                        time.sleep(.2)  # Simulate delay between data points
                else:
                    logging.error("Column 'time_UTC' not found in the CSV header.")

    except KeyboardInterrupt:
        logging.info("KeyboardInterrupt. Stopping the program.")
    except Exception as e:
        logging.error("An unexpected error occurred: {}".format(e))
    finally:
        logging.info("\nClosing connection. Goodbye.\n")
        connection.close()

if __name__ == "__main__":
    main("localhost")
