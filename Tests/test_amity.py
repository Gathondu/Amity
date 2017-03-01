import unittest
from Model.Amity import Amity


class TestAmity(unittest.TestCase):

    def setUp(self):
        # offices: valhalla, hogwarts, occulus, krypton
        # livingspaces outside, dojo
        self.reallocate_person = {
            "1": {
                "name": "denis gathondu",
                "type": "staff",
                "room": "valhalla"
                },
            "2": {
                "name": "sylvia sly",
                "type": "fellow",
                "livingspace": True,
                "room": {
                    "office": "valhalla",
                    "livingspace": "outside"
                    }
                },
            "3": {
                "name": "shem shem",
                "type": "fellow",
                "livingspace": False,
                "room": "valhalla"
                }
        }

    def test_room_is_created(self):
        room = Amity.create_room("office", "occulus")
        self.assertEqual("office occulus created", room)

    def test_staff_is_added(self):
        person = Amity.add_person("DeNis", "Gathondu", "staff")
        self.assertEqual("staff denis gathondu created", person)

    def test_staff_cannot_request_livingspace(self):
        with self.assertRaises(ValueError):
            Amity.add_person("DeNis", "Gathondu", "staff", "yes")

    def test_fellow_is_added(self):
        person = Amity.add_person("DeNis", "Gathondu", "fellow")
        self.assertEqual(
            "fellow denis gathondu created and doesn't require a living space",
            person
            )

    def test_fellow_requires_livingspace_is_added_correctly(self):
        person = Amity.add_person("DeNis", "Gathondu", "fellow", "yes")
        self.assertEqual(
            "fellow denis gathondu created and requires a living space",
            person
            )

    def test_person_type_is_required(self):
        with self.assertRaises(TypeError):
            Amity.add_person("denis", "gathondu")

    @unittest.skip("WIP")
    def test_person_should_not_be_duplicated(self):
        pass

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

    def test_that_fellow_without_livingspace_is_reallocated_office(self):
        reallocate = Amity.reallocate_person(self.reallocate_person["3"])
        self.assertEqual(
            "fellow shem shem reallocated to hogwarts office",
            reallocate
            )

    def test_that_staff_is_reallocated_office(self):
        reallocate = Amity.reallocate_person(self.reallocate_person["1"])
        self.assertEqual(
            "staff denis gathondu reallocated to hogwarts office",
            reallocate
            )

    @unittest.skip("WIP")
    def test_people_are_loaded(self):
        pass

    def test_allocations_are_printed(self):
        allocations = Amity.print_allocations()
        self.assertIsNotNone(allocations)

    @unittest.skip("WIP")
    def test_unallocations_are_printed(self):
        unallocations = Amity.print_unallocated()
        self.assertIsNotNone(unallocations)

    def test_print_room_prints_all_people_in_room(self):
        room = Amity.create_room("office", "krypton")
        # room.occupied_spaces = 2
        people = Amity.print_room("room.name")
        self.assertEqual("room.occupied_space", "len(people)")

    @unittest.skip("WIP")
    def test_state_is_saved_in_database(self):
        pass

    @unittest.skip("WIP")
    def test_state_is_loaded(self):
        pass
