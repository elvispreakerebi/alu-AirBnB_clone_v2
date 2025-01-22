"""
This module contains the DBStorage class"""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base

class DBStorage:
    """DBStorage class"""
    __engine = None
    __session = None

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

    def all(self, cls=None):
        """Query all objects"""
        if cls:
            return {f"{cls.__name__}.{obj.id}": obj for obj in self.__session.query(cls).all()}
        else:
            all_objs = []
            for cls in Base.__subclasses__():
                all_objs.extend(self.__session.query(cls).all())
            return {f"{type(obj).__name__}.{obj.id}": obj for obj in all_objs}

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
