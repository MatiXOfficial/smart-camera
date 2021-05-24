import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage


class EmailConnection:
	
	def __init__(self):
		self.from_email = 'matixmateusz52@gmail.com'
		self.from_email_password = 'mateusz52'
		self.to_email = 'matixmateusz52@gmail.com'
			
	def send_email(self, frame):
		msgRoot = MIMEMultipart('related')
		msgRoot['Subject'] = 'Face Detection Alert'
		msgRoot['From'] = self.from_email
		msgRoot['To'] = self.to_email
		msgRoot.preamble = 'Raspberry pi security camera update'

		msgAlternative = MIMEMultipart('alternative')
		msgRoot.attach(msgAlternative)
		msgText = MIMEText('Smart security cam found object')
		msgAlternative.attach(msgText)

		msgText = MIMEText('<img src="cid:frame">', 'html')
		msgAlternative.attach(msgText)

		msgImage = MIMEImage(frame)
		msgImage.add_header('Content-ID', '<frame>')
		msgRoot.attach(msgImage)

		smtp = smtplib.SMTP('smtp.gmail.com', 587)
		smtp.starttls()
		smtp.login(self.from_email, self.from_email_password)
		smtp.sendmail(self.from_email, self.to_email, msgRoot.as_string())
		smtp.quit()
