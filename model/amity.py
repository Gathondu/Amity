#!/usr/local/bin/python3
# -*- coding: utf-8 -*-


from model.person import Fellow, Staff
from model.room import Office, LivingSpace


class Amity:
    offices = {}
    living_spaces = {}
    rooms_allocations = {}
    staff = {}
    fellow = {}
    true = ('y', 'yes')

    def __init__(self):
        self.offices = {}
        self.living_spaces = {}
        self.rooms_allocations = {}
        self.staff = {}
        self.fellow = {}

    def add_person(self, *args):
        """This function employs  a new new person as  a staff or fellow."""
        # import pdb; pdb.set_trace()
        if len(args) < 1:
            raise ValueError('please specify name type and' +
                             ' if person wants living space in case of fellows'
                             )
        for person in args:
            details = person.lower().split()
            if len(details) > 4:
                raise ValueError('give just two names, type of person and' +
                                 ' y if its a fellow who wants accomodation')
            elif len(details) < 2:
                raise ValueError('give at least a name and the type of person')

            name = [name for name in details if name not in
                    ('staff', 'fellow', 'y', 'yes')]
            if ''.join(name).isalpha():
                name = ' '.join(name)
            else:
                raise ValueError('name must be alphabetic chars.' +
                                 ' {} is incorrect'.format(name))
            person_type = [typ for typ in details if typ in
                           ('staff', 'fellow')]
            wants_livingspace = [space for space in details if space
                                 in ('y', 'yes')]
            if len(wants_livingspace) == 1:
                wants_livingspace = ''.join(wants_livingspace)
            elif len(wants_livingspace) > 1:
                raise ValueError(
                    'only specify once if fellow wants living space'
                    )
            else:
                wants_livingspace = ''

            if len(person_type) > 1:
                raise ValueError('person type specified twice')
            elif len(person_type) < 1:
                raise ValueError('person type not specified.' +
                                 ' Should be staff or fellow')
            else:
                person_type = ''.join(person_type)

            if person_type == 'staff' and wants_livingspace in self.true:
                raise ValueError('staff cannot be assigned LivingSpace')
            if person_type == 'staff':
                if name in self.staff.keys():
                    raise ValueError('staff {} already exsists.'.format(name))
                else:
                    self.staff[name] = Staff(name)
                    return 'staff {} added'.format(name)
            if person_type == 'fellow':
                if name in self.fellow.keys():
                    raise ValueError('fellow {} already exsists.'.format(name))
                else:
                    if wants_livingspace in self.true:
                        fellow = Fellow(name, True)
                    else:
                        fellow = Fellow(name)
                    self.fellow[name] = fellow
                    return 'fellow {} added'.format(name)

    def allocate_space(name, position, livaing_space):
        """This function allocates space to new employees."""
        pass

    def check_room_availability(room_name):
        """This function checks for the availability of rooms in amity"""
        pass

    def create_room(*args):
        """This function creates a new room in amity"""
        pass

    def reallocate_person(person, room_name):
        """This function reallocates an employee from one room to another"""
        pass

    def load_people():
        """This function loads employees from the database."""
        pass

    def print_allocations():
        """This function prints out the allocated rooms"""
        pass

    def print_unallocated():
        """This function prints out the unallocated rooms"""
        pass

    def print_room(room_name):
        """This function prints the people in rooms contained in amity"""
        pass

    def save_state():
        """This function saves the running state of amity to the database"""
        pass

    def load_state():
        """This function loads amity resourses from the database"""
        pass
