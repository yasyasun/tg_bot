import requests
from typing import Dict, Union
from loguru import logger
from requests import Response

from config_data.config import RAPID_API_KEY

headers = {
    "X-RapidAPI-Key": RAPID_API_KEY,
    "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
}


@logger.catch
def api_request(method: str, url: str, querystring: Dict) -> requests.Response:
    """
    Функция осуществляет запрос к api.

    :param method: GET или POST метод
    :param url: строка с энд-пойнтом для запроса.
    :param querystring: словарь с параметрами для запроса.
    :return: ответ от сервера.
    """
    if method == 'GET':
        return get_request(
            url=url,
            params=querystring
        )
    else:
        return post_request(
            url=url,
            params=querystring
        )


def get_request(url, params) -> Union[Response, None]:
    """
    Функция осуществляет GET-запрос к api.
    Если ответ == 200: возвращает результат, иначе None.

    :param url: строка с энд-пойнтом для запроса.
    :param params: словарь с параметрами для запроса.
    :return: ответ от api или None.
    """
    try:
        response = requests.get(
            url,
            headers=headers,
            params=params,
            timeout=15
        )
        if response.status_code == requests.codes.ok:
            return response
    except Exception:
        return None


def post_request(url, params) -> Union[Response, None]:
    """
    Функция осуществляет POST-запрос к api.
    Если ответ == 200: возвращает результат, иначе None.

    :param url: строка с энд-пойнтом для запроса.
    :param params: словарь с параметрами для запроса.
    :return: ответ от api или None.
    """
    try:
        response = requests.post(
            url,
            headers=headers,
            json=params,
            timeout=15
        )
        if response.status_code == requests.codes.ok:
            return response
    except Exception:
        return None
