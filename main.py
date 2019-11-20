import vk_api
from vk_api.utils import get_random_id
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import pymysql.cursors
import requests

vk_session = vk_api.VkApi(token="10c946785027461510d6c0b34f69e39fd0c4bd80e8965936684066c73550fe4ed431732679aa682b9f5d6")
vk = vk_session.get_api()
longpoll = VkBotLongPoll(vk_session, "188984834")
#пример longpoll = VkBotLongPoll(vk_session, "637182735")
for event in longpoll.listen(): #Проверка действий
    if event.type == VkBotEventType.MESSAGE_NEW:

        if event.type == VkBotEventType.MESSAGE_NEW: # последняя строчка
        #проверяем не пустое ли сообщение нам пришло
            if event.obj.text != '':
            #проверяем пришло сообщение от пользователя или нет
                if event.from_user:
                    vk.messages.send(
                            user_id=event.obj.from_id,
                            random_id=get_random_id(),
                            message=event.obj.text)
