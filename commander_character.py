from SQL_handler import *

#character commands part

#unfinished feature, need to work on safety
def char_help(event):
    output = "Доступные команды:\nПомощь\nСоздать\nУдалить\nСписок\nВыбрать \
              \nВыйти\nСтоп"
    return output

def char_get_list(event):
    data = SQL_get_char_list
    if data == None:
        output = "У вас нет живых персонажей"
    else:
        return data

def char_delete(event):
    char = SQL_get_selected_char_name(event)
    if(char[2] != 0):
        output = "Вы уверены, что хотите удалить персонажа {name} {surname}\
                  \n Удаление персонажа необратимо".\
                  format(name=char[0], surname=char[1])
        SQL_set_custom_status(event, "char_del")
    else:
        output = "У вас не выбран ни один персонаж, удаление неозможно"

def char_confirmed_delete(event, user):
    if(event.object.message["text"] == "да"):
        char = SQL_get_selected_char(event)
        SQL_hide_char(event, char[2])
        SQL_set_normal_status(event, "Normal")
        output = "Удаление персонажа завершено"
    elif(event.object.message["text"] == "нет"):
        SQL_set_normal_status(event)
        output = "Удаление отменено"
    else:
        output = "Команда не распознана, введите 'да' для удаления персонажа \
        или 'нет' для отмены удаления персонажа"

def char_status_create(event):

    invisible_stats = {
        'CHAR_ID': 'CHAR_ID',
        'user_id': 'user_id',
        'USER_ID': 'USER_ID',
        'registration_date': 'registration_date',
        'datetime.date': 'datetime.date',
        'user.status': 'user.status',
        'selected_char': 'selected_char'
    }

    visible_stats = {
        'name': 'Имя',
        'surname': 'Фамилия',
        'race': 'Раса',
        'net_nick': 'Никнейм в сети',
        'money': 'Кредиты',
        'expierence': 'опыт',
        'gender': 'пол',
        'int': 'Интеллект',
        'ref': 'Телосложение',
        'tech': 'Знание технологий',
        'cool': 'Спокойствие',
        'attr': 'Телосложение',
        'luck': 'Удача',
        'MA': 'Скорость движения',
        'body': 'выносливость',
        'status': 'статус',
        'refnow': 'Настоящая ловкость',
        'EMP': 'Человечность',
        'EMPNOW': 'Настоящая человечность',
        'run': 'Скорость бега',
        'leap': 'Длина прыжка',
        'lift': 'Грузоподъёмность',
        'image_url': 'Картинка персонажа'
    }

    char = SQL_get_selected_char_all_info(event)

    output = ''

    for element in list(char.keys()):
        if element in visible_stats:
            output += "{vis_stat}: {char_stat} \n".format(\
                       vis_stat=visible_stats[element],\
                       char_stat=(char[element]))
            #output += visible_stats[element] + ': ' + (char[element]) + "\n"
    return output

def char_create(event):
    char_id = SQL_put_and_get_row_id("INSERT INTO `character` \
              (user_id, status) VALUES ('{user_id}', 'editing');".\
              format(user_id=event.object.message["from_id"]))
    SQL_set_user_selected_char_and_status(event, char_id)
    char = SQL_get_selected_char_all_info(event)
    output = char
    return str(output)

def char_menu_help(event, char_id, line):
    return "Список доступных команд: \nдобавить \nинвентарь \nнавык \nпомощь \n"

def char_help(event):
    return "Меню помощи"

#if user status = char_edit
def character_status_menu(event, user):

    char_id = user['selected_char']

    char_menu_commands = {
        #'добавить':  char_add,
        #'инвентарь': char_inventory,
        #'навыки':    char_skills,
        #'навык':     char_skills,
        'помощь':    char_menu_help
    }

    char_exit_menu_commands = {
        'выйти':   SQL_set_normal_status,
        'выход':   SQL_set_normal_status,
        'стоп':    SQL_set_normal_status
    }

    output = char_status_create(event) + "\n"

    lines = event.object.message["text"].split("\n")
    words = str(lines).split(" ")
    if words[0] in char_menu_commands:
        output += char_menu_commands.get(words[0])(event, char_id, words) + "\n"
    elif words[0] in char_exit_menu_commands:
        SQL_set_normal_status(event)
        output += "Режим работы с персонажем отключён \n"
        return output
    else:
        output += "Команда " + words[0] + "не распознана"

    return output

#main Function
def character_menu(event, user, line):
    output = "\n"
    statuses = {
        'char_edit' :character_status_menu
    }

    char_non_menu_commands = {
        'помощь':  char_help,
        'меню':    char_help,
        'создать': char_create,
        'удалить': char_delete,
        'список':  char_get_list
        #'выбрать': char_choose
    }

    print("in character menu")

    char_id = user['selected_char']
    status = user['status']
    #rewrite this shit
    if status in statuses:
        character_status_menu(event, user, char_id)
    else:
        words = list(line.split(" "))
        if words[1] in char_non_menu_commands:
            output  += char_non_menu_commands.get(words[1])(event) + "\n"
        else:
            output += "Команда " + words[1] + "не распознана \n"
    return output
