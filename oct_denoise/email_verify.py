import smtplib
from email.mime.text import MIMEText
import random


def send_mail(host, user, pwd, receiver, content, title):
    message = MIMEText(content, "plain", "utf-8")
    message["Subject"] = title
    message["From"] = user
    message["To"] = receiver

    smtp_obj = smtplib.SMTP()
    smtp_obj.connect(host, 25)
    smtp_obj.login(user, pwd)
    smtp_obj.sendmail(user, receiver, message.as_string())


def generate_code():
    code = random.sample(list(range(10)), 6)
    code = list(map(lambda x: str(x), code))
    code = ''.join(code)
    return code


if __name__ == "__main__":
    code = generate_code()
    print(code)
    email_content = "Your verify code is：%s" % code
    email_title = "Verify code"

    send_mail(
        host="smtp.qq.com",
        user="2891206380@qq.com",
        pwd="oaqyjkbbypyhdhef",
        receiver="2112165916@qq.com",
        content=email_content,
        title=email_title
    )
