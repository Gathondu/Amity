#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

from model.person import Person


class Fellow(Person):

    wants_living_space = False

    def __init__(self, name, accomodation):
        self.type = 'fellow'
        self.name = name
        if accomodation:
            self.request_living_space()

    def request_living_space(self):
        self.wants_living_space = True
