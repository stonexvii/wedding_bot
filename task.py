from DataBase import DataBase


class Task(DataBase):
    def __init__(self):
        super().__init__()

    def create_table_tasks(self):
        sql = '''CREATE TABLE IF NOT EXISTS tasks 
        (task_id INTEGER PRIMARY KEY AUTOINCREMENT, task_type VARCHAR, 
        task_level VARCHAR, task_value VARCHAR)'''
        self.execute(sql, commit=True)

    def add(self, task: tuple[str]):
        sql = '''INSERT INTO tasks (task_type, task_level, task_value) VALUES (?, ?, ?)'''
        self.execute(sql, task, commit=True)

    def select(self, task_type: str, task_level: str) -> tuple:
        user = (task_type, task_level)
        sql = '''SELECT * FROM tasks WHERE task_type=? AND task_level=?'''
        return self.execute(sql, user, fetchall=True)

    def delete(self, task_id: int):
        sql = '''DELETE FROM tasks WHERE task_id=?'''
        self.execute(sql, (task_id,), commit=True)

    def collect(self, target: str, task_type: str = None) -> list[tuple[str]]:
        if not task_type:
            sql = f'''SELECT {target} FROM tasks'''
            return self.execute(sql, fetchall=True)
        else:
            sql = f'''SELECT {target} FROM tasks WHERE task_type=?'''
            return self.execute(sql, (task_type,), fetchall=True)
