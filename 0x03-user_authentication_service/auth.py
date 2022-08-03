#!/usr/bin/env python3
""" Authorization """
import bcrypt


def _hash_password(password: str) -> str:
    """ Password hash """
    hashed_pwd = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    return hashed_pwd
