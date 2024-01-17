#!/usr/bin/python3
"""
This module contains the entry point of the command interpreter.
It defines the Console class, which contains the functionality for the
HBNB console.

Usage: ./console.py (interactive mode)
       ./console.py <command> (one time execution mode)

Classes:
    HBNBCommand - contains the functionality for the HBNB console

Dependencies:
    cmd - implements the command line interpreter
    sys - provides access to some variables used or maintained by the
          interpreter and to functions that interact strongly with the
          interpreter
    models.base_model - defines all common attributes/methods for other
                        classes
    models.__init__ - initializes a storage engine
    models.user - defines attributes/methods for the User class
    models.place - defines attributes/methods for the Place class
    models.state - defines attributes/methods for the State class
    models.city - defines attributes/methods for the City class
    models.amenity - defines attributes/methods for the Amenity class
    models.review - defines attributes/methods for the Review class
"""
import re  # Availing regular expression functionality
import json  # Availing JSON functionality
import shlex  # Availing lexical analysis functionality
import cmd  # Availing most of the functionality for the console
import sys  # Availing the isatty() method to determine interactive mode
from models.base_model import BaseModel  # Availing the BaseModel class
from models.__init__ import storage  # Availing the storage engine
from models.user import User  # Availing the User class
from models.place import Place  # Availing the Place class
from models.state import State  # Availing the State class
from models.city import City   # Availing the City class
from models.amenity import Amenity  # Availing the Amenity class
from models.review import Review  # Availing the Review class


