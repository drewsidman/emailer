import argparse
import re
import os
import json
import O365
from O365 import Account
from O365 import FileSystemTokenBackend

c = json.loads(open('secret/secret.json').read())

parser = argparse.ArgumentParser(description="Send email via M365 OAuth2.0 authentication.  By Drew Sidman <dsidman@issisystems.com>")

#required arguments
req = parser.add_argument_group('Required arguments')
req.add_argument('-t','--to', nargs='+', type=str, metavar='', required=True, help='To email address (space delimited)')
req.add_argument('-u','--subject', type=str, metavar='', required=True, help='Email subject')
req.add_argument('-o','--oauth', type=str, metavar='', required=True, help='Email account for authentication')

#optional arguments
parser.add_argument('-m','--message', type=str, metavar='', help='Email message')
parser.add_argument('-a','--attachment', type=str, metavar='', help='Email attachment')
parser.add_argument('-mf','--messageFile', type=str, metavar='', help='Email message as HTML file')
parser.add_argument('-tm','--testMode', type=str, metavar='', help='Run in test mode, email will not send.')
parser.add_argument('-cc','--cc', nargs='+', type=str, metavar='', help='CC email address')
parser.add_argument('-bcc','--bcc', nargs='+', type=str, metavar='', help='BCC email address')

args = parser.parse_args()

#checks local 'auth' directory for auth token with same name as sender
token_backend = FileSystemTokenBackend(token_path='auth', token_filename=args.oauth)

#check if both --message and --messageFiles are set, error out if so.
if args.message is not None and args.messageFile is not None:
	print("-mf/--messageFile and -m/--message can not both be set.  Exiting")
	exit()

if args.message is None and args.messageFile is None:
    print("Sending email with no body...")

#list auth tokens 
tokens = os.listdir('auth')

#check if email has auth token
if args.oauth not in tokens:
    print("Email address not authorized.  Use authorizeEmail.py to authorize a new email address.")
    exit()

credentials = (c['client_id'], c['client_secret'])

account = Account(credentials, token_backend=token_backend)

m = account.new_message()
m.subject = args.subject

if args.messageFile is not None:
    with open(args.messageFile) as f:
        m.body = f.read()
elif args.message is not None:
    m.body = args.message

for i in args.to:
    if re.fullmatch("([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)", i):
        m.to.add(i)
    else:
        print(i, "is not a valid email, skipping...")

if args.cc is not None:
    for i in args.cc:
        if re.fullmatch("([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)", i):
            m.cc.add(i)
        else:
            print(i, "is not a valid email, skipping...")

if args.bcc is not None:
    for i in args.bcc:
        if re.fullmatch("([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)", i):
            m.bcc.add(i)
        else:
            print(i, "is not a valid email, skipping...")

if args.testMode is None:
    if m.send():
        print("Email sent successfully")
else:
    print("Test mode invoked, email not sent.")
