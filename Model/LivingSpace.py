#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

from Model.Room import Room


class LivingSpace(Room):

    def __init__(self, name):
        self.name = name
        self.max_spaces = 4
        self.room_type = "LivingSpace"
