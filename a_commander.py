import datetime


def command_buy(event, user, line):
    return "Магазин закрыт на обед"


def command_help(event, user, line):
    return 'Помощь\nПерсонаж\nКупить'


class Character:

    def __init__(self, event):
        self.user_id = event.object.message["user_id"]
        #add SQL request


# main commander
def commander(event):

    commands = {
        'купить': command_buy,
        'помощь': command_help
    }

    output = "\n"

    lines = event.object.message["text"].split("\n")
    for line in lines:
        words = line.split(" ")
        if words[0] in commands:
            output += commands.get(words[0])() + "\n"

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
