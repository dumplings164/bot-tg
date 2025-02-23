import requests

import os
from dotenv import load_dotenv



url_pyrus = 'https://api.pyrus.com/v4/auth/'
api_key = "YPhSjh0khp2uu-b4~pMx5AAUZRhh~cOeqOq3WqPYxzkTqR-lHaXZCJj6M4ApHUA2Ls6WkRRB7pMNs-V7JGbNLVM0pZygWbzu"
url_task = "https://api.pyrus.com/v4/tasks"
url_upload = "https://api.pyrus.com/v4/files/upload"

def creat_task(name, inn, problem, soft, soft_id, number, photo):
    access_token = get_access_token()
    guid_photo = post_file(access_token, photo)
    id_post = post_task(access_token, name, inn, problem, soft, soft_id, number, guid_photo)
    return id_post

def info_task(idTask):
    access_token = get_access_token()
    is_close = get_task(access_token, str(idTask))
    return is_close


def get_access_token():
    response = requests.get(url_pyrus, params={ 
                                    "login" : "mva@solardsoft.ru",
                                    "security_key" : api_key
                                    })
    response = response.text.strip("}").split(":")
    access_token = response[1].strip("\"")
    return access_token

def post_file(access_token, photo):
    response = requests.post(url_upload, files={photo: (photo, open(photo, 'rb'))}, headers = {
                "Authorization": f"Bearer {access_token}"})
    response = response.json()
    goid_photo = response['guid']
    return goid_photo
    

def post_task(access_token, name, inn, problem, soft, soft_id, number, guid_photo):
    data = {
        "form_id": 1235352,
        "fields": [
            {
            "id": 23,#Поле Имя отправителя
            "value": name
            },
            {
            "id": 28,#Поле ИНН
            "value": inn
            },
            {
            "id": 3, #Поле Проблема
            "value": problem
            },
            {
            "id": 10, #Телефон
            "value": number
            },
            {
            "id": 27, #Фото
            "value": [{"guid": guid_photo, 'name': 'Error'}]
            },
            {
            "id": 22,
            "value": {
                    "choice_id": soft_id,
                    "choice_names": soft
                }}
            ]}
    response = requests.post(url_task, json = data, headers = {
                "Authorization": f"Bearer {access_token}"})
    id_post = response.json()
    id_post = id_post["task"]["id"]
    return id_post
    
def get_task(access_token, id_post_old):
    url = f"{url_task}/{id_post_old}"
    try:
        response = requests.get(url,  headers = {
                    "Authorization": f"Bearer {access_token}"})
        response = response.json()
        if response["task"]["is_closed"] == True:
            return True
        elif response["task"]["is_closed"] == False:
            return f'Закаяка {response["task"]["id"]} ещё открыта, после ее закрытия Вы сможете создать новую'
    except Exception as ex:
        print(ex)
        
        

if __name__ == '__main__':
    get_access_token()