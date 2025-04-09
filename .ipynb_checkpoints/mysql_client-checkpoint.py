import pymysql
from pymysql.err import MySQLError


class MysqlClient:
    def __init__(self, host: str, user: str, password: str, database: str):
        self.conn = pymysql.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        self.cursor = self.conn.cursor()

    def insert_data(self, data, columns, table):
        try:
            sql = f"INSERT INTO {table}  ({', '.join(f'`{col}`' for col in columns)}) VALUES (%s, %s)"
            self.cursor.executemany(sql, data)
            self.conn.commit()
            return self.cursor.rowcount
        except MySQLError as e:
            print("MySQL 에러 발생 (insert_data):", e)
            return None

    def get_data(self, columns, table, filter_clause: str = None):
        try:
            sql = f"SELECT {', '.join(f'`{col}`' for col in columns)} FROM {table}"
            if filter_clause:
                sql += f" WHERE {filter_clause}"
            self.cursor.execute(sql)
            return self.cursor.fetchall()
        except MySQLError as e:
            print("MySQL 에러 발생 (get_data):", e)
            return None

    def close(self):
        try:
            self.cursor.close()
            self.conn.close()
        except Exception as e:
            print("연결 종료 중 오류:", e)
