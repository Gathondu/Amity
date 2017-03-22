#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

'''
Usage:
    create room <room_type> <room_name> ...
    check (rooms|room_availability|person_exist) <name>
    add person <first_name> <last_name> <FELLOW>|<STAFF> [<wants_accomodation>]
    allocate space <first_name> <last_name>
    reallocate person <first_name> <last_name> <new_room_name>
    remove person <first_name> <last_name> [-r]
    load (people|state) <filename>|<database>
    print room <room_name> | (allocations|unallocated) [--o=filename]
    save state [--db=database]
    quit

Arguments:
    FELLOW|STAFF        Type of person to create/employ
    wants_accomodation  Specify if person(only fellow) wants living space

Options:
    -h, --help           : Show this help messsage
    -r                   : Specify person to be removed from room and not amity
    --o=filename         : Specify filename to save or read from
    --db=database        : Specify database to save or read from
'''


import sys
import cmd
import os

from docopt import docopt, DocoptExit
from termcolor import cprint, colored
from pyfiglet import figlet_format

from model.amity import Amity


def docopt_cmd(func):
    """
    This decorator is used to simplify the try/except block and pass the result
    of the docopt parsing to the called action.
    """
    def fn(self, arg):
        try:
            opt = docopt(fn.__doc__, arg)
        except DocoptExit as e:
            # The DocoptExit is thrown when the args do not match.
            # We print a message to the user and the usage block.
            print('Invalid Command!')
            print(e)
            return
        except SystemExit:
            # The SystemExit exception prints the usage for --help
            # We do not need to do the print here.
            return
        return func(self, opt)
    fn.__name__ = func.__name__
    fn.__doc__ = func.__doc__
    fn.__dict__.update(func.__dict__)
    return fn
border = colored("*" * 20, 'cyan').center(80)


def introduction():
    print (border)
    print ("WELCOME TO AMITY SPACE ALLOCATION!".center(70))
    print(__doc__)
    print (border)


class AmityApplication(cmd.Cmd):
    cprint(figlet_format('AMITY', font='banner3-D'), 'cyan', attrs=['bold'])
    prompt = "Amity -->"
    amity = Amity()

    @docopt_cmd
    def do_create(self, arg):
        '''Usage: create room <room_type> <room_name> ...'''
        name = arg['<room_name>']
        room_type = arg['<room_type>']
        for room in name:
            try:
                print(self.amity.create_room(room_type, room))
            except Exception as e:
                print(e)

    @docopt_cmd
    def do_check(self, arg):
        '''Usage: check room_type <type> | (room_availability |person) <name>...'''
        try:
            name = ' '.join(arg['<name>'])
            if arg['room_type']:
                rooms = self.amity.get_room(room_type=arg['<type>'])
                result = ''
                for room in rooms:
                    result += room['name'].upper() + ', '
                print(result[:-2])
            elif arg['room_availability']:
                print(self.amity.check_room_availability(name))
            elif arg['person']:
                if self.amity.person_exists(name):
                    print('{} exists'.format(name))
                else:
                    print("{} doesn't exist".format(name))
        except Exception as e:
            print(e)

    @docopt_cmd
    def do_add(self, arg):
        '''Usage: add person <first_name> <last_name> (<FELLOW>|<STAFF>)
         [<wants_accomodation>]'''
        try:
            if not arg['<first_name>']:
                raise ValueError('both names must be specifed specified')
            if arg['<last_name>'].lower() in ('fellow', 'staff'):
                raise ValueError('both names must be specifed specified')
            name = arg['<first_name>'] + ' ' + arg['<last_name>']
            if arg['<FELLOW>']:
                role = arg['<FELLOW>']
            if arg['<STAFF>']:
                role = arg['<STAFF>']
            if arg['<wants_accomodation>']:
                accomodation = arg['<wants_accomodation>'].lower()
                if accomodation in ('y', 'yes'):
                    print(self.amity.add_person(role, name, True))
                else:
                    raise ValueError('wants accomodation has to be y or yes')
            else:
                print(self.amity.add_person(role, name))
        except Exception as e:
            print(e)

    @docopt_cmd
    def do_allocate(self, arg):
        '''Usage: allocate space <name> ...'''
        try:
            person_name = ' '.join(arg['<name>'])
            print(self.amity.allocate_person(person_name))
        except Exception as e:
            print(e)

    @docopt_cmd
    def do_reallocate(self, arg):
        '''Usage: reallocate person <first_name> <last_name> <new_room_name>'''
        try:
            person = arg['<first_name>'] + ' ' + arg['<last_name>']
            room = arg['<new_room_name>']
            print(self.amity.reallocate_person(person, room))
        except Exception as e:
            print(e)

    @docopt_cmd
    def do_remove(self, arg):
        '''Usage: remove person <name> ... [-r]'''
        try:
            person = ' '.join(arg['<name>'])
            if arg['-r']:
                self.amity.remove_person_from_room(person)
            else:
                print(self.amity.remove_person(person))
        except Exception as e:
            print(e)

    @docopt_cmd
    def do_load(self, arg):
        '''Usage: load people <filename> | state <database>'''
        try:
            if arg['people']:
                print(self.amity.load_people(arg['<filename>']))
            elif arg['state']:
                print(self.amity.load_state(arg['<database>']))
        except Exception as e:
            print(e)

    @docopt_cmd
    def do_print(self, arg):
        '''Usage: print room <room_name> | (allocations|unallocated)
        [--o=filename]'''
        try:
            if arg['room']:
                print(self.amity.print_room(arg['<room_name>']))
            elif arg['allocations']:
                if arg['--o']:
                    print(self.amity.print_allocations(filename=arg['--o']))
                else:
                    print(self.amity.print_allocations())
            elif arg['unallocated']:
                if arg['--o']:
                    print(self.amity.print_unallocated(filename=arg['--o']))
                else:
                    print(self.amity.print_unallocated())
        except Exception as e:
            print(e)

    @docopt_cmd
    def do_save(self, arg):
        '''Usage: save state [--db=database]'''
        try:
            if arg['--db']:
                print(self.amity.save_state(arg['--db']))
            else:
                print(self.amity.save_state())
        except Exception as e:
            print(e)

    @docopt_cmd
    def do_quit(self, arg):
        '''Usage: quit '''
        print("GOODBYE!!!")
        exit()

if __name__ == '__main__':
    introduction()
    AmityApplication().cmdloop()
