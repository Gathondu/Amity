#!/usr/local/bin/python3
# -*- coding: utf-8 -*-


class Person:

    def __init__(self, name='person', person_type='employee'):
        self.name = name
        self.person_type = person_type


class Fellow(Person):

    _wants_living_space = False

    def __init__(self, name, accomodation=False):
        self.person_type = 'fellow'
        self.name = name
        if accomodation:
            self.request_living_space

    @property
    def wants_living_space(self):
        return self._wants_living_space

    @property
    def request_living_space(self):
        if self.wants_living_space:
            raise ValueError('{} already set to recieve living space'
                             .format(self.name))
        self._wants_living_space = True


class Staff(Person):

    def __init__(self, name):
        self.person_type = 'staff'
        self.name = name
