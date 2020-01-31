from SQL_handler import *

#character commands part

#unfinished feature, need to work on safety
def command_char_delete(line, params, char_id):
    charname = SQL_get_char_name(char_id)
    output = "Вы уверены, что хотите удалить" + charname + "?\n"
    command_set_status(line, params, 'char_del ' + char_id)

def command_char_confirmed_delete(line, params):
    status = SQL_get_user_status(params[2])

    char_id = -1
    status_line = status.split(" ")
    if status_line[0] == "char_del":
        char_id = status_line[1]
    else:
        output += "command_char_confirmed_delete EXCEPTION CAUGHT"
        #Break menu

def command_char_help(line, params):
    output = "Доступные команды:\nПомощь\nСоздать\nУдалить\nСписок\nВыбрать \
              \nВыйти\nСтоп"
    return output

def command_char_edit(line, params):
    status = status = SQL_get_user_status(params[2])
    status_line = status.split(" ")
    data = SQL_data("select * from character \
                     WHERE CHAR_ID = {char_id}".\
                     format(char_id=status_line[1]),\
                    "get")

#main Function

def command_character_menu(line, params):
    statuses = {
        'char_edit' :command_character_menu
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
        'помощь':  command_char_help,
        'меню':    command_char_help,
        'создать': command_char_create,
        'удалить': command_char_delete,
        'список':  command_char_list,
        'выбрать': command_char_choose,
    }

    status = SQL_get_user_status(params[2])

    char_id = -1
    status_line = status.split(" ")
    if status_line[0] in statuses:
        char_id = status_line[1]
        lines_ = text.split("\n")
        for line_ in lines_:
            words_ = line_.split(" ")
            if words_[0] in char_menu_commands:
                output += char_menu_commands.get(words[0])(line, params, char_id) + "\n"
            elif words_[0] in char_exit_menu_commands:
                SQL_set_normal_status(line, params)
                break
            else:
                output += "Команда'" + line + "'не распознана \n"
    else:
        words = line.split(" ")
        if words[1] in char_non_menu_commands:
            output  += char_non_menu_commands.get(words[0])(line, params) + "\n"

    data = SQL_get_char_list(params[2])
    output = "123456"
    if data == None:
        output = "У вас нет живых персонажей"
    else:
        if type(data) is list:
            output = data
        else:
            output = data
    return output
