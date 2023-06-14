from typing import Dict, Union
from .api_request import api_request
import json
from loguru import logger


@logger.catch
def parse_cities(city: str) -> Union[Dict[str, str], None]:
    """
    Функция делает запрос в api_request и десериализирует результат. Если запрос получен и десериализация прошла -
    возвращает обработанный результат в виде словаря - подходящие города и их id, иначе None.

    :param city: город для поиска.
    :return: None или словарь с результатом: {'city_id': 'city_name'}
    """
    querystring = {"q": city, "locale": "ru_RU"}
    response = api_request(
        method='GET',
        url="https://hotels4.p.rapidapi.com/locations/v3/search",
        querystring=querystring
    )
    possible_cities = {}
    data = json.loads(response.text)
    if not data:
        raise LookupError("Запрос пуст...")
    for place in data['sr']:
        try:
            possible_cities[place['gaiaId']] = place['regionNames']['fullName']
        except KeyError:
            continue
    return possible_cities
