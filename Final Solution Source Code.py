import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# Function to retrieve the number of unread messages and notifications from LinkedIn
def get_unread_counts(username, password):
    # Set up the Chrome driver
    driver = webdriver.Chrome()

    # Open LinkedIn and log in
    driver.get('https://www.linkedin.com/')
    # Locate the username and password input fields and enter the credentials
    username_field = driver.find_element_by_id('username')
    password_field = driver.find_element_by_id('password')
    username_field.send_keys(username)
    password_field.send_keys(password)
    password_field.send_keys(Keys.RETURN)

    # Wait for the page to load
    time.sleep(5)

    # Locate the elements containing the unread message and notification counts
    unread_messages_count = driver.find_element_by_class_name('msg-overlay-bubble-header__unread-count').text
    unread_notifications_count = driver.find_element_by_class_name('notifications-tab-icon').text

    # Close the browser
    driver.quit()

    return unread_messages_count, unread_notifications_count

# Function to send email notifications
def send_email_notification(sender_email, sender_password, recipient_email, unread_messages_count, unread_notifications_count):
    # Set up the email message
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = recipient_email
    message['Subject'] = 'LinkedIn Notification'

    # Create the email body
    body = f"Number of unread messages: {unread_messages_count}\n"
    body += f"Number of unread notifications: {unread_notifications_count}\n"
    # Add comparison between current data and previous occurrence data

    message.attach(MIMEText(body, 'plain'))

    # Set up the SMTP server
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_email, sender_password)

    # Send the email
    server.send_message(message)
    server.quit()

# Main code
if __name__ == "__main__":
    # Set the LinkedIn credentials
    linkedin_username = 'your_linkedin_username'
    linkedin_password = 'your_linkedin_password'

    # Set the email credentials and recipient
    sender_email = 'your_sender_email@gmail.com'
    sender_password = 'your_sender_email_password'
    recipient_email = 'recipient_email@gmail.com'

    # Get the unread message and notification counts from LinkedIn
    unread_messages, unread_notifications = get_unread_counts(linkedin_username, linkedin_password)

    # Send the email notification
    send_email_notification(sender_email, sender_password, recipient_email, unread_messages, unread_notifications)
