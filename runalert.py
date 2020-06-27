import smtplib, ssl, re, sys

class RunAlert:
  """
  RunAlert allows you to easily set up text messaging or email alerts
  for code you are running. Hit 'run', step back, wander off, and wait
  for a message to reach your phone!
  """

  def __init__(self):
    self.gmail_sender = None
    self.gmail_password = None
    self.number = None
    self.provider = None
    self.receiving_email = None

  def receiver_phone(self, number, provider=None):
    """
    Set the receiving phone number and wireless provider.\n
    :param number: receiving cell phone number for text \n
    :param provider: wireless provider. Valid options include:
        Verizon, T-Mobile, ATT
    """
    self.number = re.sub(r"\D", "", str(number))
    if provider:
      pr = provider.upper()
      if pr == "VERIZON":
        self.provider = "@vtext.com"
      elif pr == "T-MOBILE":
        self.provider = "@tmomail.net"
      elif pr == "ATT":
        self.provider = "@txt.att.net"
  
  def set_provider_texting_domain(self, provider):
    """
    Optionally set the provider's email domain for send texts.
    For example, Verizon's is '@vtext.com' || '0123456789@vtext.com'
    A quick google should help you to find the correct domain!
    """
    self.provider = provider
  
  def receiver_email(self, email):
    """
    You may choose to set a receiver email address instead of phone.
    Supply the full email address.
    """
    self.receiving_email = email
    
  
  def sender(self, account, password):
    """
    Provide the GMAIL address and password for SMTP Relay. \n
    IMPORTANT NOTE: You must turn on 'Less Secure Apps' in your 
    gmail account settings in order for this to work!
    """
    self.gmail_sender = account 
    self.gmail_password = password
  
  def send_message(self, message):
    if all([self.provider, self.gmail_password, 
            self.gmail_sender, self.number, message]) \
            or all([self.gmail_password, self.gmail_sender, 
                    self.receiving_email, message]):
      port = 465  # For SSL
      smtp_server = "smtp.gmail.com"
      sender_email = self.gmail_sender  
      if self.receiving_email:
        receiver_email = self.receiving_email
      else:
        receiver_email = self.number + self.provider  
      password = self.gmail_password

      context = ssl.create_default_context()
      with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
          server.login(sender_email, password)
          server.sendmail(sender_email, receiver_email, message)
      print("Message was sent!")
    else: 
      print("Missing necessary details to send message. \
        Be sure you have provided a sender and a receiver.")

if __name__ == "__main__":
  messenger = RunAlert()
  messenger.sender(
    account="youraccount@gmail.com",
    password="accountpassword")
  messenger.receiver_phone(
    number="(123)456-7890", 
    provider="Verizon")
  # a.receiver_email(
  #   email="receivingemail@gmail.com"
  # )

  try:
    for i in range(100):
        print(i+'s')
    messenger.send_message("Hooray! Your code completed!")
  except Exception as e:     
    messenger.send_message("Oh No! Your Code failed!")
