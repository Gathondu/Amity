#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
import pytest

from model.person import Person, Staff, Fellow


@pytest.fixture(scope='module')
def staff(request):
    return Staff('denis')


@pytest.fixture(scope='module')
def fellow(request):
    return Fellow('dng')


@pytest.fixture(scope='module')
def fellow_with_livingspace(request):
    return Fellow('dan', True)


def test_cannot_create_person_without_name(staff):
    with pytest.raises(TypeError):
        staff = Staff()


def test_person_created_with_correct_values(staff, fellow):
    assert [staff.name, fellow.name] == ['denis', 'dng']


def test_person_type_is_correct(staff, fellow):
    assert [staff.person_type, fellow.person_type] ==\
        ['staff', 'fellow']


def test_fellow_can_opt_out_of_living_space(fellow):
    assert fellow.wants_livingspace is False


def test_fellow_can_opt_for_living_space(fellow_with_livingspace):
    assert fellow_with_livingspace.wants_livingspace


def test_fellow_can_change_living_space_option(fellow):
    fellow.wants_livingspace = True
    assert fellow.wants_livingspace


def test_fellow_can_opt_out_of_living_space_after_creation(fellow_with_livingspace):
    fellow_with_livingspace.wants_livingspace = False
    assert fellow_with_livingspace.wants_livingspace is False
