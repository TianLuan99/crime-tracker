from app.database import db
import json


def get_feamle_crime_count_by_victim_descent_in_Central_Southwest():
    with db.get_connection() as conn:
        cursor = conn.cursor()
        query = '''
            SELECT cr.victim_descent AS Descent, COUNT(ci.incident_id) AS \
                Crime_Count
            FROM Crime_Incident ci
            JOIN Crime_Report_with_Incident_User cr ON ci.incident_id = \
                cr.incident_id
            JOIN Location l ON ci.location_name = l.location_name
            WHERE l.patrol_division LIKE '%Central%'
            OR l.patrol_division LIKE '%Southwest%'
            GROUP BY cr.victim_descent, cr.victim_sex
            HAVING cr.victim_sex = 'F'
            ORDER BY Crime_Count DESC
            LIMIT 5
        '''
        cursor.execute(query)
        result = cursor.fetchall()
        return result


def get_crime_stats():
    with db.get_connection() as conn:
        cursor = conn.cursor()
        query = '''
            SELECT l.patrol_division AS Patrol_Division, COUNT(ci.incident_id)\
                  AS Crime_Count
            FROM Crime_Incident ci
            JOIN Location l ON l.location_name = ci.location_name
            JOIN Crime_Incident_Crime_Type cict ON cict.incident_id =\
                  ci.incident_id
            JOIN Crime_Type ct ON cict.type_code = ct.type_code
            WHERE ct.description LIKE '%BATTERY%'
            AND ci.incident_id IN (SELECT incident_id
                                  FROM Crime_Incident
                                  NATURAL JOIN Crime_Report_with_Incident_User
                                  WHERE victim_age <= 21)
            GROUP BY l.patrol_division
            ORDER BY Crime_Count DESC
            LIMIT 5;
        '''
        cursor.execute(query)
        result = cursor.fetchall()
        return result


def generate_crime_report(start_date, end_date):
    with db.get_connection() as conn:
        cursor = conn.cursor()
        cursor.callproc('GenerateAdvancedCrimeReport', [start_date, end_date])

        cursor.execute('SELECT * FROM CrimeReport')
        result_set = cursor.fetchall()

        report_data = []
        column_names = [
            'patrol_division', 'weapon_count', 'most_common_crime_type',
            'most_common_crime_description', 'total_crimes'
        ]

        for row in result_set:
            report_data.append(dict(zip(column_names, row)))
        # print(report_data)
        return report_data
