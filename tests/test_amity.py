#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
import json

from unittest import TestCase, skip

from model.amity import Amity


class TestAmity(TestCase):

    def setUp(self):
        self.amity = Amity()
        self.occulus = self.amity.create_room('office', 'occulus')
        self.dojo = self.amity.create_room('livingspace', 'dojo')

    def test_room_is_created(self):
        self.assertEqual('office occulus created', self.occulus)

    def test_room_exists_after_creation(self):
        print(self.amity.rooms)
        self.assertTrue(self.amity.room_exists('dojo'))

    def test_room_name_and_type_must_be_specified(self):
        with self.assertRaises(TypeError):
            self.amity.create_room()

    def test_room_name_and_type_cannot_be_empty(self):
        with self.assertRaises(ValueError):
            self.amity.create_room('', '')

    def test_room_name_can_only_be_string(self):
        with self.assertRaises(ValueError):
            self.amity.create_room('office', '@here')

    def test_person_is_added(self):
        staff = self.amity.add_person('staff', 'denis')
        self.assertEqual('staff denis added.', staff)

    def test_person_exists_after_being_added(self):
        self.assertIsNotNone(self.amity.person_exists('denis'))

    def test_person_name_cannot_be_duplicated(self):
        with self.assertRaises(ValueError):
            self.amity.add_person('fellow', 'denis')

    def test_staff_cannot_be_allocated_livingspace(self):
        with self.assertRaises(ValueError):
            self.amity.add_person('staff', 'shem mwangi', True)

    def test_person_is_automatically_allocated_space(self):
        room = [
            room for room in self.amity.rooms if 'denis' in room['occupants']]
        self.assertNotEqual([], room)

    def test_is_successfully_removed_from_amity(self):
        self.amity.remove_person('denis')
        self.assertFalse(self.amity.person_exists('denis'))
