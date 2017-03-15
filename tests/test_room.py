#!/usr/local/bin/python3
# -*- coding: utf-8 -*-


from unittest import TestCase, skip

from model.room import Room, Office, LivingSpace


class TestRoom(TestCase):

    def setUp(self):
        self.r = Room()
        self.room1 = Room('room1')
        self.room2 = Room(room_type='room2')
        self.room3 = Room(max_space=1)
        self.o = Office('valhalla')
        self.l = LivingSpace('dojo')

    def test_room_is_created_with_default_values_if_not_specified(self):
        self.assertEqual(
            ['Room Name', 'Room Type', 0],
            [self.r.name, self.r.room_type, self.r.max_space]
         )

    def test_room_is_created_with_correct_values_if_specified(self):
        self.assertEqual(
            ['room1', 'room2', 1],
            [self.room1.name, self.room2.room_type, self.room3.max_space]
         )

    def test_room_is_created_correctly(self):
        self.assertIsInstance(self.r, Room)
        self.assertIsInstance(self.o, Office)
        self.assertIsInstance(self.l, LivingSpace)

    def test_room_name_is_correct(self):
        self.assertEqual('valhalla', self.o.name)
        self.assertEqual('dojo', self.l.name)

    def test_max_space_is_correct(self):
        self.assertEqual(6, self.o.max_space)
        self.assertEqual(4, self.l.max_space)

    def test_room_type_is_correct(self):
        self.assertEqual('living space', self.l.room_type)
        self.assertEqual('office', self.o.room_type)

    def test_max_space_is_correctly_updated(self):
        self.o._max_space = 7
        self.assertEqual(7, self.o.max_space)

    def test_non_int_max_space_value_raies_ValueError(self):
        with self.assertRaises(ValueError):
            self.o._max_space = 'a'

    def test_str_method_on_room_returns_type_name_and_maxspace(self):
        self.assertEqual(
            'office valhalla can accomodate 6 occupants.', str(self.o)
            )
        self.assertEqual(
            'living space dojo can accomodate 4 occupants.', str(self.l)
            )
