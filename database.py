import _sqlite3 as sql


class DbMain:
    """
    Основная база данных хранит пользователей.
    """

    def __init__(self):
        """
        Инизиализация класса( параметры по умолчанию).
        """
        self.con = sql.connect('users.db')
        self.cur = self.con.cursor()
        self.create_table()
        self.con.execute('''PRAGMA case_sensitive_like=true''')

    def create_table(self):
        """
        Создание основной таблицы.
        """
        self.con.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        login TEXT NOT NULL,
        password TEXT NOT NULL)
        ''')
        self.con.commit()

    def add_users(self, login: str, password: str):
        """
        Добавление пользователя.
        """
        self.cur.execute('''INSERT INTO users (login, password) VALUES (?, ?)''', (login, password))
        self.con.commit()

    def check_user(self, login: str):
        """Проверка наличия/соответствия  логина и пароля в базе данных.
        На выходе список с 2-мя значениями: 1 - состояние логина, 2 - состояние пароля
        """
        self.cur.execute('''SELECT * FROM users WHERE login LIKE ? ''', (login,))
        result = self.cur.fetchone()
        return result


class DB:
    """База данных на пользователя """

    def __init__(self, login):
        self.con = sql.connect('{}.db'.format(login))
        self.cur = self.con.cursor()
        self.cur.execute('''PRAGMA foreign_keys=on''')

    def create_table(self):
        """Создание основных таблиц в базе данных:
        1 - Таблица с источниками доходов
        2 - Таблица со счетами
        3 - Таблица с обязательными(ежемесячными расходами)
        4 - Таблица Расходов
        5 - Таблица с финансовыми целями
        6 - Таблица с категориями расходов
        """
        self.con.execute('''CREATE TABLE IF NOT EXISTS salary (
        salary_id INTEGER PRIMARY KEY,
        salary_name TEXT NOT NULL,
        salary_sum FLOAT NOT NULL)
        ''')

        self.con.execute('''CREATE TABLE IF NOT EXISTS bills (
        bill_id INTEGER PRIMARY KEY,
        bill_name TEXT NOT NULL,
        bill_sum FLOAT NOT NULL,
        bill_status INTEGER NOT NULL)
        ''')

        self.con.execute('''CREATE TABLE IF NOT EXISTS must_costs (
        mc_id INTEGER PRIMARY KEY,
        mc_name TEXT NOT NULL,
        mc_sum FLOAT NOT NULL)
        ''')

        self.con.execute('''CREATE TABLE IF NOT EXISTS costs (
        costs_id INTEGER PRIMARY KEY,
        costs_name TEXT NOT NULL,
        categories_id INTEGER NOT NULL,
        date DATETIME NOT NULL,
        costs_sum FLOAT NOT NULL,
        bills_id INTEGER NOT NULL,
        FOREIGN KEY (bills_id) REFERENCES bills(bill_id),
        FOREIGN KEY (categories_id) REFERENCES categories(cat_id))
        ''')

        self.con.execute('''CREATE TABLE IF NOT EXISTS goals (
        goal_id INTEGER PRIMARY KEY,
        goal_name TEXT NOT NULL,
        goal_sum FLOAT NOT NULL,
        goal_date DATETIME NOT NULL)
        ''')

        self.con.execute('''CREATE TABLE IF NOT EXISTS categories (
        cat_id INTEGER PRIMARY KEY,
        category_name TEXT NOT NULL)
        ''')

        self.con.execute('''CREATE TABLE IF NOT EXISTS income (
        income_id INTEGER PRIMARY KEY,
        date DATETIME NOT NULL,
        salary_id INTEGER,
        income_sum FLOAT NOT NULL,
        bill_id INTEGER, 
        FOREIGN KEY (bill_id) REFERENCES bills(bill_id), 
        FOREIGN KEY (salary_id) REFERENCES salary(salary_id))''')
        self.con.commit()

    def update_table(self):
        self.cur.execute(
            '''PRAGMA foreign_keys=off
            ''')
        self.cur.execute(
            '''CREATE TABLE costs_backups 
            (costs_id INTEGER PRIMARY KEY,
            costs_name TEXT NOT NULL,
            categories_id INTEGER NOT NULL,
            date DATETIME NOT NULL,
            costs_sum FLOAT NOT NULL,
            bills_id INTEGER NOT NULL,
            FOREIGN KEY (bills_id) REFERENCES bills(bill_id),
            FOREIGN KEY (categories_id) REFERENCES categories(cat_id) total FLOAT)
            ''')
        self.cur.execute(
            '''INSERT INTO costs_backups SELECT  
            costs_id,
            costs_name,
            categories_id,
            date DATETIME,
            costs_sum,
            bills_id
            FROM costs
            ''')
        self.cur.execute(
            '''
            DROP TABLE costs
            ''')
        self.cur.execute(
            '''
            ALTER TABLE costs_backups RENAME TO costs
            ''')
        self.cur.execute(
            '''PRAGMA foreign_keys=on
            ''')
        self.con.commit()

    def add_salary(self, salary_name, salary_sum):
        self.cur.execute('''INSERT INTO salary (salary_name, salary_sum) VALUES (?, ?)''', (salary_name,
                                                                                            salary_sum))
        self.con.commit()

    def change_salary(self, salary_id, salary_name, salary_sum: float):
        self.cur.execute('''UPDATE salary SET salary_name=?, salary_sum=? WHERE salary_id=?''', (salary_name,
                                                                                                 salary_sum,
                                                                                                 salary_id))
        self.con.commit()

    def delete_salary(self, salary_id):
        self.cur.execute('''DELETE FROM salary WHERE salary_id=?''', salary_id)
        self.con.commit()

    def select_salary(self, salary_id):
        self.cur.execute('''SELECT * FROM salary WHERE salary_id=?''', salary_id)
        return self.cur.fetchall()[0]

    def add_bill(self, bill_name, bill_sum, bill_status=0):
        self.cur.execute('''INSERT INTO bills (bill_name, bill_sum, bill_status) VALUES (?, ?, ?)''', (bill_name,
                                                                                                       bill_sum,
                                                                                                       bill_status))
        self.con.commit()

    def change_bill(self, bill_id, bill_name, bill_sum: float, bill_status):
        self.cur.execute('''UPDATE bills SET bill_name=?, bill_sum=?, bill_status=? WHERE bill_id=?''', (bill_name,
                                                                                                       bill_sum,
                                                                                                       bill_status,
                                                                                                       bill_id))
        self.con.commit()

    def delete_bill(self, bill_id):
        self.cur.execute('''DELETE FROM bills WHERE bill_id=?''', bill_id)
        self.con.commit()

    def select_bill(self, bill_id):
        self.cur.execute('''SELECT bill_id, bill_name, bill_sum FROM bills WHERE bill_id=?''', bill_id)
        return self.cur.fetchall()[0]

    def add_category(self, category_name):
        self.cur.execute('''INSERT INTO categories (category_name) VALUES (?)''', [category_name])
        self.con.commit()

    def change_category(self, string_id, category_name):
        self.cur.execute('''UPDATE categories SET category_name=? WHERE cat_id=?''', (category_name, string_id,))
        self.con.commit()

    def delete_category(self, string_id):
        self.cur.execute('''DELETE FROM categories WHERE cat_id=?''', string_id)
        self.con.commit()

    def select_categories(self, cat_id):
        self.cur.execute('''SELECT * FROM categories WHERE cat_id=?''', cat_id)
        return self.cur.fetchall()[0]

    def add_must_costs(self, mc_name, mc_sum):
        self.cur.execute('''INSERT INTO must_costs (mc_name, mc_sum) VALUES (?, ?)''', (mc_name, mc_sum))
        self.con.commit()

    def change_must_costs(self, mc_name, mc_sum, mc_id):
        self.cur.execute('''UPDATE must_costs SET mc_name=?, mc_sum=? WHERE mc_id=?''', (mc_name, mc_sum, mc_id))

    def delete_must_costs(self, mc_id):
        self.cur.execute('''DELETE FROM must_costs WHERE mc_id=?''', mc_id)
        self.con.commit()

    def select_mc(self, mc_id):
        self.cur.execute('''SELECT * FROM must_costs WHERE mc_id=?''', mc_id)
        return self.cur.fetchall()[0]

    def add_costs(self, costs_name, categories_id, date, costs_sum, bills_id):
        self.cur.execute(
            '''
            INSERT INTO costs (costs_name, categories_id, date, costs_sum, bills_id) 
            VALUES (?, ?, ?, ?, ?)
            ''', (costs_name, categories_id, date, costs_sum, bills_id))
        self.con.commit()

    def change_costs(self, costs_id, costs_name, categories_id, date, costs_sum, bills_id):
        self.cur.execute(
            '''
            UPDATE costs SET costs_name=?, categories_id=?, date=?, costs_sum=?, bills_id=? WHERE costs_id=?
            ''', (costs_name, categories_id, date, costs_sum, bills_id, costs_id))
        self.con.commit()

    def delete_costs(self, costs_id):
        self.cur.execute('''DELETE FROM costs WHERE costs_id=?''', costs_id)
        self.con.commit()

    def get_string_values_costs(self, string_id):
        self.cur.execute('''SELECT * FROM costs WHERE costs_id={}'''.format(string_id))
        return self.cur.fetchall()[0]

    def get_costs_val(self, treeview):
        self.cur.execute(
            '''
            SELECT costs_id, costs_name, categories.category_name, date, costs_sum, bills.bill_name
            FROM costs 
            JOIN categories ON costs.categories_id=categories.cat_id
            JOIN bills ON costs.bills_id=bills.bill_id
            '''
        )
        [treeview.delete(i) for i in treeview.get_children()]
        [treeview.insert('', '0', values=row) for row in self.cur.fetchall()]

    def add_income(self, date, salary_id, income_sum, bill_id):
        self.cur.execute('''INSERT INTO income (date, salary_id, income_sum, bill_id) Values(?, ?, ?, ?)''',
                         (date, salary_id, income_sum, bill_id))
        self.con.commit()

    def change_income(self, income_id, date, salary_id, income_sum, bill_id):
        self.cur.execute('''UPDATE income SET date=?, salary_id=?, income_sum=?, bill_id=? WHERE income_id=?''',
                         (date, salary_id, income_sum, bill_id, income_id))
        self.con.commit()

    def delete_income(self, income_id):
        self.cur.execute('''DELETE FROM income WHERE income_id=?''', income_id)
        self.con.commit()

    def add_goal(self, name, summ, date):
        self.cur.execute('''INSERT INTO goals (goal_name, goal_sum, goal_date) Values(?, ?, ?)''',
                         (name, summ, date))
        self.con.commit()

    def change_goal(self, name, summ, date, goal_id):
        self.cur.execute('''UPDATE goals SET goal_name=?, goal_sum=?, goal_date=? WHERE goal_id=?''',
                         (name, summ, date, goal_id))
        self.con.commit()

    def delete_goal(self, goal_id):
        self.cur.execute('''DELETE FROM goals WHERE goal_id=?''', goal_id)
        self.con.commit()

    def get_income_val(self, treeview):
        self.cur.execute(
            '''
            SELECT income_id, date, salary.salary_name, income_sum, bills.bill_name
            FROM income 
            JOIN salary ON income.salary_id=salary.salary_id
            JOIN bills ON income.bill_id=bills.bill_id
            '''
        )
        [treeview.delete(i) for i in treeview.get_children()]
        [treeview.insert('', 'end', values=row) for row in self.cur.fetchall()]

    def get_string_values_income(self, string_id):
        self.cur.execute('''SELECT * FROM income WHERE income_id={}'''.format(string_id))
        return self.cur.fetchall()[0]

    def get_values(self, table_name):
        self.cur.execute('''SELECT * FROM {}'''.format(table_name))
        return self.cur.fetchall()

    def show_info(self, treeview, table_name: str):
        self.cur.execute("""SELECT * FROM {}""".format(table_name))
        [treeview.delete(i) for i in treeview.get_children()]
        [treeview.insert('', 'end', values=row) for row in self.cur.fetchall()]

    def show_info_bills(self, treeview):
        self.cur.execute("""SELECT bill_id, bill_name, bill_sum FROM bills""")
        [treeview.delete(i) for i in treeview.get_children()]
        [treeview.insert('', '0', values=row) for row in self.cur.fetchall()]

    def bill_sum_minus(self, values, bill_id):
        self.cur.execute('''UPDATE bills SET bill_sum=(bill_sum-?) WHERE bill_id=?''', (values, bill_id))
        self.con.commit()

    def bill_sum_plus(self, values, bill_id):
        self.cur.execute('''UPDATE bills SET bill_sum=(bill_sum+?) WHERE bill_id=?''', (values, bill_id))
        self.con.commit()

    def select_old_sum_id_costs(self, costs_id):
        self.cur.execute('''SELECT costs_sum, bills_id FROM costs WHERE costs_id=?''', costs_id)
        values = list(self.cur.fetchall()[0])
        return values

    def select_old_sum_id_income(self, income_id):
        self.cur.execute('''SELECT income_sum, bill_id FROM income WHERE income_id=?''', income_id)
        values = list(self.cur.fetchall()[0])
        return values

