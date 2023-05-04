import os
from dotenv import load_dotenv
import os
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def forgot_password_format(email, reset_code):
    """
    Structure for Forgot Password Reset Link.
    Parameters
    ----------------------------------------------------------
    reset_code: str - Token to reset Password
    email: User Object - Current Logged-In User Session
    ----------------------------------------------------------
    Returns
    ----------------------------------------------------------
    response: str - Mail Body
    """
    subject = "Reset Password Request"
    recipient = email
    message = """
        <!DOCTYPE html>
        <html>
        <title>Reset Password</title>
        <body>
        <h3>Hello, {0:}</h3>
        <p>Password Reset Request has been received by Someone.</p>
        <p>Below is the code to Reset Your Password. Use it to reset your password<br><u>{1}</u></p>
        <p>If you did not requested, You can ignore this mail!<p>
        </body>
        </html>
        """.format(email, reset_code)
    return subject, recipient, message


def send_email(subject, to, text):
    """
    Function Call when Email process execution takes place.
    Parameters
    ----------------------------------------------------------
    subject: str - Mail Subject
    to: str - List of Recipients
    text: str - Mail Body Message
    ----------------------------------------------------------
    Returns
    ----------------------------------------------------------
    response: Mail object - Mail Sent or not
    """
    try:
        load_dotenv()
        MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
        MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
        MAIL_PORT = os.environ.get('MAIL_PORT')
        MAIL_SERVER = os.environ.get('MAIL_SERVER')

        """Defining The Message"""
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = MAIL_USERNAME
        msg["To"] = to

        part = MIMEText(text, "html")
        msg.attach(part)

        context = ssl.create_default_context()
        """Create your SMTP session"""
        with smtplib.SMTP_SSL(MAIL_SERVER, int(MAIL_PORT), context=context) as server:
            # User Authentication
            server.login(MAIL_USERNAME, MAIL_PASSWORD)
            """Sending the Email"""
            server.sendmail(
                MAIL_USERNAME, to, msg.as_string()
            )

    except Exception as ex:
        print("Something went wrong....", ex)
