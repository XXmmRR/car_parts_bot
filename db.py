"""Тут будет вся логика связанная с бд"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean, DateTime
from keyboard import alphabet_buttons_ru_text

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


def get_mark_list(letter):
    session = Session()
    if letter in alphabet_buttons_ru_text:
        mark = session.query(BaseCars).filter(BaseCars.cyrillic_mark.like(f'{letter}%')).all()
    else:
        mark = session.query(BaseCars).filter(BaseCars.mark.like(f'{letter}%')).all()
    session.close()
    return mark


def get_mark_markup(mark_list, letter):
    if letter in alphabet_buttons_ru_text:
        markup = [x.cyrillic_mark for x in mark_list]
    else:
        markup = [x.mark for x in mark_list]
    return sorted(list(frozenset(markup)))


def get_model_list(mark):
    session = Session()
    if mark[0] in alphabet_buttons_ru_text:
        models = session.query(BaseCars).filter(BaseCars.cyrillic_mark.like(f'{mark}%')).all()
    else:
        models = session.query(BaseCars).filter(BaseCars.mark.like(f'{mark}%')).all()
    session.close()
    return models


def get_model_markup(model_list, model):
    if model[0] in alphabet_buttons_ru_text:
        markup = [x.cyrillic_model for x in model_list]
    else:
        markup = [x.model for x in model_list]
    return sorted(frozenset(markup))


def create_db():
    Base.metadata.create_all(engine)
    session = Session()
    session.commit()


def get_generation_list(model):
    session = Session()
    if model[0] in alphabet_buttons_ru_text:
        models = session.query(BaseCars).filter(BaseCars.model.like(f'{model}%')).all()
    else:
        models = session.query(BaseCars).filter(BaseCars.model.like(f'{model}%')).all()
    session.close()
    return models


def get_generation_markup(model_data):
    try:
        markup = [x.generation + ' ' + str(x.year_from) + "-" + str(x.year_to) for x in model_data]
    except:
        pre_markup = [x.generation for x in model_data if x]
        markup = [x for x in pre_markup if x]
    return sorted(list(frozenset(markup)))

def get_steps(model):
    session = Session()
    if model[0] in alphabet_buttons_ru_text:
        steps = session.query(BaseCars).filter(BaseCars.cyrillic_model.like(f'{model}')).all()
    else:
        steps = session.query(BaseCars).filter(BaseCars.model.like(f'{model}%')).all()
    bodies = list(frozenset([x.body_type for x in steps]))
    transmissions = list(frozenset([x.transmission for x in steps]))
    engine_types = list(frozenset([x.engine_type for x in steps]))
    volume = list(frozenset([x.volume for x in steps]))
    session.close()
    return bodies, transmissions, engine_types, volume



def get_bodies(data):
    return data[0]


def get_transmissiom(data):
    return data[1]


def get_engine(data):
    return data[2]


def get_engine_volume(data):
    return data[3]


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
