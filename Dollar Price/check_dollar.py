import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import requests

# 1. Leer las variables del entorno (se definen en GitHub Secrets)
TARGET_PRICE = float(os.getenv("TARGET_PRICE", "1500"))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL")


def send_email(subject, body):
  msg = MIMEMultipart()
  msg["From"] = SMTP_USER
  msg["To"] = RECEIVER_EMAIL
  msg["Subject"] = subject

  msg.attach(MIMEText(body, "plain", "utf-8"))

  # Configuración para servidor SMTP de Gmail
  with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
    server.login(SMTP_USER, SMTP_PASSWORD)
    server.send_message(msg)


def main():
  # API pública de cotización del dólar blue (o cambia a /v1/dolares/oficial, etc.)
  url = "https://dolarapi.com/v1/dolares/blue"
  response = requests.get(url)
  response.raise_for_status()
  data = response.json()

  precio_compra = float(data["compra"])
  nombre = data.get("nombre", "Dólar")

  print(f"Cotización actual de {nombre}: ${precio_compra}")

  # Condición: notificar si la compra supera o iguala el precio objetivo
  if precio_compra >= TARGET_PRICE:
    subject = f"🚨 Alerta Dólar: ¡Alcanzó los ${precio_compra}!"
    body = (
        f"El precio del {nombre} ({data.get('casa', 'blue')}) ha alcanzado tu"
        f" objetivo.\n\nPrecio actual (compra): ${precio_compra}\nPrecio"
        f" objetivo: ${TARGET_PRICE}\nÚltima actualización:"
        f" {data.get('fechaActualizacion')}"
    )

    send_email(subject, body)
    print("Notificación enviada por correo electrónico.")
  else:
    print(
        f"El precio (${precio_compra}) está por debajo de tu objetivo"
        f" (${TARGET_PRICE}). No se envía correo."
    )


if __name__ == "__main__":
  main()