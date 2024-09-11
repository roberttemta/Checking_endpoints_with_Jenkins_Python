import requests
import boto3
from botocore.exceptions import ClientError

url_set = ['https://www.google.com', 'https://www.netflix.com', 'http://uber.net', 'http://upmenu.org', 'https://www.youtube.com']
REGION= "us-west-1"
url_broke= []
SENDER_EMAIL="kanaestephe@gmail.com"
RECEIVER_EMAIL="estephe.kana@utrains.org"
SUBJECT = "List of endpoints down"      
CHARSET = "UTF-8"

for url in url_set:
    try:
        response = requests.get(url)
        code = response.status_code
        if code == 200:
            print(f"{url} is up and running")
        else: 
            print(f"{url} is down!!")
    except:
        print(f"The url of {url} is unreachable")
        url_broke.append(url)

#function to get all the verified email.
def get_list_of_verified_emails():
    # Create SES client
    ses = boto3.client('ses', region_name=REGION)

    response = ses.list_verified_email_addresses()
    print(response)
    return(response['VerifiedEmailAddresses'])

#function to send verification email.    
def verify_email(email):
    # Create SES client
    ses = boto3.client('ses', region_name=REGION)
    
    response = ses.verify_email_identity(
      EmailAddress = email
    )

    print(response)
    
#check if email is verified and send verification.
def is_verified_email(sender_email_address,receiver_email_address):
    verified_emails= get_list_of_verified_emails()
    setemail=[sender_email_address,receiver_email_address]
    print(setemail)
    # verifies if sender and receiver are verified then sends the message.
    if set(setemail).issubset(set(verified_emails)):
        return True
        #send_plain_email(sender_email_address,receiver_email_address,subject,message)
    else:
        # sends sends verification emails to the unverified email.
        unverified_emails=list(set(setemail)- set(setemail).intersection(set(verified_emails)))
        print(unverified_emails)
        for email in unverified_emails:
            verify_email(email)
        return False
        
def send_mail(sender, receiver, subject, region):
    ses_client = boto3.client('ses', region_name=region)
    BODY_TEXT = (f"""
    Hello all,
    Please check the below endpoints as they seem broken:

    {url_broke}
    Thanks and best regards !!!


    DevOps Team 
    Email: {SENDER_EMAIL}
    """)    
    try:
        response = ses_client.create_configuration_set(
            ConfigurationSet={
                'Name': 'my-config-set'
            }
        )   
    except Exception as e:
        print('Configuration set exists: ' + e.response['Error']['Message'])

    else:
        print(f'Configuration set creation error !!! Please check your configuration set')
        
    try:
        response = ses_client.send_email(
            Destination={
                'ToAddresses': [
                    receiver,
                ],
            },
            Message={
                'Body': {
                    'Text': {
                        'Charset': CHARSET,
                        'Data': BODY_TEXT,
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': subject,
                },
            },
            Source=sender,
            ConfigurationSetName='my-config-set',
        )
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print(f"Email sent! Message ID: {response['MessageId']}")

# send an email to the dev team if any url is found down

if url_broke:
    if is_verified_email(SENDER_EMAIL,RECEIVER_EMAIL):
        send_mail(SENDER_EMAIL,RECEIVER_EMAIL,SUBJECT,REGION)
    else:
        print("verification email sent, please confirm your identity ")
else:
    print("All the endpoints are up and running !!!")  
