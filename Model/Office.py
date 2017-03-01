#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

from Model.Room import Room


class Office(Room):

    def __init__(self, name):
        self.name = name
        self.max_spaces = 6
        self.room_type = "Office"
