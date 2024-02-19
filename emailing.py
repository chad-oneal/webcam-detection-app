import smtplib  # Importing the SMTP library for sending emails
import imghdr  # Importing the imghdr library to determine the image type
from email.message import EmailMessage  # Importing the EmailMessage class for email composition

PASSWORD = 'stdzzmsrgfzhccfv'  # Sender's email password (ensure secure handling)
SENDER = 'chadoneal3@gmail.com'  # Sender's email address
RECEIVER = 'chadoneal3@gmail.com'  # Receiver's email address

def send_email(image_path):
    """
    Function to send an email with an image attachment.
    :param image_path: Path to the image file to be attached.
    """
    print('Sending email...')  # Informing about the email sending process

    # Creating an instance of EmailMessage for composing the email
    email_message = EmailMessage()
    email_message['Subject'] = 'Webcam Detection'  # Setting the email subject
    email_message.set_content('New Webcam Detection')  # Setting the email content

    # Opening the image file in binary mode and reading its content
    with open(image_path, 'rb') as file:
        content = file.read()

    # Adding the image file as an attachment to the email message
    email_message.add_attachment(content, maintype='image', subtype=imghdr.what(None, content))

    # Establishing a connection to Gmail's SMTP server
    gmail = smtplib.SMTP('smtp.gmail.com', 587)
    gmail.ehlo()  # Starting the SMTP connection
    gmail.starttls()  # Initiating TLS encryption for secure communication
    gmail.login(SENDER, PASSWORD)  # Logging into the sender's email account
    gmail.sendmail(SENDER, RECEIVER, email_message.as_string())  # Sending the email message
    gmail.quit()  # Quitting the SMTP server connection
    print('Email has been sent')  # Notifying about the successful email sending


if __name__ == '__main__':
    # Calling the send_email function with a sample image path
    send_email(image_path='images/19.png')

