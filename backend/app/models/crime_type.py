from app.database import db
from typing import Union, List


class CrimeType:
    """A class to represent a crime type.

    Attributes:
        type_code (int): The unique identifier of the crime type.
        description (str): The description of the crime type.
    """

    def __init__(self, type_code: int, description: str) -> None:
        """Initializes a CrimeType object.

        Args:
            type_code (int): The unique identifier of the crime type.
            description (str): The description of the crime type.
        """
        self.type_code = type_code
        self.description = description

    @staticmethod
    def create(type_code: int, description: str) -> None:
        """Creates a new crime type.

        Args:
            type_code (int): The unique identifier of the crime type.
            description (str): The description of the crime type.
        """
        with db.get_connection() as conn:
            cursor = conn.cursor()
            query = 'INSERT INTO Crime_Type (type_code, description) \
                VALUES (%s, %s)'

            params = (type_code, description)
            cursor.execute(query, params)
            conn.commit()

    @staticmethod
    def get(type_code: int) -> 'CrimeType':
        """Gets a crime type.

        Args:
            type_code (int): The unique identifier of the crime type.

        Returns:
            CrimeType: The crime type.
        """
        with db.get_connection() as conn:
            cursor = conn.cursor()
            query = 'SELECT * FROM Crime_Type WHERE type_code = %s'
            params = (type_code, )
            cursor.execute(query, params)
            row = cursor.fetchone()
            if row:
                return CrimeType(*row)
            return None

    @staticmethod
    def get_all() -> List['CrimeType']:
        """Gets all crime types.

        Returns:
            List[CrimeType]: A list of all crime types.
        """
        with db.get_connection() as conn:
            cursor = conn.cursor()
            query = 'SELECT * FROM Crime_Type ORDER BY type_code limit 15'
            cursor.execute(query)
            rows = cursor.fetchall()
            return [CrimeType(*row) for row in rows]

    @staticmethod
    def delete(type_code: int) -> Union[str, None]:
        """Deletes a crime type.

        Args:
            type_code (int): The unique identifier of the crime type.
        """
        with db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Crime_Type WHERE type_code = %s",
                           (type_code, ))
            result = cursor.fetchone()
            if result is None:
                return "Crime type does not exist"
            else:
                query = 'DELETE FROM Crime_Type WHERE type_code = %s'
                params = (type_code, )
                cursor.execute(query, params)
                conn.commit()
