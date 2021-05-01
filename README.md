# emailer
## Send emails via M365 with Oauth2.0 modern authentication
---

### Dependencies/Requirements 
1. Python >= 3.4
2. O365 library which can be downloaded via pip:

```
pip3 install O365
```

### Initial setup

Create a secret folder with secret.json file formatted with your Client ID and token secret from Graph API:

```json
{
    "client_id": "<client ID>",
    "client_secret": "<token secret>"
}
```

### Authenticate email

Authenticate an email using the authenticate.py script with a mandatory -e argument which names the returned token file:

```python
python authenticate.py -e foo@bar.com
```

this will return a URL.  Paste into the browser, log into the appropriate M365 account and paste the response URL into the browser.  That email addres will now be authenticated and a token will be generated into an 'auth' directory with the token inside named by the -e argument.

### Send an email

This is an example of how to send an email after authenticating a token named foo@bar.com:

```python
python emailer.py -o foo@bar.com -t billgates@microsoft.com -u "This is a subject" -m "This is the body of the email"