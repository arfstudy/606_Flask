import requests


print('\n  Получен ответ от сервера:')


# 1. Создать объявление.
response = requests.post(url='http://127.0.0.1:5000/advert',
                         json={"title": 'Погода в доме',
                               "description": 'Погода хорошая.',
                               'owner': 'user_1'},)

# response = requests.post(url='http://127.0.0.1:5000/advert',
#                          json={"title": 'В мире кошек',
#                                "description": 'А у нас сегодня кошка принесла котят.',
#                                'owner': 'user_5'},)


# 2. Изменить объявление.
# response = requests.patch(url='http://127.0.0.1:5000/advert/1',
#                          json={"title": 'Новая Новая погода в доме',
#                                "description": 'Погода становится ещё лучше.'})


# 3. Удалить объявление.
# response = requests.delete('http://127.0.0.1:5000/advert/1')
# print(f'\nСтатус код ответа:  {response.status_code}')
# print(f'Один из заголовков: {response.headers["Content-Type"]}')
# print(f'Содержимое (JSON):  {response.text}')


# 4. Получить объявление.
# response = requests.get(url='http://127.0.0.1:5000/advert/1')


print(f'\nСтатус код ответа:  {response.status_code}')
print(f'Один из заголовков: {response.headers["Content-Type"]}')
print(f'Содержимое (JSON):  {response.text}')
