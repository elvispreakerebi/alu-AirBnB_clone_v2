#!/Users/elviskerebi/Documents/python/alu-works/alu-AirBnB_clone_v2/myenv/bin/python3

"""
Command interpreter for managing objects.
"""

import cmd
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
import shlex

class_map = {
    "BaseModel": BaseModel,
    "User": User,
    "State": State,
    "City": City,
    "Amenity": Amenity,
    "Place": Place,
    "Review": Review,
}


class HBNBCommand(cmd.Cmd):
    """Command interpreter for the HBNB application."""
    prompt = "(hbnb) "

    def do_quit(self, arg):
        """Quit command to exit the program."""
        return True

    def do_EOF(self, arg):
        """Handle EOF to exit the program."""
        print()
        return True

    def emptyline(self):
        """Do nothing on empty input line."""
        pass

    def do_help(self, arg):
        """Display help information."""
        print("Commands:")
        print("create <class> - Create a new instance of a class.")
        print("show <class> <id> - Show the string representation of an instance.")
        print("destroy <class> <id> - Delete an instance based on the class name and id.")
        print("all <class> - Show all instances of a class, "
              "or all classes if no class is specified."
        )
        print(
            "update <class> <id> <attribute_name> <attribute_value> - Update an instance "
            "based on the class name and id."
        )

    def parse_create_args(self, arg):
        """Helper function to parse arguments for create."""
        args = shlex.split(arg)
        if len(args) == 0:
            return None, None, "** class name missing **"
        
        class_name = args[0]
        if class_name not in class_map:
            return None, None, "** class doesn't exist **"
        
        attributes = {}
        for pair in args[1:]:
            if "=" in pair:
                key, value = pair.split("=", 1)
                if value.startswith('"') and value.endswith('"'):
                    value = value[1:-1].replace('\\"', '"')  # Remove surrounding quotes and unescape quotes
                attributes[key] = value
        
        return class_name, attributes, None
    def do_create(self, arg):
        """Create a new instance of a model, save it to the database, and print the ID."""
        class_name, attributes, error = self.parse_create_args(arg)
        if error:
            print(error)
            return
        try:
            new_instance = class_map[class_name](**attributes)
            new_instance.save()
            print(new_instance.id)
        except Exception as e:
            print(f"Error: {e}")

    def do_show(self, arg):
        """Show the string representation of an instance."""
        args = arg.split()
        if len(args) == 0:
            print("** class name missing **")
            return
        if args[0] not in class_map:
            print("** class doesn't exist **")
            return
        if len(args) == 1:
            print("** instance id missing **")
            return
        key = f"{args[0]}.{args[1]}"
        obj = storage.all().get(key)
        if not obj:
            print("** no instance found **")
        else:
            print(obj)

    def do_destroy(self, arg):
        """Destroy an instance."""
        args = arg.split()
        if len(args) == 0:
            print("** class name missing **")
            return
        if args[0] not in class_map:
            print("** class doesn't exist **")
            return
        if len(args) == 1:
            print("** instance id missing **")
            return
        key = f"{args[0]}.{args[1]}"
        if key in storage.all():
            storage.delete(storage.all()[key])
            storage.save()
        else:
            print("** no instance found **")

    def do_all(self, arg):
        """Show all instances, or all instances of a specific class."""
        if arg and arg not in class_map:
            print("** class doesn't exist **")
            return
        obj_list = []
        for obj in storage.all().values():
            if not arg or obj.__class__.__name__ == arg:
                obj_list.append(str(obj))
        print(obj_list)

    def do_update(self, arg):
        """Update an instance based on class name and id."""
        args = arg.split()
        if len(args) == 0:
            print("** class name missing **")
            return
        if args[0] not in class_map:
            print("** class doesn't exist **")
            return
        if len(args) == 1:
            print("** instance id missing **")
            return
        key = f"{args[0]}.{args[1]}"
        obj = storage.all().get(key)
        if not obj:
            print("** no instance found **")
            return
        if len(args) == 2:
            print("** attribute name missing **")
            return
        if len(args) == 3:
            print("** value missing **")
            return
        attr_name = args[2]
        attr_value = args[3]
        # Convert value to appropriate type
        try:
            if attr_value.isdigit():
                attr_value = int(attr_value)
            elif attr_value.replace(".", "", 1).isdigit():
                attr_value = float(attr_value)
            else:
                attr_value = attr_value.strip('"').strip("'")
        except ValueError:
            pass
        setattr(obj, attr_name, attr_value)
        obj.save()


if __name__ == "__main__":
    HBNBCommand().cmdloop()
