from server import Server
from config import vk_api_token

server1 = Server(vk_api_token, 188984834, "earth")
# vk_api_token - API токен, который мы ранее создали
# 172998024 - id сообщества-бота
# "server1" - имя сервера

server1.main()
