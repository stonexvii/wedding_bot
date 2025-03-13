import sqlite3


class DataBase:
    instance = None

    def __new__(cls, *args, **kwargs):
        if cls.instance is None:
            instance = super().__new__(cls)
            cls.instance = instance
        return cls.instance

    def __init__(self, db_path: str = 'wedding.db'):
        self.db_path = db_path

    @property
    def connection(self):
        return sqlite3.connect(self.db_path)

    def execute(self, sql: str, parameters: tuple = tuple(),
                fetchone=False, fetchall=False, commit=False):
        connection = self.connection
        cursor = connection.cursor()
        data = None
        cursor.execute(sql, parameters)
        if commit:
            connection.commit()
        if fetchone:
            data = cursor.fetchone()
        if fetchall:
            data = cursor.fetchall()
        connection.close()
        return data

    # @staticmethod
    # def extract_kwargs(sql: str, parameters: dict) -> tuple:
    #     sql += ' AND '.join([f'{key} = ?' for key in parameters])
    #     return sql, tuple(parameters.values())

    def create_tables(self):
        sqls = [
            '''CREATE TABLE IF NOT EXISTS user_answers (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id     INTEGER, 
                question_id INTEGER,
                answer_id   INTEGER
                    )''',
            '''CREATE TABLE IF NOT EXISTS images (
                    id          INTEGER PRIMARY KEY AUTOINCREMENT,
                    photo_id    VARCHAR
                    )''',
        ]
        for sql in sqls:
            self.execute(sql, commit=True)

    def add_answer(self, user_id: int, question_id: int, answer_id: int):
        sql = '''INSERT INTO user_answers (user_id, question_id, answer_id) VALUES (?, ?, ?)'''
        self.execute(sql, (user_id, question_id, answer_id), commit=True)

    def get_answers(self, user_id: int) -> tuple:
        sql = '''SELECT question_id FROM user_answers WHERE user_id=?'''
        return self.execute(sql, (user_id,), fetchall=True)

    def add_photo(self, photo_id: str):
        sql = '''INSERT INTO images (photo_id) VALUES (?)'''
        self.execute(sql, (photo_id,), commit=True)

    def get_photo(self, photo_id: int) -> str:
        sql = '''SELECT photo_id FROM images WHERE id=?'''
        return self.execute(sql, (photo_id,), fetchone=True)[0]

    # def delete(self, task_id: int):
    #     sql = '''DELETE FROM tasks WHERE task_id=?'''
    #     self.execute(sql, (task_id,), commit=True)
    #
    # def collect(self, target: str, task_type: str = None) -> list[tuple[str]]:
    #     if not task_type:
    #         sql = f'''SELECT {target} FROM tasks'''
    #         return self.execute(sql, fetchall=True)
    #     else:
    #         sql = f'''SELECT {target} FROM tasks WHERE task_type=?'''
    #         return self.execute(sql, (task_type,), fetchall=True)

    def disconnect(self):
        self.connection.close()
