#!/usr/local/bin/python3
# -*- coding: utf-8 -*-


class Room:

    name = "Room Name"
    room_type = "Room Type"
    _MAX_SPACE = 0
    _occupied_spaces = 0
    _occupants = set()

    def __str__(self):
        return '{} {} has {} occupant[s].'.format(self.room_type, self.name,
                                                  self.occupied_spaces())

    def add_person(self, person_name):
        if self.check_availability():
            if person_name in self._occupants:
                return '{} already assigned space in {}'.format(person_name,
                                                                self.name)
            self._occupied_spaces += 1
            self._occupants.add(person_name)
            return '{} assigned space in {}'.format(person_name, self.name)

    def check_availability(self):
        return self._MAX_SPACE - self.occupied_spaces()

    def occupants(self):
        return self._occupants

    def occupied_spaces(self):
        return self._occupied_spaces


class Office(Room):

    def __init__(self, name):
        self.name = name
        self.room_type = "office"
        self._set_max_space()
        self._occupants = set()

    def _set_max_space(self):
        self._MAX_SPACE = 6


class LivingSpace(Room):

    def __init__(self, name):
        self.name = name
        self.room_type = "living space"
        self._set_max_space()
        self._occupants = set()

    def _set_max_space(self):
        self._MAX_SPACE = 4
