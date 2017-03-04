from unittest import TestCase, skip

from model.room import Office, LivingSpace


class TestRoom(TestCase):

    def setUp(self):
        self.o = Office('valhalla')
        self.l = LivingSpace('dojo')
        self.add_to_office = self.o.add_person('denis')
        self.add_to_living_space = self.l.add_person('denis')

    def test_room_is_created_correctly(self):
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

    def test_person_is_added(self):
        self.assertEqual('denis assigned space in valhalla', self.add_to_office)

    def test_add_same_person_fails_with_ValueError(self):
        with self.assertRaises(ValueError):
            self.o.add_person('denis')

    def test_same_person_can_be_assigned_space_in_all_rooms(self):
        self.assertEqual('denis assigned space in valhalla', self.add_to_office)
        self.assertEqual('denis assigned space in dojo', self.add_to_living_space)

    def test_correct_occupants(self):
        self.assertEqual(['denis'], self.l.occupants)

    def test_correct_number_of_occupied_spaces(self):
        self.assertEqual(1, self.l.occupied_spaces)

    def test_correct_value_of_available_spaces(self):
        self.assertEqual(5, self.o.availability)

    def test_max_space_is_correctly_updated(self):
        self.o._max_space = 7
        self.assertEqual(7, self.o.max_space)

    def test_non_int_max_space_value_raies_ValueError(self):
        with self.assertRaises(ValueError):
            self.o._max_space = 'a'

    def test_adding_to_fully_occupied_room_raises_ValueError(self):
        for person in ['dan', 'shem', 'brian']:
            self.l.add_person(person)
        with self.assertRaises(ValueError):
            self.l.add_person('allan')

    def test_empty_room_is_correctly_displayed(self):
        office = Office('krypton')
        self.assertEqual('no one has been assigned to krypton yet.', office.occupants)

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
