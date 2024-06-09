import sqlite3

class Database:
    def __init__(self, db_name):
        self.db_name = db_name

    def connect(self):
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()

    def close(self):
        if self.conn:
            self.conn.commit()
            self.conn.close()

    def init_db(self):
        self.connect()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                name TEXT,
                surname TEXT,
                contact TEXT UNIQUE,
                birth_date TEXT,
                city TEXT,
                education TEXT,
                languages TEXT
            )
        """)
        self.close()

    def insert_user_data(self, user_info):
        self.connect()
        try:
            self.cursor.execute("""
                INSERT INTO users (name, surname, contact, birth_date, city, education, languages)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                user_info['name'],
                user_info['surname'],
                user_info['contact'],
                user_info['birth_date'],
                user_info['city'],
                user_info['education'],
                user_info['languages']
            ))
        except sqlite3.IntegrityError as e:
            print(f"Error inserting data: {e}")
            return False
        finally:
            self.close()
        return True

    def check_user_exists(self, contact):
        self.connect()
        self.cursor.execute("SELECT * FROM users WHERE contact = ?", (contact,))
        user_exists = self.cursor.fetchone() is not None
        self.close()
        return user_exists

    def get_vacation_type(self):
        self.connect()
        self.cursor.execute("SELECT name FROM vacation_type")
        vacation_types = [row[0] for row in self.cursor.fetchall()]
        self.close()
        return vacation_types

    def get_vacations(self, selected_vacation_type, lang):
        self.connect()
        if lang == "UZ":
            self.cursor.execute("""
                SELECT 
                    vacation.image_uz, 
                    vacation.name_uz, 
                    vacation.company, 
                    vacation.location_uz, 
                    vacation.requirements_uz, 
                    vacation.amenities_uz, 
                    vacation.salary, 
                    vacation.experience, 
                    vacation.contacts1, 
                    vacation.contacts2
                FROM vacation
                JOIN vacation_type ON vacation.vacation_id = vacation_type.id
                WHERE vacation_type.name = ?
            """, (selected_vacation_type,))
            vacations = self.cursor.fetchall()
            self.close()
            return vacations
        else:
            self.cursor.execute("""
                SELECT 
                    vacation.image_ru, 
                    vacation.name_ru, 
                    vacation.company, 
                    vacation.location_ru, 
                    vacation.requirements_ru, 
                    vacation.amenities_ru, 
                    vacation.salary, 
                    vacation.experience, 
                    vacation.contacts1, 
                    vacation.contacts2
                FROM vacation
                JOIN vacation_type ON vacation.vacation_id = vacation_type.id
                WHERE vacation_type.name = ?
            """, (selected_vacation_type,))
            vacations = self.cursor.fetchall()
            self.close()
            return vacations

    def get_questions(self, selected_vacation_type, lang):
        self.connect()
        if lang == "UZ":
            self.cursor.execute("""
            SELECT 
                test.test_uz
            FROM test 
            JOIN vacation_type ON test.vacancy_type_id = vacation_type.id
            WHERE vacation_type.name = ?
            """, (selected_vacation_type,))
            tests = self.cursor.fetchall()
            self.close()
            return tests
        else:
            self.cursor.execute("""
                        SELECT 
                        test.test_ru
                        FROM test 
                        JOIN vacation_type ON test.vacancy_type_id = vacation_type.id
                        WHERE vacation_type.name = ?
                        """, (selected_vacation_type,))
            tests = self.cursor.fetchall()
            self.close()
            return tests

    def update_answers(self, name, surname, birth_date, test_id, answers, lang):
        try:
            self.connect()
            answers_str = '\n'.join(answers)

            if lang == "UZ":
                query = """
                            UPDATE users
                            SET test_id = ?, answer_uz = ?
                            WHERE name = ? AND surname = ? AND birth_date = ?
                            """
                self.cursor.execute(query, (test_id, answers_str, name, surname, birth_date))
            else:
                query = """
                            UPDATE users
                            SET test_id = ?, answer_ru = ?
                            WHERE name = ? AND surname = ? AND birth_date = ?
                            """
                self.cursor.execute(query, (test_id, answers_str, name, surname, birth_date))
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
        finally:
            self.close()


    def get_test_id(self, selected_vacation_type):
        self.connect()
        self.cursor.execute("""
            SELECT test.id
            FROM test
            JOIN vacation_type ON test.vacancy_type_id = vacation_type.id
            WHERE vacation_type.name = ?
            LIMIT 1
        """, (selected_vacation_type,))
        test_id = self.cursor.fetchone()[0]
        self.close()
        print(test_id)
        return test_id


    def get_user_id(self, contact):
        self.connect()
        self.cursor.execute("SELECT id FROM users WHERE contact = ? LIMIT 1", (contact,))
        user_row = self.cursor.fetchone()
        self.close()
        if user_row:
            user_id = user_row[0]
            print(user_id)
            return user_id
        return None

    def insert_answers(self, name, surname, birth_date, test_id, answers, lang):
        try:
            self.connect()
            answers_str = '\n'.join(answers)

            if lang == "UZ":
                query = """
                    INSERT INTO answers (user_id, test_id, answer_uz)
                    SELECT id, ?, ?
                    FROM users
                    WHERE name = ? AND surname = ? AND birth_date = ?
                """
                self.cursor.execute(query, (test_id, answers_str, name, surname, birth_date))
            else:
                query = """
                    INSERT INTO answers (user_id, test_id, answer_ru)
                    SELECT id, ?, ?
                    FROM users
                    WHERE name = ? AND surname = ? AND birth_date = ?
                """
                self.cursor.execute(query, (test_id, answers_str, name, surname, birth_date))
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
        finally:
            self.close()