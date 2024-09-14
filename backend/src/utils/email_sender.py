from backend.src.config import Config
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