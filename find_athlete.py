import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import datetime

DB_PATH = "sqlite:///sochi_athletes.sqlite3"
Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    # идентификатор пользователя, первичный ключ
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    # имя пользователя
    first_name = sa.Column(sa.Text)
    # фамилия пользователя
    last_name = sa.Column(sa.Text)
    gender = sa.Column(sa.Text)
    # адрес электронной почты пользователя
    email = sa.Column(sa.Text)
    birthdate = sa.Column(sa.Text)
    height = sa.Column(sa.REAL)

class Athletes(Base):
    __tablename__ = 'athelete'
    # идентификатор пользователя, первичный ключ
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    age = sa.Column(sa.Integer)
    birthdate = sa.Column(sa.Text)
    gender = sa.Column(sa.Text)
    height = sa.Column(sa.REAL)
    name = sa.Column(sa.Text)
    gender = sa.Column(sa.Text)
    weight = sa.Column(sa.Integer)
    gold_medals = sa.Column(sa.Integer)
    silver_medals = sa.Column(sa.Integer)
    bronze_medals = sa.Column(sa.Integer)
    total_medals = sa.Column(sa.Integer)
    sport = sa.Column(sa.Text)
    country = sa.Column(sa.Text)

def connect_db():

    # создаем соединение к базе данных (там наши обе таблички)
    engine = sa.create_engine(DB_PATH)
    # создаем описанные таблицы
    Base.metadata.create_all(engine)
    # создаем фабрику сессию
    Session = sessionmaker(engine)
    # возвращаем сессию
    return Session()

def convert_str_to_date(date_str):  ## Конвертирует строку с датой в формате ГГГГ-ММ-ЧЧ в объект  datetime.date
    parts = date_str.split("-")
    date_parts = map(int, parts)
    date = datetime.date(*date_parts)
    return date

def def_closer (key, searching_dict):
    our_id = None
    our_data = None
    min_x = None
    for key_, value_ in searching_dict.items():
        if value_ is None:
            continue
        x = abs(key - value_)
        if not min_x or x < min_x:
            min_x = x
            our_id = key_
            our_data = value_
    return our_id, our_data

def main():
    session = connect_db()
    print("Привет! Кого ищем?")
    first_name = input("Введи имя: ")
    last_name= input("А теперь фамилию: ")

    query = session.query(User).filter((User.first_name == first_name) and (User.last_name == last_name)).first()
    if query:
        ## фиксируем свои данные
        our_name = first_name + " " + last_name
        our_birthdate = convert_str_to_date(query.birthdate)
        our_height = query.height
        ## забираем словарь из таблицы athelete из id, даты рождения и роста
        query2 = session.query(Athletes)
        birthdate_dict = {x.id: convert_str_to_date(x.birthdate) for x in query2.all()}
        height_dict = {x.id: x.height for x in query2.all()}
        print("Наш спортсмен: {} с ростом {} родился: {}".format(our_name, our_height,our_birthdate))
        ## определяем ближайшего по дате рождения спортсмена
        relative_birthdate_id, la = def_closer(our_birthdate, birthdate_dict)
        query4 = session.query(Athletes).filter(Athletes.id == relative_birthdate_id).first()
        print("Ближайший по дате рождения: {} (id в базе: {}). Родился: {}".format(query4.name, relative_birthdate_id, la))

        ## определяем ближайшего по росту спортсмена
        relative_height_id, ll = def_closer(our_height, height_dict)
        query3 = session.query(Athletes).filter(Athletes.id == relative_height_id).first()
        print("Ближайший по росту: {} (id в базе: {}) с ростом: {}".format(query3.name, relative_height_id, ll))
    else:
        print("Такого",first_name," ",last_name, "нет в базе!")

if __name__ == "__main__":
    main()
"""
##то вывести на экран двух атлетов: ближайшего по дате рождения к данному пользователю и ближайшего по росту к данному пользователю;
        print(our_height)
        print(relative_height_id, ll)
"""