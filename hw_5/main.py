import psycopg2
import configparser
import logging

# import json
# from datetime import datetime as dt
#
# import requests
# from tqdm import tqdm

from classes import Client


def create_tables(connector):
    query1 = """
        DROP TABLE phones;
        DROP TABLE clients;"""
    query2 = """
        CREATE TABLE IF NOT EXISTS clients (
        PRIMARY KEY (client_id), 
        client_id SERIAL,
        first_name VARCHAR(20) NOT NULL,
        last_name VARCHAR(20) NOT NULL,
        e_mail VARCHAR(60) NOT NULL UNIQUE);

        CREATE TABLE IF NOT EXISTS phones (
        PRIMARY KEY (phone_number),
        phone_number VARCHAR(30),
        client_id INTEGER NOT NULL,
        FOREIGN KEY (client_id) REFERENCES clients(client_id));    
    """
    with connector.cursor() as cur:
        try:
            cur.execute(query1)
        except psycopg2.errors.Error as e:
            connector.rollback()
            return False, e

        try:
            cur.execute(query2)
        except psycopg2.errors.Error as e:
            connector.rollback()
            return False, e

        connector.commit()
    return True, "Таблицы созданы"


def add_client(connector, client):
    query1 = """
        INSERT INTO clients (first_name, last_name, e_mail)
        VALUES
        (%s, %s, %s)
        RETURNING client_id;"""
    query2 = """
        INSERT INTO phones (phone_number, client_id)
        VALUES
        (%s, %s);"""

    with connector.cursor() as cur:
        try:
            cur.execute(
                query1,
                (client.first_name, client.last_name, client.e_mail)
            )
            client.client_id = cur.fetchone()[0]
        except psycopg2.errors.Error as e:
            connector.rollback()
            return False, e

        for phone in client.phones:
            try:
                cur.execute(query2, (phone, client.client_id))
            except psycopg2.errors.Error as e:
                logging.error(f"Не удалось добавить телефон {phone} клиенту id={client.client_id} {e}")
    try:
        connector.commit()
    except psycopg2.errors.Error as e:
        connector.rollback()
        return False, e

    return True, f"Клиент добавлен в БД {client}"


def find_clients(connector, cl_id=None, f_name=None, l_name=None, e_mail=None):
    cond_lst = []
    result = []
    if cl_id:
        cond_lst.append(f"client_id={cl_id}")
    elif e_mail:
        cond_lst.append(f"e_mail='{e_mail}'")
    else:
        if f_name:
            cond_lst.append(f"first_name='{f_name}'")
        if l_name:
            cond_lst.append(f"last_name='{l_name}'")
    cond = " AND ".join(cond_lst)
    if cond:
        query = "SELECT * FROM clients WHERE " + cond + ";"
    else:
        query = "SELECT * FROM clients;"

    with connector.cursor() as cur:
        try:
            cur.execute(query)
        except psycopg2.errors.Error as e:
            logging.error(e)
            return False, e
        cl_lst = cur.fetchall()
        for cl in cl_lst:
            cl_id, f_name, l_name, e_mail = cl
            cur.execute("""SELECT phone_number FROM phones WHERE client_id = %s;""", str(cl_id))
            phones = ", ".join([p[0] for p in cur.fetchall()])
            client = Client(f_name, l_name, e_mail, phones, cl_id)
            result.append(client)

    return True, result


def add_phone_number(connector, client_id, phone_number):
    status, clients = find_clients(connector, cl_id=client_id)
    if status:
        if len(clients) == 1:
            client = clients[0]
        elif len(clients) == 0:
            return False, f"Не найден клиент {client_id = }"
        else:
            return False, f"Найдено больше одного клиента"
    else:
        # logging.error(clients[0])
        return False, f"Ошибка поиска клиента {client_id = }"

    phone_number = phone_number.replace(" ", "")
    query = (f"INSERT INTO phones (phone_number, client_id)\n"
             f"VALUES\n"
             f"('{phone_number}', {client.client_id});")
    logging.debug(f"add_phone_number\n{query}")

    with connector.cursor() as cur:
        try:
            cur.execute(query)
        except psycopg2.errors.Error as e:
            connector.rollback()
            return False, e
        connector.commit()
    return True, f"Телефонный номер {phone_number} добавлен клиенту с {client_id = }"


