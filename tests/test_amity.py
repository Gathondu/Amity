#!/usr/local/bin/python3
# -*- coding: utf-8 -*-


from unittest import TestCase, skip
from model.amity import Amity

# edge cases
# simplify logic
# input vs output don't complicate


class TestAmity(TestCase):

    def setUp(self):
        self.a = Amity()
        self.occulus = self.a.create_room('office occulus')
        self.dojo = self.a.create_room('livingspace dojo')
        self.staff = self.a.add_person('denis gathondu staff')
        self.fellow = self.a.add_person('denis gathondu fellow')
        self.fellow_with_living_space = self.a.add_person(
            'shem mwangi fellow y'
            )

    def test_room_is_created(self):
        self.assertEqual("office occulus created", self.occulus)
        self.assertEqual("livingspace dojo created", self.dojo)

    def test_room_is_created_correctly(self):
        from model.room import Office, LivingSpace
        self.assertIsInstance(self.occulus, Office)
        self.assertIsInstance(self.dojo, LivingSpace)

    def test_multiple_rooms_creation(self):
        multi_rooms = self.a.create_room(
            'office valhalla', 'livingspace outside', 'office krypton',
            'livingspace flats'
            )
        self.assertEqual(
            'offices valhalla, krypton and livingspaces outside, ' +
            'flats created',
            multi_rooms
            )

    def test_empty_room_name_raises_ValueError(self):
        with self.assertRaises(ValueError):
            self.a.create_room()

    def test_room_name_can_only_be_a_string(self):
        with self.assertRaises(ValueError):
            self.a.create_room(4)
            self.a.create_room('4.7')

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
        self.assertEqual("fellow denis gathondu added", self.fellow)
        self.assertEqual(
            "fellow shem mwangi added", self.fellow_with_living_space
            )

    def test_person_is_added_correctly(self):
        from model.person import Fellow, Staff
        self.assertIsInstance(self.a.fellow['denis gathondu'], Fellow)
        self.assertIsInstance(self.a.staff['denis gathondu'], Staff)

    def test_staff_cannot_request_livingspace(self):
        with self.assertRaises(ValueError):
            self.a.add_person('dan otieno staff y')

    def test_fellow_requires_livingspace_is_added_correctly(self):
        fellow = [
            fellow for fellow in self.a.fellow.values()
            if fellow.wants_living_space is True
            ]
        self.assertTrue(fellow[0].wants_living_space)

    def test_fellow_not_requiring_livingspace_is_added_correctly(self):
        fellow = [
            fellow for fellow in self.a.fellow.values()
            if fellow.wants_living_space is False
            ]
        self.assertFalse(fellow[0].wants_living_space)

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

    def test_person_should_not_be_duplicated(self):
        with self.assertRaises(ValueError):
            self.a.add_person('denis gathondu staff')
            self.a.add_person('shem mwangi fellow')

    def test_person_is_assigned_room(self):
        self.assertEqual('denis assigned space in valhalla',
                         self.add_to_office)

    @skip('WIP')
    def test_that_fellow_with_livingspace_is_reallocated_livingspace(self):
        reallocate = Amity.reallocate_person(self.reallocate_person["2"])
        self.assertEqual(
            "fellow sylvia sly reallocated to dojo livingspace",
            reallocate
            )
        # self.assertEqual(
        #     "fellow sylvia sly still in valhalla office",
        #     reallocate[1]
        #     )

    @skip('WIP')
    def test_that_fellow_with_livingspace_is_reallocated_office(self):
        reallocate = Amity.reallocate_person(self.reallocate_person["2"])
        self.assertEqual(
            "fellow sylvia sly reallocated to hogwarts office",
            reallocate
            )
        # self.assertEqual(
        #     "fellow sylvia sly still in outside livingspace",
        #     reallocate[0]
        #     )

    @skip('WIP')
    def test_that_fellow_without_livingspace_is_reallocated_office(self):
        reallocate = Amity.reallocate_person(self.reallocate_person["3"])
        self.assertEqual(
            "fellow shem shem reallocated to hogwarts office",
            reallocate
            )

    @skip('WIP')
    def test_that_staff_is_reallocated_office(self):
        reallocate = Amity.reallocate_person(self.reallocate_person["1"])
        self.assertEqual(
            "staff denis gathondu reallocated to hogwarts office",
            reallocate
            )

    @skip("WIP")
    def test_people_are_loaded(self):
        pass

    @skip('WIP')
    def test_allocations_are_printed(self):
        allocations = Amity.print_allocations()
        self.assertIsNotNone(allocations)

    @skip("WIP")
    def test_unallocations_are_printed(self):
        unallocations = Amity.print_unallocated()
        self.assertIsNotNone(unallocations)

    @skip("WIP")
    def test_print_room_prints_all_people_in_room(self):
        room = Amity.create_room("office", "krypton")
        # room.occupied_spaces = 2
        people = Amity.print_room(room.name)
        self.assertEqual(2, len(people))

    @skip("WIP")
    def test_state_is_saved_in_database(self):
        pass

    @skip('WIP')
    def test_state_is_loaded(self):
        pass

    @skip('WIP')
    def test_check_room_availability(self):
        pass

    def test_adding_to_fully_occupied_room_raises_ValueError(self):
        for person in ['dan', 'shem', 'brian']:
            self.l.add_person(person)
        with self.assertRaises(ValueError):
            self.l.add_person('allan')

    def test_empty_room_is_correctly_displayed(self):
        office = Office('krypton')
        self.assertEqual('no one has been assigned to krypton yet.',
                         office.occupants)

    @skip('WIP')
    def test_person_is_successfully_removed_from_room(self):
        pass

    @skip('WIP')
    def test_if_person_does_not_exist_remove_person_raises_ValueError(self):
        pass

    @skip('WIP')
    def test_if_room_is_empty_removing_person_raises_ValueError(self):
        pass

    @skip('WIP')
    def test_room_availability_is_updated_upon_removing_person(self):
        pass

    @skip('WIP')
    def test_occupants_are_correctly_updated_upon_removing_person(self):
        pass

    @skip('WIP')
    def test_correct_number_of_occupied_spaces_after_removing_person(self):
        pass
