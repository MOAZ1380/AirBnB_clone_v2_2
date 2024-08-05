#!/usr/bin/python3
""" class"""
from models.base_model import BaseModel


class User(BaseModel):
    """ class """
    # print("class user")
    email = ''
    password = ''
    first_name = ''
    last_name = ''
