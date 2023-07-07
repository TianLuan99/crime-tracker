from app.database import db
import datetime
from typing import Union, List


class CrimeReport:
    """A class to represent a crime report.

    Attributes:
        report_id (int): The unique identifier of the crime report.
        user_id (int): The unique identifier of the user who submitted the
            crime report.
        incident_id (int): The unique identifier of the crime incident.
        date (datetime.date): The date when the crime report was submitted.
        weapon (str): The weapon used in the crime incident.
        premise (str): The premise where the crime incident occurred.
        victim_age (int): The age of the victim.
    """

    def __init__(self, report_id: int, user_id: int, incident_id: int,
                 date: datetime.date, weapon: str, premise: str,
                 victim_age: int, victim_sex: str, victim_descent: str):
        """Initializes a CrimeReport object.

        Args:
            report_id (int): The unique identifier of the crime report.
            user_id (int): The unique identifier of the user who submitted the
                crime report.
            incident_id (int): The unique identifier of the crime incident.
            date (datetime.date): The date when the crime report was submitted.
            weapon (str): The weapon used in the crime incident.
            premise (str): The premise where the crime incident occurred.
            victim_age (int): The age of the victim.
        """
        self.report_id = report_id
        self.user_id = user_id
        self.incident_id = incident_id
        self.date = date
        self.weapon = weapon
        self.premise = premise
        self.victim_age = victim_age
        self.victim_sex = victim_sex
        self.victim_descent = victim_descent

    @staticmethod
    def create(user_id: int, incident_id: int, date: datetime.date,
               weapon: str, premise: str, victim_age: int, victim_sex: str,
               victim_descent: str) -> None:
        """Creates a new crime report.

        Args:
            report_id (int): The unique identifier of the crime report.
            user_id (int): The unique identifier of the user who submitted the
                crime report.
            incident_id (int): The unique identifier of the crime incident.
            date (datetime.date): The date when the crime report was submitted.
            weapon (str): The weapon used in the crime incident.
            premise (str): The premise where the crime incident occurred.
            victim_age (int): The age of the victim.
            victim_sex (str): The sex of the victim.
            victim_descent (str): The descent of the victim.
        """
        with db.get_connection() as conn:
            cursor = conn.cursor()
            params = (user_id, incident_id, date, weapon, premise, victim_age,
                      victim_sex, victim_descent)
            cursor.callproc('insert_report', params)
            # Procedure to create a new crime report:
            # CREATE PROCEDURE `insert_report`(
            # IN p_user_id INT,
            # IN p_incident_id INT,
            # IN p_date DATE,
            # IN p_weapon VARCHAR(255),
            # IN p_premise VARCHAR(255),
            # IN p_victim_age INT,
            # IN p_victim_sex VARCHAR(10),
            # IN p_victim_descent VARCHAR(25)
            # )
            # BEGIN
            #     DECLARE new_id INT;
            #     SET new_id = 0;
            #     SELECT MAX(report_id) + 1 INTO new_id FROM Crime_Report_with_Incident_User;
            #     IF new_id IS NULL THEN
            #         SET new_id = 1;
            #     END IF;
            #     INSERT INTO Crime_Report_with_Incident_User (report_id, user_id, incident_id, date, weapon, premise, victim_age, victim_sex, victim_descent)
            #     VALUES (new_id, p_user_id, p_incident_id, p_date, p_weapon, p_premise, p_victim_age, p_victim_sex, p_victim_descent);
            # END
            conn.commit()

    @staticmethod
    def get(incident_id: int, user_id: int, report_id: int) -> 'CrimeReport':
        """Gets a crime report by its unique identifier.

        Args:
            incident_id (int): The identifier of the crime incident.
            user_id (int): The identifier of the user of crime report.
            report_id (int): The identifier of the crime report.

        Returns:
            CrimeReport: The crime report with the given unique identifier.
        """
        with db.get_connection() as conn:
            cursor = conn.cursor()
            query = 'SELECT * FROM Crime_Report_with_Incident_User \
                WHERE incident_id = %s and user_id = %s and report_id = %s'

            params = (incident_id, user_id, report_id)
            cursor.execute(query, params)
            row = cursor.fetchone()
            if row:
                return CrimeReport(*row)
            return None

    @staticmethod
    def get_all() -> List['CrimeReport']:
        """Gets all crime reports.

        Returns:
            List[CrimeReport]: A list of all crime reports.
        """
        with db.get_connection() as conn:
            cursor = conn.cursor()
            query = 'SELECT * FROM Crime_Report_with_Incident_User \
                ORDER BY incident_id, user_id, report_id limit 15'

            cursor.execute(query)
            rows = cursor.fetchall()
            return [CrimeReport(*row) for row in rows]

    @staticmethod
    def delete(incident_id: int, user_id: int,
               report_id: int) -> Union[str, None]:
        """Deletes a crime report by its unique identifier.

        Args:
            incident_id (int): The unique identifier of the incident.
            user_id (int): The unique identifier of the user who write.
            report_id (int): The unique identifier of the crime report.
        """
        with db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                'SELECT * FROM Crime_Report_with_Incident_User \
                WHERE incident_id = %s and user_id = %s and report_id = %s',
                (incident_id, user_id, report_id))
            result = cursor.fetchone()
            if result is None:
                return "Crime report does not exist"
            else:
                query = 'DELETE FROM Crime_Report_with_Incident_User \
                    WHERE incident_id = %s and user_id = %s and report_id = %s'

                params = (incident_id, user_id, report_id)
                cursor.execute(query, params)
                conn.commit()

    def update(incident_id: int,
               user_id: int,
               report_id: int,
               weapon: str = None,
               premise: str = None,
               victim_age: int = None,
               victim_sex: str = None,
               victim_descent: str = None) -> None:
        """ Update the age of victim in a crime report.

        Args:
            incident_id (int): The unique identifier of the incident.
            user_id (int): The unique identifier of the user who write.
            report_id (int): The unique identifier of the crime report.
            new_age (int): The new age of the victim of the report.
        """
        params = ()
        with db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                'SELECT * FROM Crime_Report_with_Incident_User \
                WHERE incident_id = %s and user_id = %s and report_id = %s',
                (incident_id, user_id, report_id))
            result = cursor.fetchone()
            if result is None:
                return "Crime report does not exist"
            else:
                query = 'UPDATE Crime_Report_with_Incident_User SET'
                if weapon is not None:
                    query += ' weapon = %s,'
                    params += (weapon, )
                if premise is not None:
                    query += ' premise = %s,'
                    params += (premise, )
                if victim_age is not None:
                    query += ' victim_age = %s,'
                    params += (victim_age, )
                if victim_sex is not None:
                    query += ' victim_sex = %s,'
                    params += (victim_sex, )
                if victim_descent is not None:
                    query += ' victim_descent = %s,'
                    params += (victim_descent, )
                query = query[:-1]
                query += ' WHERE incident_id = %s and user_id = %s \
                    and report_id = %s'

                params += (incident_id, user_id, report_id)
                cursor.execute(query, params)
                conn.commit()

    @staticmethod
    def search(weapon: str = None,
               premise: str = None,
               victim_age: int = None,
               victim_sex: str = None,
               victim_descent: str = None) -> List['CrimeReport']:
        """Search the crime incident based on keyword match

        Args:
            weapon (str): The weapon of the crime incident.
            premise (str): The premise of the crime incident.
            victim_age (int): The age of the victim.
            victim_sex (str): The sex of the victim.
            victim_descent (str): The descent of the victim.
        """
        params = ()
        with db.get_connection() as conn:
            cursor = conn.cursor()
            query = "SELECT * FROM Crime_Report_with_Incident_User WHERE "
            if weapon is not None:
                query += "weapon Like %s AND "
                params += (f'%{weapon}%', )
            if premise is not None:
                query += "premise Like %s AND "
                params += (f'%{premise}%', )
            if victim_age is not None:
                query += "victim_age = %s AND "
                params += (f'%{victim_age}%', )
            if victim_sex is not None:
                query += "victim_sex Like %s AND "
                params += (f'%{victim_sex}%', )
            if victim_descent is not None:
                query += "victim_descent Like %s AND "
                params += (f'%{victim_descent}%', )
            query = query[:-4]
            query += " limit 15"
            # print(query)
            # print(params)
            cursor.execute(query, params)
            rows = cursor.fetchall()
            return [CrimeReport(*row) for row in rows]

    @staticmethod
    def get_all_by_incident(incident_id: int) -> List['CrimeReport']:
        """Gets all crime reports by incident.

        Args:
            incident_id (int): The identifier of the crime incident.

        Returns:
            List[CrimeReport]: A list of all crime reports.
        """
        with db.get_connection() as conn:
            cursor = conn.cursor()
            query = 'SELECT * FROM Crime_Report_with_Incident_User \
                WHERE incident_id = %s ORDER BY incident_id, user_id, \
                    report_id limit 15'

            params = (incident_id, )
            cursor.execute(query, params)
            rows = cursor.fetchall()
            return [CrimeReport(*row) for row in rows]
