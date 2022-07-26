#!/usr/bin/env python3
""" Class to manage the API authontication """
from typing import List, TypeVar
from flask import Flask, request


class Auth:
    """ Class to authentication """
    
    def require_auth(self, path: str, excluded_path: List[str]) -> bool:
        """ Method that implements auth requirements """
        return False
    
    def authorization_header(self, request=None) -> str:
        """ Method that implements auth header """
        return request
    
    def current_user(self, request=None) -> TypeVar('User'):
        """ Current user """
        return request
 