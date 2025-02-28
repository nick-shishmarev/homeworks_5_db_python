import os
from dotenv import load_dotenv
import json

import sqlalchemy
from sqlalchemy.orm import sessionmaker

import db_structure as db


def get_values_from_json(file_name):
    models = {
        'publisher': db.Publisher,
        'shop':  db.Shop,
        'book':  db.Book,
        'stock': db.Stock,
        'sale':  db.Sale,
    }

    with open(file_name, encoding='utf-8') as f:
        values = json.load(f)

    return [models[r.get('model')](id=r.get("pk"), **r.get('fields')) for r in values]


def main():

    # Задание 1

    load_dotenv()
    db_name = os.getenv("db_name")
    db_user = os.getenv("db_user")
    db_pwd = os.getenv("db_pwd")
    db_type = os.getenv('db_type')
    db_host = os.getenv("db_host")
    DSN = f"{db_type}://{db_user}:{db_pwd}@{db_host}/{db_name}"
    engine = sqlalchemy.create_engine(DSN)
    db.create_tables(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    # Задание 3

    session.add_all(get_values_from_json("fixtures/tests_data.json"))
    session.commit()

    # Задание 2

    publisher_id = 0
    publisher_name = input("Укажите название или ID издательства: ").strip()
    if publisher_name.isdigit():
        publisher_id = int(publisher_name)

    result = session.query(
        db.Book.title,
        db.Shop.name,
        db.Sale.price,
        db.Sale.date_sale,
        db.Publisher.name
    ).join(db.Publisher).join(db.Stock).join(db.Shop).join(db.Sale).filter(
        (db.Publisher.name == publisher_name) | (db.Publisher.id == publisher_id)
    ).all()
    print(f"Продажи книг издательства {result[0][4]} по магазинам")
    print(f"{'Название книги':^40} | {'Магазин':^40} | {'Цена':^10} | {'Дата':^10}")
    print("-"*109)
    for line in result:
        name, shop, price, data, _ = line
        print(f"{name:<40} | {shop:40} | {price:10.2f} | {data:%Y.%m.%d}")


if __name__ == '__main__':
    main()
