"""
FileStorage class that serializes instances to a 
JSON file and deserializes JSON file to instances"""

import json
from models.user import User
from models.base_model import BaseModel
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review

class FileStorage:
    """Serializes instances to a JSON file and deserializes JSON file to instances."""

    __file_path = "storage.json"
    __objects = {}

    def all(self, cls=None):
        """Returns a dictionary of all objects, or filtered by class if cls is provided."""
        if cls:
            cls_name = cls.__name__
            return {key: obj for key, obj in self.__objects.items() if key.startswith(cls_name)}
        return self.__objects

    def new(self, obj):
        """Sets in __objects the obj with key <obj class name>.id."""
        key = f"{obj.__class__.__name__}.{obj.id}"
        self.__objects[key] = obj

    def save(self):
        """Serializes __objects to the JSON file."""
        obj_dict = {key: obj.to_dict() for key, obj in self.__objects.items()}
        with open(self.__file_path, "w", encoding="utf-8") as file:
            json.dump(obj_dict, file)

    def reload(self):
        """Deserializes the JSON file to __objects."""
        for key, value in self.__objects.items():
            print(f"Key: {key}, Value: {value}")  # Debugging statement
            class_name = value['__class__']
            print(f"Class name: {class_name}")  # Debugging statement
            class_map = {
                'BaseModel': BaseModel,
                'User': User,
                'State': State,
                'City': City,
                'Amenity': Amenity,
                'Place': Place,
                'Review': Review
            }
            if class_name in class_map:
                self.__objects[key] = class_map[class_name](**value)
            else:
                print(f"Class {class_name} not found in class_map")

    def delete(self, obj=None):
        """Deletes obj from __objects if it exists."""
        if obj is not None:
            key = f"{obj.__class__.__name__}.{obj.id}"
            if key in self.__objects:
                del self.__objects[key]
                self.save()

    def close(self):
        """Call reload() method for deserializing the JSON file to objects"""
        self.reload()
