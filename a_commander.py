import datetime
from SQL_handler import *
from commander_character import *


def new_user(user_id):
    status = SQL_get("SELECT USER_ID FROM user \
                       WHERE user_id = {user_id};".\
                       format(user_id=user_id))
    if status == None:
        current_date = str(datetime.date.today())
        SQL_set("INSERT INTO user (USER_ID, registration_date, status) \
                  VALUES ('{user_id}', '{current_date}', 'Normal');".\
                  format(user_id=user_id, current_date=current_date))
        SQL_set("INSERT INTO user_type (user_USER_ID, rights) \
                  VALUES ('{user_id}', 'guest');".\
                  format(user_id=user_id))
    return 0


def command_buy(line, params):
    return "Магазин закрыт на обед"

# main commander
def commander(event):

    statuses = {
        'char_edit' :command_character_menu,
        'char_del'  :command_char_confirmed_delete
    }

    commands = {
        'купить': command_buy,
        'персонаж': command_character_menu
    }

    output = "\n"
    if(event.object.message["conversation_message_id"] == 1):
        new_user(user_id)

    status = SQL_get_user_status(event.object.message["from_id"])

    status_line = status["status"].split(" ")
    if status_line[0] in statuses:
        output += statuses.get(status_line[0])(line, params) + "\n"
    else:
        lines = event.object.message["text"].split("\n")
        for line in lines:
            words = line.split(" ")
            if words[0] in commands:
                output += commands.get(words[0])(line, params) + "\n"

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
