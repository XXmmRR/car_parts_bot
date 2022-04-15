"""Тут будет вся логика связанная с бд"""
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean, DateTime

import datetime


DATABASE_NAME = 'bot.sqlite'

engine = create_engine(f"sqlite:///{DATABASE_NAME}")
Session = sessionmaker(bind=engine)

Base = declarative_base()


class BaseCars(Base):
    __tablename__ = 'cars'
    element_id = Column(Integer, primary_key=True)
    id = Column(String(10), nullable=True)
    mark = Column(String(150), nullable=True,)
    model = Column(String(150), nullable=True)
    generation = Column(String(150), nullable=True)
    year_from = Column(Integer, nullable=True)
    year_to = Column(Integer, nullable=True)
    body_type = Column(String(150), nullable=True)
    notice = Column(String(150), nullable=True)
    volume = Column(Integer, nullable=True)
    transmission = Column(String(150), nullable=True)
    complectation = Column(String(150), nullable=True)
    horse_power = Column(Integer, nullable=True)
    engine_type = Column(String(150), nullable=True)
    photo = Column(Integer, nullable=True)
    logo = Column(String(20), nullable=True)
    cyrillic_mark = Column(String(150), nullable=True,)
    cyrillic_model = Column(String(150), nullable=True)
    door_count = Column(Integer, nullable=True)
    seats = Column(String(50), nullable=True)
    length = Column(Integer, nullable=True)
    width = Column(Integer, nullable=True)
    height = Column(Integer, nullable=True)
    wheel_base = Column(Integer, nullable=True)
    clearance = Column(String(150), nullable=True)
    front_wheel_base = Column(Integer, nullable=True)
    back_wheel_base = Column(Integer, nullable=True)
    wheel_size = Column(String(150), nullable=True)
    trunks_min_capacity = Column(Integer, nullable=True)
    trunks_max_capacity = Column(Integer, nullable=True)
    weight = Column(Integer, nullable=True)
    full_weight = Column(Integer, nullable=True)
    gear_value = Column(Integer, nullable=True)
    gear_type = Column(String(150), nullable=True)
    front_suspension = Column(String(150), nullable=True)
    back_suspension = Column(String(150), nullable=True)
    front_brake = Column(String(150), nullable=True)
    back_brake = Column(String(150), nullable=True)
    max_speed = Column(Integer, nullable=True)
    time_to_100 = Column(Float, nullable=True)
    consumption_mixed = Column(Float, nullable=True)
    consumption_hiway = Column(Float, nullable=True)
    consumption_city = Column(Float, nullable=True)
    petrol_type = Column(String(150), nullable=True)
    emission_euro_class = Column(String(150), nullable=True)
    fuel_emission = Column(Integer, nullable=True)
    engine_order = Column(String(150), nullable=True)
    feeding = Column(String(150), nullable=True)
    cylinders_order = Column(String(150), nullable=True)
    cylinders_value = Column(Integer, nullable=True)
    valves = Column(Integer, nullable=True)
    engine_feeding = Column(String(150), nullable=True)
    compression = Column(Float, nullable=True)
    diametr = Column(Integer, nullable=True)
    piston_stroke = Column(Integer, nullable=True)
    moment = Column(Integer, nullable=True)
    moment_rpm = Column(String(50), nullable=True)
    kvt_power = Column(Integer, nullable=True)
    rpm_power = Column(String(150), nullable=True)
    fuel_tank_capacity = Column(Integer, nullable=True)


class Customer(Base):
    __tablename__ = 'customer'
    id = Column(Integer, primary_key=True)
    chat_id = Column(Integer, nullable=True)
    username = Column(String(60), nullable=True, name='Ник')
    phone = Column(String(60), nullable=True, name='Телефон')
    seller = Column(Integer, nullable=True, name='Продавец', default=0)
    buys = Column(Integer, nullable=True, name='Покупатель', default=0)
    orders = relationship("Order", backref='customer')
    offers = relationship("Offers", backref='customer')


