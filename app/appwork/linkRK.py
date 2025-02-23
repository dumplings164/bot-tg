
import requests
import fake_useragent
from datetime import timedelta, datetime

import os
from dotenv import load_dotenv

user = fake_useragent.UserAgent().random
session = requests.session()


url = 'https://l.ucs.ru/ls5api/api/Auth/Login'
url_object = 'https://l.ucs.ru/ls5api/api/Object/GetObjectById'
url_objects = 'https://l.ucs.ru/ls5api/api/Object/GetObjectList'
url_object_order = 'https://l.ucs.ru/ls5api/api/Order/GetOrdersByObjectIdList'
url_application = 'https://l.ucs.ru/ls5api/api/Order/GetOrderByIdRequest'


login = 'lar@solardsoft.ru'
password = '1q2w3e4R!'

today = datetime.now()
dateEnd = today + timedelta(days=15)

header = {
    "user-agent": user,
}

header_file = {
    "user-agent": user,
    "Content-Type": "application/octet-stream"
}

data_login =  {"RequestObject": {"login": login,
    "pass": password,
    'systemVersion': "v5"}
    }


def chekRk(codeRk):
    response = session.post(os.getenv('url_rk'), json=data_login, headers=header).json()
    SessionId = response['value']['guid']
    langId = response['value']['langId']
    objectId, objectName = find_object(codeRk, SessionId, langId)
    if objectId != None:
        task = source_task(objectId, SessionId, langId)
        links_file = check_and_create_list_application(task, SessionId, langId)
    else:
        links_file = 'Вы указали неверный код ресторана'
    return links_file, objectName


def find_object(codeRk, SessionId, langId):
    data_objects = {"RequestObject": 
                {'PageNum': 1,
                    'PageSize': 500,
                    'SortField': "", 
                    'SortOrder': "asc"},
                    'SessionId': SessionId,
                    'langId': langId}
    response_objects = session.post(url_objects, json=data_objects, headers=header).json()
    source = response_objects['value']['source']
    for s in source:
        if s['longCode'] == codeRk:
            objectId = s['id']
            objectName = s['name']
            return objectId, objectName
    return None, None


def source_task(objectId, SessionId, langId):
    data_object = {"RequestObject": 
                    {'PageNum': 1,
                        'PageSize': 500,
                        'SortField': "", 
                        'SortOrder': "asc",
                        'objectId': objectId},
                        'SessionId': SessionId,
                        'langId': langId}
    response_object = session.post(url_object_order, json=data_object, headers=header).json()
    task = response_object['value']['source']
    return task


def check_and_create_list_application(task, SessionId, langId):
    list_application = []
    for t in task:
        create_order = str(t['createdDate']).split("T")[0]
        create_order = datetime.strptime(create_order, '%Y-%m-%d') + timedelta(days=14)
        check = today < create_order
        if check:
            if t['paymentStatusName'] == "Не оплачена" and t["statusName"] == "Выставлен счет":
                application = t['id']
                list_application.append(application)
                links_file = creat_list_order(list_application, SessionId, langId)
            elif t['paymentStatusName'] == "Полностью оплачена":
                break
        else:      
            break
    try:
        links_file = f'Сыллка для скачивание счета(ов): {links_file}'
        return links_file
    except:
        links_file = 'У Вас все счета оплачены' 
        return links_file


def creat_list_order(list_application, SessionId, langId):
    links_file = None
    if len(list_application) > 1:
        for application in list_application:
            data_application = {"RequestObject": 
                                        {'id': application,
                                            'isReadonly': True,
                                            'PageSize': 500},
                                            'SessionId': SessionId,
                                            'langId': langId}
            response_application = session.post(url_application, json=data_application, headers=header).json()
            response_files = response_application['value']['files']
            link_file = creat_links_order(response_files)
            if links_file != None:
                links_file = links_file + ' , ' + link_file
            else:
                links_file = link_file
        return links_file
    else:
        for application in list_application:
            data_application = {"RequestObject": 
                                        {'id': application,
                                            'isReadonly': True,
                                            'PageSize': 500},
                                            'SessionId': SessionId,
                                            'langId': langId}
            response_application = session.post(url_application, json=data_application, headers=header).json()
            response_files = response_application['value']['files']
            link_file = creat_links_order(response_files)
            return link_file


def creat_links_order(response_files):
    try:
        for idfile in response_files:
            idfile = idfile['id']
            link_file = f"https://l.ucs.ru/ls5api/api/Order/Generate?id={idfile}"
    except Exception as ex:
        print(ex)
        link_file = 'Ссылка на данный счет отсутствует, обратитесь в техническую поддержку или к Вашему менеджеру. Так же можете создать заявку через бота'
    return link_file

