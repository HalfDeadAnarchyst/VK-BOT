import datetime
from SQL_handler import *
from commander_character import *


def new_user(event):
    data = SQL_get("SELECT USER_ID FROM user \
                       WHERE user_id = {user_id};".\
                       format(user_id=event.object.message["from_id"]))
    if data == None:
        current_date = str(datetime.date.today())
        SQL_set("INSERT INTO user (USER_ID, registration_date, status, selected_char) \
                 VALUES ('{user_id}', '{current_date}', 'Normal', '0');".\
                 format(user_id=event.object.message["from_id"], \
                 current_date=current_date))
        SQL_set("INSERT INTO user_type (user_USER_ID, rights) \
                 VALUES ('{user_id}', 'guest');".\
                 format(user_id=event.object.message["from_id"]))
    return 0


def command_buy(event, user, line):
    return "Магазин закрыт на обед"

def command_help(event, user, line):
    return 'Помощь\nПерсонаж\nКупить'

# main commander
def commander(event):

    statuses = {
        'char_edit' :character_status_menu,
        'char_create': character_status_menu,
        'char_del'  :char_confirmed_delete
    }

    commands = {
        'купить': command_buy,
        'персонаж': character_menu,
        'помощь': command_help
    }

    output = "\n"
    #if(event.object.message["conversation_message_id"] == 1):


    user = SQL_get_user_info(event)
    if user == None:
        new_user(event)
        user = SQL_get_user_info(event)
    status = user["status"]

    if status in statuses:
        output += statuses.get(status)(event, user) + "\n"
    else:
        lines = event.object.message["text"].split("\n")
        for line in lines:
            words = line.split(" ")
            if words[0] in commands:
                output += commands.get(words[0])(event, user, line) + "\n"

#    if peer_id == user_id:
#        group_status = 0 #личные сообщения
#    elif peer_id == 2000000001:
#        group_status = 1 #разрешённая группа
#    else:
#        group_status = 2 #запрещённая группа
#        return "Запрещённая группа"

    if output == "\n":
        output = "Команды не распознаны"
    return output
