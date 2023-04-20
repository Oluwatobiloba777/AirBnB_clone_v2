#!/usr/bin/python3
"""Defines the FileStorage class."""
import json
from models.base_model import BaseModel
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


class FileStorage:
    """Represent an abstracted storage engine.

    Attributes:
        __file_path (str): The name of the file to save objects to.
        __objects (dict): A dictionary of instantiated objects.
    """

    __file_path = "file.json"
    __objects = {}

    def all(self, cls=None):
        """Return a dictionary of instantiated objects in storage.

        If a cls is specified, returns a dictionary of objects of that type.
        Otherwise, returns the __objects dictionary.
        """
        model_dict = {}
        if cls:
            for key in FileStorage.__objects.keys():
                if key.split('.')[0] == cls.__name__:
                    model_dict[key] = FileStorage.__objects[key]
            return model_dict
        return FileStorage.__objects

    def new(self, obj):
        """Set in __objects obj with key <obj_class_name>.id."""
        self.all().update({obj.to_dict()['__class__'] + '.' + obj.id: obj})

    def save(self):
        """Serialize __objects to the JSON file __file_path."""
        with open(self.__file_path, "w", encoding="utf-8") as f:
            odict = {}
            odict.update(FileStorage.__objects)
            for key, value in odict.items():
                odict[key] = value.to_dict()
            json.dump(odict, f)

    def reload(self):
        """ it loads storage from file"""

        model_classes = {
            'BaseModel': BaseModel, 'Amenity': Amenity, 'City': City, 'Place': Place,
            'Review': Review, 'State': State, 'User': User
        }
        try:
            with open(self.__file_path, "r", encoding="utf-8") as f:
                load_file = json.load(f)
                for key, value in load_file.items():
                    self.all()[key] = model_classes[value['__class__']](**value)
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        """Delete a given object from __objects, if it exists."""
        try:
            del self.__objects["{}.{}".format(type(obj).__name__, obj.id)]
        except (AttributeError, KeyError):
            pass

    def close(self):
        """Call the reload method."""
        self.reload()
