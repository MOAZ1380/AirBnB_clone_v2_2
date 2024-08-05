#!/usr/bin/python3
"""An interactive shell?"""
import cmd
from models.base_model import BaseModel
from models import storage
from models.engine.file_storage import FileStorage
from models.user import User
from models.city import City
from models.amenity import Amenity
from models.review import Review
from models.state import State
from models.place import Place

classname = {
            "BaseModel": BaseModel,
            "User": User,
            "Place": Place,
            "State": State,
            "Review": Review,
            "Amenity": Amenity,
            "City": City
        }


class HBNBCommand(cmd.Cmd):

    prompt = '(hbnb)'

    def do_quit(self, arg):
        """Quit command to exit the program"""
        return True

    def do_EOF(self, arg):
        """End of File command to exit the program"""
        print('')
        return True

    def emptyline(self):
        """Do nothing on empty input line"""
        pass

    def do_help(self, arg):
        if arg:
            if arg == 'quit':
                print('Quit command to exit the program')
            elif arg == 'EOF':
                print('End of File command to exit the program')
            else:
                print(f"No help available for {arg}")
        else:
            print("""
Documented commands (type help <topic>):
========================================
EOF  help  quit
            """)

    # def do_create(self, arg):
    #     """Creates a new instances of a class"""
    #     if arg:
    #         if arg in classname:
    #             new_instance = classname[arg]()
    #             new_instance.save()
    #             print(new_instance.id)
    #         else:
    #             print("** class doesn't exist **")
    #     else:
    #         print("** class name missing **")
            
    def do_create(self, arg):
        """Creates a new instance of a class with given parameters"""
        if not arg:
            print("** class name missing **")
            return
        
        args = arg.split()
        class_name = args[0]
        
        if class_name not in classname:
            print("** class doesn't exist **")
            return
        
        
        
        new_instance = classname[class_name]()
        params = args[1:]

        for param in params:
            key_value = param.split("=")
            if len(key_value) != 2:
                continue
            key, value = key_value
            if value.startswith('"') and value.endswith('"'):
                value = value[1:-1].replace('_', ' ').replace('\\"', '"')
                # print(value)
            elif '.' in value:
                try:
                    value = float(value)
                except ValueError:
                    continue
            else:
                try:
                    value = int(value)
                except ValueError:
                    continue

            setattr(new_instance, key, value)
            
        new_instance.save()
        print(new_instance.id)
            
        
        
        
        
        
        
        


    def do_show(self, arg):
        """print <class name> <id>"""
        split_arg = arg.split()

        if len(split_arg) < 1:
            print("** class name missing **")
        elif split_arg[0] not in classname:
            print("** class doesn't exist **")
        elif len(split_arg) < 2:
            print("** instance id missing **")
        else:
            new_str = f"{split_arg[0]}.{split_arg[1]}"
            obj_sp = storage.all().get(new_str)
            if obj_sp:
                print(obj_sp)
            else:
                print("** no instance found **")

    def do_destroy(self, arg):
        """Destroy command deletes an instance based on the cl"""
        split_arg = arg.split()

        if len(split_arg) < 1:
            print("** class name missing **")
        elif split_arg[0] not in classname:
            print("** class doesn't exist **")
        elif len(split_arg) < 2:
            print("** instance id missing **")
        else:
            new_str = f"{split_arg[0]}.{split_arg[1]}"
            if new_str not in storage.all().keys():
                print("** no instance found **")
            else:
                del(storage.all()[new_str])
                storage.save()

    def do_all(self, arg):
        """ Print all instances in string representation """

        if arg:
            if arg in classname:
                for key, value in storage.all().items():
                    print(str(value))

            else:
                print("** class doesn't exist **")
        else:
            for key, value in storage.all().items():
                print(str(value))

    def do_update(self, arg):
        """Update a class instance of a given id by adding or updating
        a given attribute key/value pair or dictionary.
        usage:  update <class> <id> <attribute_name> <attribute_value> or
                <class>.update(<id>, <attribute_name>, <attribute_value>) or
                <class>.update(<id>, <dictionary>)
        """
        split_arg = arg.split()

        if len(split_arg) < 1:
            print("** class name missing **")

        elif split_arg[0] not in classname:
            print("** class doesn't exist **")

        elif len(split_arg) < 2:
            print("** instance id missing **")

        else:
            new_str = f"{split_arg[0]}.{split_arg[1]}"
            if new_str not in storage.all().keys():
                print("** no instance found **")

            elif len(split_arg) < 3:
                print("** attribute name missing **")

            elif len(split_arg) < 4:
                print("** value missing **")

            else:
                setattr(storage.all()[new_str], split_arg[2], split_arg[3])
                storage.save()
                
    


if __name__ == '__main__':
    HBNBCommand().cmdloop()