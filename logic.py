import pandas as pd
import sqlite3 as sql
import database as db
import datetime as dt


class MyDataFrame:
    def __init__(self, login):
        self.login = login
        self.db = db.DB(login)
        self.con = sql.connect('{}.db'.format(login))


class SalaryFrame(MyDataFrame):
    def __init__(self, login):
        super().__init__(login)
        self.sf = pd.read_sql ('''SELECT * FROM salary''', self.con, 
                               index_col='salary_id')
        
    def sum_salary(self):
        return self.sf['salary_sum'].sum()


class BillsFrame(MyDataFrame):
    def __init__(self, login):
        super().__init__(login)
        self.bf = pd.read_sql("""SELECT * FROM bills""", self.con, 
                              index_col='bill_id')
    
    def sum_bills(self):
        return self.bf['bill_sum'].sum()
    

class MustCostsFrame(MyDataFrame):
    def __init__(self, login):
        super().__init__(login)
        self.mcf = pd.read_sql('''SELECT * FROM must_costs''', self.con,
                               index_col='mc_id')
    
    def sum_mc(self):
        return self.mcf['mc_sum'].sum()
    
class CostsFrame(MyDataFrame):
    def __init__(self, login):
        super().__init__(login)
        self.now_weak = dt.datetime.today().strftime('%V')
        self.to_day = dt.datetime.today()
        self.start_date_month = (self.to_day - dt.timedelta(days=self.to_day.day))
        self.now_month = self.to_day.month
        self.previous_month = self.now_month - 1
        
        self.cf = pd.read_sql('''SELECT * FROM costs''', self.con,
                               index_col='costs_id')
        
        self.cf['date'] = pd.to_datetime(self.cf['date'], yearfirst=True, 
                                         format='%Y.%m.%d')
        self.frame_month = self.cf[self.cf['date'].dt.month >= self.now_month]
        self.frame_previous_month = self.cf[(self.cf['date'].dt.month >= self.previous_month) &
                                            (self.cf['date'].dt.month < self.now_month)]
    
    def sum_costs_for_bills(self):
        return self.cf.groupby(self.cf['bills_id'], 
                               as_index=False)['costs_sum'].sum()
    
    def filter_weak_sum(self, month='now'):
        if month == 'now':
            df = self.frame_month.groupby([pd.Grouper(key='date', freq='W')])['costs_sum'].sum()
        elif month == 'previous':
            df = self.frame_previous_month.groupby([pd.Grouper(key='date', freq='W')])['costs_sum'].sum()
        else:
            return ValueError
        num_weak = df.index.strftime('%V').tolist()
        df = df.to_frame()
        df['num_weak'] = num_weak
        result_df = pd.DataFrame({'num_weak': num_weak, 'costs_sum': df['costs_sum']})
        self.sum_weakcosts = df['costs_sum'].sum()
        return result_df
    
    def filter_categories_sum(self, month='now'):
        if month == 'now':
            df = self.frame_month.groupby(['categories_id'], as_index=False)['costs_sum'].sum()
        elif month == 'previous':
            df = self.frame_previous_month.groupby(['categories_id'], as_index=False)['costs_sum'].sum()
        else:
            return ValueError
        self.sum_catcosts = df['costs_sum'].sum()
        return df
    
    def how_costs_in_month(self):
        costs_in_weak = self.filter_weak_sum()
        month_costs = costs_in_weak['costs_sum'].sum()
        weak_costs = costs_in_weak[costs_in_weak['num_weak'] == self.now_weak]['costs_sum'].sum()
        result = {'month': month_costs, 'weak': weak_costs}
        return result
        

class MainParametres(SalaryFrame, MustCostsFrame):
    def __init__(self, login):
        super().__init__(login)
        self.costs_frame = CostsFrame(login)
        self.bills_frame = pd.read_sql('''SELECT 
                                       bill_id, 
                                       bill_name, 
                                       bill_sum FROM bills 
                                       WHERE bill_status=0''', 
                                       self.con, index_col='bill_id')
        self.today = dt.datetime.today()
        self.salary_sum = self.sum_salary()
        self.must_cost_sum = self.sum_mc()
        self.table_df = pd.DataFrame(columns=['param', 
                                         'weak', 
                                         'month', 
                                         'quarter', 
                                         'half_year'
                                         ])
        to_month = dt.datetime.today().strftime('%Y-%m')
        self.first_weak_in_month = dt.datetime.strptime('{}-01'.format(to_month), 
                                                   '%Y-%m-%d').strftime('%V')
        self.last_weak_in_month = dt.datetime.strptime('{}-28'.format(to_month),
                                                  '%Y-%m-%d').strftime('%V')
        self.now_weak = dt.datetime.today().strftime('%V')
    
    def how_money_month_weak_plan(self):
        weeks_in_month = self.how_weaks_in_month()[0]
        month = self.salary_sum - self.must_cost_sum
        weak = month / weeks_in_month
        result = [month, weak]
        return result
    
    def how_costs_in_month(self):
        costs_in_weak = self.costs_frame.filter_weak_sum()
        all_costs = costs_in_weak.sum()
        return self.bills_frame['bill_sum'].sum()
    
    def how_weaks_in_month(self):
        weaks = int(self.last_weak_in_month) - int(self.first_weak_in_month)
        now_weak_number = int(self.now_weak) - int(self.first_weak_in_month)
        result = [weaks, now_weak_number]
        return result
    
    def how_money_i_have_weak(self):
        money_for_month = self.bills_frame['bill_sum'].sum()
        count = int(self.last_weak_in_month) - int(self.now_weak)
        result = money_for_month / count
        return result
    

class ParamTable(MyDataFrame):
    def __init__(self, login):
        super().__init__(login)
        self.param = MainParametres(login)
        self.cost_frame = CostsFrame(login)
        self.df_costs_weak = self.cost_frame.filter_weak_sum()
        self.now_weak = self.param.how_weaks_in_month()[1]
        self.optimal_month_sum = self.param.how_money_month_weak_plan()[0]
        self.optimal_weak_sum = self.param.how_money_month_weak_plan()[1]
        self.fact_month_sum = self.cost_frame.how_costs_in_month()['month']
        self.fact_weak_sum = self.cost_frame.how_costs_in_month()['weak']
        self.money_sum_weak = 0
        self. money_sum_month = 0
        self.values_table = self.create_table()
    
    def create_table(self):
        data = {'name_param': ['Оптимальная сумма трат:', 
                               'Фактическая сумма трат:', 
                               'Остаток:'], 
                'weak': [self.optimal_weak_sum, 
                         self.fact_weak_sum,
                         self.money_sum_weak], 
                'month': [self.optimal_month_sum, 
                          self.fact_month_sum,
                          self.money_sum_month]}
        self.table_df = pd.DataFrame(data=data)
        return self.table_df.values.tolist()


