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


def SQL_put_and_get_row_id(sql_command):
    con = pymysql.connect(mysql_server_adress,   mysql_server_login,
                          mysql_server_password, mysql_server_database,
                          cursorclass=pymysql.cursors.DictCursor)
    cur = con.cursor()
    cur.execute(sql_command)
    output = cur.lastrowid
    con.commit()
    con.close()
    return output

def SQL_set(sql_command):
    SQL_put(sql_command) #To avoid some errors

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
    return SQL_get_all("SELECT name, surname, CHAR_ID FROM `character` \
                        WHERE user_id={user_id} AND status <> 'hidden' \
                        AND status <> 'killed';".\
                        format(user_id=event.object.message["from_id"]))

def SQL_set_char_status(event, char_id, status):
    SQL_set("UPDATE `character` SET status = '{status}'\
            WHERE CHAR_ID = {char_id};".\
            format(char_id=char_id, status=status))

def SQL_set_char_free_param(char_id, stat, value):
    SQL_set("UPDATE `character` SET {stat} = '{value}'\
            WHERE CHAR_ID = {char_id};".\
            format(char_id=char_id, stat=stat, value=value))


def SQL_set_char_cost_param(char_id, stat, points, remain):
    SQL_set("UPDATE `character` SET {stat} = {points}, skillpoints = {remain}\
            WHERE CHAR_ID = {char_id};".\
            format(char_id=char_id, stat=stat, points=points, remain=remain))

def SQL_remove_char_completely(char_id):
    SQL_set("DELETE FROM `character` WHERE CHAR_ID={char_id};").\
            format(char_id=char_id)

def SQL_select_char_by_name(event, name):
    SQL_get("SELECT CHAR_ID, name, surname from `character` WHERE user_id={user_id} AND name = '{name}'").\
            format(user_id=event.object.message["from_id"], name=name)

def SQL_select_char_by_surname(event, surname):
    SQL_get("SELECT CHAR_ID, name, surname from `character` WHERE user_id={user_id} AND surname = '{surname}'").\
            format(user_id=event.object.message["from_id"], surname=surname)

#user
def SQL_get_user_info(event):
    return SQL_get("SELECT * from `user` WHERE user_id = {user_id};".\
                    format(user_id=event.object.message["from_id"]))

def SQL_set_user_selected_char(event, char_id):
    SQL_put("UPDATE user SET selected_char = '{char_id}' \
             WHERE user_id = {user_id};".\
             format(user_id=event.object.message["from_id"],
             char_id=char_id))

def SQL_set_user_selected_char_and_status(event, char_id):
    return SQL_put("UPDATE user SET selected_char={char_id},status ='char_create' \
             WHERE user_id = {user_id};".\
             format(user_id=event.object.message["from_id"],
             char_id=char_id))

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

def SQL_hide_char(event):
    return SQL_put("UPDATE `character` \
                    INNER JOIN user ON `character`.CHAR_ID = user.selected_char \
                    SET user.selected_char = 0, user.status = 'Normal', \
                    `character`.status = 'hidden' \
                    WHERE user.user_id = {user_id};".\
                    format(user_id=event.object.message["from_id"]))
