#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
import pytest

from model.room import Room, Office, LivingSpace


@pytest.fixture(scope='module')
def office(request):
    return Office('valhalla')


@pytest.fixture(scope='module')
def livingspace(request):
    return LivingSpace('dojo')


def test_room_name_is_correct(office, livingspace):
    assert office.name == 'valhalla'
    assert livingspace.name == 'dojo'


def test_max_space_is_correct(office, livingspace):
    assert office.max_space == 6
    assert livingspace.max_space == 4


def test_room_type_is_correct(office, livingspace):
    assert livingspace.room_type == 'livingspace'
    assert office.room_type == 'office'


def test_max_space_is_correctly_updated(office):
    office.max_space_set(7)
    assert office.max_space == 7


def test_non_int_max_space_value_raies_ValueError(office):
    with pytest.raises(ValueError):
        office.max_space_set('a')
