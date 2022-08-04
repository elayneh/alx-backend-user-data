#!/usr/bin/env python3
""" Hashing """

from user import User
import bcrypt
from db import DB
import uuid
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> str:
    """ Password hash """
    hashed_pwd = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    return hashed_pwd


def _generate_uuid() -> str:
    """ UUID generator """
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        """ Constractor """
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """ method to register new user """
        try:
            user = self._db.find_user_by(email=email)
            if user:
                raise ValueError('User {} already exists'.format(email))
        except NoResultFound:
            hashed_pwd = _hash_password(password)
            user = self._db.add_user(email, hashed_pwd)
            return user

    def valid_login(self, email: str, password: str) -> bool:
        """ Credentials validation """
        try:
            user = self._db.find_user_by(email=email)
            if user:
                return bcrypt.checkpw(password.encode(), user.hashed_password)
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """ Session creator """
        try:
            user = self._db.find_user_by(email=email)
            if user:
                session_id = _generate_uuid()
                return session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> str:
        """ Return corresponding user if exists """

        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
            if user:
                return user
        except Exception:
            return None

    def destroy_session(self, user_id: int) -> None:
        """ Destroy session """
        self._db.update_user(user_id, session_id=None)
        return None
