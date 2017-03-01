#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
from Model.Fellow import Fellow
from Model.Staff import Staff
from Model.Office import Office
from Model.LivingSpace import LivingSpace


class Amity:

    def __init__(self):
        offices = set()
        living_spaces = set()
        rooms_allocations = {
            "offices": {
                "name": "", "allocated_spaces": 0
            },
            "living_spaces": {
                "name": "", "allocated_spaces": 0
            }
        }
        staff = []
        fellows = []

    def add_person(first_name, last_name, position, living_space=None):
        """This function employs  a new new person as  a staff or fellow."""
        pass

    def allocate_space(name, position, living_space):
        """This function allocates space to new employees."""
        pass

    def check_room_availability(name):
        """This function checks for the availability of rooms in amity"""
        pass

    def create_room(name, type):
        """This function creates a new room in amity"""
        pass

    def reallocate_person(name, previous):
        """This function reallocates an employee from one room to another"""
        pass

    def load_people():
        """This function loads employees from the database."""
        pass

    def print_allocations():
        """This function prints out the allocated rooms"""
        pass

    def print_unallocated():
        """This function prints out the unallocated rooms"""
        pass

    def print_room():
        """This function prints the rooms contained in amity"""
        pass

    def save_state():
        """This function saves the running state of amity to the database"""
        pass

    def load_state():
        """This function loads amity resourses from the database"""
        pass
