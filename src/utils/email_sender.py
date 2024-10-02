"""
The function `sending_email` sends an email with the specified subject and body to the provided
email address using SMTP.

:param email: The `email` parameter in the `sending_email` function is the email address of the
recipient to whom you want to send the email
:param sub: The `sub` parameter in the `sending_email` function stands for the subject of the email
that you want to send. It is a string that represents the subject line of the email message. This
subject will be displayed in the recipient's email inbox to give them an idea of what the email is
:param body_data: The `body_data` parameter in the `sending_email` function is the content or body
of the email that you want to send. It should be a string containing the message you want to include
in the email body
:return: The function `sending_email` is returning a JSONResponse with a success message "Mail send
successfully" and a status code of 200 if the email is sent successfully. If there is an exception
during the email sending process, it will return a JSONResponse with an error message describing the
exception.
"""
from src.config import Config
from email.mime.text import MIMEText
import smtplib
from email.mime.multipart import MIMEMultipart
from fastapi.responses import JSONResponse

def sending_email(email,sub,body_data):

        receiver_email = email
        subject = sub
        body = body_data
        try:
            server = smtplib.SMTP(Config.MAIL_HOST, Config.MAIL_PORT)
            server.starttls()
            server.login(Config.MAIL_USERNAME, Config.MAIL_PASSWORD)
            
            msg = MIMEMultipart()
            msg['From'] = Config.MAIL_USERNAME
            msg['To'] = receiver_email
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'plain'))
            
            server.send_message(msg)
            server.quit()
        except Exception as e:
            return {"error": str(e)}
        return JSONResponse({"Message": "Mail send successfully"}, status_code=200)