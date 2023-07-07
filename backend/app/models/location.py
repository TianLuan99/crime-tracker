from app.database import db
from typing import Union, List


class Location:
    """A class to represent a location.

    Attributes:
        location_name (str): The name of the location.
        latitude (float): The latitude of the location.
        longitude (float): The longitude of the location.
        patrol_division (str): The patrol division of the location.
    """

    def __init__(self, location_name: str, latitude: float, longitude: float,
                 patrol_division: str) -> None:
        """Initializes a Location object.

        Args:
            location_name (str): The name of the location.
            latitude (float): The latitude of the location.
            longitude (float): The longitude of the location.
            patrol_division (str): The patrol division of the location.
        """
        self.location_name = location_name
        self.latitude = latitude
        self.longitude = longitude
        self.patrol_division = patrol_division

    @staticmethod
    def create(location_name: str, latitude: float, longitude: float,
               patrol_division: str):
        """Creates a new location.

        Args:
            location_name (str): The name of the location.
            latitude (float): The latitude of the location.
            longitude (float): The longitude of the location.
            patrol_division (str): The patrol division of the location.
        """
        with db.get_connection() as conn:
            cursor = conn.cursor()
            query = 'INSERT INTO Location (location_name, latitude, longitude,\
                patrol_division) VALUES (%s, %s, %s, %s)'

            params = (location_name, latitude, longitude, patrol_division)
            cursor.execute(query, params)
            conn.commit()

    @staticmethod
    def get(location_name: str) -> 'Location':
        """Gets a location.

        Args:
            location_name (str): The name of the location.

        Returns:
            Location: The location.
        """
        with db.get_connection() as conn:
            cursor = conn.cursor()
            query = 'SELECT * FROM Location WHERE location_name = %s'
            params = (location_name, )
            cursor.execute(query, params)
            row = cursor.fetchone()
            if row:
                return Location(*row)
            return None

    @staticmethod
    def get_all() -> List['Location']:
        """Gets all locations.

        Returns:
            List[Location]: A list of locations.
        """
        with db.get_connection() as conn:
            cursor = conn.cursor()
            query = 'SELECT * FROM Location ORDER BY location_name limit 15'
            cursor.execute(query)
            rows = cursor.fetchall()
            locations = []
            for row in rows:
                locations.append(Location(*row))
            return locations

    @staticmethod
    def delete(location_name: str) -> Union[str, None]:
        """Deletes a location.

        Args:
            location_name (str): The name of the location.
        """
        with db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Location WHERE location_name = %s", (location_name,))
            result = cursor.fetchone()
            if result is None:
                return "Location does not exist"
            else:
                query = 'DELETE FROM Location WHERE location_name = %s'
                params = (location_name, )
                cursor.execute(query, params)
                conn.commit()
