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