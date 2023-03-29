import json
import pika
from pika.exceptions import AMQPConnectionError
import django
import os
import sys
import time
from django.core.mail import send_mail


sys.path.append("")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "presentation_mailer.settings")
django.setup()
while True:
    try:
        #ch is channel, method is the message method, properties is the message properteies, body is the message body
        def process_approval(ch, method, properties, body):
            #loads the message body into a python dictionary
            message = json.loads(body)
            #extracts the presenter name, email, and presentation title from the message dictionary
            presenter_name = message["presenter_name"]
            presenter_email = message["presenter_email"]

            subject = "Presentation approved"
            message = f"Hello {presenter_name}, your presentation has been approved"
            from_email = "admin@conference.go"
            recipient_list = [presenter_email]
            #sends the email to the presenter
            send_mail(subject, message, from_email, recipient_list)


        def process_rejection(ch, method, properties, body):
            #loads the message body into a python dictionary
            message = json.loads(body)
            #extracts the presenter name, email, and presentation title from the message dictionary
            presenter_name = message["presenter_name"]
            presenter_email = message["presenter_email"]

            subject = "Presentation Rejected"
            message = f"Hello {presenter_name}. Unfortunately, your presentation has been rejected. Get gud"
            from_email = "admin@conference.go"
            recipient_list = [presenter_email]
            #sends the email to the presenter
            send_mail(subject, message, from_email, recipient_list)


        parameters = pika.ConnectionParameters(host='rabbitmq')
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()
        channel.queue_declare(queue='presentation_approvals')
        channel.basic_consume(
            queue='presentation_approvals',
            on_message_callback=process_approval,
            auto_ack=True,
        )
        channel.queue_declare(queue='presentation_rejections')
        channel.basic_consume(
            queue='presentation_rejections',
            on_message_callback=process_rejection,
            auto_ack=True,
        )
        print("YO WTF MAN")
        channel.start_consuming()

    except AMQPConnectionError:
        print("Could not connect to RabbitMQ")
        time.sleep(2.0)