class Order(Base):
    __tablename__ = 'order'
    id = Column(Integer, primary_key=True, name='id')
    mark = Column(String(50), nullable=True, name='Марка')
    model = Column(String(50), nullable=True, name='Модель')
    generation = Column(String(60), nullable=True, name='Поколение')
    body_type = Column(String(50), nullable=True, name='Тип кузова')
    transmission = Column(String(50), nullable=True, name='КПП')
    engine_type = Column(String(50), nullable=True, name='Бензин')
    VIN = Column(String(20), nullable=True, name='VIN')
    customer_id = Column(Integer, ForeignKey('customer.id'), name='Имя клиента')
    buy_status = Column(Boolean, nullable=True, name='Статус')
    status = Column(Boolean, nullable=True, name='Статус покупки', default=None)
    created_date = Column(DateTime, default=datetime.datetime.utcnow, name='Дата и время заказа')
    detail_len = Column(Integer, name='Запчастей в заказе')
    detail = relationship("Detail", backref='order')
    offers = relationship("Offers", backref='order')


class Detail(Base):
    __tablename__ = 'detail'
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey('order.id'))
    number = Column(Integer, nullable=True, name='Номер запчасти')
    detail = Column(String(200), nullable=True, name='Название заказа')
    detail_status = Column(Boolean, nullable=True, default=True, name='Статус запчасти')


class Offers(Base):
    __tablename__ = 'offer'
    element_id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey('order.id'))
    detail_numer = Column(Integer, nullable=True)
    detail = Column(String(200), nullable=True, name='Название запчасти')
    price = Column(Integer, nullable=True)
    seller_comment = Column(String(200), name='Комментарий продавца')
    seller_id = Column(Integer, ForeignKey('customer.id'), name='ID продавца')
    get_phone = Column(Boolean, name='Номер запрашивался', default=False)


def append_customer_data(chat_id, username, phone, seller, buys,):
    session = Session()
    add_customer = Customer(chat_id=chat_id, username=username, phone=phone,
                            seller=seller, buys=buys)
    session.add(add_customer)
    session.commit()
    session.close()


def get_mark_list(letter):
    session = Session()
    mark = session.query(BaseCars).filter(BaseCars.mark.like(f'{letter}%')).all()
    session.close()
    return mark


def get_mark_markup(mark_list, letter):
    markup = [x.mark for x in mark_list]
    return sorted(list(frozenset(markup)))


def get_model_list(mark):
    session = Session()
    models = session.query(BaseCars).filter(BaseCars.mark.like(f'{mark}')).all()
    session.close()
    return models


def get_model_markup(model_list, model):
    markup = [x.model for x in model_list]
    return string_sort(frozenset(markup))


def create_db():
    Base.metadata.create_all(engine)
    session = Session()
    session.commit()


def get_generation_list(mark, model):
    session = Session()
    models = session.query(BaseCars).filter(BaseCars.model.like(f'{model}'), BaseCars.mark.like(mark)).all()
    session.close()
    return models


def string_sort(x):
    return sorted(list(x), key=lambda x: x.lower())


def get_gen_year(mark, model, gen):
    session = Session()
    pre_year = session.query(BaseCars).filter(BaseCars.model.like(model), BaseCars.mark.like(mark),
                                              BaseCars.generation.like(gen)).all()
    year = [str(x.year_from) + '-' + str(x.year_to) for x in pre_year if x]
    return sorted(list(frozenset(year)))[0]


def get_generation_markup(model_data):
    pre_markup = [x.generation for x in model_data if x]
    markup = [x for x in pre_markup if x]
    return sorted(list(frozenset(markup)))


def get_engine_volume(model, gen=None, body_type=None, transmission=None, engine_type=None):
    session = Session()
    search_condition = []
    if model:
        search_condition.append(BaseCars.model.like(model))
    if gen:
        search_condition.append(BaseCars.generation.like(gen))
    if body_type:
        search_condition.append(BaseCars.body_type.like(body_type))
    if transmission:
        search_condition.append(BaseCars.transmission.like(transmission))
    if engine_type:
        search_condition.append(BaseCars.engine_type.like(engine_type))
    where = sqlalchemy.and_(*search_condition)
    query = session.query(BaseCars).filter(where)
    return sorted(list(frozenset([x.volume for x in query.all()])))


