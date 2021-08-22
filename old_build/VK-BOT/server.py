import vk_api.vk_api
from vk_api.bot_longpoll import VkBotLongPoll
from vk_api.bot_longpoll import VkBotEventType
from vk_api.utils import get_random_id
from a_commander import commander


class Server:

    def __init__(self, api_token, group_id, server_name: str="Empty"):

        self.server_name = server_name
        self.vk = vk_api.VkApi(token=api_token)
        self.long_poll = VkBotLongPoll(self.vk, group_id)
        self.vk_api = self.vk.get_api()

    def send_msg(self, send_id, message):
        self.vk_api.messages.send(peer_id=send_id,
                                  message=message,
                                  random_id=get_random_id())

#    def test(self):
#        self.send_msg(29627071, "Привет-привет!")

#    def repeater(self):
#        for event in self.long_poll.listen(): #Проверка действий
#            print(event)
#            if event.type == VkBotEventType.MESSAGE_NEW:
#                if event.type == VkBotEventType.MESSAGE_NEW: # последняя строчка
#                #проверяем не пустое ли сообщение нам пришло
#                    if event.object.message["text"] != '':
#                        self.send_msg(event.object.message["peer_id"],
#                                      event.object.message["text"])

    def main(self):
        for event in self.long_poll.listen():
            print(event)
            if event.type == VkBotEventType.MESSAGE_NEW:
                if  event.object.message["text"] != '':
                    event.object.message["text"] = event.object.message["text"].lower()
                    output = commander(event)
                             #event.object.message["text"].lower(),
                             #event.object.message["peer_id"],
                             #event.object.message["from_id"],
                             #event.object.message["conversation_message_id"])
                    self.send_msg(event.object.message["peer_id"],
                                  output)