def update_client(connector, client_id, first_name=None, last_name=None, e_mail=None, phone_numbers=None):
    status, clients = find_clients(connector, cl_id=client_id)
    if status:
        if len(clients) == 1:
            client = clients[0]
        elif len(clients) == 0:
            return False, f"Не найден клиент {client_id = }"
        else:
            return False, f"Найдено больше одного клиента"
    else:
        return False, f"Ошибка поиска клиента {client_id = }"

    text = ""
    sets = []
    if first_name:
        client.first_name = first_name.capitalize()
        sets.append(f"first_name='{client.first_name}'")
    if last_name:
        client.last_name = last_name.capitalize()
        sets.append(f"last_name='{client.last_name}'")
    if e_mail:
        client.e_mail = e_mail.lower()
        sets.append(f"e_mail='{client.e_mail}'")
    query_sets = ', '.join(sets)
    if query_sets:
        query = (f"UPDATE clients\n"
                 f"SET {query_sets}\n"
                 f"WHERE client_id={client_id};")

        logging.debug(f"update_client\n{query}")
        with connector.cursor() as cur:
            try:
                cur.execute(query)
            except psycopg2.errors.Error as e:
                connector.rollback()
                return False, e
        connector.commit()
        text = f"Изменен клиент {client_id = }: {client}"

    if len(phone_numbers) > 0:
        for ph in phone_numbers:
            ph = ph.replace(" ", "")
            status, message = add_phone_number(connector, client_id, ph)
            if status:
                logging.info(message)
                text += f", добавлен номер {ph}"
            else:
                logging.info(message)
                print(message)

    return True, text


def del_phone_number(connector, cl_id, phone_number):
    phone_number = phone_number.replace(" ", "")
    query = (f"SELECT * FROM phones\n"
             f"WHERE client_id={cl_id} AND phone_number='{phone_number}';")
    with connector.cursor() as cur:
        try:
            cur.execute(query)
        except psycopg2.errors.Error as e:
            logging.error(f"del_phone_number\n{e}")
            return False, e

        if not cur.fetchall():
            return False, f"Not found"

    query = (f"DELETE FROM phones\n"
             f"WHERE client_id={cl_id} AND phone_number='{phone_number}';")

    with connector.cursor() as cur:
        try:
            cur.execute(query)
        except psycopg2.errors.Error as e:
            connector.rollback()
            return False, e
        connector.commit()
    return True, "Success"


def del_client(connector, cl_id):
    status, clients = find_clients(connector, cl_id=cl_id)
    if status:
        if len(clients) == 1:
            client = clients[0]
        elif len(clients) == 0:
            return False, f"Не найден клиент {cl_id = }"
        else:
            return False, f"Найдено больше одного клиента"
    else:
        logging.error(clients[0])
        return False, f"Ошибка поиска клиента {cl_id = }"

    query = (f"DELETE FROM phones\n"
             f"WHERE client_id={cl_id};")
    with connector.cursor() as cur:
        try:
            cur.execute(query)
        except psycopg2.errors.Error as e:
            connector.rollback()
            return False, e
        connector.commit()

    query = (f"DELETE FROM clients\n"
             f"WHERE client_id={cl_id};")
    with connector.cursor() as cur:
        try:
            cur.execute(query)
        except psycopg2.errors.Error as e:
            connector.rollback()
            return False, e
        connector.commit()

    return True, f"Клиент удален {client}"


