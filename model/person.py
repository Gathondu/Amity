#!/usr/local/bin/python3
# -*- coding: utf-8 -*-


class Person:

    name = None
    person_type = None


class Staff(Person):

    def __init__(self, name):
        self.name = name
        self.person_type = 'staff'


class Fellow(Person):
    wants_livingspace = False

    def __init__(self, name, accomodation=None):
        self.name = name
        self.person_type = 'fellow'
        if accomodation:
            self.wants_livingspace = accomodation
