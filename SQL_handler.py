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

#characters
def SQL_get_char_name(char_id):
    return SQL_get("SELECT name, surname FROM character \
                     WHERE char_id = {char_id};".\
                     format(char_id=char_id))

def SQL_get_char_list(user_id):
    return SQL_get_all("SELECT name, surname FROM character \
                     WHERE user_id = {user_id};".\
                     format(user_id=user_id))

#status
def SQL_get_user_status(user_id):
    return SQL_get("SELECT status FROM user \
                     WHERE user_id = {user_id};".\
                     format(user_id=user_id))

def SQL_set_normal_status(line, params):
    SQL_put("UPDATE user SET status = 'Normal' \
              WHERE user_id = {user_id};".\
              format(user_id=params[2]))

def SQL_set_custom_status(line, params, status):
    SQL_put("UPDATE user SET status = '{status}' \
              WHERE user_id = {user_id};".\
              format(user_id=params[2], status=status))
