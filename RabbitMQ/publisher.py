import pika
import json
import os

def publish_message():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=os.environ.get('RABBITMQ_HOST', 'localhost')))
    channel = connection.channel()

    channel.queue_declare(queue='Reservations')

    reserva = {
        "cliente": {
            "nombre": "Juan Perez",
            "email": "juan.perez@example.com"
        },
        "restaurante": {
            "nombre": "Restaurante A",
            "mesas": 10
        }
    }

    message = json.dumps(reserva)
    channel.basic_publish(exchange='', routing_key='Reservations', body=message)

    print(" [x] Sent 'Reservation made'")
    connection.close()

if __name__ == "__main__":
    publish_message()
