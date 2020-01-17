import pymysql
import pymysql.cursors
from switch import switch
#import re
import datetime

from config import mysql_server_password, mysql_server_adress
from config import mysql_server_database, mysql_server_login

#class SQL_server:
#    def __init__(self):
#        con = pymysql.connect(mysql_server_password, mysql_server_adress,
#                              mysql_server_database, mysql_server_login)
#        #with con:
#        #    cur = con.cursor()
#        return con



def SQL_data(sql_command, type):
    output = "1"
    con = pymysql.connect(mysql_server_adress,   mysql_server_login,
                          mysql_server_password, mysql_server_database,
                          cursorclass=pymysql.cursors.DictCursor)
    cur = con.cursor()
    cur.execute(sql_command)
    if type == "get":
        output = cur.fetchone()
    elif type == "multiget":
        output = cur.fetchall()
    elif type == "input":
        con.commit()
    else:
        print("SQL type error")
        output = "SQL DB ERROR TYPE"
    con.close()
    return output

def new_user(user_id):
    current_date = str(datetime.date.today())
    SQL_data("INSERT INTO user (USER_ID, registration_date) VALUES ('{user_id}', '{current_date}');".format(user_id=user_id, current_date=current_date), "input")
    SQL_data("INSERT INTO user_type (user_USER_ID, rights) VALUES ('{user_id}', 'guest')".format(user_id=user_id), "input")
    return 1

def command_buy(line, group_status):
    return "Магазин закрыт на обед"

def command_get_character():
    data = SQL_data("SELECT name, surname, race, money, gender FROM `character` WHERE CHAR_ID=1;", "get")
    output = "123456"
    if data == None:
        output = "У вас нет живых персонажей"
    return output

def commander(text, peer_id, user_id, conversation_message_id):

    commands = {
        'купить': command_buy(line, group_status),
        'персонаж': command_get_character()
    }

    output = -1
    if(conversation_message_id == 1):
        new_user(user_id)

    if peer_id == user_id:
        group_status = 0 #личные сообщения
    elif peer_id == 2000000001:
        group_status = 1 #разрешённая группа
    else:
        group_status = 2 #запрещённая группа
'''
    lines = text.split("\n")
    for line in lines:
        words = line.split(" ")
        for case in switch(words[0]):
            if case("купить"):
                output = command_buy(line, group_status)
                break;
            if case("персонаж"):
                output = command_get_character()
                break;
'''

    lines = text.split("\n")
    for line in lines:
        words = line.split(" ")
        if words[0] in commands
            commands.get[words[0]](line)

        #switch lowercased text
        #SQL command if needed
        #return handled message
        #output = text.lower()
    if output != -1:
        output = "Команда не опознана"
    return "Команда не опознана"
