#!/usr/local/bin/python3
# -*- coding: utf-8 -*-


class Person:

    def __init__(self, name='person', person_type='employee'):
        self.name = name
        self.person_type = person_type

    def __str__(self):
        return '{} is a {}.'.format(
            self.name, self.person_type
            )


class Staff(Person):

    def __init__(self, name):
        super().__init__(name, person_type='staff')


class Fellow(Person):
    _wants_living_space = False

    def __init__(self, name, accomodation=False):
        super().__init__(name, person_type='fellow')
        if accomodation:
            self.wants_living_space = accomodation

    @property
    def wants_living_space(self):
        return self._wants_living_space

    @wants_living_space.setter
    def wants_living_space(self, boolean):
        if not isinstance(boolean, bool):
            raise ValueError('{} is not a boolean'.format(boolean))
        if self.wants_living_space == boolean:
            if bool is True:
                raise ValueError('{} already set to recieve living space'
                                 .format(self.name))
            else:
                raise ValueError('{} already set to not recieve living space'
                                 .format(self.name))
        self._wants_living_space = boolean
