import pymysql
import pymysql.cursors
import datetime

from config import mysql_server_password, mysql_server_adress
from config import mysql_server_database, mysql_server_login

# SQL commands handler

def SQL_data(sql_command, type):
    output = "1"

    con = pymysql.connect(mysql_server_adress,   mysql_server_login,
                          mysql_server_password, mysql_server_database,
                          cursorclass=pymysql.cursors.DictCursor)
    cur = con.cursor()
    cur.execute(sql_command)

    sql_type = {
        "get": cur.fetchone,
        "multiget": cur.fetchall,
        "input": con.commit
    }

    if type in sql_type:
        output = sql_type.get(type)()
    else:
        print("SQL type error")
        output = "SQL DB ERROR TYPE"

    con.close()
    return output

# SQL repeated commands

def SQL_get_char_name(char_id):
    return SQL_data("SELECT name, surname FROM character \
                     WHERE char_id = {char_id};".\
                     format(char_id=char_id),
                    "get")

def SQL_get_char_list(user_id):
    return SQL_data("SELECT name, surname FROM character \
                     WHERE user_id = {user_id};".\
                     format(user_id=user_id),
                    "multiget")

def SQL_get_user_status(user_id):
    return SQL_data("SELECT status FROM user \
                     WHERE user_id = {user_id};".\
                     format(user_id=user_id),
                    "get")

def SQL_set_normal_status(line, params):
    SQL_data("UPDATE user SET status = 'Normal' \
              WHERE user_id = {user_id};".\
              format(user_id=user_id),
             "input")

def SQL_set_custom_status(line, params, status):
    SQL_data("UPDATE user SET status = '{status}' \
              WHERE user_id = {user_id};".\
              format(user_id=user_id, status=status),
             "input")

# Functions of commander

def new_user(user_id):
    status = SQL_data("SELECT USER_ID FROM user \
                       WHERE user_id = {user_id};".\
                       format(user_id=user_id),
                      "get")
    if status == None:
        current_date = str(datetime.date.today())
        SQL_data("INSERT INTO user (USER_ID, registration_date, status) \
                  VALUES ('{user_id}', '{current_date}', 'Normal');".\
                  format(user_id=user_id, current_date=current_date),
                 "input")
        SQL_data("INSERT INTO user_type (user_USER_ID, rights) \
                  VALUES ('{user_id}', 'guest');".\
                  format(user_id=user_id),
                 "input")
    return 1

def command_buy(line, params):
    return "Магазин закрыт на обед"

#character commands part
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
    return ouput

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
                SQL_set_normal_status
                break
            else:
                output += "Команда'" + line + "'не распознана \n"
    else:
        words = line.split(" ")
        if words[1] in char_non_menu_commands:
            output  += char_non_menu_commands.get(words[0])(line, params) + "\n"


    data = SQL_data("SELECT name, surname FROM character \
                     WHERE user_id = {user_id};".\
                     format(user_id=params[2]),
                    "multiget")
    output = "123456"
    if data == None:
        output = "У вас нет живых персонажей"
    else:
        if type(data) is list:
            output = data
        else:
            output = data
    return output





# main commander

def commander(text, peer_id, user_id, conversation_message_id):

    params = [text, peer_id, user_id, conversation_message_id]

    statuses = {
        'char_edit' :command_character_menu,
        'char_del'  :command_char_confirmed_delete
    }

    commands = {
        'купить': command_buy,
        'персонаж': command_character_menu
    }

    output = "\n"
    if(conversation_message_id == 1):
        new_user(user_id)

    status = SQL_get_user_status

    status_line = status.split(" ")
    if status_line[0] in statuses:
        output += statuses.get(status_line[0])(line, params) + "\n"
    else:
        lines = text.split("\n")
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
