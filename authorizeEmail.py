import argparse
import re
import O365
from O365 import Account
from O365 import FileSystemTokenBackend

c = json.loads(open('secret/secret.json').read())

parser = argparse.ArgumentParser(description="Authenticate email via M365 OAuth2.0 authentication.  By Drew Sidman <dsidman@issisystems.com>")

#required arguments
req = parser.add_argument_group('Required arguments')
req.add_argument('-e','--email', type=str, metavar='', required=True, help='Email address')

args = parser.parse_args()

credentials = (c['client_id'], c['client_secret'])

token_backend = FileSystemTokenBackend(token_path='auth', token_filename=args.email)

account = Account(credentials, token_backend=token_backend)

if account.authenticate(scopes=['basic', 'message_all']):
   print('Authenticated!')