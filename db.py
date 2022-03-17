"""Тут будет вся логика связанная с бд"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float
import datetime

DATABASE_NAME = 'bot.sqlite'

engine = create_engine("mysql+pymysql://root:ujhjldrjnjhjvvtyzytn@localhost/carbot?charset=utf8mb4")
Session = sessionmaker(bind=engine)

Base = declarative_base()


class BaseCars(Base):
    __tablename__ = 'cars'
    element_id = Column(Integer, primary_key=True)
    id = Column(String(10), nullable=True)
    mark = Column(String(150), nullable=True,)
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


def create_db():
    Base.metadata.create_all(engine)
    session = Session()
    session.commit()

