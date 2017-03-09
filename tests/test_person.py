#!/usr/local/bin/python3
# -*- coding: utf-8 -*-


from unittest import TestCase, skip

from model.person import Person, Staff, Fellow


class TestPerson(TestCase):

    def setUp(self):
        self.p = Person('someone')
        self.s = Staff('denis')
        self.f = Fellow('denis')
        self.fellow = Fellow('dan', True)

    def test_cannot_create_person_without_name(self):
        with self.assertRaises(TypeError):
            s = Staff()

    def test_person_created_with_correct_values(self):
        self.assertEqual(
            ['someone', 'denis', 'denis', 'dan'],
            [self.p.name, self.s.name, self.f.name, self.fellow.name]
        )

    def test_person_created_correctly(self):
        self.assertIsInstance(self.p, Person)
        self.assertIsInstance(self.s, Staff)
        self.assertIsInstance(self.f, Fellow)
        self.assertIsInstance(self.fellow, Fellow)

    def test_person_type_is_correct(self):
        self.assertEqual(
            ['employee', 'staff', 'fellow', 'fellow'],
            [self.p.person_type, self.s.person_type, self.f.person_type,
             self.fellow.person_type]
        )

    def test_fellow_can_opt_out_of_living_space(self):
        self.assertFalse(self.f.wants_living_space)

    def test_fellow_can_opt_for_living_space(self):
        self.assertTrue(self.fellow.wants_living_space)

    def test_fellow_can_change_living_space_option(self):
        self.f.wants_living_space = True
        self.assertTrue(self.f.wants_living_space)

    def test_str_on_person_returns_correct_output(self):
        self.assertEqual(
            [
                'someone is a employee.',
                'denis is a staff.',
                'dan is a fellow.'
            ],
            [str(self.p), str(self.s), str(self.fellow)]
            )

    def test_fellow_can_opt_out_of_living_space_after_creation(self):
        self.fellow.wants_living_space = False
        self.assertFalse(self.fellow.wants_living_space)

    def test_set_wants_living_space_with_same_values_raises_ValueError(self):
        with self.assertRaises(ValueError):
            self.f.wants_living_space = False
            self.fellow.wants_living_space = True
