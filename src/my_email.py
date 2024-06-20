import smtplib
from email.mime.text import MIMEText

def enviar_alerta_por_correo(mensaje, asunto, desde, destinatario, servidor_smtp, puerto, usuario, contrasena):
    msg = MIMEText(mensaje)
    msg['Subject'] = asunto
    msg['From'] = desde
    msg['To'] = destinatario

    try:
        with smtplib.SMTP(servidor_smtp, puerto) as server:
            server.starttls()
            server.login(usuario, contrasena)
            server.sendmail(desde, destinatario, msg.as_string())
            print("Correo de alerta enviado correctamente.")
    except Exception as e:
        print(f"Error al enviar el correo: {e}")
