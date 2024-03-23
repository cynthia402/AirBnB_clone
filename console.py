#!/usr/bin/python3
""" a command interpreter to manage the AirBnB objects."""
from models import storage
from datetime import datetime
import cmd
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class HBNBCommand(cmd.Cmd):
    """HBNB Command Interpreter."""

    prompt = '(hbnb) '
    __all_cls = {
        "BaseModel", "User", "State", "City", "Amenity",
        "Place", "Review"
    }

    def do_quit(slef, line):
        """Quit command to exit the program"""
        return True

    def do_EOF(self, line):
        """EOF command to exit the program, reached end of line"""
        print()
        return True

    def emptyline(self):
        """Do nothing if the input is empty, newline"""
        pass

    def do_create(self, line):
        """Create a new instance of BaseModel"""
        if line == "":
            print("** class name missing **")
            return
        line = str.split(line)
        if line[0] in HBNBCommand.__all_cls:
            print(eval(line[0])().id)
            storage.save()
        else:
            print("** class doesn't exist **")

    def do_show(self, line):
        """Shows string representation of an instance using class name + id"""
        if line:
            cmd_flag = str.split(line)
            dic_from_storage = storage.all()
            if cmd_flag[0] in self.__all_cls:
                if len(cmd_flag) == 1:
                    print("** instance id missing **")
                elif (len(cmd_flag) > 1 and f"{cmd_flag[0]}.{cmd_flag[1]}"
                        in dic_from_storage.keys()):
                    print(dic_from_storage[f"{cmd_flag[0]}.{cmd_flag[1]}"])
                else:
                    print("** no instance found **")
            else:
                print("** class doesn't exist **")
        else:
            print("** class name missing **")

    def do_destroy(self, line):
        """Delete an instance based on class name and id"""
        if line:
            cmd = str.split(line)
            dic = storage.all()
            if cmd[0] in self.__all_cls:
                if len(cmd) >= 2 and f"{cmd[0]}.{cmd[1]}" in dic:
                    del dic[f"{cmd[0]}.{cmd[1]}"]
                    storage.save()
            else:
                print("** class doesn't exist **")
        else:
            print("** class name missing **")

    def do_all(self, line):
        """Print all instances string format"""
        cmd = str.split(line)
        if (cmd and cmd[0] in self.__all_cls) or len(cmd) == 0:
            dics = storage.all().values()
            alls = []
            for obj in dics:
                if len(cmd) == 0:
                    alls.append(obj.__str__())
                elif cmd[0] == obj.__class__.__name__:
                    alls.append(obj.__str__())
            print(alls)
        else:
            print("** class doesn't exist **")

    def do_update(self, line):
        """Updates an instance based on the class name and
        id by adding or updating attribute (save the change
        into the JSON file)"""

        if line:
            cmd = str.split(line)
            length = len(cmd)
            dics = storage.all()
            if length == 1 and cmd[0] in self.__all_cls:
                print("** instance id missing **")
            elif length == 1 and cmd not in self.__all_cls:
                print("** class doesn't exist **")
            elif (length == 2 and cmd[0] in self.__all_cls and
                    f"{cmd[0]}.{cmd[1]}" in dics):
                print("** attribute name missing **")
            elif (length == 2 and cmd[0] in self.__all_cls and
                    f"{cmd[0]}.{cmd[1]}" not in dics):
                print("** no instance found **")
            elif (length == 3 and cmd[0] in self.__all_cls and
                    f"{cmd[0]}.{cmd[1]}" in dics and cmd[2]):
                print("** value missing **")
            else:
                key = dics[f"{cmd[0]}.{cmd[1]}"].__dict__.keys()
                if cmd[2] in key:
                    t_k = type(dics[f"{cmd[0]}.{cmd[1]}"].__dict__[cmd[2]])
                    dics[f"{cmd[0]}.{cmd[1]}"].__dict__[cmd[2]] = t_k(cmd[3])
                else:
                    dics[f"{cmd[0]}.{cmd[1]}"].__dict__[cmd[2]] = cmd[3]
                storage.save()
        else:
            print("** class name missing **")


if __name__ == '__main__':
    HBNBCommand().cmdloop()
