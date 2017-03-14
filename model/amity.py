#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
import random
import sqlite3


from model.person import Fellow, Staff
from model.room import Office, LivingSpace


class Amity:
    __true = ('y', 'yes')
    __person_type = ('staff', 'fellow')
    __room_type = ('office', 'livingspace')

    def __init__(self):
        self.rooms = []
        self.people = []
        self._results = []
        self.conn = sqlite3.connect('amity.db')

    def room_exists(self, name):
        if self.rooms != []:
            for room in self.rooms:
                if name == room['name']:
                    return True
        return False

    def create_room(self, *args):
        """This function creates a new room in amity"""
        self._results = []  # clear the results
        if len(args) < 1:  # check that at least one room has been specified
            raise ValueError('specify the name and type of class to create')

        for room in args:
            if not isinstance(room, str):
                raise ValueError(
                    'name must be a string and not an integer or float'
                    )
            details = room.lower().split()
            # ensure that atleast the room type and name is given
            if len(details) > 2:
                raise ValueError(
                    'give just the type and name of the room or' +
                    'livingspace without spaces'
                    )
            elif len(details) < 2:
                raise ValueError('give at least room type and name')

            name = [name for name in details if name not in (self.__room_type)]
            name = ' '.join(name)
            room_type = [typ for typ in details if typ in self.__room_type]
            # ensure room type is only specified once
            if len(room_type) > 1:
                raise ValueError(
                    'room type specifed {} times'.format(len(room_type))
                    )
            elif len(room_type) < 1:
                raise ValueError(
                    'room type not specified. should be office or livingspace'
                    )
            else:
                room_type = ''.join(room_type)

            if room_type == 'office':
                if self.room_exists(name):
                    raise ValueError(
                        'room with name {} already exists.'.format(name)
                        )
                else:
                    office = Office(name)
                    # add attribute to hold occupants
                    office.__dict__['occupants'] = []
                    self.rooms.append(office.__dict__)
                    self._results.append('office {} created'.format(name))

            if room_type == 'livingspace':
                if self.room_exists(name):
                    raise ValueError(
                        'room with name {} already exists.'.format(name)
                        )
                else:
                    ls = LivingSpace(name)
                    # add attribute to hold occupants
                    ls.__dict__['occupants'] = []
                    self.rooms.append(ls.__dict__)
                    self._results.append('livingspace {} created'.format(name))
        if len(self._results) > 1:
            return self._results
        else:
            return self._results[0]

    def allocate_space(self, person, livingSpace=False):
        """This function allocates space to new employees."""
        if person['type'] == 'staff':
            rooms = [
                room for room in self.rooms
                if room['room_type'] == 'office'
                ]
            room = random.choice(rooms)
            ind = self.rooms.index(room)
            if self.check_room_availability(self.rooms[ind]['name']):
                self.rooms[ind]['occupants'].append(person['name'])
            else:
                self.allocate_space(person)
        else:
            rooms = [
                room for room in self.rooms
                if room['room_type'] == 'office'
                ]
            room = random.choice(rooms)
            ind = self.rooms.index(room)
            if self.check_room_availability(self.rooms[ind]['name']):
                self.rooms[ind]['occupants'].append(person['name'])
            else:
                self.allocate_space(person)

            # if fellow wants living space assign them a living space too
            if livingSpace:
                rooms = [
                    room for room in self.rooms
                    if room['room_type'] == 'living space'
                    ]
                room = random.choice(rooms)
                ind = self.rooms.index(room)
                if self.check_room_availability(self.rooms[ind]['name']):
                    self.rooms[ind]['occupants'].append(person['name'])
                else:
                    self.allocate_space(person, True)

    def check_room_availability(self, room_name):
        """This function checks for the availability of rooms in amity"""
        return [
            room['_MAX_SPACE'] - len(room['occupants'])
            for room in self.rooms
            if room['name'] == room_name
        ][0]

    def person_exists(self, name):
        if self.people != []:
            for person in self.people:
                if name == person['name']:
                    return True
        return False

    def remove_person(self, name, room_name):
        if self.room_exists(room_name):
            room = [
                room for room in self.rooms if room['name'] == room_name
            ][0]
            ind = self.rooms.index(room)
            if self.person_exists(name):
                if name in room['occupants']:
                    self.rooms[ind]['occupants'].remove(name)
                    return '{} removed successfully from {}'.format(name, room_name)
                else:
                    raise ValueError(
                        '{} is not assigned to {}'.format(name, room_name)
                    )
            else:
                raise ValueError("person {} doesn't exist.".format(name))
        else:
            raise ValueError("room {} doesn't exist".format(room_name))

    def reallocate_person(self, person, room_name):
        """This function reallocates an employee from one room to another"""
        typ = [
            room['room_type'] for room in self.rooms
            if room['name'] == room_name
        ]
        if typ == []:  # check if the room exists
            raise ValueError('no such room as {}'.format(room_name))
        typ = typ[0]  # index 0 to return the string and not the list
        person_validate = [p for p in self.people if p['name'] == person]
        # check if that person exists
        if person_validate == []:
            raise ValueError("person {} doesn't exsist".format(person))
        # validate staff isn't allocated to living space
        if person_validate[0]['person_type'] == 'staff':
            if typ == 'living space':
                raise ValueError(
                    'staff {} cannot be allocated living space'.format(person)
                    )
        # validate fellow who doesn't want living space isn't
        # allocated living space
        if person_validate[0]['person_type'] == 'fellow':
            if typ == 'living space' and '_wants_living_space' not in person_validate[0].keys():
                raise ValueError(
                    'fellow {} cannot be allocated living space' +
                    ' as they opted out'.format(person)
                    )
        room = [
            room for room in self.rooms if person in room['occupants'] and
            room['room_type'] == typ
        ]
        room = room[0]
        if room['name'] == room_name:  # check if reallocating to same room
            raise ValueError(
                '{} is already allocated to {} {}'
                .format(person, typ, room_name))
        # index 0 to return the dictionary and not the list
        ind = self.rooms.index(room)
        new_room = [
            room for room in self.rooms if room['name'] == room_name and
            room['room_type'] == typ
        ][0]
        new_ind = self.rooms.index(new_room)
        if self.check_room_availability(room_name):
            self.rooms[new_ind]['occupants'].append(person)
            self.rooms[ind]['occupants'].remove(person)
            return '{} reallocated to {} {}'.format(person, typ, room_name)
        else:
            raise ValueError(
                '{} {} has maximum number of occupants'.
                format(self.rooms[new_ind]['room_type'],
                       self.rooms[new_ind]['name'])
                )

    def load_people(self, filename):
        """This function loads employees from a txt file."""
        with open(filename, 'r') as file:
            people = file.readlines()
        for line in people:
            if line != '':
                self.add_person(line[:-1])

    def print_allocations(self, filename=None):
        """This function prints out the allocated rooms"""
        allocations = {
            room['name'].upper(): room['occupants'] for room in self.rooms
            if room['occupants'] != []
            }
        result = ''
        for name, people in allocations.items():
            persons = ''
            for person in people:
                persons += person.upper() + ', '
            # persons[:-2] to strip out the last comma
            result += '{}\n'.format(name)+'-'*20+' \n{}\n\n'.format(persons[:-2])
        if filename is None:
            return result
        else:
            with open(filename, 'w') as file:
                file.writelines(result)

    def print_unallocated(self, filename=None):
        """This function prints out the unallocated rooms"""
        allocated = set()
        for room in self.rooms:
            for person in room['occupants']:
                allocated.add(person)
        unallocated = [
            person['name'].upper() for person in self.people
            if person['name'] not in allocated
        ]
        result = '\nUNALLOCATED\n'+'-'*20+'\n'
        if unallocated == []:
            result += 'NONE'
        else:
            for person in unallocated:
                result += '{}\n'.format(person)
        if filename is None:
            return result
        else:
            with open(filename, 'w') as file:
                file.writelines(result)

    def print_room(self, room_name):
        """This function prints the people in rooms contained in amity"""
        if room_name in [room['name'] for room in self.rooms]:
            num = [
                [people.upper() for people in room['occupants']]
                for room in self.rooms if room['name'] == room_name
            ][0]
            if num == []:
                return 'no one has been assigned to {} yet'.format(room_name)
            else:
                return ', '.join(num)
        else:
            raise ValueError('no such room as {} in amity'.format(room_name))

    def add_person(self, *args):
        """This function employs  a new new person as  a staff or fellow."""
        if len(args) < 1:  # check that at least one person has been specified
            raise ValueError('please specify name, type of person and' +
                             ' if person wants living space in case of fellows'
                             )

        self._results = []  # clear the results argument
        for person in args:
            details = person.lower().split()
            # ensure that only 2 names are supplied, person type
            # and y for fellows.
            if len(details) > 4:
                raise ValueError('give just two names, type of person and' +
                                 ' y if its a fellow who wants accomodation')
            elif len(details) < 3:
                raise ValueError(
                    'give at least two names and the type of person'
                    )

            name = [name for name in details if name not in
                    (self.__person_type + self.__true)]
            # ensure that name contains only alphabetic chars
            if ''.join(name).isalpha():
                name = ' '.join(name)
            else:
                raise ValueError('name must be alphabetic chars.' +
                                 ' {} is incorrect'.format(' '.join(name)))

            wants_livingspace = [space for space in details if space
                                 in self.__true]
            # ensure that only one value for the fellow wanting living space
            # has been provided
            if len(wants_livingspace) == 1:
                wants_livingspace = ''.join(wants_livingspace)
            elif len(wants_livingspace) > 1:
                raise ValueError(
                    'only specify once if fellow wants living space'
                    )
            else:
                wants_livingspace = ''

            person_type = [typ for typ in details if typ in
                           (self.__person_type)]
            # ensure that the person type is only specified once
            if len(person_type) > 1:
                raise ValueError(
                    'person type specified {} times'.format(len(person_type))
                    )
            elif len(person_type) < 1:
                raise ValueError('person type not specified.' +
                                 ' Should be staff or fellow')
            else:
                person_type = ''.join(person_type)
            if person_type == 'staff' and wants_livingspace in self.__true:
                raise ValueError('staff cannot be assigned LivingSpace')
            if person_type == 'staff':
                if self.person_exists(name):
                    raise ValueError('person {} already exsists.'.format(name))
                else:
                    self.people.append(Staff(name).__dict__)
                    self.allocate_space({'name': name, 'type': 'staff'})
                    self._results.append('staff {} added'.format(name))
            if person_type == 'fellow':
                if self.person_exists(name):
                    raise ValueError('person {} already exsists.'.format(name))
                else:
                    if wants_livingspace in self.__true:
                        self.people.append(Fellow(name, True).__dict__)
                        self.allocate_space(
                            {'name': name, 'type': 'fellow'}, True
                            )
                    else:
                        self.people.append(Fellow(name).__dict__)
                        self.allocate_space({'name': name, 'type': 'fellow'})
                    self._results.append('fellow {} added'.format(name))
        if len(self._results) > 1:
            return self._results
        else:
            return self._results[0]

    def save_state(self):
        """This function saves the running state of amity to the database"""
        for person in self.people:
            self.conn.execute('''
            INSERT INTO people (name,type,wants_livingspace)
            VALUES ({},{},{})
            '''.format(
                person['name'],
                person['person_type'],
                person['_wants_living_space'] if '_wants_living_space' in person.keys() else False
            ))

    def load_state(self):
        """This function loads amity resourses from the database"""
        pass
