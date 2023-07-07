from app.database import db
import datetime
from typing import Union, List


class CrimeIncident:
    """A class to represent a crime incident.

    Attributes:
        incident_id (int): The unique identifier of the crime incident.
        location_name (str): The name of the location where the crime incident
            occurred.
        date (datetime.date): The date when the crime incident occurred.
        time (datetime.time): The time when the crime incident occurred.
        status (str): The status of the crime incident.
    """

    def __init__(self, incident_id: int, location_name: str,
                 date: datetime.date, time: datetime.time,
                 status: str) -> None:
        """Initializes a CrimeIncident object.

        Args:
            incident_id (int): The unique identifier of the crime incident.
            location_name (str): The name of the location where the crime
                incident occurred.
            date (datetime.date): The date when the crime incident occurred.
            time (datetime.time): The time when the crime incident occurred.
            status (str): The status of the crime incident.
        """
        self.incident_id = incident_id
        self.location_name = location_name
        self.date = date
        self.time = time
        self.status = status

    @staticmethod
    def create(location_name: str, date: datetime.date, time: datetime.time,
               status: str) -> None:
        """Creates a new crime incident.

        Args:
            location_name (str): The name of the location where the crime
                incident occurred.
            date (datetime.date): The date when the crime incident occurred.
            time (datetime.time): The time when the crime incident occurred.
            status (str): The status of the crime incident.
        """
        with db.get_connection() as conn:
            cursor = conn.cursor()
            params = (location_name, date, time, status)
            cursor.callproc('insert_incident', params)
            # Procudure Like:
            # CREATE PROCEDURE `insert_incident`(
            #     IN p_location_name VARCHAR(255),
            #     IN p_date DATE,
            #     IN p_time TIME,
            #     IN p_status VARCHAR(255)
            # )
            # BEGIN
            #     DECLARE new_id INT;
            #     SET new_id = 0;
            #     SELECT MAX(incident_id) + 1 INTO new_id FROM Crime_Incident;
            #     IF new_id IS NULL THEN
            #         SET new_id = 1;
            #     END IF;

            #     INSERT IGNORE INTO Location(location_name)
            #     VALUES(p_location_name);

            #     INSERT INTO Crime_Incident (
            #         incident_id,
            #         location_name,
            #         date,
            #         time,
            #         status
            #     ) VALUES (
            #         new_id,
            #         p_location_name,
            #         p_date,
            #         p_time,
            #         p_status
            #     );
            # END
            conn.commit()

    @staticmethod
    def get(incident_id: int) -> 'CrimeIncident':
        """Gets a crime incident.

        Args:
            incident_id (int): The unique identifier of the crime incident.

        Returns:
            CrimeIncident: The crime incident with the given incident_id.
        """
        with db.get_connection() as conn:
            cursor = conn.cursor()
            query = 'SELECT * FROM Crime_Incident WHERE incident_id = %s'
            params = (incident_id, )
            cursor.execute(query, params)
            row = cursor.fetchone()
            if row:
                return CrimeIncident(*row)
            return None

    @staticmethod
    def get_all() -> List['CrimeIncident']:
        """Gets all crime incidents.

        Returns:
            List[CrimeIncident]: A list of all crime incidents.
        """
        with db.get_connection() as conn:
            cursor = conn.cursor()
            query = 'SELECT * FROM Crime_Incident \
                ORDER BY date DESC, time DESC limit 15'

            cursor.execute(query)
            rows = cursor.fetchall()
            return [CrimeIncident(*row) for row in rows]

    @staticmethod
    def delete(incident_id: int) -> Union[str, None]:
        """Deletes a crime incident.

        Args:
            incident_id (int): The unique identifier of the crime incident.
        """
        with db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                'SELECT * FROM Crime_Incident WHERE incident_id = %s',
                (incident_id, ))
            result = cursor.fetchone()
            if result is None:
                return "Crime incident does not exist"
            else:
                query = 'DELETE FROM Crime_Incident WHERE incident_id = %s'
                params = (incident_id, )
                cursor.execute(query, params)
                conn.commit()

    @staticmethod
    def update(incident_id: int,
               date: datetime.date = None,
               time: datetime.time = None,
               status: str = None) -> None:
        """ Update the age of victim in a crime report.

        Args:
            incident_id (int): The unique identifier of the incident.
            date (datetime.date): The date when the crime incident occurred.
            time (datetime.time): The time when the crime incident occurred.
            status (str): The status of the crime incident.
        """
        params = ()
        with db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                'SELECT * FROM Crime_Incident \
                WHERE incident_id = %s', (incident_id, ))
            result = cursor.fetchone()
            if result is None:
                return "Crime report does not exist"
            else:
                query = 'UPDATE Crime_Incident SET'
                if date is not None:
                    query += ' date = %s,'
                    params += (date, )
                if time is not None:
                    query += ' time = %s,'
                    params += (time, )
                if status is not None:
                    query += ' status = %s,'
                    params += (status, )
                query = query[:-1]
                query += ' WHERE incident_id = %s'

                params += (incident_id, )
                cursor.execute(query, params)
                conn.commit()

    @staticmethod
    def search(location_name: str = None,
               date: datetime.date = None,
               time: datetime.time = None,
               status: str = None) -> List['CrimeIncident']:
        """Search the crime incident based on keyword match

        Args:
            location_name (str): The location name of the crime incident.
            date (datetime.date): The date of the crime incident.
            time (datetime.time): The time of the crime incident.
            status (str): The status of the crime incident.
        """
        params = ()
        with db.get_connection() as conn:
            cursor = conn.cursor()
            query = "SELECT * FROM Crime_Incident WHERE "
            if location_name is not None:
                query += "location_name Like %s AND "
                params += (f'%{location_name}%', )
            if date is not None:
                query += "date = %s AND "
                params += (f'%{date}%', )
            if time is not None:
                query += "time = %s AND "
                params += (f'%{time}%', )
            if status is not None:
                query += "status Like %s AND "
                params += (f'%{status}%', )
            query = query[:-4]
            query += " limit 15"
            # print(query)
            cursor.execute(query, params)
            rows = cursor.fetchall()
            return [CrimeIncident(*row) for row in rows]
