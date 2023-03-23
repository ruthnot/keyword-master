import json
import datetime as dt
import os

PATH = 'keyword.json'

class DBHelper(object):
    def __init__(self):
        pass

    @property
    def keywords(self):
        f = open(PATH)
        return json.load(f)

    @property
    def today(self):
        today_date = dt.datetime.today().date()
        return f'{today_date.year}-{today_date.month}-{today_date.day}'

    def overwrite(self, data):
        with open(PATH, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

if __name__=='__main__':
    x = DBHelper()
    b = x.keywords