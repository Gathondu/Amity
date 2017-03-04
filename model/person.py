#!/usr/local/bin/python3
# -*- coding: utf-8 -*-


class Person:

    name = 'Person'
    person_type = 'Employee'


class Fellow(Person):

    _wants_living_space = False

    def __init__(self, name, accomodation=False):
        self.person_type = 'fellow'
        self.name = name
        if accomodation:
            self.request_living_space()

    def request_living_space(self):
        if self.wants_living_space():
            return '{} already set to recieve living space'.format(self.name)
        self._wants_living_space = True
        return '{} set to recieve living space'.format(self.name)

    def wants_living_space(self):
        return self._wants_living_space


class Staff(Person):

    def __init__(self, name):
        self.person_type = 'staff'
        self.name = name
