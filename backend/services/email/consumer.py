from confluent_kafka import Consumer, KafkaError
import json
import os
from dotenv import load_dotenv
import sys
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
#from pathlib import Path

# Ajusta o caminho para o .env (dois níveis acima)
ENV_PATH = '/app/.env'
load_dotenv(ENV_PATH)

# Force Python to flush prints immediately
sys.stdout.reconfigure(line_buffering=True)

def send_magic_link_email(email: str, token: str) -> bool:
    """Send magic link email to user"""
    try:
        # Email settings
        smtp_server = os.getenv('SMTP_SERVER')
        smtp_port = os.getenv('SMTP_PORT')
        smtp_username = os.getenv('SMTP_USERNAME')
        smtp_password = os.getenv('SMTP_PASSWORD')
        
        print(f"Loading SMTP settings from: {ENV_PATH}", flush=True)
        print(f"SMTP Settings: server={smtp_server}, port={smtp_port}, username={smtp_username}", flush=True)
        
        if not all([smtp_server, smtp_port, smtp_username, smtp_password]):
            raise ValueError("Missing SMTP configuration")
        
        # Create message
        msg = MIMEMultipart()
        msg['From'] = smtp_username
        msg['To'] = email
        msg['Subject'] = 'Your PetSpa Login Link'
        
        # Create magic link
        magic_link = f"http://localhost:3000/auth/verify?token={token}"
        
        # Email body
        body = f"""
        Hello!
        
        Click the link below to log in:
        {magic_link}
        
        This link will expire in 15 minutes.
        
        If you didn't request this link, please ignore this email.
        """
        
        msg.attach(MIMEText(body, 'plain'))
        
        # Send email
        with smtplib.SMTP(smtp_server, int(smtp_port)) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.send_message(msg)
            
        print(f"Magic link email sent to {email}", flush=True)
        return True
        
    except Exception as e:
        print(f"Error sending email: {e}", flush=True)
        return False

def create_consumer():
    """Create and return a Kafka consumer"""
    config = {
        'bootstrap.servers': os.getenv('KAFKA_BROKERS', 'kafka:9092'),
        'group.id': 'email_service_group',
        'auto.offset.reset': 'earliest',
        'enable.auto.commit': True,
        'allow.auto.create.topics': True,
        'group.instance.id': 'email_instance_1',
        'session.timeout.ms': 45000
    }
    return Consumer(config)

def main():
    print("Starting email consumer...", flush=True)
    print(f"Environment loaded from: {ENV_PATH}", flush=True)
    
    try:
        consumer = create_consumer()
        topic = 'magic-links.created'
        consumer.subscribe([topic])
        print(f"Subscribed to topic: {topic}", flush=True)
        
        while True:
            msg = consumer.poll(timeout=1.0)
            
            if msg is None:
                continue
                
            if msg.error():
                if msg.error().code() != KafkaError._PARTITION_EOF:
                    print(f"Error: {msg.error()}", flush=True)
                continue
                
            try:
                value = json.loads(msg.value().decode('utf-8'))
                print(f"Received: {value}", flush=True)
                
                # Send magic link email
                if 'email' in value and 'token' in value:
                    send_magic_link_email(value['email'], value['token'])
                else:
                    print("Invalid message format: missing email or token", flush=True)
                    
            except Exception as e:
                print(f"Error processing message: {e}", flush=True)

    except Exception as e:
        print(f"Critical error: {e}", flush=True)
    finally:
        consumer.close()

if __name__ == "__main__":
    main()
