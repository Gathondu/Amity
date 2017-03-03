#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

from model.room import Room


class Office(Room):

    def __init__(self, name):
        self.name = name
        self.room_type = "office"
        self._set_max_space()
        self._occupants = set()

    def _set_max_space(self):
        self._MAX_SPACE = 6
