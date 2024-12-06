"""Thanks to Sushan Tawari for the code involving the email verifier validator. Original code found here: 
https://medium.com/@tsushan8222/check-if-an-email-address-really-exists-without-sending-an-email-3fcab3cf0e6f"""

import re
import smtplib
import dns.resolver

import validators
from wtforms.validators import ValidationError

# Custom validator to make sure profile picture URL corresponds to an actual valid not-malformed image.
def url_corresponding_to_image_check(form, field):
  """First, checks to see if it's a valid URL. Then checks to see if it's a valid image URL. 3 file formats accepted are .jpg,
  .png, and .svg. Thus, either the URL ends with one of these extensions or the extension is right before the query string."""
  
  url = field.data
  if not validators.url(url):
    raise ValidationError("Must be a valid URL!")
  
  url_without_query_string = url if url.find('?') == -1 else url[:url.find('?')]
  if not url_without_query_string.endswith(('.jpg', '.png', '.svg')):
    raise ValidationError("URL must correspond to either a .jpg, .png, or .svg image")

# Custom validator to make sure an email actually exists, not just that it follows the valid email format.
def does_email_exist_check(form, field):
   """Thanks to Sushan Tawari for the code involving the email verifier validator. Original code found here: 
   https://medium.com/@tsushan8222/check-if-an-email-address-really-exists-without-sending-an-email-3fcab3cf0e6f"""

   # Address used for SMTP MAIL FROM command.
   fromAddress = 'test@example.com'

   # Simple Regex for syntax checking
   regex = '^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,})$'

   # Email address to verify
   addressToVerify = field.data

   # Syntax check
   match = re.match(regex, addressToVerify)
   if match == None:
      raise ValidationError('The email you inputted does not match the valid email syntax.')

   # Get domain for DNS lookup
   splitAddress = addressToVerify.split('@')
   domain = str(splitAddress[1])
   print('Domain:', domain)

   # MX record lookup
   records = dns.resolver.query(domain, 'MX')
   mxRecord = records[0].exchange
   mxRecord = str(mxRecord)


   # SMTP lib setup (use debug level for full output)
   server = smtplib.SMTP()
   server.set_debuglevel(0)

   # SMTP Conversation
   server.connect(mxRecord)
   server.helo(server.local_hostname) ### server.local_hostname(Get local server hostname)
   server.mail(fromAddress)
   code, message = server.rcpt(str(addressToVerify))
   server.quit()

   #print(code)
   #print(message)

   # Assume SMTP response 250 is success
   if code != 250:
      raise ValidationError(f"The email address {addressToVerify} does not exist")