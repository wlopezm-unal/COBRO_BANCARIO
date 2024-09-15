import smtplib
from email.message import EmailMessage
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email( estado_prestamo, nombre):

    # Configurar los detalles del correo
    email_address = ''
    password = ''
    recipient = ''
    subject = 'Incumplimiento con el pago del prestamo'
    message = f"Buenos días {nombre}, para informarle que el pago de su prestamo esta vencido, por favor realizar el respectivo pronto. Muchas gracias por su atención."

    # Configurar el servidor SMTP
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587

    # Crear el mensaje
    msg = MIMEMultipart()
    msg['From'] = email_address
    msg['To'] = recipient
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))

    # Iniciar la conexión con el servidor SMTP
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        # Iniciar sesión en la cuenta de correo
        server.login(email_address, password)
        # Enviar el correo
        server.sendmail(email_address, recipient, msg.as_string())
        print('Correo enviado exitosamente!')
    except Exception as e:
        print(f'Error al enviar el correo: {str(e)}')
    finally:
        # Cerrar la conexión con el servidor SMTP
        server.quit()

   
