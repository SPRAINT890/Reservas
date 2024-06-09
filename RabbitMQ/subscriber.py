import pika
import json
import asyncio
import os
from aiosmtplib import send
from email.message import EmailMessage

async def send_email(to_email, subject, content):
    message = EmailMessage()
    message["From"] = os.environ['EMAIL_FROM']
    message["To"] = to_email
    message["Subject"] = subject
    message.set_content(content)

    try:
        await send(message, hostname=os.environ['SMTP_HOST'], port=int(os.environ['SMTP_PORT']),
                   username=os.environ['SMTP_USER'], password=os.environ['SMTP_PASS'], use_tls=False, start_tls=True)
        print(f"Correo enviado a {to_email}")
    except Exception as e:
        print(f"Error al enviar correo a {to_email}: {e}")

def callback(ch, method, properties, body):
    reserva = json.loads(body)
    mensaje = f"Hola, tu reserva ha sido confirmada."

    destinatario = reserva['cliente']['email']

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(send_email(destinatario, "Reserva Confirmada", mensaje))
    loop.close()

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
    channel = connection.channel()
    channel.queue_declare(queue='Reservations')
    channel.basic_consume(queue='Reservations', on_message_callback=callback, auto_ack=True)

    print(' [*] Esperando por mensajes. Presiona CTRL+C para salir')
    channel.start_consuming()

if __name__ == "__main__":
    main()
