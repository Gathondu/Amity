#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

'''
Usage:
    create room <room_type> <room_name> ...
    check (room_exists|room_availability|person_exist) <name>
    add person <first_name> <last_name> <FELLOW|STAFF> [wants_accomodation]
    allocate space <first_name> <last_name> <person_type> [wants_accomodation]
    reallocate person <first_name> <last_name> <new_room_name>
    remove person <first_name> <last_name> <room_name>
    load (people|state) <filename|database>
    print room <room_name> | (allocations|unallocated) [--o=filename]
    save state [--db=database]
    quit

Arguments:
    FELLOW|STAFF        Type of person to create/employ
    wants_accomodation  Specify if person(only fellow) wants living space

Options:
    -h, --help                          : Show this help messsage
    -o=filename, --option filename      : Specify file
    --db                                : Specify database
'''


import sys
import cmd
import os

from docopt import docopt, DocoptExit
from model.amity import Amity
from termcolor import cprint, colored
from pyfiglet import figlet_format


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
        try:
            name = arg['<room_name>']
            room_type = arg['<room_type>']
            print(self.amity.create_room(room_type+' '+name[0]))
        except Exception as e:
            print(e)

    @docopt_cmd
    def do_check(self, arg):
        '''Usage: check (room_exists|room_availability|person_exist) <name>'''
        try:
            name = arg['<name>']
            if arg['room_exists']:
                print(self.amity.room_exists(name))
            elif arg['room_availability']:
                print(self.amity.check_room_availability(name))
            elif arg['person_exist']:
                print(self.amity.person_exists(name))
        except Exception as e:
            print(e)

    @docopt_cmd
    def do_add(self, arg):
        '''Usage: add person <first_name> <last_name> <FELLOW|STAFF> [wants_accomodation]'''
        try:
            name = arg['<first_name>'] + ' ' + arg['<last_name>']
            if arg['<FELLOW']:
                typ = arg['<FELLOW']
            if arg['STAFF>']:
                typ = arg['STAFF>']
            person = name + ' ' + typ
            if arg['wants_accomodation']:
                acc = arg['wants_accomodation']
                print(self.amity.add_person(person+' '+acc))
            else:
                print(self.amity.add_person(person))
        except Exception as e:
            print(e)

    @docopt_cmd
    def do_allocate(self, arg):
        '''Usage: allocate space <first_name> <last_name> <person_type> [wants_accomodation]'''
        try:
            person = arg['<first_name>'] + ' ' + arg['<last_name>']
            person = {
                'name': person,
                'type': arg['<person_type>']
            }
            if arg['want_accomodation']:
                print(self.amity.allocate_space(person, True))
            else:
                print(self.amity.allocate_space(person))
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
        '''Usage: remove person <first_name> <last_name> <room_name>'''
        try:
            person = arg['<first_name>'] + ' ' + arg['<last_name>']
            room = arg['<room_name>']
            print(self.amity.remove_person(person, room))
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
        '''Usage: print room <room_name> | (allocations|unallocated) [--o=filename]'''
        try:
            if arg['room']:
                print(self.amity.print_room(arg['<room_name>']))
            elif arg['allocations']:
                if arg['--o']:
                    print(self.amity.print_allocations(arg['--o']))
                else:
                    print(self.amity.print_allocations())
            elif arg['unallocated']:
                if arg['--o']:
                    print(self.amity.print_unallocated(arg['--o']))
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
