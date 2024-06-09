import pika
import json
import asyncio
from aiosmtplib import send
from email.message import EmailMessage

async def send_email(to_email, subject, content):
    message = EmailMessage()
    message["From"] = "your-email@example.com"
    message["To"] = to_email
    message["Subject"] = subject
    message.set_content(content)

    try:
        await send(message, hostname="smtp.your-email-provider.com", port=587,
                   username="your-email@example.com", password="your-email-password", use_tls=False, start_tls=True)
        print(f"Correo enviado a {to_email}")
    except Exception as e:
        print(f"Error al enviar correo a {to_email}: {e}")

def callback(ch, method, properties, body):
    reserva = json.loads(body)
    mensaje = f"Hola, tu reserva ha sido confirmada."

    # Cambia la dirección de correo electrónico aquí
    destinatario = "destinatario@example.com"
    
    # Envía el correo electrónico al destinatario
    asyncio.run(send_email(destinatario, "Reserva Confirmada", mensaje))

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='reservations')
    channel.basic_consume(queue='reservations', on_message_callback=callback, auto_ack=True)

    print(' [*] Esperando por mensajes. Presiona CTRL+C para salir')
    channel.start_consuming()

if __name__ == "__main__":
    main()

