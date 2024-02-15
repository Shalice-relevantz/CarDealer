from sqlalchemy import Column, ForeignKey, Integer, String, Float, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from apps.database import Base


class Dealer(Base):
    __tablename__ = "dealer"

    id = Column(Integer, primary_key=True,index=True)
    name = Column(String(100), nullable=False, index=True)
    address = Column(String(250), nullable=False)
    phone = Column(String(20), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now())
    modified_at = Column(DateTime, nullable=True)

    cars = relationship("Car", backref="dealer")


class Car(Base):
    __tablename__ = "cars"
    __table_args__= {
        'mysql_engine':'InnoDB'
    }

    id = Column(Integer, primary_key=True,index=True)
    name = Column(String(100), nullable=False, index=True)
    componentry = Column(String(150), nullable=True, index=False) #features of the vehicle like color, power window, alloy and system.
    year_release = Column(Integer)
    price = Column(Float, index=True)
    date_purchase = Column(DateTime)
    reg_no = Column(String(150), nullable=False)
    km_travelled = Column(Float, nullable=True)
    modelname = Column(String(100), nullable=False)
    dealer_id = Column(Integer,ForeignKey('dealer.id'),nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now())
    modified_at = Column(DateTime, nullable=True)

    dealers = relationship("Dealer", backref="car")
