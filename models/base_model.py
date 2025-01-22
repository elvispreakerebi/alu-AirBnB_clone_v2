"""
This module contains BaseModel class.
"""
# create base model class with the following attributes:
#  id: string - assign with an uuid when an instance is created:
# you can use uuid.uuid4() to generate unique id but don’t forget to convert to a string
# the goal is to have unique id for each BaseModel
# created_at, datetime - assign with the current datetime when an instance is created
# updated_at: datetime - assign with the current datetime when an instance is created and it
# will be updated every time you change your object
# you can use datetime.datetime.now() to get the current datetime
# __str__: should print: [<class name>] (<self.id>) <self.__dict__>
# and the following methods:
# save(self): updates the public instance attribute updated_at with the current datetime
# to_dict(self): returns a dictionary containing all keys/values of __dict__ of the instance:
# by using self.__dict__, only instance attributes set will be returned
# a key __class__ must be added to this dictionary with the class name of the object
# created_at and updated_at must be converted to string object in ISO format:
# format: %Y-%m-%dT%H:%M:%S.%f (ex: 2017-06-14T22:31:03.285259)
# you can use isoformat() of datetime object
# This method will be the first piece of the serialization/deserialization process: create a
# dictionary representation with “simple object type” of our BaseModel


from datetime import datetime
import uuid

class BaseModel:
    """
    Base model class with common attributes and methods.

    Attributes:
        id (str): Unique identifier for the object.
        created_at (datetime): Timestamp when the object was created.
        updated_at (datetime): Timestamp when the object was last updated.

    Methods:
        __init__: Initializes the object with the given attributes.
        __str__: Returns a string representation of the object.
        save: Updates the updated_at attribute with the current datetime.
        to_dict: Returns a dictionary representation of the object.
    """
    def __init__(self, **kwargs):
        """
        Initializes the object with the given attributes.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        from models import storage
        if kwargs:
            for key, value in kwargs.items():
                if key == "created_at" or key == "updated_at":
                    value = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f")
                if key != "__class__":
                    setattr(self, key, value)
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            storage.new(self)

    def __str__(self):
        return f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}"
    def save(self):
        """
        Updates the updated_at attribute with the current datetime.

        Args:
            None

        Returns:
            None
        """
        from models import storage
        self.updated_at = datetime.now()
        storage.save()

    def to_dict(self):
        """
        Returns a dictionary representation of the object.

        Args:
            None

        Returns:
            dict: A dictionary containing all keys/values of the object's __dict__.
        """
        # Copy the instance's attributes
        obj_dict = self.__dict__.copy()
        # Add the __class__ key with the class name
        obj_dict["__class__"] = self.__class__.__name__
        # Convert datetime attributes to ISO format
        if "created_at" in obj_dict:
            obj_dict["created_at"] = self.created_at.isoformat()
        if "updated_at" in obj_dict:
            obj_dict["updated_at"] = self.updated_at.isoformat()
        return obj_dict