# %%
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime

today = datetime.today().date()

# config email
sender_email = "sylv.srv24@gmail.com"
receiver_email = "sy2000dn0@gmail.com"
app_password = "plmq fgrj mvdx dsqh"  # Sử dụng App Password thay vì mật khẩu chính

# config header: subject, from, to
msg = MIMEMultipart()
msg['From'] = sender_email
msg['To'] = receiver_email
msg['Subject'] = f"[Crawl data] Output {today}"

# body
body = "Hello, here is an email with an attachment of crawl data results for GSM-Forum and Youtube"
msg.attach(MIMEText(body, 'plain'))


# %%
# path
filename = f"output_{today}.xlsx"
attachment = open(f"{filename}", "rb")

# Định dạng file đính kèm
part = MIMEBase('application', 'octet-stream')
part.set_payload((attachment).read())
encoders.encode_base64(part)
part.add_header('Content-Disposition', f"attachment; filename= {filename}")

# add attachment
msg.attach(part)

# %%
# Thiết lập server SMTP và gửi email
try:
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()  # Bảo mật kết nối
    server.login(sender_email, app_password)
    text = msg.as_string()
    server.sendmail(sender_email, receiver_email, text)
    print("Email đã được gửi thành công!")
except Exception as e:
    print(f"Không thể gửi email. Lỗi: {str(e)}")
finally:
    server.quit()
    attachment.close()