def get_engine_type(mark, model, gen=None, body_type=None, transmission=None):
    session = Session()
    search_condition = []
    if mark:
        search_condition.append(BaseCars.mark.like(mark))
    if model:
        search_condition.append(BaseCars.model.like(model))
    if gen:
        search_condition.append(BaseCars.generation.like(gen))
    if body_type:
        search_condition.append(BaseCars.body_type.like(body_type))
    if transmission:
        search_condition.append(BaseCars.transmission.like(transmission))
    where = sqlalchemy.and_(*search_condition)
    query = session.query(BaseCars).filter(where)
    session.close()
    return sorted(list(frozenset([x.engine_type for x in query.all()])))


def get_box(mark, model, gen=None, body_type=None):
    session = Session()
    search_condition = []
    if mark:
        search_condition.append(BaseCars.mark.like(mark))
    if model:
        search_condition.append(BaseCars.model.like(model))
    if gen:
        search_condition.append(BaseCars.generation.like(gen))
    if body_type:
        search_condition.append(BaseCars.body_type.like(body_type))
    where = sqlalchemy.and_(*search_condition)
    query = session.query(BaseCars).filter(where)
    return sorted(list(frozenset([x.transmission for x in query.all()])))


def get_steps(mark, model, gen=None):
    session = Session()
    search_condition = []
    if mark:
        search_condition.append(BaseCars.mark.like(mark))
    if model:
        search_condition.append(BaseCars.model.like(model))
    if gen:
        search_condition.append(BaseCars.generation.like(gen))
    where = sqlalchemy.and_(*search_condition)
    query = session.query(BaseCars).filter(where)
    bodies = sorted(list(frozenset([x.body_type for x in query.all()])))
    session.close()
    return bodies


def get_all_cars():
    session = Session()
    return session.query(BaseCars).all()


def get_param(tmp, message):
    parameters = ''
    for key, value in tmp[message.chat.id].items():
        if key != 'details':
            if value:
                parameters = parameters + key + " : " + value + '\n'

        parameters = parameters.replace('mark', 'Марка').replace('model', 'Модель').replace('transmission', 'КПП') \
            .replace('body', 'Кузов').replace('engine_type', 'Тип двигателя').replace('vin', 'VIN') \
            .replace('gen', 'Поколение').replace('engine_volume', 'Обьем двигателя')

    return parameters


def get_param_anon(tmp, callback):
    parameters = ''
    for key, value in tmp[callback.message.chat.id].items():
        if key != 'details':
            if value:
                parameters = parameters + key + " : " + value + '\n'

        parameters = parameters.replace('mark', 'Марка').replace('model', 'Модель').replace('transmission', 'КПП') \
            .replace('body', 'Кузов').replace('engine_type', 'Тип двигателя').replace('vin', 'VIN') \
            .replace('gen', 'Поколение').replace('engine_volume', 'Обьем двигателя')

    return parameters


def make_dict(tmp, mark, model, generation, body_type, transmission, engine_type, VIN):
    if mark:
        tmp['mark'] = mark
    if model:
        tmp['model'] = model
    if generation:
        tmp['gen'] = generation
    if body_type:
        tmp['body'] = body_type
    if transmission:
        tmp['transmission'] = transmission
    if engine_type:
        tmp['engine_type'] = engine_type
    if VIN:
        tmp['vin'] = VIN
    return tmp


def get_parametrs(tmp):
    parameters = ''
    for key, value in tmp.items():
        if key != 'details':
            if value:
                parameters = parameters + key + " : " + value + '\n'

        parameters = parameters.replace('mark', 'Марка').replace('model', 'Модель').replace('transmission', 'КПП') \
            .replace('body', 'Кузов').replace('engine_type', 'Тип двигателя').replace('vin', 'VIN') \
            .replace('gen', 'Поколение').replace('engine_volume', 'Обьем двигателя')

    return parameters


if __name__ == '__main__':
    create_db()