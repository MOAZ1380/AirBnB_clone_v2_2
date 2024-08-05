#!/usr/bin/python3
"""
Serializes instances to a JSON file and
deserializes JSON file to instances.
"""
import json
from models.base_model import BaseModel
from models.user import User
from models.city import City
from models.amenity import Amenity
from models.review import Review
from models.state import State
from models.place import Place
import os


class FileStorage:
    """The file storage engine class, that is;
    A class that serialize and deserialize instances to a JSON file
    """

    __file_path = 'file.json'
    __objects = {}
    # print("basemodel class Filestorage ")

    def all(self, cls=None):
        """Returns a dictionary of objects, optionally filtered by class."""
        if cls is None:
            return FileStorage.__objects
        else:
            cls_name = cls.__name__
            return {k: v for k, v in FileStorage.__objects.items() if k.startswith(cls_name)}
        

    def new(self, obj):
        """Sets new obj in __objects dictionary."""
        # print("class Filestorage new ")
        key = f"{obj.__class__.__name__}.{obj.id}"
        FileStorage.__objects[key] = obj

    def save(self):
        """serializes __objects to the JSON file (path: __file_path)"""
        # print("class Filestorage save ")
        new_dict = {}
        for key, obj in type(self).__objects.items():
                new_dict[key] = obj.to_dict()
                # print("class Filestorage save for  ")

        with open(type(self).__file_path, "w", encoding='utf-8') as file:
                json.dump(new_dict, file, indent=4)
                # print("class Filestorage with open save ")

    def reload(self):
        """Deserializes the JSON file to __objects if it exists"""
        # print("class Filestorage reload ")
        class_d = {
            "BaseModel": BaseModel,
            "User": User,
            "Place": Place,
            "State": State,
            "Review": Review,
            "Amenity": Amenity,
            "City": City
        }

        if os.path.exists(FileStorage.__file_path):
            with open(FileStorage.__file_path, "r", encoding='utf-8') as file:
                try:
                    obj_dict = json.load(file)
                    for key, value in obj_dict.items():
                        class_name = value['__class__']
                        obj = class_d[class_name](**value)
                        FileStorage.__objects[key] = obj
                except json.JSONDecodeError:
                    pass
                
    def delete(self, obj=None):
        if obj:
            key = f"{__class__.__name__}.{obj.id}"
            if key in self.__objects:
                del self.__objects[key]