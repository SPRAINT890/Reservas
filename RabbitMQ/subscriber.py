import pika
import json
import asyncio
import os
from aiosmtplib import send
from email.message import EmailMessage

async def send_email(to_email, subject, content):
    message = EmailMessage()
    message["From"] = 'spraint098@gmail.com'
    message["To"] = to_email
    message["Subject"] = subject
    message.set_content(content)

    try:
        await send(message, hostname="smtp.gmail.com", port=587,
                   username='spraint098@gmail.com', password='bfxbjtjzqlwluymx', use_tls=False, start_tls=True)
        print(f"Correo enviado a {to_email}")
    except Exception as e:
        print(f"Error al enviar correo a {to_email}: {e}")

def callback(ch, method, properties, body):
    reserva = json.loads(body)
    mensaje =  "Estimado " + reserva['cliente']['nombre'] + ", tu reserva a sido confirmada en " + reserva['restaurante']['nombre']

    destinatario = reserva['cliente']['email']

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(send_email(destinatario, "Reserva Confirmada", mensaje))
    loop.close()

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='Reservations')
    channel.basic_consume(queue='Reservations', on_message_callback=callback, auto_ack=True)

    print(' [*] Esperando por mensajes. Presiona CTRL+C para salir')
    channel.start_consuming()

if __name__ == "__main__":
    main()
