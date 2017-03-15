#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
import json


from unittest import TestCase, skip
from model.amity import Amity


class TestAmity(TestCase):

    def setUp(self):
        self.a = Amity()
        self.occulus = self.a.create_room('office occulus')
        self.krypton = self.a.create_room('office krypton')
        self.dojo = self.a.create_room('livingspace dojo')
        self.out = self.a.create_room('livingspace out')
        self.staff = self.a.add_person('denis gathondu staff')
        self.fellow = self.a.add_person('dan gathondu fellow')
        self.fellow_with_living_space = self.a.add_person(
            'shem mwangi fellow y'
            )

    def test_room_is_created(self):
        self.assertEqual("office occulus created", self.occulus)
        self.assertEqual("livingspace dojo created", self.dojo)

    def test_multiple_rooms_creation(self):
        amity = Amity()
        multi_rooms = amity.create_room(
            'office valhalla', 'livingspace outside', 'office krypton',
            'livingspace flats'
            )
        self.assertEqual(
            [
                'office valhalla created', 'livingspace outside created',
                'office krypton created', 'livingspace flats created'
            ],
            multi_rooms
            )

    def test_empty_room_name_raises_ValueError(self):
        with self.assertRaises(ValueError):
            self.a.create_room()

    def test_room_name_can_only_be_a_string(self):
        with self.assertRaises(ValueError):
            self.a.create_room(4)
            self.a.create_room(4.7)

    def test_room_name_cannot_be_duplicated(self):
        with self.assertRaises(ValueError):
            self.a.create_room('office occulus')
            self.a.create_room('livingspace occulus')
            self.a.create_room('livingspace dojo')
            self.a.create_room('office dojo')

    def test_room_type_must_be_specified_upon_creation(self):
        with self.assertRaises(ValueError):
            self.a.create_room('krypton')

    def test_room_type_and_name_must_be_space_separated(self):
        with self.assertRaises(ValueError):
            self.a.create_room('officekrypton')

    def test_person_is_added(self):
        self.assertEqual("staff denis gathondu added", self.staff)
        self.assertEqual("fellow dan gathondu added", self.fellow)
        self.assertEqual(
            "fellow shem mwangi added", self.fellow_with_living_space
        )

    def test_multiple_people_added(self):
        amity = Amity()
        multi_rooms = amity.create_room(
            'office valhalla', 'livingspace outside', 'office krypton',
            'livingspace flats'
            )
        people = amity.add_person(
            'denis gathondu staff', 'dan miti fellow', 'sly sly fellow y'
        )
        self.assertEqual(
            [
                'staff denis gathondu added', 'fellow dan miti added',
                'fellow sly sly added'
            ],
            people
            )

    def test_staff_cannot_request_livingspace(self):
        with self.assertRaises(ValueError):
            self.a.add_person('dan otieno staff y')

    def test_fellow_requires_livingspace_is_added_correctly(self):
        fellow = [
            fellow for fellow in self.a.people
            if '_wants_living_space' in fellow.keys()
            ]
        self.assertTrue(fellow[0]['_wants_living_space'])

    def test_fellow_not_requiring_livingspace_is_added_correctly(self):
        fellow = [
            fellow for fellow in self.a.people
            if fellow['person_type'] == 'fellow' and
            '_wants_living_space' not in fellow.keys()
            ]
        with self.assertRaises(KeyError):
            fellow[0]['_wants_living_space']

    def test_person_name_is_required(self):
        with self.assertRaises(ValueError):
            self.a.add_person()

    def test_person_type_is_required(self):
        with self.assertRaises(ValueError):
            self.a.add_person('dan otieno')

    def test_person_type_cannot_be_specified_twice(self):
        with self.assertRaises(ValueError):
            self.a.add_person('dan otieno y y')

    def test_person_name_and_type_should_be_space_separated(self):
        with self.assertRaises(ValueError):
            self.a.add_person('danotienostaff')

    def test_person_cannot_not_be_duplicated(self):
        with self.assertRaises(ValueError):
            self.a.add_person('denis gathondu staff')
        with self.assertRaises(ValueError):
            self.a.add_person('shem mwangi fellow')

    def test_fellow_with_livingspace_is_reallocated_livingspace(self):
        r = [
            room for room in self.a.rooms
            if 'shem mwangi' in room['occupants'] and
            room['room_type'] == 'living space'
        ][0]
        if r['name'] == 'dojo':
            reallocate = self.a.reallocate_person('shem mwangi', 'out')
            self.assertEqual(
                "shem mwangi reallocated to living space out",
                reallocate
                )
        if r['name'] == 'out':
            reallocate = self.a.reallocate_person('shem mwangi', 'dojo')
            self.assertEqual(
                "shem mwangi reallocated to living space dojo",
                reallocate
                )

    def test_fellow_with_livingspace_is_reallocated_office(self):
        r = [
            room for room in self.a.rooms
            if 'shem mwangi' in room['occupants'] and
            room['room_type'] == 'office'
        ][0]
        if r['name'] == 'occulus':
            reallocate = self.a.reallocate_person('shem mwangi', 'krypton')
            self.assertEqual(
                "shem mwangi reallocated to office krypton",
                reallocate
                )
        if r['name'] == 'krypton':
            reallocate = self.a.reallocate_person('shem mwangi', 'occulus')
            self.assertEqual(
                "shem mwangi reallocated to office occulus",
                reallocate
                )

    def test_fellow_without_livingspace_is_reallocated_office(self):
        r = [
            room for room in self.a.rooms
            if 'dan gathondu' in room['occupants']
        ][0]
        if r['name'] == 'occulus':
            reallocate = self.a.reallocate_person('dan gathondu', 'krypton')
            self.assertEqual(
                "dan gathondu reallocated to office krypton",
                reallocate
                )
        if r['name'] == 'krypton':
            reallocate = self.a.reallocate_person('dan gathondu', 'occulus')
            self.assertEqual(
                "dan gathondu reallocated to office occulus",
                reallocate
                )

    def test_staff_reallocated_to_living_space_raises_ValueError(self):
        with self.assertRaises(ValueError):
            self.a.reallocate_person('denis gathondu', 'dojo')

    def test_fellow_without_livingspace_reallocated_to_living_space_raises_ValueError(self):
        with self.assertRaises(ValueError):
            self.a.reallocate_person('dan gathondu', 'dojo')

    def test_people_are_loaded(self):
        self.a.load_people('people.txt')
        self.assertTrue(self.a.person_exists('oluwafemi sule'))

    def test_allocations_are_printed(self):
        allocations = self.a.print_allocations()
        self.assertIsNotNone(allocations)

    def test_unallocations_are_printed(self):
        unallocations = self.a.print_unallocated()
        self.assertIsNotNone(unallocations)

    def test_print_room_prints_people_in_room(self):
        self.assertIsNotNone(self.a.print_room('occulus'))

    def test_check_room_availability(self):
        num = [
            room['_MAX_SPACE'] - len(room['occupants']) for room in
            self.a.rooms if room['name'] == 'occulus'
        ][0]
        self.assertEqual(num, self.a.check_room_availability('occulus'))

    def test_empty_room_is_correctly_displayed(self):
        self.a.create_room('office narnia')
        self.assertEqual('no one has been assigned to narnia yet',
                         self.a.print_room('narnia'))

    def test_person_is_successfully_removed_from_room(self):
        person = self.a.print_room('krypton')
        person = person.split(',')[0].lower()
        if person != '' and person !=\
                     'no one has been assigned to krypton yet':
            remove = self.a.remove_person(person, 'krypton')
            self.assertEqual(
                '{} removed successfully from krypton'
                .format(person), remove
                )

    def test_if_person_does_not_exist_remove_person_raises_ValueError(self):
        with self.assertRaises(ValueError):
            self.a.remove_person('amina', 'occulus')

    def test_if_room_is_empty_removing_person_raises_ValueError(self):
        room = [
            room for room in self.a.rooms if room['name'] == 'occulus'
        ][0]
        ind = self.a.rooms.index(room)
        self.a.rooms[ind]['occupants'] = []
        with self.assertRaises(ValueError):
            self.a.remove_person('denis gathondu', 'occulus')

    def test_room_availability_is_updated_upon_removing_person(self):
        num = self.a.check_room_availability('dojo')
        if num != 4:
            person = self.a.print_room('dojo')
            person = person.split(',')[0].lower()
            remove = self.a.remove_person(person.lower(), 'dojo')
            if person != '':
                self.assertEqual(
                    num + 1, self.a.check_room_availability('dojo')
                )

    @skip("WIP")
    def test_state_is_saved_in_database(self):
        pass

    @skip('WIP')
    def test_state_is_loaded(self):
        pass
