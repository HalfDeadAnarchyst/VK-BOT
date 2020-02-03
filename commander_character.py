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

def char_confirmed_delete(event):
    if(event.object.message["text"] = "да"):
        char = SQL_get_selected_char(event)
        SQL_hide_char(event, char[2])
        SQL_set_normal_status(event, "Normal")
        output = "Удаление персонажа завершено"
    elif(event.object.message["text"] = "нет"):
        SQL_set_normal_status(event)
        output = "Удаление отменено"
    else:
        output = "Команда не распознана, введите 'да' для удаления персонажа \
        или 'нет' для отмены удаления персонажа"

def char_create(event):
    return bgggg

def character_status_menu(event):
    char = SQL_get_selected_char

#main Function
def character_menu(event):
    statuses = {
        'char_edit' :character_status_menu
    }

    char_menu_commands = {
        'добавить':  char_add,
        'инвентарь': char_inventory,
        'навыки':    char_skills,
        'навык':     char_skills
    }

    char_exit_menu_commands = {
        'выйти':   SQL_set_normal_status,
        'выход':   SQL_set_normal_status,
        'стоп':    SQL_set_normal_status
    }

    char_non_menu_commands = {
        'помощь':  char_help,
        'меню':    char_help,
        'создать': char_create,
        'удалить': char_delete,
        'список':  char_get_list,
        'выбрать': char_choose,
    }

    temp = SQL_get_user_status_and_char(event)
    char_id = temp[1]
    status = temp[0]
    #rewrite this shit
    if status_line in statuses:
        lines = event.object.message["text"].split("\n").split("\n")
        for line in lines:
            words = line.split(" ")
            if words_[0] in char_menu_commands:
                output += char_menu_commands.get(words[0])(event) + "\n"
            elif words_[0] in char_exit_menu_commands:
                SQL_set_normal_status(event)
                break
            else:
                output += "Команда'" + line + "'не распознана \n"
    else:
        words = line.split(" ")
        if words[1] in char_non_menu_commands:
            output  += char_non_menu_commands.get(words[0])(event) + "\n"

    output = "123456"
    return output