class HBNBCommand(cmd.Cmd):  # Implementation of the HBNB console
    """
    Fully functional command interpreter for the HBNB project.

    Attributes:
        prompt - determines prompt for interactive/non-interactive modes
        classes - dictionary of classes available for use in console
        dot_cmds - list of commands that use dot notation
        types - dictionary of types for dot notation commands

    Methods:
        preloop - prints if isatty is false
        precmd - reformat command line for advanced command syntax
        postcmd - prints if isatty is false
        do_quit - method to exit the HBNB console
        help_quit - prints the help documentation for quit
        do_EOF - handles EOF to exit program
        help_EOF - prints the help documentation for EOF
        emptyline - overrides the emptyline method of CMD
        do_create - create an object of any class
        _parse_value - parse a value string based on its format
        help_create - help information for the create method
        do_show - method to show an individual object
        help_show - help information for the show command
        do_destroy - destroys a specified object
        help_destroy - help information for the destroy command
        do_all - shows all objects, or all objects of a class
        help_all - help information for the all command
        do_count - count current number of class instances
        help_count - help information for the count command
        do_update - updates a certain object with new info
        help_update - help information for the update class
    """
    prompt = '(hbnb)'  # Set prompt to be used by Cmd

    classes = {
               'BaseModel': BaseModel, 'User': User, 'Place': Place,
               'State': State, 'City': City, 'Amenity': Amenity,
               'Review': Review
              }
    types = {
             'number_rooms': int, 'number_bathrooms': int,
             'max_guest': int, 'price_by_night': int,
             'latitude': float, 'longitude': float
            }

    def default(self, line):
        """
        Handles advanced command syntax.
        It is executed when a command is not recognized.

        Usage: <class name>.<command>([<id> [<*args> or <**kwargs>]])
        (Brackets denote optional fields in usage example.)
        The following commands are supported:
            <class name>.all()
            <class name>.count()
            <class name>.create()
            <class name>.show(<id>)
            <class name>.destroy(<id>)
            <class name>.update(<id>, <attribute name>, <attribute value>)
            <class name>.update(<id>, <dictionary representation>)
        """
        functions = {
                "all": self.do_all,
                "count": self.do_count,
                "create": self.do_create,
                "show": self.do_show,
                "destroy": self.do_destroy,
                "update": self.do_update
                }
        regex = r"(.*)\.(.*)\((.*)\)"  # Matches <class>.<command>(<id>)
        if re.search(regex, line):  # If line matches regex
            inputs = re.sub(regex, r"\2 \1 \3", line)  # Rearrange to normal
            inputs = shlex.split(inputs)  # Split into list respecting quotes
            if inputs[0] in functions.keys():  # If command is supported
                # The update is a special case, so it is handled separately
                if inputs[0] == "update" and '{' in line and '}' in line:
                    self.dict_update(inputs[1], line)

                else:
                    functions[inputs[0]](' '.join(inputs[1:]))  # Execute
            else:  # If command is not supported
                print(f"*** Unknown syntax: {line}")
        else:  # If line does not match regex
            print(f"*** Unknown syntax: {line}")

    def dict_update(self, classname, line):
        '''
        Performs the update method on an item passed with a dictionary
            of attribute/value pairs.

        Args:
            classname (str): Name of the class of object to be updated.
            line (str): Unprocessed string as recieved from the console.
        '''
        dictionary = re.findall("({.*})", line)
        dictionary[0] = dictionary[0].replace("\'", "\"")
        inputs = json.loads(dictionary[0])
        grouped_strings = re.findall("(\".*?\")", line)
        id_string = grouped_strings[0].replace("\"", "")
        for key, val in inputs.items():
            self.do_update(classname + " " + id_string + " " + key + " " +
                           str(val))

    def do_quit(self, command):
        """ Method to exit the HBNB console"""
        exit()

    def help_quit(self):
        """ Prints the help documentation for quit  """
        print("Exits the program with formatting\n")

    def do_EOF(self, arg):
        """ Handles EOF to exit program """
        print()
        exit()

    def help_EOF(self):
        """ Prints the help documentation for EOF """
        print("Exits the program without formatting\n")

    def emptyline(self):
        """ Overrides the emptyline method of CMD """
        pass

    def do_create(self, arg):
        """
        Create a new instance of a class and print its id.
        Usage: create <class name> [<param name>=<param value>]
               <class name>.create()
        (Brackets denote optional fields in usage example.)
        NOTE: Spacing in strings must be done using a dash (_).
              Strings must start and end with double_quotes(").

        Exceptions:
            Prints "** class name missing **" if no class name is given.
            Prints "** class doesn't exist **" if the class name is invalid.
        """
        # Handle missing class name
        if not arg:
            print("** class name missing **")
            return
        # Extract class name and parameters
        arg_list = arg.split()
        # Handle invalid class name
        if arg_list[0] not in self.classes.keys():
            print("** class doesn't exist **")
            return

        class_name = arg_list[0]

        # Create an instance of the class with the parsed parameters
        new_instance = eval(class_name)(**self._parse_value(arg_list[1:]))

        # Save the instance and print its id
        print(new_instance.id)
        storage.save()

    def _parse_value(self, args):
        """
        Converts a list into a dictionary of parameters and values.
        Args:
            args (list): List of parameters and values.
                Format: ["<param name>=<param value>", ...]

        Description:
            If value is a string, it is converted to a string.
            If vlue is a number, it is converted to an int or float.
                > The ones containing a dot are converted to float.

        Returns:
            Dictionary of parameters and values. Empty dictionary if
            args is empty or no parameters could be parsed.
        """
        # Initialize dictionary
        kwargs = {}

        # Iterate through args
        for arg in args:
            if '=' in arg:  # If arg is in a valid format
                key, value = arg.split('=')  # Split into key and value
                # Parse value
                if value.startswith('"') and value.endswith('"'):
                    value = value[1:-1].replace("_", " ").replace('"', '')

                elif "." in value:
                    try:
                        value = float(value)
                    except ValueError:
                        continue
                else:
                    try:
                        value = int(value)
                    except ValueError:
                        continue
                # Add key and value to dictionary
                kwargs[key] = value
        return kwargs

    def help_create(self):
        """ Help information for the create method """
        print("Creates a class of any type")
        print("[Usage]: create <className>\n")

    def do_show(self, args):
        """
        Method to show an individual object
        Usage: show <class name> <object id>
                <class name>.show(<object id>)
        Exceptions:
            Prints "** class name missing **" if no class name is given.
            Prints "** class doesn't exist **" if the class name is invalid.
            Prints "** instance id missing **" if no object id is given.
            Prints "** no instance found **" if the object id is invalid.
        """
        if not args:
            print("** class name missing **")
            return
        args = args.strip()  # Remove leading and trailing spaces
        args = args.split()  # Split into list

        if args[0] not in self.classes.keys():
            print("** class doesn't exist **")
            return

        if len(args) == 1:  # If no id is given
            print("** instance id missing **")
            return

        key = f"{args[0]}.{args[1]}"  # Generate key: <class name>.<id>
        try:
            print(storage.all()[key])
        except KeyError:
            print("** no instance found **")

    def help_show(self):
        """ Help information for the show command """
        print("Shows an individual instance of a class")
        print("[Usage]: show <className> <objectId>\n")

    def do_destroy(self, args):
        """
        Destroys a specified object by class name and id.

        Usage: destroy <class name> <object id>
                <class name>.destroy(<object id>)

        Exceptions:
            Prints "** class name missing **" if no class name is given.
            Prints "** class doesn't exist **" if the class name is invalid.
            Prints "** instance id missing **" if no object id is given.
            Prints "** no instance found **" if the object id is invalid.
        """
        if not args:  # Case no argument passed
            print("** class name missing **")
            return
        args = shlex.split(args)  # Turning args into a list
        if args[0] not in self.classes.keys():  # If class name is invalid
            print("** class doesn't exist **")
            return
        if len(args) < 2:  # If no id is given
            print("** instance id missing **")
            return
        key = f"{args[0]}.{args[1]}"  # Generate key: <class name>.<id>
        try:  # Try to delete object
            del storage.all()[key]
            storage.save()
        except KeyError:  # If instance id is invalid
            print("** no instance found **")

    def help_destroy(self):
        """ Help information for the destroy command """
        print("Destroys an individual instance of a class")
        print("[Usage]: destroy <className> <objectId>\n")

    def do_all(self, args):
        """
        Shows all objects, or all objects of a class
        Usage: all [<className>]
                <className>.all()
        """
        print_list = []

        if args:
            args = args.strip()  # Remove leading and trailing spaces
            if args not in self.classes.keys():
                print("** class doesn't exist **")
                return
            for instance in storage.all().values():
                if instance.__class__.__name__ == args:
                    if hasattr(instance, "_sa_instance_state"):
                        delattr(instance, "_sa_instance_state")
                    print_list.append(str(instance))
        else:
            for instance in storage.all().values():
                if hasattr(instance, "_sa_instance_state"):
                    delattr(instance, "_sa_instance_state")
                print_list.append(str(instance))
        print(print_list)

    def help_all(self):
        """ Help information for the all command """
        print("Shows all objects, or all of a class")
        print("[Usage]: all <className>\n")

    def do_count(self, args):
        """
        Count current number of class instances
        Usage: count <class name>
               <class name>.count()
        """
        args = args.split()
        count = 0
        for instance in storage.all().values():  # Iterate through instances
            if args[0] == instance.__class__.__name__:  # If class name matches
                count += 1
        print(count)

    def help_count(self):
        """ """
        print("Usage: count <class_name>")

    def do_update(self, args):
        """
        Updates the attribute values of an object.

        Usage: update <class name> <id> <attribute name> <attribute value>
               <class name>.update(<id>, <attribute name>, <attribute value>)
               <class name>.update(<id>, <dictionary representation>)

        Exceptions:
            Prints "** class name missing **" if no class name is given.
            Prints "** class doesn't exist **" if the class name is invalid.
            Prints "** instance id missing **" if no object id is given.
            Prints "** no instance found **" if the object id is invalid.
            Prints "** attribute name missing **" if no attribute name is
                given.
            Prints "** value missing **" if no attribute value is given.
        """
        if not args:  # Unprovided arguments
            print("** class name missing **")
            return
        args = args.replace(",", "")  # Remove commas
        args = shlex.split(args)  # Split into list respecting quotes

        if args[0] not in self.classes.keys():  # Invalid class name
            print("** class doesn't exist **")
            return
        if len(args) < 2:  # No id provided
            print("** instance id missing **")
            return
        key = f"{args[0]}.{args[1]}"  # Generate key: <class name>.<id>
        # determine if key is present
        if key not in storage.all():
            print("** no instance found **")
            return
        if len(args) < 3:  # No attribute name provided
            print("** attribute name missing **")
            return
        if len(args) < 4:  # No attribute value provided
            print("** value missing **")
            return

        current_obj = storage.all()[key]  # Get current object
        if args[2] == "id" or args[2] == "created_at" or\
                args[2] == "updated_at":
            return
        if args[3].isnumeric():  # If value is a number
            args[3] = int(args[3])
        else:
            try:
                _ = float(args[3])  # Try to convert to float
                arg[3] = float(args[3])  # If successful, convert to float
            except ValueError:
                pass
        setattr(current_obj, args[2], args[3])
        storage.save()

    def help_update(self):
        """ Help information for the update class """
        print("Updates an object with new information")
        print("Usage: update <className> <id> <attName> <attVal>\n")


if __name__ == "__main__":
    HBNBCommand().cmdloop()
