#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
from model.person import Fellow, Staff
from model.room import Office, LivingSpace


class Amity:
    offices = []
    living_spaces = []
    rooms = [["name", "type", "allocated_spaces"]]
    rooms_allocations = {
        "offices": {
            "name": "",
            "allocated_spaces": 0
        },
        "living_spaces": {
            "name": "",
            "allocated_spaces": 0
        }
    }
    staff = []
    fellows = []

    def add_person(first_name, last_name, position, living_space=None):
        """This function employs  a new new person as  a staff or fellow."""
        pass

    def allocate_space(name, position, livaing_space):
        """This function allocates space to new employees."""
        pass

    def check_room_availability(room_name):
        """This function checks for the availability of rooms in amity"""
        pass

    def create_room(type, room_name):
        """This function creates a new room in amity"""
        pass

    def reallocate_person(person, room_name):
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

    def print_room(room_name):
        """This function prints the people in rooms contained in amity"""
        pass

    def save_state():
        """This function saves the running state of amity to the database"""
        pass

    def load_state():
        """This function loads amity resourses from the database"""
        pass