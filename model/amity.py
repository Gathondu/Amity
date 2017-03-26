#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
import random

from termcolor import cprint, colored

from model.person import Fellow, Staff
from model.room import Office, LivingSpace
from model.database import Database, Person, Room


class Amity:
    '''This class creates rooms, adds people and randomly allocates people
       to the rooms'''

    rooms = []  # list of rooms in amity
    people = []  # list of people in amity

    def __init__(self, database=None):
        '''Initialize this class with a database or let the class
        create one automatically'''
        self.database = Database(database)

    def room_exists(self, name):
        '''Check that a room with the specified name exists'''
        if self.rooms:
            for room in self.rooms:
                if name == room['name']:
                    return room
        return None

    def create_room(self, room_type, room_name):
        """Create a new room in amity"""
        try:
            if not isinstance(room_type, str) or not \
                    isinstance(room_name, str):
                raise ValueError('Room name and type must be a string and ' +
                                 'not an integer or float!')
            elif room_type.lower() not in ('livingspace', 'office'):
                raise ValueError('Room type is incorrect. Must be office or ' +
                                 'livingspace!')
            elif not room_name.isalpha():
                raise ValueError('Room name cannot be empty or have special ' +
                                 'characters.\n{} is not a valid name!\n'
                                 .format(room_name))
            if self.room_exists(room_name):
                raise ValueError('Room with name {} already exists!'.format(
                    room_name))
            elif room_type == 'office':
                return self.create_office(room_name)
            elif room_type == 'livingspace':
                return self.create_livingspace(room_name)
        except Exception:
            raise

    def create_livingspace(self, name):
        """Create a new livingspace in amity"""
        livingspace = LivingSpace(name)
        self.rooms.append(livingspace.__dict__)
        return colored('Livingspace {} created.'.format(name), 'white',
                       'on_green')

    def create_office(self, name):
        """Create a new office in amity"""
        office = Office(name)
        self.rooms.append(office.__dict__)
        return colored('Office {} created.'.format(name), 'white', 'on_green')

    def allocate_person(self, person_name):
        '''Allocate a person randomly to a room'''
        person = self.person_exists(person_name)
        try:
            if person:
                room = self.get_room(person=person_name)
                if room:
                    if 'wants_livingspace' in person.keys() and \
                            len(room) == 1:
                        # check if fellow  who wants livingspace and was only
                        # allocated one room and allocate the other room
                        # now that it's available
                        if room[0]['room_type'] != 'livingspace':
                            return self.allocate_livingspace(person_name)
                        else:
                            return self.allocate_office(person_name, 'fellow')
                    raise ValueError(
                        '{} already allocated a space!'.format(person_name))
                elif person['person_type'] == 'staff':
                    return self.allocate_office(person_name, 'staff')
                elif 'wants_livingspace' in person.keys():
                    result = self.allocate_office(person_name, 'fellow') + \
                        '\n' + self.allocate_livingspace(person_name)
                    return result
                return self.allocate_office(person_name, 'fellow')
            else:
                raise ValueError("Person {} doesn't exist!".format(person_name))
        except ValueError:
            raise

    def allocate_livingspace(self, name):
        """Allocate livingspace to fellows."""
        rooms = self.get_room(available_rooms='livingspace')
        if not rooms:
            return colored(
                'There are no available livingspaces to allocate {}!'
                .format(name), 'white', 'on_red')
        else:
            room = random.choice(rooms)
            room['occupants'].append(name)
            return colored(
                'Fellow {} allocated space in livingspace {}.'
                .format(name, room['name']), 'white', 'on_green')

    def allocate_office(self, name, person_type):
        """Allocate office to staff or fellow."""
        rooms = self.get_room(available_rooms='office')
        result = ''
        if not rooms:
            return colored(
                'There are no available offices to allocate {}!'
                .format(name), 'white', 'on_red')
        else:
            room = random.choice(rooms)
            room['occupants'].append(name)
            return colored('{} {} allocated space in office {}.'
                           .format(person_type.capitalize(), name,
                                   room['name']), 'white', 'on_green')

    def get_room(self, room_type=None, room_name=None, available_rooms=None,
                 person=None):
        """Get a list of specific rooms in amity depending on room type, name
           availability or occupants"""
        if room_name:
            return [room for room in self.rooms if room['name'] ==
                    room_name][0]
        elif room_type:
            return [room for room in self.rooms if
                    room['room_type'] == room_type]
        elif available_rooms:
            return [room for room in self.rooms if
                    self.check_room_availability(room['name'])and
                    room['room_type'] == available_rooms]
        elif person:
            return [room for room in self.rooms if
                    person in room['occupants']]
        return None

    def check_room_availability(self, room_name):
        """Check for the availability of a specific room in amity"""
        if self.room_exists(room_name):
            room = self.get_room(room_name=room_name)
            return room['max_space'] - len(room['occupants'])
        else:
            return colored("Room {} doesn't exist!".format(room_name), 'white',
                           'on_red')

    def person_exists(self, name):
        """Check if a person exists in amity"""
        if self.people:
            for person in self.people:
                if name == person['name']:
                    return person
        return None

    def remove_person_from_room(self, person_name, office=None,
                                livingspace=None):
        '''Remove a person from all assigned rooms in amity'''
        if office:
            rooms = [room for room in self.rooms if
                     person_name in room['occupants'] and
                     room['room_type'] == 'office']
        elif livingspace:
            rooms = [room for room in self.rooms if
                     person_name in room['occupants'] and
                     room['room_type'] == 'livingspace']
        else:
            rooms = [room for room in self.rooms if
                     person_name in room['occupants']]
        if rooms:
            for room in rooms:
                room['occupants'].remove(person_name)
                cprint('{} removed successfully from {} {}.'
                       .format(person_name.capitalize(), room['room_type'],
                               room['name']), 'white', 'on_green')
        else:
            cprint(
                "{} isn't allocated or is not assigned to the specified room!"
                .format(person_name.capitalize()), 'white', 'on_red')

    def remove_person(self, name):
        '''Remove a person completely from amity'''
        try:
            if self.person_exists(name):
                self.people.remove(self.person_exists(name))
                self.remove_person_from_room(name)
                return colored('Person {} removed.'.format(name), 'white',
                               'on_green')
            else:
                raise ValueError("Person {} doesn't exist!".format(name))
        except ValueError:
            raise

    def reallocate_person(self, person_name, room_name):
        """Reallocate an employee from one room to another"""
        try:
            if self.room_exists(room_name):
                room = self.get_room(room_name=room_name)
                room_type = room['room_type']
            else:
                raise ValueError("Room {} doesn't exist!".format(room_name))
            # check if that person exists
            person = self.person_exists(person_name)
            if not person:
                raise ValueError("Person {} doesn't exist!".format(person))
            # validate staff isn't allocated to livingspace
            elif (person['person_type'] == 'staff' and
                  room_type == 'livingspace'):
                raise ValueError('Staff {} cannot be allocated livingspace!'
                                 .format(person_name))
            # validate fellow who doesn't want livingspace isn't
            # allocated livingspace
            elif (person['person_type'] == 'fellow' and
                  room_type == 'livingspace' and 'wants_livingspace' not in
                  person.keys()):
                raise ValueError('Fellow {} cannot be '.format(person_name) +
                                 'allocated livingspace as they opted out!')
            else:
                return self.reallocate(person['name'], room_type, room_name)
        except ValueError:
            raise

    def reallocate(self, person_name, room_type, room_name):
        '''Helper function to reallocating person'''
        room = [room for room in self.rooms if person_name in
                room['occupants'] and room['room_type'] == room_type]
        if not room:
            raise ValueError(
                'Allocate {} to {} first!'.format(room_type, person_name))
        room = room[0]
        # check if reallocating to same room
        if room['name'] == room_name:
            raise ValueError(
                '{} is already allocated to {} {}!'.format(
                    person_name.capitalize(), room_type, room_name))
        if self.check_room_availability(room_name):
            self.get_room(room_name=room_name)['occupants'].append(person_name)
            room['occupants'].remove(person_name)
            return colored('{} reallocated to {} {}.'
                           .format(person_name.capitalize(),
                                   room_type, room_name), 'white', 'on_green')
        else:
            raise ValueError(
                '{} {} has maximum number of occupants!'.format(
                    room_type.capitalize(), room_name))

    def load_rooms(self, filename):
        """Load rooms from a file."""
        with open(filename, 'r') as file:
            lines = list(line for line in (l.rstrip() for l in file)if line)
            for line in lines:
                line = line.lower().split()
                names = [name for name in line if name not in
                         ('office', 'livingspace')]
                room_type = ' '.join([room for room in line if room in
                                     ('office', 'livingspace')])
                try:
                    for name in names:
                        print(self.create_room(room_type, name))
                except Exception as error:
                    cprint(error, 'white', 'on_red')
        return colored(
            'Rooms loaded from {} successfully.'.format(filename), 'white',
            'on_green')

    def load_people(self, filename):
        """Load people from a file."""
        with open(filename, 'r') as file:
            lines = list(line for line in (l.rstrip() for l in file)if line)
            for line in lines:
                line = line.lower().split()
                name = ' '.join([
                    name for name in line if name not in
                    ('fellow', 'staff', 'y', 'yes')])
                role = ' '.join([
                    role for role in line if role in ('staff', 'fellow')])
                want_livingspace = [
                    space for space in line if space in ('y', 'yes')]
                try:
                    if want_livingspace:
                        print(self.add_person(role, name, True))
                    else:
                        print(self.add_person(role, name))
                except Exception as error:
                    cprint(error, 'white', 'on_red')
        return colored(
            'People loaded from {} successfully.'.format(filename), 'white',
            'on_green')

    def print_allocations(self, filename=None):
        """Print out the allocated rooms"""
        allocations = {room['name']: [room['room_type'], room['occupants']]
                       for room in self.rooms if room['occupants']}
        result = ''
        if not allocations:
            result = '\nALLOCATIONS\n' + '-'*20+'\n' +\
                colored('NO ALLOCATIONS HAVE BEEN DONE YET', 'white', 'on_red')
        for name, details in allocations.items():
            persons = ''
            for person in details[1]:
                persons += person.upper() + ', '
            # persons[:-2] to strip out the last comma
            result += '{} ({})\n'.format(name.upper(), details[0].upper()) + \
                      '-'*20+' \n{}\n\n'.format(persons[:-2])
        if not filename:
            return result
        with open(filename, 'w') as file:
            file.writelines(result)
        return colored(
            'Allocations have been saved to file {}.'.format(filename), 'white',
            'on_green')

    def print_unallocated(self, filename=None):
        """Print out the unallocations in amity"""
        allocated = {}
        for room in self.rooms:
            for person in room['occupants']:
                if person not in allocated.keys():
                    allocated[person] = []
                if room['room_type'] not in allocated[person]:
                    allocated[person].append(room['room_type'])
        # label fellow who wants livingspace but without livingspace
        # as unallocated to livingspace or office
        unallocated = [person['name'] for person in self.people
                       if person['name'] not in allocated.keys()]
        for person, details in allocated.items():
            person = self.person_exists(person)
            if 'wants_livingspace' in person.keys():
                if len(details) == 1 and details[0] == 'office':
                    unallocated.append(
                        '{} (not allocated livingspace)'.format(person['name'])
                        )
                elif len(details) == 1 and details[0] == 'livingspace':
                    unallocated.append(
                        '{} (not allocated office)'.format(person['name']))
        result = '\nUNALLOCATED\n'+'-'*20+'\n'
        if not unallocated:
            result += colored('NO UNALLOCATED PEOPLE', 'white', 'on_red')
        else:
            for person in unallocated:
                result += '{}\n'.format(person.upper())
        if not filename:
            return result
        with open(filename, 'w') as file:
            file.writelines(result)
        return colored(
            'Unallocations have been saved to file {}.'.format(filename),
            'white', 'on_green')

    def print_room(self, room_name):
        """Print the people in a specific room in amity"""
        try:
            if self.room_exists(room_name):
                people = [
                    [people.upper() for people in room['occupants']]
                    for room in self.rooms if room['name'] == room_name
                    ][0]
                if not people:
                    raise ValueError(
                        'No one has been assigned to {} yet!'.format(room_name))
                else:
                    return ', '.join(people)
            raise ValueError('No such room as {} in amity!'.format(room_name))
        except ValueError:
            raise

    def add_person(self, role, person_name, wants_livingspace=False):
        """Add a new person in amity"""
        try:
            if role.lower() not in ('staff', 'fellow'):
                raise ValueError(
                    'Person role is incorrect. Should be fellow or staff!')
            elif self.person_exists(person_name):
                raise ValueError(
                    'Person {} already exists!'.format(person_name))
            else:
                role = role.lower()
                person_name = person_name.lower()
                # ensure that name contains only alphabetic chars
                if not ''.join(person_name.split()).isalpha():
                    raise ValueError(
                        'Name must be alphabetic chars. {} is incorrect!'
                        .format(person_name))
                elif role == 'staff' and wants_livingspace:
                    self.add_staff(person_name)
                    result = colored(
                        'Staff cannot be assigned livingspace!', 'white',
                        'on_red')
                    result += colored(
                        '\n{} {} added.'.format(
                            role.capitalize(), person_name), 'white',
                                                             'on_green')
                    return result
                elif role == 'staff':
                    self.add_staff(person_name)
                    return colored(
                        '{} {} added.'.format(
                            role.capitalize(), person_name), 'white',
                                                             'on_green')
                elif role == 'fellow':
                    self.add_fellow(person_name, wants_livingspace)
                    return colored(
                        '{} {} added.'.format(
                            role.capitalize(), person_name), 'white',
                                                             'on_green')
        except ValueError:
            raise

    def add_fellow(self, person_name, wants_livingspace):
        '''Add a fellow to amity'''
        if wants_livingspace:
            self.people.append(Fellow(person_name, True).__dict__)
            print(self.allocate_livingspace(person_name))
        else:
            self.people.append(Fellow(person_name).__dict__)
        print(self.allocate_office(person_name, 'fellow'))

    def add_staff(self, person_name):
        '''Add a staff to amity'''
        self.people.append(Staff(person_name).__dict__)
        print(self.allocate_office(person_name, 'staff'))

    def save_state(self, database=None):
        """Save the current state of amity to the database"""
        self.database.clear()
        self.database.initialize(database)
        print(self.save_people())
        print(self.save_rooms())
        self.database.save()
        return colored("Amity's state saved successfully.", 'white',
                       'on_green')

    def save_rooms(self):
        '''Save the current state of rooms in amity to the database'''
        for room in self.rooms:
            people = []  # hold the people objects from db query on person name
            for occupant in room['occupants']:
                occupant = occupant.split()
                person = self.database.session.query(Person).filter_by(
                    first_name=occupant[0],
                    last_name=occupant[1]
                    ).first()
                people.append(person)
            room_to_save = Room(
                name=room['name'],
                type=room['room_type'],
                max_space=room['max_space'],
                occupants=people
            )
            self.database.session.add(room_to_save)
        return colored('Rooms in amity saved successfully.', 'white',
                       'on_green')

    def save_people(self):
        '''Save the current state of people in amity to the database'''
        for person in self.people:
            person_name = person['name'].split()
            first_name = person_name[0]
            last_name = person_name[1]
            wants_livingspace = person['wants_livingspace'] if\
                'wants_livingspace' in person.keys() else False
            person_to_save = Person(
                first_name=first_name,
                last_name=last_name,
                role=person['person_type'],
                wants_livingspace=wants_livingspace
            )
            self.database.session.add(person_to_save)
        return colored('People in amity saved successfully.',
                       'white', 'on_green')

    def load_state(self, database=None):
        """Load amity resources from the database"""
        self.database.initialize(database)
        amity_rooms = self.database.session.query(Room).all()
        print(self.rooms_load(amity_rooms))
        people = self.database.session.query(Person).all()
        print(self.people_load(people))
        return colored("Amity's previous state loaded successfully.", 'white',
                       'on_green')

    def rooms_load(self, amity_rooms):
        '''Load rooms from the database to amity'''
        for room in amity_rooms:
            room_dict = {
                'name': room.name,
                'room_type': room.type,
                'max_space': room.max_space,
                'occupants': []
            }
            if not self.room_exists(room.name):
                self.rooms.append(room_dict)
            else:
                cprint('{} {} already exists in amity!'.format(
                    room.type.capitalize(), room.name
                ), 'white', 'on_red')
        return colored('Rooms loaded successfully.', 'white', 'on_green')

    def people_load(self, people):
        '''Load people from the database to amity'''
        for person in people:
            person_name = person.first_name + ' ' + person.last_name
            if not self.person_exists(person_name):
                if person.wants_livingspace:
                    person_dict = {
                        'name': person_name,
                        'person_type': person.role,
                        'wants_livingspace': True
                    }
                else:
                    person_dict = {
                        'name': person_name,
                        'person_type': person.role
                    }
                self.people.append(person_dict)
                self.load_person_to_rooms(person)
            else:
                cprint('{} {} already exists in amity!'.format(
                    person.role.capitalize(), person_name), 'white', 'on_red')
        return colored('People loaded successfully.', 'white', 'on_green')

    def load_person_to_rooms(self, person):
        '''Load people into rooms from the previous states allocation'''
        person_name = person.first_name + ' ' + person.last_name
        for person_room in person.room:
            for room in self.rooms:
                if room['name'] == person_room.name:
                    if person_name not in room['occupants']:
                        room['occupants'].append(person_name)
                    else:
                        cprint('{} already assigned to {} {}!'.format(
                            person_name.capitalize(), room['room_type'],
                            room['name']), 'white', 'on_red')
