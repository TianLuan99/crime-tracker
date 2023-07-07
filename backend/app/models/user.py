from app.database import db
from typing import Union, List


class User:
    """A class to represent a user.

    Attributes:
        user_id (int): The unique identifier of the user.
        name (str): The name of the user.
        email (str): The email of the user.
        password (str): The password of the user.
    """

    def __init__(self, user_id: int, name: str, email: str,
                 password: str) -> None:
        """Initializes a User object.

        Args:
            user_id (int): The unique identifier of the user.
            name (str): The name of the user.
            email (str): The email of the user.
            password (str): The password of the user.
        """
        self.user_id = user_id
        self.name = name
        self.email = email
        self.password = password

    @staticmethod
    def create(user_id: int, name: str, email: str, password: str) -> None:
        """Creates a new user.

        Args:
            user_id (int): The unique identifier of the user.
            name (str): The name of the user.
            email (str): The email of the user.
            password (str): The password of the user.
        """
        with db.get_connection() as conn:
            cursor = conn.cursor()
            query = 'INSERT INTO User (user_id, name, email, password) \
                VALUES (%s, %s, %s, %s)'

            params = (user_id, name, email, password)
            cursor.execute(query, params)
            conn.commit()

    @staticmethod
    def get(user_id: str) -> 'User':
        """Gets a user.

        Args:
            user_id (int): The unique identifier of the user.

        Returns:
            User: The user with the specified user_id.
        """
        with db.get_connection() as conn:
            cursor = conn.cursor()
            query = 'SELECT * FROM User WHERE user_id = %s'
            params = (user_id, )
            cursor.execute(query, params)
            row = cursor.fetchone()
            if row:
                return User(*row)
            return None

    @staticmethod
    def get_all() -> List['User']:
        """Gets all users.

        Returns:
            List[User]: A list of all users.
        """
        with db.get_connection() as conn:
            cursor = conn.cursor()
            query = 'SELECT * FROM User ORDER BY user_id limit 15'
            cursor.execute(query)
            rows = cursor.fetchall()
            return [User(*row) for row in rows]

    @staticmethod
    def delete(user_id: int) -> Union[str, None] :
        """Deletes a user.

        Args:
            user_id (int): The unique identifier of the user.
        """
        with db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM User WHERE user_id = %s", (user_id,))
            result = cursor.fetchone()
            if result is None:
                return "User does not exist"
            else:
                query = 'DELETE FROM User WHERE user_id = %s'
                params = (user_id, )
                cursor.execute(query, params)
                conn.commit()
