#!/usr/local/bin/python3
# -*- coding: utf-8 -*-


class Room:

    def __init__(self, name='Room Name', room_type='Room Type', max_space=0):
        self._MAX_SPACE = max_space
        self.name = name
        self.room_type = room_type

    def __str__(self):
        return '{} {} can accomodate {} occupants.'.format(
            self.room_type, self.name, self.max_space
            )

    @property
    def max_space(self):
        return self._MAX_SPACE

    @max_space.setter
    def _max_space(self, space):
        if not isinstance(space, int):
            raise ValueError('{} is not an integer!!!')
        self._MAX_SPACE = space


class Office(Room):

    def __init__(self, name):
        super().__init__(name, room_type='office', max_space=6)


class LivingSpace(Room):

    def __init__(self, name):
        super().__init__(name, room_type='living space', max_space=4)
