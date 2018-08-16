#used https://github.com/deadrime/vk-bot/blob/master/bot.py as a source.
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time
import datetime
import requests
import json
import vk
from execute_database import ExecuteDataBaseOperator
from recommendations import get_recommendations
import random
from parameters import access_token, user_token, heh_id, version
from pprint import pprint

def get_public_id(api, text, data):
        if not text:
            if 'attachments' in data:
                attachments = data['attachments'][0]
                if 'wall' in attachments:
                    public_id = -attachments['wall']['from_id']
                    return True, '', public_id
            return False, 'сообщение не несет смысловой нагрузки:)', -1
        if text.isdigit():
            public_id = int(text)
            return True, '', int(text)

        public_strs = ['https://vk.com/', 'vk.com/', 'https://m.vk.com/',
                       'm.vk.com/', 'http://vk.com/', 'http://m.vk.com/']

        for s in public_strs:
            if text.startswith(s):
                splits = text.split(s)
                text = splits[1]
        print('screen_name={}'.format(text))
        try:
            response = api.utils.resolveScreenName(
                screen_name=text,
                version=version,
                access_token=access_token)
        except Exception as e:
            print(e)
            return False, 'нет паблика с таким сокращенным именем.', 0

        if not 'type' in response or not 'object_id' in response:
            return False, 'некорректный id.', 0
        if response['type'] not in ['group', 'page']:
            return False, 'не является группой или страницей.', 0
        return True, '', response['object_id']

def get_bot_recommendations(api, public_id):
        dbo = ExecuteDataBaseOperator(api, access_token, user_token, version)
        try:
            recommendations = get_recommendations(public_id,
                                                  dbo,
                                                  members_to_proceed=2000,
                                                  top=100,
                                                  output=True)
        except Exception as e:
            print(e)
            return 'по этому айдишнику получить ничего не удастся.'

        final_msg = ""
        for i, r in enumerate(recommendations):
    
            final_msg += '{}: {}, {}\n'.format(i, r['name'], 'https://' + r['link'])
   
            if i % 25 == 0 and i > 0:
                final_msg += '\n'

        return final_msg

def get_public_name(api, public_id):
    response = api.groups.getById(group_id=public_id,
                                  access_token=access_token,
                                  v=version)
    if isinstance(response, list) and len(response) > 0 and 'name' in response[0]:
        return response[0]['name']
    return ''


class vk_bot:
    def __init__(self):
        # добавить парсинг из конфига
        self.session = vk.Session()
        self.api = vk.API(self.session)
        self.access_token = access_token
        self.key = ''
        self.server = ''
        self.ts = 0
        self.pts = 0

        self.commands = []
        self.commands_classes = []

    def read_msg(self, msg_data):  # Чтение сообщения из 'updates'
        print('msg_data:')
        pprint(msg_data)
        obj = msg_data['object']
        msg_text = obj['body']
        msg_date = datetime.datetime.fromtimestamp(obj['date']).strftime("%b %d %Y %H:%M:%S")
        print('date:{}'.format(msg_date))
        user_id = obj['user_id']
        success, error_msg, public_id = get_public_id(self.api, msg_text, obj)
        if not success:
            self.api.messages.send(message=error_msg,
                                   user_id=user_id,
                                   version=version,
                                   access_token=access_token)
            return
        self.api.messages.send(message='сейчас подумаю...',
                                   user_id=user_id,
                                   version=version,
                                   access_token=access_token)
        final_msg = get_bot_recommendations(self.api, public_id)
        msgs = final_msg.split('\n\n')
        public_name = get_public_name(self.api, public_id)
        title = '{} ({})'.format(public_name, str(public_id))
        page_id = self.api.pages.save(access_token=user_token,
                             title=title + 'exp',
                             text=final_msg,
                             group_id=heh_id,
                             v=version)
        print('рекомендации для <' + public_name + '>' + '\nvk.com/page-{}_{}'.format(heh_id, page_id))
        
        self.api.messages.send(message='рекомендации для <' + public_name + '>' + \
                                       '\nvk.com/page-{}_{}'.format(heh_id, page_id),
                               user_id=user_id,
                               version=version,
                               access_token=access_token)
        print('---------------------------------------------------------------------------')
        # for msg in msgs:
        #     self.api.messages.send(message=msg,
        #                                user_id=user_id,
        #                                version=version,
        #                                access_token=heh_token)

    def get_new_msg(self):
        try:

            # https://{$server}?act=a_check&key={$key}&ts={$ts}&wait=25&mode=2&version=2
            params = {  # Стандартные параметры указанные в документации
                'act': 'a_check',
                'key': self.key,
                'ts': self.ts,
                'wait': 25,
            }
            url = self.server

            try: # Пробуем получить ответ от long poll
                r = requests.request(method='GET', url=url, params=params, timeout=90)  # Если поставить 25 - сервер немного не успевает
            except requests.exceptions.RequestException as e:  # This is the correct syntax
                print(e)
                return
            try: # Пробуем прочитать этот ответ
                data = json.loads(r.text)
            except Exception as error: # Пока не разобрался, какие именно ошибки отлавливать
                print(error)
                return

            if 'failed' in data:  # Если сервер прислал сообщение об ошибке
                pprint(data)
                if data['failed'] == 1:  # ts устарел
                    self.ts = data['ts']
                    return
                if data['failed'] in [2, 3]:  # ts и lps устарел
                    self.get_lps()
                    return

            if 'ts' in data:  # Обновляем ts, если есть что обновлять
                self.ts = data['ts']

            user_requests = {}
            for upd in data['updates']:  # Ищем событие о новом сообщении
                user_requests[upd['object']['user_id']] = upd
            for _, upd in user_requests.items():
                self.read_msg(upd)

        except requests.exceptions.ReadTimeout as error:
            print('Read timeout')
            pass

        except requests.exceptions.ConnectTimeout:
            print('Connection timeout')
            pass

    def get_lps(self):
        lps = self.api.groups.getLongPollServer(
            group_id = heh_id,
            access_token = access_token,
            version = version)
        pprint(lps)
        self.key = lps['key']
        self.server = lps['server']
        self.ts = lps['ts']

    def get_msgs(self):
        while True:
            time.sleep(1.0)
            self.get_new_msg()

bot = vk_bot()
bot.get_lps()
bot.get_msgs()