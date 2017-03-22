#!/usr/local/bin/python3
# -*- coding: utf-8 -*-


from unittest import TestCase, skip

from model.person import Person, Staff, Fellow


class TestPerson(TestCase):

    def setUp(self):
        self.s = Staff('denis')
        self.f = Fellow('dng')
        self.fellow = Fellow('dan', True)

    def test_cannot_create_person_without_name(self):
        with self.assertRaises(TypeError):
            s = Staff()

    def test_person_created_with_correct_values(self):
        self.assertEqual(
            ['denis', 'dng', 'dan'],
            [self.s.name, self.f.name, self.fellow.name]
        )

    def test_person_created_correctly(self):
        self.assertIsInstance(self.s, Staff)
        self.assertIsInstance(self.fellow, Fellow)

    def test_person_type_is_correct(self):
        self.assertEqual(
            ['staff', 'fellow', 'fellow'],
            [self.s.person_type, self.f.person_type,
             self.fellow.person_type]
        )

    def test_fellow_can_opt_out_of_living_space(self):
        self.assertFalse(self.f.wants_livingspace)

    def test_fellow_can_opt_for_living_space(self):
        self.assertTrue(self.fellow.wants_livingspace)

    def test_fellow_can_change_living_space_option(self):
        self.f.wants_livingspace = True
        self.assertTrue(self.f.wants_livingspace)

    def test_fellow_can_opt_out_of_living_space_after_creation(self):
        self.fellow.wants_livingspace = False
        self.assertFalse(self.fellow.wants_livingspace)
