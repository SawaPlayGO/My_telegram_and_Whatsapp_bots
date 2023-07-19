import requests
from config import token_phone_api


def postPhone(phone: str):
    token = token_phone_api
    phone_number = phone

    url = f'https://my.lead2call.ru/v2/api/index?token={token}&phone={phone_number}'

    formatted_url = url.format(phone=phone)
    response = requests.get(formatted_url)
