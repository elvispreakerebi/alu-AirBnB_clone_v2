#!/usr/bin/python3
""" State Module for HBNB project """
from sqlalchemy import Column, String
from models.base_model import BaseModel

class Amenity(BaseModel):
    """Amenity class for storing amenity information."""
    __tablename__ = 'amenities'
    name = Column(String(128), nullable=False)
