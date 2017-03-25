#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
import pytest

from termcolor import colored

from model.amity import Amity
from model.database import Database


@pytest.fixture(scope='module')
def amity():
    '''Set up amity instance to be used in the module'''
    return Amity()


def test_add_person_before_room_creation_does_not_allocate(amity):
    amity.add_person('staff', 'slyvia sly')
    assert amity.print_allocations() ==\
        '\nALLOCATIONS\n' + '-'*20+'\n' + \
        colored('NO ALLOCATIONS HAVE BEEN DONE YET', 'white', 'on_red')
    amity.remove_person('slyvia sly')


def test_room_is_created(amity):
    assert amity.create_room('office', 'occulus') ==\
        colored('Office occulus created.', 'white', 'on_green')


def test_room_created_with_correct_values(amity):
    amity.create_room('livingspace', 'dojo')
    assert amity.get_room(room_name='dojo')['max_space'] == 4


def test_room_name_must_be_string(amity):
    with pytest.raises(ValueError):
        amity.create_room('office', 4)


def test_room_name_duplicates_not_allowed(amity):
    with pytest.raises(ValueError):
        amity.create_room('office', 'occulus')
        amity.create_room('livingspace', 'dojo')


def test_room_exists_after_creation(amity):
    assert amity.room_exists('occulus')


def test_cannot_operate_on_non_existent_room(amity):
    assert amity.check_room_availability('hog') ==\
        colored("Room hog doesn't exist!", 'white', 'on_red')


def test_room_name_and_type_must_be_specified(amity):
    with pytest.raises(TypeError):
        amity.create_room()


def test_room_name_and_type_cannot_be_empty(amity):
    with pytest.raises(ValueError):
        amity.create_room('', '')


def test_room_name_can_only_be_string(amity):
    with pytest.raises(ValueError):
        amity.create_room('office', '@here')


def test_person_is_added(amity):
    assert amity.add_person('staff', 'denis gathondu') ==\
        colored('Staff denis gathondu added.', 'white', 'on_green')


def test_person_exists_after_being_added(amity):
    assert amity.person_exists('denis gathondu')


def test_person_name_duplicates_not_allowed(amity):
    with pytest.raises(ValueError):
        amity.add_person('fellow', 'denis gathondu')


def test_person_name_must_be_string(amity):
    with pytest.raises(ValueError):
        amity.add_person('fellow', '@denis')


def test_wrong_person_role_raises_error(amity):
    with pytest.raises(ValueError):
        amity.add_person('fella', 'dng')


def test_person_is_automatically_allocated_space(amity):
    room = [
        room for room in amity.rooms if 'denis gathondu'
        in room['occupants']]
    assert room


def test_person_can_be_manually_allocated(amity):
    amity.remove_person_from_room('denis gathondu')
    amity.allocate_person('denis gathondu')
    assert 'DENIS GATHONDU' in amity.print_room('occulus')


def test_person_who_wants_livingspace_is_allocated_livingspace(amity):
    amity.add_person('fellow', 'dan mwangi', True)
    assert amity.print_room('dojo') == 'DAN MWANGI'


def test_person_is_reallocated(amity):
    amity.create_room('office', 'valhalla')
    assert amity.reallocate_person('denis gathondu', 'valhalla') ==\
        colored('Denis gathondu reallocated to office valhalla.', 'white',
                'on_green')


def test_staff_cannot_be_reallocated_to_livingspace(amity):
    with pytest.raises(ValueError):
        amity.reallocate_person('denis gathondu', 'dojo')


def test_person_with_allocation_cannot_be_allocated(amity):
    with pytest.raises(ValueError):
        amity.allocate_person('denis gathondu')


def test_non_existent_person_cannot_be_allocated_space(amity):
    with pytest.raises(ValueError):
        amity.allocate_person('daisy wanjiru')


def test_allocations_are_printed_to_file(amity):
    assert amity.print_allocations('alloc.txt') ==\
        colored('Allocations have been saved to file alloc.txt.', 'white',
                'on_green')


def test_unallocated_is_correct(amity):
    assert amity.print_unallocated() ==\
        '\nUNALLOCATED\n'+'-'*20+'\n' + colored('NO UNALLOCATED PEOPLE',
                                                'white', 'on_red')


def test_unallocated_are_printed_to_file(amity):
    assert amity.print_unallocated('unalloc.txt') ==\
        colored('Unallocations have been saved to file unalloc.txt.', 'white',
                'on_green')


def test_room_prints_correctly(amity):
    assert amity.print_room('valhalla') == 'DENIS GATHONDU'


def test_cannot_print_non_existent_room(amity):
    with pytest.raises(ValueError):
        amity.print_room('narnia')


def test_person_is_successfully_removed_from_amity(amity):
    amity.remove_person('denis gathondu')
    assert amity.person_exists('denis') is None


def test_people_are_loaded_from_file(amity):
    assert amity.load_people('people.txt') == \
        colored('People loaded from people.txt successfully.', 'white',
                'on_green')


def test_rooms_are_loaded_from_file(amity):
    assert amity.load_rooms('rooms.txt') == \
        colored('Rooms loaded from rooms.txt successfully.', 'white',
                'on_green')


def test_state_is_saved(amity):
    assert amity.save_state() ==\
        colored("Amity's state saved successfully.", 'white', 'on_green')


def test_state_is_loaded(amity):
    assert amity.load_state() ==\
        colored("Amity's previous state loaded successfully.", 'white',
                'on_green')
