import sqlite3

from config import default_tg_chat_id


# создание псевдо-таблицы расписания
def create_table_schedule():
    connection_to_db_main = sqlite3.connect('./data_bases/schedule.sqlite3')
    cursor_db = connection_to_db_main.cursor()
    cursor_db.execute('''
        DROP TABLE IF EXISTS
            'group_info';
    ''')
    cursor_db.execute('''
        DROP TABLE IF EXISTS
            'lessons_info';
    ''')
    cursor_db.execute('''
        CREATE TABLE IF NOT EXISTS 
            'group_info' (
                'group_id' INTEGER PRIMARY KEY AUTOINCREMENT, 
                'schedule_course' SMALLINT NOT NULL DEFAULT 1, 
                'schedule_platoon' VARCHAR(128) NOT NULL DEFAULT '931', 
                'schedule_group' VARCHAR(128) NOT NULL DEFAULT '1');
    ''')
    cursor_db.execute('''
        CREATE TABLE IF NOT EXISTS 
            'lessons_info' (
                'lesson_id' INTEGER PRIMARY KEY AUTOINCREMENT,
                'group_id' INTEGER,
                'schedule_lesson_day' VARCHAR(8) NOT NULL DEFAULT "Нет информации",
                'schedule_lesson_month' VARCHAR(8) NOT NULL DEFAULT "Нет информации",
                'schedule_lesson_time' VARCHAR(30) NOT NULL DEFAULT "Нет информации",
                'schedule_lesson' VARCHAR(128) NOT NULL DEFAULT "Нет информации",
                'schedule_type_of_lesson' VARCHAR(16) NOT NULL DEFAULT "Нет информации",
                'schedule_tutor' VARCHAR(128) NOT NULL DEFAULT "Нет информации",
                'schedule_lesson_room' VARCHAR(16) NOT NULL DEFAULT "Нет информации",
                FOREIGN KEY ('group_id') REFERENCES group_info('group_id'));
    ''')

    connection_to_db_main.commit()
    cursor_db.close()
    connection_to_db_main.close()


# создание псевдо-таблицы обучающихся
def create_table_students():
    connection_to_db_main = sqlite3.connect('./data_bases/students.sqlite3')
    cursor_db = connection_to_db_main.cursor()
    cursor_db.execute('''
                DROP TABLE IF EXISTS 
                    'cadets';
                ''')
    cursor_db.execute('''
                DROP TABLE IF EXISTS 
                    'parameters';
                ''')
    cursor_db.execute('''
        CREATE TABLE IF NOT EXISTS 'cadets' (
            'student_id' INTEGER PRIMARY KEY AUTOINCREMENT,
            'course' SMALLINT NOT NULL DEFAULT 1,
            'platoon' SMALLINT NOT NULL DEFAULT 931,
            'cadet' VARCHAR(64) NOT NULL);
    ''')
    cursor_db.execute('''
        CREATE TABLE IF NOT EXISTS 'parameters' (
            'student_id' INTEGER,
            'grade' SMALLINT NOT NULL DEFAULT 1000,
            'discipline' SMALLINT NOT NULL DEFAULT 1000,
            'last_change' VARCHAR(60) NOT NULL DEFAULT 'Нет последних изменений',
            FOREIGN KEY ('student_id') REFERENCES cadets('student_id'));
    ''')
    num_of_man = 1
    help_uch = 1000
    help_dis = 1000
    for course in range(1, 4):
        for platoon in range(1, 4):
            vzvod_help = '9' + str((4 - course) % 10) + str(platoon)
            for cadet in range(1, 5):
                man_help = 'Курсант ' + str(num_of_man)
                cursor_db.execute('''
                    INSERT INTO
                        'cadets' (
                            course,
                            platoon,
                            cadet)
                    VALUES ('%d','%d', '%s');
                '''
                                  % (int(course), int(vzvod_help), man_help))
                cursor_db.execute('''
                    INSERT INTO
                        'parameters' (
                            student_id,
                            grade,
                            discipline)
                    VALUES (
                        (SELECT
                            student_id
                        FROM
                            cadets
                        WHERE
                            course == '%d' AND platoon == '%d' AND cadet == '%s'), 
                        '%d',
                        '%d');
                '''
                                  % (int(course), int(vzvod_help), man_help, help_uch, help_dis))
                num_of_man += 1
                help_uch += 1
                help_dis -= 1
    for course in range(4, 5):
        for platoon in range(1, 5):
            vzvod_help = '9' + str((4 - course) % 10) + str(platoon)
            for cadet in range(1, 5):
                man_help = 'Курсант ' + str(num_of_man)
                cursor_db.execute('''
                    INSERT INTO
                        'cadets' (
                            course,
                            platoon,
                            cadet)
                    VALUES ('%d','%d', '%s');
                '''
                                  % (int(course), int(vzvod_help), man_help))
                cursor_db.execute('''
                    INSERT INTO
                        'parameters' (
                            student_id,
                            grade,
                            discipline)
                    VALUES (
                        (SELECT
                            student_id
                        FROM
                            cadets
                        WHERE
                            course == '%d' AND platoon == '%d' AND cadet == '%s'), 
                        '%d',
                        '%d');
                '''
                                  % (int(course), int(vzvod_help), man_help, help_uch, help_dis))
                num_of_man += 1
                help_uch += 1
                help_dis -= 1
    for course in range(5, 6):
        for platoon in range(1, 3):
            vzvod_help = '9' + str((4 - course) % 10) + str(platoon)
            for cadet in range(1, 5):
                man_help = 'Курсант ' + str(num_of_man)
                cursor_db.execute('''
                    INSERT INTO
                        'cadets' (
                            course,
                            platoon,
                            cadet)
                    VALUES ('%d','%d', '%s');
                '''
                                  % (int(course), int(vzvod_help), man_help))
                cursor_db.execute('''
                    INSERT INTO
                        'parameters' (
                            student_id,
                            grade,
                            discipline)
                    VALUES (
                        (SELECT
                            student_id
                        FROM
                            cadets
                        WHERE
                            course == '%d' AND platoon == '%d' AND cadet == '%s'), 
                        '%d',
                        '%d');
                '''
                                  % (int(course), int(vzvod_help), man_help, help_uch, help_dis))
                num_of_man += 1
                help_uch += 1
                help_dis -= 1

    connection_to_db_main.commit()
    cursor_db.close()
    connection_to_db_main.close()


