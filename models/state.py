#!/usr/bin/python3
""" State Module for HBNB project """
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base
import models
from models.city import City

class State(BaseModel, Base):
    """ State class for HBNB project """
    __tablename__ = 'states'

    name = Column(String(128), nullable=False)

    # Relationship with City
    cities = relationship("City", back_populates="state", cascade="all, delete")

    @property
    def cities(self):
        """Returns the list of City objects from storage linked to the current State"""
        if models.storage_type != "db":
            city_list = []
            for city in models.storage.all(City).values():
                if city.state_id == self.id:
                    city_list.append(city)
            return city_list
        return self.cities
