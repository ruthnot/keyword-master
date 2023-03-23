import json
import datetime as dt
import os

PATH = 'keyword.json'
BACKUP_PATH = 'keyword_backup.json'

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
        # Always backup first
        self.backup()
        with open(PATH, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def backup(self):
        with open(PATH, "r") as f_from:
            with open(BACKUP_PATH, "w") as f_to:
                f_to.write(f_from .read())


if __name__=='__main__':
    x = DBHelper()
    b = x.keywords