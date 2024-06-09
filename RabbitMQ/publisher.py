import pika
import json

def publish_message():
    # Establece la conexión con el servidor RabbitMQ
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    # Declara la cola en la que se publicará el mensaje
    channel.queue_declare(queue='reservations')

    # Define el mensaje a enviar
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

    # Convierte el mensaje a formato JSON
    message = json.dumps(reserva)

    # Publica el mensaje en la cola
    channel.basic_publish(exchange='', routing_key='reservations', body=message)

    # Imprime un mensaje de confirmación
    print(" [x] Sent 'Reservation made'")

    # Cierra la conexión
    connection.close()

if __name__ == "__main__":
    publish_message()

