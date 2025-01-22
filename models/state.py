#!/usr/bin/python3
""" State Module for HBNB project """
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base

class State(BaseModel, Base):
    """ State class for HBNB project """
    __tablename__ = 'states'

    name = Column(String(128), nullable=False)

    # Relationship with City
    cities = relationship("City", back_populates="state", cascade="all, delete")