def create_table_users():
    connection = sqlite3.connect('./data_bases/users.sqlite3')
    cursor = connection.cursor()

    # создание псевдо-таблицы пользователей
    cursor.execute('''
        DROP TABLE IF EXISTS 
            'users';
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS 'users' (
            'user_id' INTEGER PRIMARY KEY AUTOINCREMENT,
            'user_login' VARCHAR(40) NOT NULL,
            'user_password' VARCHAR(40) NOT NULL,
            'user_role' VARCHAR(40) NOT NULL DEFAULT 'cadet',
            'tg_chat_id' INTEGER DEFAULT ('%d'));
    '''
                   % (int(default_tg_chat_id)))
    for current_user in range(15):
        if current_user == 0:
            user_role = 'officer'
        elif current_user % 3 == 0:
            user_role = 'helper'
        else:
            user_role = 'cadet'
        current_user_login = 'user' + str(current_user)
        current_user_password = str(current_user_login) + 'password' + str(current_user)
        cursor.execute('''
            INSERT INTO 
                'users' (
                    user_login, 
                    user_password, 
                    user_role) 
            VALUES ('%s', '%s', '%s');
        '''
                       % (current_user_login, current_user_password, user_role))

    cursor.execute('''
        INSERT INTO 
            'users' (
                user_login, 
                user_password, 
                user_role) 
        VALUES ('Q', 'Q', 'cadet');
    ''')
    cursor.execute('''
        INSERT INTO 
            'users' (
                user_login, 
                user_password, 
                user_role) 
        VALUES ('q', 'q', 'officer');
    ''')

    connection.commit()
    cursor.close()
    connection.close()

    # # подключение к базе данных
    # connection = sqlite3.connect('./data_bases/users.sqlite3')
    #
    # # объект в памяти компьютера с методами для проведения SQL-команд
    # # хранения итогов их выполнения (например, части таблицы)
    # # и методов доступа к ним
    # cursor = connection.cursor()
    #
    # # работа с базой данных
    # cursor.execute('''
    #     CREATE TABLE IF NOT EXISTS 'users' (
    #         'user_id' INTEGER PRIMARY KEY AUTOINCREMENT,
    #         'user_login' VARCHAR(40) NOT NULL,
    #         'user_password' VARCHAR(40) NOT NULL,
    #         'user_role' VARCHAR(40) NOT NULL DEFAULT 'cadet',
    #         'tg_chat_id' INTEGER DEFAULT ('%d'));
    # '''
    #                % (int(default_tg_chat_id)))
    #
    # # подтверждение изменений в базе данных
    # connection.commit()
    #
    # # освобождение памяти и закрытие подключения к базе данных
    # cursor.close()
    # connection.close()
