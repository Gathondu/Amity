#!/usr/local/bin/python3
# -*- coding: utf-8 -*-


from unittest import TestCase, skip

from model.room import Room, Office, LivingSpace


class TestRoom(TestCase):

    def setUp(self):
        self.office = Office('valhalla')
        self.livingspace = LivingSpace('dojo')

    def test_room_is_created_correctly(self):
        self.assertIsInstance(self.office, Office)
        self.assertIsInstance(self.livingspace, LivingSpace)

    def test_room_name_is_correct(self):
        self.assertEqual('valhalla', self.office.name)
        self.assertEqual('dojo', self.livingspace.name)

    def test_max_space_is_correct(self):
        self.assertEqual(6, self.office.max_space)
        self.assertEqual(4, self.livingspace.max_space)

    def test_room_type_is_correct(self):
        self.assertEqual('livingspace', self.livingspace.room_type)
        self.assertEqual('office', self.office.room_type)

    def test_max_space_is_correctly_updated(self):
        self.office.max_space_set(7)
        self.assertEqual(7, self.office.max_space)

    def test_non_int_max_space_value_raies_ValueError(self):
        with self.assertRaises(ValueError):
            self.office.max_space_set('a')
