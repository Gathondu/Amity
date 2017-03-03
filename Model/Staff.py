#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

from model.person import Person


class Staff(Person):

    def __init__(self, name):
        self.type = 'staff'
        self.name = name
