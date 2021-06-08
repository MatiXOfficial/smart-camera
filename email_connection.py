import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage


class EmailConnection:
	
	def __init__(self, config):
		self.from_email = config.email_from
		self.from_email_password = config.email_from_password
		self.to_email = config.email_to
			
	def send_email(self, frame):
		try:
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
		except smtplib.SMTPAuthenticationError:
			print(f'Could not send the email. Wrong username or password.')
		except smtplib.SMTPRecipientsRefused:
			print(f'Could not send the email to {self.to_email}. Wrong recipient address.')
		except TypeError:
			print('Could not send the email. Check the configuration.')
		except Exception as e:
			print('Could not send the email.')
