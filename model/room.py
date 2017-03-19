#!/usr/local/bin/python3
# -*- coding: utf-8 -*-


class Room:

    max_space = None
    name = None
    room_type = None
    occupants = []

    def max_space_set(self, value):
        if isinstance(value, int):
            self.max_space = value
        else:
            raise ValueError('max space value can only be an integer')


class Office(Room):

    def __init__(self, name):
        self.name = name
        self.room_type = 'office'
        self.max_space = 6


class LivingSpace(Room):

    def __init__(self, name):
        self.name = name
        self.room_type = 'livingspace'
        self.max_space = 4
