import pymysql
import pymysql.cursors

from config import mysql_server_password, mysql_server_adress
from config import mysql_server_database, mysql_server_login

# SQL commands handler

#def SQL_data(sql_command, type):
#    output = "1"
#
#    con = pymysql.connect(mysql_server_adress,   mysql_server_login,
#                          mysql_server_password, mysql_server_database,
#                          cursorclass=pymysql.cursors.DictCursor)
#    cur = con.cursor()
#    cur.execute(sql_command)
#
#    sql_type = {
#        "get": cur.fetchone,
#        "multiget": cur.fetchall,
#        "input": con.commit
#    }
#
#    if type in sql_type:
#        output = sql_type.get(type)()
#    else:
#        print("SQL type error")
#        output = "SQL DB ERROR TYPE"
#
#    con.close()
#    return output

#SQL connection commands

def SQL_put(sql_command):
    con = pymysql.connect(mysql_server_adress,   mysql_server_login,
                          mysql_server_password, mysql_server_database,
                          cursorclass=pymysql.cursors.DictCursor)
    cur = con.cursor()
    cur.execute(sql_command)
    output = con.commit()
    con.close()

def SQL_get(sql_command):
    con = pymysql.connect(mysql_server_adress,   mysql_server_login,
                          mysql_server_password, mysql_server_database,
                          cursorclass=pymysql.cursors.DictCursor)
    cur = con.cursor()
    cur.execute(sql_command)
    output = cur.fetchone()
    con.close()
    return output

def SQL_get_all(sql_command):
    con = pymysql.connect(mysql_server_adress,   mysql_server_login,
                          mysql_server_password, mysql_server_database,
                          cursorclass=pymysql.cursors.DictCursor)
    cur = con.cursor()
    cur.execute(sql_command)
    output = cur.fetchall()
    con.close()
    return output

# SQL repeated commands

#character
def SQL_get_char_name(char_id):
    return SQL_get("SELECT name, surname FROM `character` \
                    WHERE CHAR_ID = {char_id};".\
                    format(char_id=char_id))

def SQL_get_char_list(event):
    return SQL_get_all("SELECT name, surname FROM `character` \
                        WHERE user_id = {user_id};".\
                        format(user_id=event.object.message["from_id"]))

def SQL_hide_char(event, char_id):
    SQL_set("UPDATE `character` SET status = 'hidden'\
             WHERE CHAR_ID = {char_id};".\
             format(char_id=char_id))

def

#user
def SQL_get_user_status(event):
    return SQL_get("SELECT status FROM user \
                    WHERE user_id = {user_id};".\
                    format(user_id=event.object.message["from_id"]))

def SQL_get_user_status_and_char(event):
    return SQL_get("SELECT status, selected_char FROM user \
                   WHERE user_id = {user_id};".\
                   format(user_id=event.object.message["from_id"]))

def SQL_get_selected_char(event):
    return SQL_get("SELECT selected_char FROM user \
                   WHERE user_id = {user_id};".\
                   format(user_id=event.object.message["from_id"]))

def SQL_set_normal_status(event):
    SQL_put("UPDATE user SET status = 'Normal' \
              WHERE user_id = {user_id};".\
              format(user_id=event.object.message["from_id"]))

def SQL_set_custom_status(event, status):
    SQL_put("UPDATE user SET status = '{status}' \
              WHERE user_id = {user_id};".\
              format(user_id=event.object.message["from_id"], status=status))

#user and character
def SQL_get_selected_char_name(event):
    return SQL_get("SELECT name, surname FROM `character` INNER JOIN user ON \
                   `character`.CHAR_ID = user.selected_char \
                   WHERE user.user_id = {user_id};".\
                   format(user_id=event.object.message["from_id"]))

def SQL_get_selected_char_all_info(event):
    return SQL_get("SELECT * FROM `character` INNER JOIN user ON \
                   `character`.CHAR_ID = user.selected_char \
                   WHERE user.user_id = {user_id};".\
                   format(user_id=event.object.message["from_id"]))
