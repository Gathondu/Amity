#!/usr/local/bin/python3
# -*- coding: utf-8 -*-


class Room:

    def __init__(self, name='Room Name', room_type='Room Type', max_space=0):
        self._MAX_SPACE = max_space
        self._occupants = []
        self.name = name
        self.room_type = room_type

    def __str__(self):
        return '{} {} has {} occupant[s].'.format(self.room_type, self.name,
                                                  self.occupied_spaces)

    @property
    def max_space(self):
        return self._MAX_SPACE

    @property
    def occupants(self):
        if self._occupants == []:
            return '{} is empty.'.format(self.name)
        return self._occupants

    @property
    def occupied_spaces(self):
        return len(self._occupants)

    @max_space.setter
    def _max_space(self, space):
        if not isinstance(space, int):
            return '{} is not an integer!!!'
        self._MAX_SPACE = space
        return "maximum number of people allowed to be assigned to {} has"
        " been updated to {}.".format(self.name, space)

    @property
    def availability(self):
        return self.max_space - self.occupied_spaces

    def add_person(self, person_name):
        if self.availability:
            if person_name in self._occupants:
                return '{} already assigned space in {}'.format(person_name,
                                                                self.name)
            self._occupants.append(person_name)
            return '{} assigned space in {}'.format(person_name, self.name)


class Office(Room):

    def __init__(self, name):
        self._MAX_SPACE = 0
        self.name = name
        self.room_type = "office"
        self._max_space = 6
        self._occupants = []


class LivingSpace(Room):

    def __init__(self, name):
        self._MAX_SPACE = 0
        self.name = name
        self.room_type = "living space"
        self._max_space = 4
        self._occupied_spaces = 0
        self._occupants = []
