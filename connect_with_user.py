import smtplib
from email.message import EmailMessage


def send_email(email, coin, action):
    msg = EmailMessage()
    msg.set_content(f"This is notification about stocks: {coin}")
    if action == "buy":
        msg['Subject'] = f"Time to buy stock: {coin}"
    elif action == "sell":
        msg['Subject'] = f"Time to sell stock: {coin}"
    msg['From'] = "malkovila32@gmail.com"
    msg['To'] = email

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login("malkovila32@gmail.com", "Ilia1234")
        server.send_message(msg)
        server.quit()
        print('Email sent successfully.')
    except Exception as e:
        print(f'Error sending email: {e}')


