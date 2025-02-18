"""
This module contains the DBStorage class"""

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review

load_dotenv()

class DBStorage:
    """DBStorage class"""
    __engine = None
    __session = None
    __models = {
        'User': User,
        'State': State,
        'City': City,
        'Amenity': Amenity,
        'Place': Place,
        'Review': Review
    }

    def __init__(self):
        """Initialize DBStorage"""
        user = os.getenv("HBNB_MYSQL_USER")
        pwd = os.getenv("HBNB_MYSQL_PWD")
        host = os.getenv("HBNB_MYSQL_HOST")
        db = os.getenv("HBNB_MYSQL_DB")
        self.__engine = create_engine(
            f"mysql+mysqldb://{user}:{pwd}@{host}/{db}", pool_pre_ping=True
        )

        if os.getenv("HBNB_ENV") == "test":
            Base.metadata.drop_all(bind=self.__engine)

        Base.metadata.create_all(self.__engine)  # Create all tables

        self.__session = scoped_session(sessionmaker(bind=self.__engine, expire_on_commit=False))

        if os.getenv("HBNB_ENV") == "test":
            self.reload()

    def all(self, cls=None):
        """Query on the current database session."""
        all_objs = {}
        if cls:
            objs = self.__session.query(cls).all()
            for obj in objs:
                key = f"{obj.__class__.__name__}.{obj.id}"
                all_objs[key] = obj
        else:
            for cls in self.__models.values():
                objs = self.__session.query(cls).all()
                for obj in objs:
                    key = f"{obj.__class__.__name__}.{obj.id}"
                    all_objs[key] = obj
        return all_objs

    def new(self, obj):
        """Add new object to session"""
        self.__session.add(obj)

    def save(self):
        """Commit all changes to the session"""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete object from session"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """Create all tables and start the session"""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()

    def close(self):
        """Remove the current session"""
        self.__session.remove()