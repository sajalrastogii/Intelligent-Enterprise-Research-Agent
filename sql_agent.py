import psycopg2

class SQLAgent:
    def __init__(self, connection_string):
        self.conn = psycopg2.connect(connection_string)

    def safe_execute(self, query):
        if any(word in query.lower() for word in ["drop", "delete", "truncate"]):
            return "Unsafe query detected."

        cursor = self.conn.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        return result
