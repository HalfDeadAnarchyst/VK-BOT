from SQL_handler import *

#character commands part

#unfinished feature, need to work on safety

def char_get_list(event, words):
    output = ''
    data = SQL_get_char_list(event)
    if data == None:
        output = "У вас нет живых персонажей"
    else:
        output += "Ваши перонажи: \n"
        for element in data:
            output += "{index}. {name} {surname} \n".format(index=data.index(element)+1, name=element['name'], surname=element['surname'])
    return output

def char_delete(event, words):
    char = SQL_get_selected_char_name(event)
    if(char['CHAR_ID'] != 0):
        output = "Вы уверены, что хотите удалить персонажа {name} {surname}?\
                  \n Удаление персонажа необратимо\n".\
                  format(name=char['name'], surname=char['surname'])
        SQL_set_custom_status(event, "char_del")
    else:
        output = "У вас не выбран ни один персонаж, удаление неозможно\n"

def char_confirmed_delete(event, user):
    if(event.object.message["text"] == "да"):
        char = SQL_get_selected_char_all_info(event)
        if char['status'] == "creating":
            SQL_remove_char_completely(char['CHAR_ID'])
        else:
            SQL_hide_char(event)
        output = "Удаление персонажа завершено\n"
    elif(event.object.message["text"] == "нет"):
        SQL_set_normal_status(event)
        output = "Удаление отменено\n"
    else:
        output = "Команда не распознана, введите 'да' для удаления персонажа \
        или 'нет' для отмены удаления персонажа\n"

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
        'EMPnow': 'Настоящая человечность',
        'race': 'Раса',
        'role': 'Роль',
        'expierence': 'опыт',
        'leap': 'Длина прыжка',
        'lift': 'Грузоподъёмность',
        'run': 'Скорость бега',
        'money': 'Кредиты'
    }

    visible_stats = {
        'name': 'Имя',
        'surname': 'Фамилия',
        'net_nick': 'Никнейм в сети',
        'gender': 'Пол',
        'intellect': 'Интеллект',
        'ref': 'Рефлексы',
        'tech': 'Технические способности',
        'cool': 'Хладнокровие',
        'attr': 'Привлекательность',
        'luck': 'Удача',
        'MA': 'Скорость движения',
        'body': 'выносливость',
        'status': 'статус',
        'EMP': 'Человечность',
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
            output += ''
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
        'интеллект': 'intellect',
        'рефлексы': 'ref',
        'технические': 'tech',
        'техника': 'tech',
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

    if len(words)<2:
        return "Вы должны указать параметр"

    if words[1] == "картинку" or words[1] == "картинка" or words[1] == "изображение":
        image_get_maximum_size_url(event)
        return "КОРТИНКООООО\n\n\n\n"
    elif len(words)<3:
        return "Вы должны указать значение параметра\n"

    words[2].replace("'", "/'", 99)

    if words[1] in free_stats:
        if words[1] == 'пол':
            if words[2] == 'мужской' or words[2] == 'парень':
                SQL_set_char_free_param(char['CHAR_ID'], free_stats[words[1]], 1)
                char["gender"]=1
            elif words[2] == 'женский' or words[2] == 'девушка':
                SQL_set_char_free_param(char['CHAR_ID'], free_stats[words[1]], 0)
                char["gender"]=0
            else:
                return 'Вы можете выбрать только "Мужской" или "Женский" пол \n'
        elif char["status"] == "creating":
            if char[free_stats[words[1]]] == None:
                char[free_stats[words[1]]] = '[Пусто]'
            words[2] = words[2].capitalize()
            SQL_set_char_free_param(char['CHAR_ID'], free_stats[words[1]], words[2])
            char[free_stats[words[1]]] += words[2]
        elif user["status"] == "char_edit":
            output += 'Вы не можете изменять {param} в уже созданном персонаже\n'.\
                      format(param=words[1])
        else:
            output += 'Ошибка в состоянии пользователя, сообщите администратору\n'
    elif words[1] in cost_stats:
        if words[2].isdigit():
            print(char)
            print(char['skillpoints'])
            if ((char['skillpoints'] - int(words[2])) >= 0):
                if char[cost_stats[words[1]]] == None:
                    char[cost_stats[words[1]]] = 0
                words[2] = int(words[2])
                result = (char[cost_stats[words[1]]] + words[2])
                SQL_set_char_cost_param(char['CHAR_ID'], cost_stats[words[1]], \
                             result, char['skillpoints'] - words[2])
                char[cost_stats[words[1]]] += words[2]
                char['skillpoints'] -= words[2]
            else:
                output += 'У вас не хватает {count} очков для добавления {need}\
                к {param}'.format(count=(int(char["skillpoints"]) - int(words[2])),\
                need=words[2], param=words[1])
        else:
            output += 'Вы должны использовать число после названия параметра\n'
    else:
        output += 'Параметр {param} не распознан'.format(param=words[1])

    return output

def char_create(event, words):
    data = char_get_list(event, words)

    if len(data.splitlines()) > 3:
        print(data)
        return 'Вы не можете создать персонажа, достигнуто максимальное количество'

    char_id = SQL_put_and_get_row_id("INSERT INTO `character` \
              (user_id, status) VALUES ('{user_id}', 'creating');".\
              format(user_id=event.object.message["from_id"]))
    SQL_set_user_selected_char_and_status(event, char_id)
    char = SQL_get_selected_char_all_info(event)
    output = 'Персонаж успешно создан\n'
    output += char_status_create(event)
    return output

def char_menu_help(event, user, char, line):
    return "Список доступных команд: \nдобавить \nинвентарь \nнавык \nпомощь \n"

def char_help(event, words):
    output = "Доступные команды:\nПомощь\nСоздать\nУдалить\nСписок\nВыбрать \
              \nВыйти\nСтоп"
    return output

def char_exit_menu(event, user, char):

    invisible_stats = {
        'CHAR_ID': 'CHAR_ID',
        'user_id': 'user_id',
        'USER_ID': 'USER_ID',
        'registration_date': 'registration_date',
        'datetime.date': 'datetime.date',
        'user.status': 'user.status',
        'selected_char': 'selected_char',
        'refnow': 'Настоящая ловкость',
        'EMPnow': 'Настоящая человечность',
        'race': 'Раса',
        'leap': 'Длина прыжка',
        'lift': 'Грузоподъёмность',
        'role': 'Роль'
    }

    visible_stats = {
        'name': 'Имя',
        'surname': 'Фамилия',
        'net_nick': 'Никнейм в сети',
        'money': 'Кредиты',
        'expierence': 'опыт',
        'gender': 'пол',
        'intellect': 'Интеллект',
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
        'image_url': 'Картинка персонажа',
        'skillpoints': 'Доступные очки навыков'
    }

    flag_is_char_ready = True;

    if char['name'] == None or char['name'] == 0 or char['surname'] == None or char['surname'] == 0:
        return 'Вы должны указать имя и фамилию перед выходом из меню создания персонажа\n'
    else:
        if char['status'] == 'creating':
            for element in list(char.keys()):
                if element in visible_stats:
                    if char[element] == None or char[element] == 0:
                        flag_is_char_ready = False;
            if flag_is_char_ready == True:
                char['status'] = 'Normal'
                SQL_set_char_status(event, char['CHAR_ID'], 'Normal')
                SQL_set_normal_status(event)
                return 'Создание персонажа завершено'
            else:
                SQL_set_normal_status(event)
                return 'Создание персонажа не завершено, вы не можете его использовать \nВы вышли из меню редактирования персонажа'
        elif char['status'] == 'editing':
            char['status'] = 'Normal'
            SQL_set_char_status(event, char['CHAR_ID'], 'Normal')
            SQL_set_normal_status(event)
            return 'Вы вышли из меню редактирования персонажа'
        else:
            return 'char_exit_menu status error, current status is {status}'.\
                    format(status=char['status'])
    return 'char_exit exception, свяжитесь с администратором'

def char_select(event, words):
    data = SQL_get_char_list(event)
    char_id = -1
    count = 0
    index = -1
    output = ''
    if len(words)<3:
        return 'Вы должны указать либо номер, либо имя или фамилию персонажа\n'
    if data == None:
        output = "У вас нет живых персонажей"
    else:
        if words[2].isdigit():
            index = int(words[2])-1
            if index <= len(data) and index >= 0:
                char_id = data[index]['CHAR_ID']
            else:
                return 'Выбраннай индекс больше или меньше существующего списка персонажей'
        else:
            for element in data:
                if words[2] == element['name']:
                    char_id = SQL_select_char_by_name(event, words[2])
                    count += 1
                elif words[2] == element['surname']:
                    char_id = SQL_select_char_by_surname(event, words[2])
                    count += 1
            if count > 1:
                return "Найдено больше одного совпадения по запросу\nИспользуйте выбор по индексу персонажа\n"
        SQL_set_user_selected_char(event, char_id)
        for element in data:
            if element['CHAR_ID'] == char_id:
                    output += 'Выбран персонаж {name} {surname}'.format(name=element['name'], surname=element['surname'])

    return output

def char_set_edit(event, words):
    user = SQL_get_user_info(event)
    if user['selected_char'] == 0:
        return 'У вас не выбран ни один персонаж'
    else:
        SQL_set_custom_status(event, 'char_edit')
        return 'Вы вошли в меню редактирования персонажа'

def char_char_info(event, user, char, words):
    return 'Вы находитесь в меню создания персонажа\nВ данном меню нет необходимости писать "Персонаж" для работы с персонажем\nВведите "помощь" для списка команд'

#if user status = char_edit
def character_status_menu(event, user):

    char_id = user['selected_char']
    char = SQL_get_selected_char_all_info(event)

    char_menu_commands = {
        'добавить':  char_add,
        'персонаж':  char_char_info,
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

    output = ''

    lines = event.object.message["text"].split("\n")
    for line in lines:
        words = line.split(" ")
        if words[0] in char_menu_commands:
            output += char_menu_commands.get(words[0])(event, user, char, words) + "\n"
        elif words[0] in char_exit_menu_commands:
            output += char_exit_menu(event, user, char) + "\n"
            return output
        elif words[0] in char_exit_menu_commands:
            output += char_outer_menu_commands.get(words[0])() + "\n"
        else:
            output += "[cs]Команда " + words[0] + " не распознана"

    output = char_status_create(event) + "\n" + output

    return output

#main Function
def character_menu(event, user, line):
    output = "\n"

    char_non_menu_commands = {
        'помощь':  char_help,
        'меню':    char_help,
        'создать': char_create,
        'удалить': char_delete,
        'список':  char_get_list,
        'выбрать': char_select,
        'редактировать': char_set_edit
    }


    words = list(line.split(" "))

    if len(words)<2:
        return 'Вы должны написать что-нибудь после "Персонаж" \nНапример "Персонаж помощь"\n'

    if words[1] in char_non_menu_commands:
        output  += char_non_menu_commands.get(words[1])(event, words) + "\n"
    else:
        output += "[cns]Команда " + words[1] + " не распознана \n"

    return output
