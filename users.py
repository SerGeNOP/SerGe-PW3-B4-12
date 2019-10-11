import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

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


def connect_db():
    """
    Устанавливает соединение к базе данных, создает таблицы, если их еще нет и возвращает объект сессии
    """
    # создаем соединение к базе данных
    engine = sa.create_engine(DB_PATH)
    # создаем описанные таблицы
    Base.metadata.create_all(engine)
    # создаем фабрику сессию
    Session = sessionmaker(engine)
    # возвращаем сессию
    return Session()

def request_data():
    """
    Запрашивает у пользователя данные и добавляет их в список users
    """
    # выводим приветствие
    print("Привет! Я запишу твои данные!")
    # запрашиваем у пользователя данные
    first_name = input("Введи своё имя: ")
    last_name = input("А теперь фамилию: ")
    gender = input("Ваш пол: ")
    email = input("Мне еще понадобится адрес электронной почты: ")
    birthdate = input("Дата Вашего рождения (формат ГГГГ-ММ-ДД): ")
    height = float(input("Рост (в см.): "))

    # создаем нового пользователя
    user = User(
        first_name=first_name,
        last_name=last_name,
        gender=gender,
        email=email,
        birthdate=birthdate,
        height=height / 100
    )
    # возвращаем созданного пользователя
    return user

def main():
    """
    Осуществляет взаимодействие с пользователем, обрабатывает пользовательский ввод
    """

    session = connect_db()
    user = request_data()
    # добавляем нового пользователя в сессию
    session.add(user)
    # сохраняем все изменения, накопленные в сессии
    session.commit()
    print("Спасибо, данные сохранены!")

if __name__ == "__main__":
    main()

"""    
def find(name, session):

    Производит поиск пользователя в таблице user по заданному имени name
  
    # находим все записи в таблице User, у которых поле User.first_name совпадает с параметром name
    query = session.query(User).filter(User.first_name == name)
    # подсчитываем количество таких записей в таблице с помSergощью метода .count()
    users_cnt = query.count()
    # составляем список идентификаторов всех найденных пользователей
    user_ids = [user.id for user in query.all()]
    # находим все записи в таблице LastSeenLog, у которых идентификатор совпадает с одним из найденных
    last_seen_query = session.query(LastSeenLog).filter(LastSeenLog.id.in_(user_ids))
    # строим словарь вида идентификатор_пользователя: время_его_последней_активности
    log = {log.id: log.timestamp for log in last_seen_query.all()}
    # возвращаем кортеж количество_найденных_пользователей, список_идентификаторов, словарь_времени_активности
    return (users_cnt, user_ids, log)
"""
