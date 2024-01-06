import jwt
import requests

url_base = 'http://web.cryptohack.org/rsa-or-hmac'
response = requests.get(url=f'{url_base}/get_pubkey').json()

encoded_jwt = jwt.encode({'admin': True}, response['pubkey'], algorithm='HS256').decode()
response = requests.get(url=f'{url_base}/authorise/{encoded_jwt}').json()
print(response['response'])
