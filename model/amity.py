#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
import random

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from model.person import Fellow, Staff
from model.room import Office, LivingSpace
from model.db import CreateDb, Person, Room


class Amity:

    rooms = []
    people = []

    def __init__(self, database=None):
        self.db = CreateDb(database)
        self.session = self.db.Session()

    def room_exists(self, name):
        if self.rooms:
            for room in self.rooms:
                if name == room['name']:
                    return room
        return False

    def create_room(self, room_type, room_name):
        """This function creates a new room in amity"""
        try:
            if not isinstance(room_type, str) or not \
                    isinstance(room_name, str):
                raise ValueError('room name and type must be a string and ' +
                                 'not an integer or float.')
            elif room_type.lower() not in ('livingspace', 'office'):
                raise ValueError('Room type is incorrect. Must be office or ' +
                                 'livingspace')
            elif not room_name.isalpha():
                raise ValueError('room name cannot be empty or have special ' +
                                 'characters\n{} is not a valid name\n'
                                 .format(room_name))
            elif room_type == 'office':
                return self.create_office(room_name)
            elif room_type == 'livingspace':
                return self.create_livingspace(room_name)
        except ValueError:
            raise

    def create_livingspace(self, name):
        """This function creates a new livingspace in amity"""
        if self.room_exists(name):
            raise ValueError('room with name {} already exists.'.format(name))
        else:
            livingspace = LivingSpace(name)
            self.rooms.append(livingspace.__dict__)
            return 'livingspace {} created'.format(name)

    def create_office(self, name):
        """This function creates a new office in amity"""
        if self.room_exists(name):
            raise ValueError('room with name {} already exists.'.format(name))
        else:
            office = Office(name)
            self.rooms.append(office.__dict__)
            return 'office {} created'.format(name)

    def allocate_person(self, person_name):
        person = self.person_exists(person_name)
        try:
            if person:
                room = [room for room in self.rooms if
                        person_name in room['occupants']]
                if room:
                    raise ValueError(
                        '{} already allocated'.format(person_name))
                if person['person_type'] == 'staff':
                    return self.allocate_staff(person_name)
                if 'wants_livingspace' in person.keys():
                    return self.allocate_fellow(person_name, True)
                return self.allocate_fellow(person_name)
            else:
                raise ValueError("person {} doesn't exist".format(person_name))
        except ValueError:
            raise

    def allocate_fellow(self, name, livingspace=None):
        """This function allocates space to new fellows."""
        try:
            rooms = self.get_room(room_type='office')
            room = random.choice(rooms)
            result = ''
            if self.check_room_availability(room['name']):
                room['occupants'].append(name)
                result += ('fellow {} allocated space in office {}'
                           .format(name, room['name']))
            else:
                self.allocate_fellow(name, livingspace)
            # if fellow wants livingspace assign them a livingspace too
            if livingspace:
                rooms = self.get_room(room_type='livingspace')
                room = random.choice(rooms)
                if self.check_room_availability(room['name']):
                    room['occupants'].append(name)
                    result += ('\nfellow {} allocated space in livingspace {}'
                               .format(name, room['name']))
                else:
                    self.allocate_fellow(name, livingspace)
            return result
        except IndexError:
            return 'No rooms in amity to allocate person'

    def allocate_staff(self, name):
        """This function allocates space to new staff."""
        try:
            rooms = self.get_room(room_type='office')
            room = random.choice(rooms)
            if self.check_room_availability(room['name']):
                room['occupants'].append(name)
                return ('staff {} allocated space in office {}'
                        .format(name, room['name']))
            else:
                self.allocate_staff(name)
        except IndexError:
            return 'No rooms in amity to allocate person'

    def get_room(self, room_type=None, room_name=None):
        """This function gets a list of specific rooms in amity"""
        if room_name:
            return [room for room in self.rooms if room['name'] ==
                    room_name][0]
        elif room_type:
            return [room for room in self.rooms if
                    room['room_type'] == room_type]
        return None

    def check_room_availability(self, room_name):
        """This function checks for the availability of rooms in amity"""
        if self.room_exists(room_name):
            room = self.get_room(room_name=room_name)
            return room['max_space'] - len(room['occupants'])
        else:
            return "room {} doesn't exist".format(room_name)

    def person_exists(self, name):
        """This function checks if a person exists in amity"""
        if self.people:
            for person in self.people:
                if name == person['name']:
                    return person
        return False

    def remove_person_from_room(self, person_name):
        rooms = [room for room in self.rooms if
                 person_name in room['occupants']]
        if rooms:
            for room in rooms:
                room['occupants'].remove(person_name)
                print('{} removed successfully from {}'
                      .format(person_name, room['name']))
        else:
            print("{} doesn't have allocations".format(person_name))

    def remove_person(self, name):
        try:
            if self.person_exists(name):
                self.people.remove(self.person_exists(name))
                self.remove_person_from_room(name)
                return 'person {} removed'.format(name)
            else:
                raise ValueError("person {} doesn't exist".format(name))
        except ValueError:
            raise

    def reallocate_person(self, person_name, room_name):
        """This function reallocates an employee from one room to another"""
        try:
            if self.room_exists(room_name):
                room = self.get_room(room_name=room_name)
                # index 0 to return the string and not the list
                room_type = room['room_type']
            else:
                raise ValueError("room {} doesn't exist".format(room_name))
            # check if that person exists
            person = self.person_exists(person_name)
            if not person:
                raise ValueError("person {} doesn't exist".format(person))
            # validate staff isn't allocated to livingspace
            elif (person['person_type'] == 'staff' and
                    room_type == 'livingspace'):
                raise ValueError('staff {} cannot be allocated livingspace'
                                 .format(person_name))
            # validate fellow who doesn't want livingspace isn't
            # allocated livingspace
            elif (person['person_type'] == 'fellow'and
                    room_type == 'livingspace' and 'wants_livingspace' not in
                    person.keys()):
                raise ValueError('fellow {} cannot be '.format(person_name) +
                                 'allocated livingspace as they opted out')
            else:
                return self.reallocate(person['name'], room_type, room_name)
        except ValueError:
            raise

    def reallocate(self, person_name, room_type, room_name):
        room = [room for room in self.rooms if person_name in
                room['occupants'] and room['room_type'] == room_type]
        if not room:
            raise ValueError('allocate {} first'.format(person_name))
        room = room[0]
        # check if reallocating to same room
        if room['name'] == room_name:
            raise ValueError(
                '{} is already allocated to {} {}'.format(
                    person_name, room_type, room_name))
        if self.check_room_availability(room_name):
            self.get_room(room_name=room_name)['occupants'].append(person_name)
            room['occupants'].remove(person_name)
            return('{} reallocated to {} {}'
                   .format(person_name, room_type, room_name))
        else:
            raise ValueError(
                '{} {} has maximum number of occupants'.format(
                    room_type, room_name))

    def load_people(self, filename):
        """This function loads employees from a txt file."""
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
                except ValueError as e:
                    print(e)

    def print_allocations(self, filename=None):
        """This function prints out the allocated rooms"""
        allocations = {room['name']: room['occupants'] for room in self.rooms
                       if room['occupants']}
        result = ''
        if not allocations:
            result = '\nALLOCATIONS\n'+'-'*20+'\n'+'NONE'
        for name, people in allocations.items():
            persons = ''
            for person in people:
                persons += person.upper() + ', '
            # persons[:-2] to strip out the last comma
            result += '{}\n'.format(name.upper())+'-'*20+' \n{}\n\n'\
                .format(persons[:-2])
        if not filename:
            return result
        with open(filename, 'w') as file:
            file.writelines(result)
        return 'Allocations haved been saved to file {}'.format(filename)

    def print_unallocated(self, filename=None):
        """This function prints out the unallocated rooms"""
        allocated = set()
        for room in self.rooms:
            for person in room['occupants']:
                allocated.add(person)
        unallocated = [person['name'] for person in self.people
                       if person['name'] not in allocated]
        result = '\nUNALLOCATED\n'+'-'*20+'\n'
        if not unallocated:
            result += 'NONE'
        else:
            for person in unallocated:
                result += '{}\n'.format(person.upper())
        if not filename:
            return result
        with open(filename, 'w') as file:
            file.writelines(result)
        return 'Unallocations haved been saved to file {}'.format(filename)

    def print_room(self, room_name):
        """This function prints the people in rooms contained in amity"""
        try:
            if self.room_exists(room_name):
                people = [[people.upper() for people in room['occupants']]
                          for room in self.rooms if room['name'] == room_name
                          ][0]
                if not people:
                    raise ValueError(
                        'no one has been assigned to {} yet'.format(room_name))
                else:
                    return ', '.join(people)
            raise ValueError('no such room as {} in amity'.format(room_name))
        except ValueError:
            raise

    def add_person(self, role, person_name, wants_livingspace=False):
        """This function employs  a new new person as  a staff or fellow."""
        try:
            if role.lower() not in ('staff', 'fellow'):
                raise ValueError(
                    'Person role is incorrect. Should be fellow or staff')
            elif self.person_exists(person_name):
                raise ValueError(
                    'person {} already exists.'.format(person_name))
            else:
                role = role.lower()
                person_name = person_name.lower()
                # ensure that name contains only alphabetic chars
                if not ''.join(person_name.split()).isalpha():
                    raise ValueError(
                        'name must be alphabetic chars. {} is incorrect'.format(
                            person_name))
                elif role == 'staff' and wants_livingspace:
                    raise ValueError('staff cannot be assigned LivingSpace')
                elif role == 'staff':
                    self.add_staff(person_name)
                    return '{} {} added.'.format(role, person_name)
                elif role == 'fellow':
                    self.add_fellow(person_name, wants_livingspace)
                    return '{} {} added.'.format(role, person_name)
        except ValueError:
            raise

    def add_fellow(self, person_name, wants_livingspace):
        if wants_livingspace:
            self.people.append(Fellow(person_name, True).__dict__)
            print(self.allocate_fellow(person_name, True))
        else:
            self.people.append(Fellow(person_name).__dict__)
            print(self.allocate_fellow(person_name))

    def add_staff(self, person_name):
        self.people.append(Staff(person_name).__dict__)
        print(self.allocate_staff(person_name))

    def save_state(self, database=None):
        """This function saves the running state of amity to the database"""
        for person in self.people:
            first_name = person['name'].split()[0]
            last_name = person['name'].split()[1]
            wants_livingspace = person['wants_livingspace'] if\
                'wants_livingspace' in person.keys() else False
            person_to_save = Person(
                first_name=first_name,
                last_name=last_name,
                role=person['person_type'],
                wants_livingspace=wants_livingspace
            )
            self.session.add(person_to_save)

            for room in self.rooms:
                room_to_save = Room(
                    name=room['name'],
                    type=room['room_type'],
                    max_space=room['_MAX_SPACE'],
                    occupants=room['occupants']
                )
                self.session.add(room_to_save)

        self.session.commit()
        return 'amity state saved successfully'

    def load_state(self, database=None):
        """This function loads amity resourses from the database"""
        pass