def main():
    """
    [db_parameters]
    db_name='clients'
    db_user='user'
    db_pwd='1234'
    """
    config = configparser.ConfigParser()
    config.read('settings.ini')
    database_name = config['db_params']['db_name']
    database_user = config['db_params']['db_user']
    database_password = config['db_params']['db_pwd']
    logging.info(f"Starting client_service database: {database_name} user_name: {database_user}")

    conn = psycopg2.connect(database=database_name, user=database_user, password=database_password)

    status, message = create_tables(conn)
    if status:
        logging.info(message)
    else:
        print(message)
        logging.error(message)

    # Заполнение таблицы clients
    clients = [
        Client("John",
               "Silver",
               "johnsilver@gmail.com",
               phones="+7(903) 156-1234, +7(926) 123-4534"),
        Client("Billy", "Bons", "billybones@yahoo.com", phones="+7(925) 245 5487"),
        Client("John", "Watson", "johnwatson@gmail.com", phones="+7(921) 145 2547"),
        Client("Billy", "Watson", "billywatson@yahoo.com"),
        Client("John", "Nixon", "johnnixon@gmail.com", phones="+7(926) 368 5784"),
        Client("Richard", "Nixon", "richardnixon@yahoo.com"),
        Client("John", "Carter", "johncarter@gmail.com"),
    ]
    for client in clients:
        status, message = add_client(conn, client)
        if status:
            print(f"{message}")
            logging.info(f"{message}")
        else:
            print(f"Не удалось создать клиента {client}\n{message}")
            logging.error(f"Не удалось создать клиента {client}\n{message}")

    # Поиск клиентов по разным полям
    first_name = 'John'
    last_name = 'Silver'
    print(f"\nПоиск клиента {first_name=} {last_name=}")
    status, clients = find_clients(conn, f_name=first_name, l_name=last_name)
    if status:
        if len(clients) == 0:
            logging.error(f"Не найден клиент {first_name=} {last_name=}")
            print(f"Не найден клиент {first_name=} {last_name=}")
        for c in clients:
            print(c)
    else:
        logging.error(clients[0])

    first_name = 'John'
    print(f"\nПоиск клиента {first_name=}")
    status, clients = find_clients(conn, f_name=first_name)
    if status:
        if len(clients) == 0:
            logging.info(f"Не найден клиент {first_name=}")
            print(f"Не найден клиент {first_name=}")
        for c in clients:
            print(c)
    else:
        logging.error(clients[0])

    email = 'billybans@yahoo.com'
    print(f"\nПоиск клиента {email=}")
    status, clients = find_clients(conn, e_mail=email)
    if status:
        if len(clients) == 0:
            logging.error(f"Не найден клиент с {email=}")
            print(f"Не найден клиент с {email=}")
        for c in clients:
            print(c)
    else:
        logging.error(clients[0])

    email = 'johnwatson@gmail.com'
    print(f"\nПоиск клиента {email=}")
    status, clients = find_clients(conn, e_mail=email)
    if status:
        if len(clients) == 0:
            logging.info(f"Не найден клиент с {email=}")
            print(f"Не найден клиент с {email=}")
        for c in clients:
            print(c)
    else:
        logging.error(clients[0])

    last_name = 'Watson'
    print(f"\nПоиск клиента {last_name=}")
    status, clients = find_clients(conn, l_name=last_name)
    if status:
        if len(clients) == 0:
            logging.info(f"Не найден клиент с {last_name=}")
            print(f"Не найден клиент с {last_name=}")
        for c in clients:
            print(c)
    else:
        logging.error(clients[0])

    last_name = 'Nixon'
    print(f"\nПоиск клиента {last_name=}")
    status, clients = find_clients(conn, l_name=last_name)
    if status:
        if len(clients) == 0:
            logging.info(f"Не найден клиент с {last_name=}")
            print(f"Не найден клиент с {last_name=}")
        for c in clients:
            print(c)
    else:
        logging.error(clients[0])

    client_id = 1
    print(f"\nПоиск клиента {client_id=}")
    status, clients = find_clients(conn, cl_id=client_id)
    if status:
        if len(clients) == 0:
            logging.info(f"Не найден клиент с {client_id=}")
            print(f"Не найден клиент с {client_id=}")
        for c in clients:
            print(c)
    else:
        logging.error(clients[0])

    # Добавление номера телефона клиенту
    print(f"\nДобавление телефонных номеров")
    phone = '+7 (916) 563-2673'
    client_id = 3
    status, message = add_phone_number(conn, client_id, phone)
    if status:
        logging.info(message)
        print(message)
    else:
        logging.error(message)
        print(message)

    phone = '+7 (926) 563-2678'
    client_id = 5
    status, message = add_phone_number(conn, client_id, phone)
    if status:
        logging.info(message)
        print(message)
    else:
        logging.error(message)
        print(message)

    phone = '+7 (903) 654-8345'
    client_id = 4
    status, message = add_phone_number(conn, client_id, phone)
    if status:
        logging.info(message)
        print(message)
    else:
        logging.error(message)
        print(message)

    phone = '+7 (924) 321-5467'
    client_id = 2
    status, message = add_phone_number(conn, client_id, phone)
    if status:
        logging.info(message)
        print(message)
    else:
        logging.error(message)
        print(message)

    phone = '+7 (924) 321-5467'
    client_id = 7
    status, message = add_phone_number(conn, client_id, phone)
    if status:
        logging.info(message)
        print(message)
    else:
        logging.error(message)
        print(message)

    # Изменение данных клиента
    client_id = 3
    new_first_name = 'Nick'
    new_last_name = 'Johnson'
    new_e_mail = 'johnson@yandex.ru'
    ph_lst = ['+7 (985) 123-1234', '+7 (920) 764-0925']
    print(f"\nИзменение данных клиента {client_id=} на "
          f"{new_first_name=}, {new_last_name=}, {new_e_mail=}")

    status, message = update_client(
        conn,
        client_id,
        first_name=new_first_name,
        last_name=new_last_name,
        e_mail=new_e_mail,
        phone_numbers=ph_lst
    )
    if status:
        logging.info(message)
        print(message)
    else:
        logging.error(message)
        print(message)

    # Удаление номера телефона у клиента
    print(f"\nУдаление телефонных номеров клиентов")
    client_id = 3
    phone = '+7 (916) 563-2673'
    status, message = del_phone_number(conn, cl_id=client_id, phone_number=phone)
    if status:
        logging.info(f"Удален номер {phone} у клиента {client_id=}")
        print(f"Удален номер {phone} у клиента {client_id=}")
    else:
        if message == 'Not found':
            logging.error(f"Не найден номер {phone} у клиента {client_id=} удаление невозможно")
            print(f"Не найден номер {phone} у клиента {client_id=} удаление невозможно")
        else:
            logging.error(message)
            print(message)

    client_id = 7
    phone = '+7 (926) 563-2678'
    status, message = del_phone_number(conn, cl_id=client_id, phone_number=phone)
    if status:
        logging.info(f"Удален номер {phone} у клиента {client_id=}")
        print(f"Удален номер {phone} у клиента {client_id=}")
    else:
        if message == 'Not found':
            logging.info(f"Не найден номер {phone} у клиента {client_id=}")
            print(f"Не найден номер {phone} у клиента {client_id=}")
        else:
            logging.error(message)
            print(message)

    client_id = 1
    phone = '+7 (920) 764-0925'
    status, message = del_phone_number(conn, cl_id=client_id, phone_number=phone)

    if status:
        logging.info(f"Удален номер {phone} у клиента {client_id=}")
        print(f"Удален номер {phone} у клиента {client_id=}")
    else:
        if message == 'Not found':
            logging.info(f"Не найден номер {phone} у клиента {client_id=}")
            print(f"Не найден номер {phone} у клиента {client_id=}")
        else:
            logging.error(message)
            print(message)

    client_id = 6
    print(f"\nУдаление клиента {client_id}")
    status, message = del_client(conn, client_id)
    if status:
        logging.info(message)
        print(message)
    else:
        logging.error(message)
        print(message)

    print("\nИтоговое состояние БД")
    status, clients = find_clients(conn)
    if status:
        for client in clients:
            print(client)
    else:
        print(clients)

    conn.close()


logging.basicConfig(
    level=logging.INFO,
    filename='clients_db.log',
    encoding='utf-8',
    filemode='w',
    format='[%(asctime)s] %(levelname)s - %(message)s'
)

if __name__ == '__main__':
    main()
