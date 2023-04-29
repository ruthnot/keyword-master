import json
import datetime as dt

PATH = 'keyword.json'
BACKUP_PATH = 'keyword_backup.json'


class DBHelper(object):
    def __init__(self):
        self.keywords = json.load(open(PATH))

    # @property
    # def keywords(self):
    #     f = open(PATH)
    #     return json.load(f)

    @property
    def today(self):
        today_date = dt.datetime.today().date()
        return f'{today_date.year}-{today_date.month}-{today_date.day}'

    def add(self, keyword, type=None):
        if len(keyword) == 0:
            print('Error: Empty keyword, input again!\n')
        elif keyword in self.keywords:
            print('Warning: Keyword already existed!\n')
        elif keyword in self.keywords:
            print(f'Keyword exsited!')
        else:
            self.keywords[keyword] = {'date_added': self.today, 'review_history': [[self.today, 'm']], 'type': type, 'priority': 100.}
            print(f'Added keyword: "{keyword}", with type: "{type}"!\n')

    def overwrite(self, data):
        # Always backup first
        self.backup()
        with open(PATH, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def backup(self):
        with open(PATH, "r") as f_from:
            with open(BACKUP_PATH, "w") as f_to:
                f_to.write(f_from .read())

    def print(self):
        for key, val in self.keywords.items():
            print(f'{key}: {val}')

    def total_count(self):
        count = len(self.keywords)
        print(count)
        return count

    def review_freq(self):
        freq_count = {}
        freq_perc = {}
        total_count = self.total_count()
        for kw, val in self.keywords.items():
            if val['priority'] == 100:   # means it's in calm window
                freq_count[-1] = freq_count.get(-1, 0) + 1
                continue
            freq = len(val['review_history']) - 1
            freq_count[freq] = freq_count.get(freq, 0) + 1
        for freq, count in freq_count.items():
            perc = round(count / total_count * 100, 2)
            freq_perc[freq] = f'{perc}%'

        sorted_perc = dict(sorted(freq_perc.items(), key=lambda x: x[0]))
        sorted_count = dict(sorted(freq_count.items(), key=lambda x: x[0]))
        print(sorted_perc)
        print(sorted_count)
        return sorted_perc
