from SQL_handler import *

#character commands part

#unfinished feature, need to work on safety

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
        'selected_char': 'selected_char',
        'refnow': 'Настоящая ловкость',
        'EMPNOW': 'Настоящая человечность',
        'race': 'Раса'
    }

    visible_stats = {
        'name': 'Имя',
        'surname': 'Фамилия',
        'net_nick': 'Никнейм в сети',
        'money': 'Кредиты',
        'expierence': 'опыт',
        'gender': 'пол',
        'int': 'Интеллект',
        'ref': 'Рефлексы',
        'tech': 'Технические способности',
        'cool': 'Хладнокровие',
        'attr': 'Привлекательность',
        'luck': 'Удача',
        'MA': 'Скорость движения',
        'body': 'выносливость',
        'status': 'статус',
        'EMP': 'Человечность',
        'run': 'Скорость бега',
        'leap': 'Длина прыжка',
        'lift': 'Грузоподъёмность',
        'image_url': 'Картинка персонажа',
        'skillpoints': 'Доступные очки навыков'
    }

    char = SQL_get_selected_char_all_info(event)

    output = ''

    for element in list(char.keys()):
        if element in visible_stats:
            output += "{vis_stat}: {char_stat} \n".format(\
                       vis_stat=visible_stats[element],\
                       char_stat=(char[element]))
        elif element in invisible_stats:
            output += ' '
        else:
            output += "{element} не найден!".format(element=element)
    return output

def char_add(event, user, char, words):

    free_stats = {
        'имя': 'name',
        'фамилия': 'surname',
        'никнейм': 'net_nick',
        'пол': 'gender',
        'картинка': 'image_url',
    }

    cost_stats = {
        'интеллект': 'int',
        'рефлексы': 'ref',
        'технические': 'tech',
        'техника': 'tech',
        'хладнокровие': 'cool',
        'привлекательность': 'attr',
        'удача': 'luck',
        'скорость': 'MA',
        'движение': 'MA',
        'выносливость': 'body',
        'тело': 'body',
        'человечность': 'EMP',
        'эмпатия': 'EMP',
    }

    output = ''

    if words[1] in free stats:
        if user["status"] == "char_create":
            if words[2].isdigit():
                SQL_set_char_free_param(char['CHAR_ID'], free_stats(words[1]), words[2])
            else:
                output += 'Вы должны использовать число после названия параметра\n'
        elif user["status"] == "char_edit":
            output += 'Вы не можете изменять {param} в уже созданном персонаже\n'.\
                       format(param=words[1])
        else:
            output += 'Ошибка в состоянии пользователя, сообщите администратору\n'
    elif words[1] in cost_stats:
        if words[2].isdigit():
            if (int(char[skillpoints]) - int(words[2])) >= 0:
                SQL_set_char_cost_param(char['CHAR_ID'], free_stats(words[1]), \
                             words[2], (int(char[skillpoints]) - int(words[2])))
            else:
                output += 'У вас не хватает {count} очков для добавления {need}\
                к {param}'.format(count=(int(char[skillpoints]) - int(words[2])),\
                need=words[2], param=words[1])
        else:
            output += 'Вы должны использовать число после названия параметра\n'
    else:
        output += 'Параметр {param} не распознан'.format(param=words[1])

    return output

def char_create(event):
    char_id = SQL_put_and_get_row_id("INSERT INTO `character` \
              (user_id, status) VALUES ('{user_id}', 'creating');".\
              format(user_id=event.object.message["from_id"]))
    SQL_set_user_selected_char_and_status(event, char_id)
    char = SQL_get_selected_char_all_info(event)
    output = char
    return str(output)

def char_menu_help(event, user, char, line):
    return "Список доступных команд: \nдобавить \nинвентарь \nнавык \nпомощь \n"

def char_help(event):
    output = "Доступные команды:\nПомощь\nСоздать\nУдалить\nСписок\nВыбрать \
              \nВыйти\nСтоп"
    return output

#if user status = char_edit
def character_status_menu(event, user):

    char_id = user['selected_char']
    char = SQL_get_selected_char_all_info(event)

    char_menu_commands = {
        'добавить':  char_add,
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

    char_outer_menu_commands = {
        'список': 'Вы не можете воспользоваться командой в меню \
                   редактирования персонажа'
    }

    output = char_status_create(event) + "\n"

    lines = event.object.message["text"].split("\n")
    for line in lines:
        words = line.split(" ")
        if words[0] in char_menu_commands:
            output += char_menu_commands.get(words[0])(event, user, char, words) + "\n"
        elif words[0] in char_exit_menu_commands:
            SQL_set_normal_status(event)
            output += "Режим работы с персонажем отключён \n"
            return output
        elif words[0] in char_exit_menu_commands:
            output += char_outer_menu_commands.get(words[0])() + "\n"
        else:
            output += "Команда " + words[0] + " не распознана"

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
