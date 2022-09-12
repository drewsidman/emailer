#! /usr/bin/env python

import argparse
import sys
import os
import json
from O365 import Account
from O365 import FileSystemTokenBackend

if not os.path.exists('auth'):
    print('auth directory does not exist.  Creating...')
    os.makedirs('auth')

c = json.loads(open('secret/secret.json').read())

parser = argparse.ArgumentParser(description="Authenticate email via M365 OAuth2.0 authentication.  By Drew Sidman <dsidman@issisystems.com>")

#required arguments
req = parser.add_mutually_exclusive_group(required=True)
req.add_argument('-e','--email', type=str, metavar='', help='Email address')
req.add_argument('-g','--generate', action='store_true', help='Generate initial app authorization link')

args = parser.parse_args()

if args.generate is True:
    print(f'https://login.microsoftonline.com/common/oauth2/v2.0/authorize?response_type=code&client_id={c["client_id"]}&redirect_uri=https%3A%2F%2Flogin.microsoftonline.com%2Fcommon%2Foauth2%2Fnativeclient&scope=offline_access+https%3A%2F%2Fgraph.microsoft.com%2FMail.ReadWrite+https%3A%2F%2Fgraph.microsoft.com%2FMail.Send+https%3A%2F%2Fgraph.microsoft.com%2FUser.Read')
    sys.exit()

my_credentials = (c['client_id'], c['client_secret'])

token_backend = FileSystemTokenBackend(token_path='auth', token_filename=args.email)

account = Account(credentials=my_credentials, token_backend=token_backend)

if account.authenticate(scopes=['basic', 'message_all']):
   print('Authenticated!')