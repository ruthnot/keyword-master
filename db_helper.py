import datetime
import json
import datetime as dt
import yaml

PATH = 'keyword.json'
BACKUP_PATH = 'keyword_backup.json'
with open('configs/priority.yml', 'r') as file:
    CONFIGS = yaml.safe_load(file)
with open('configs/glossary.yml', 'r') as file2:
    GLOSSARY = yaml.safe_load(file2)


class DBHelper(object):
    def __init__(self):
        self.keywords = json.load(open(PATH))

    @property
    def today(self):
        today_date = dt.datetime.today().date()
        return f'{today_date.year}-{today_date.month}-{today_date.day}'

    @staticmethod
    def type_convert(raw_type):
        if raw_type in GLOSSARY:
            return GLOSSARY[raw_type]
        return raw_type

    def get_keywords_subset(self, type):
        if type in GLOSSARY:
            type = GLOSSARY[type]
        print(type)
        subset = dict()
        for keyword, value in self.keywords.items():
            if type == value['type']:
                subset[keyword] = value
        return subset

    def add(self, keyword, type=None):
        if len(keyword) == 0:
            print(f'Error: Empty keyword, input again!\n')
        elif keyword in self.keywords:
            print(f'Warning: "{keyword}" already existed!\n')
        else:
            convert_type = self.type_convert(type)
            self.keywords[keyword] = {'date_added': self.today,
                                      'review_history': [[self.today, 'm']],
                                      'type': convert_type,
                                      'priority': 100.}
            print(f'Added keyword: "{keyword}", with type: "{convert_type}"!\n')

    def update(self, new_keywords):
        for key, val in new_keywords.items():
            self.keywords[key] = val
        print('Database updated!')

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

    def type_count(self):
        count = dict()
        for word, val in self.keywords.items():
            type = val['type']
            count[type] = count.get(type, 0) + 1
        sorted_count = dict(sorted(count.items(), key=lambda item: item[1], reverse=True))
        for k, v in sorted_count.items():
            print(k, v)

    def date_to_datetimedate(self, date):
        assert isinstance(date, str)
        info = date.split('-')
        year, month, day = int(info[0]), int(info[1]), int(info[2])
        datetimedate = datetime.date(year, month, day)
        return datetimedate

    def review_freq(self):
        freq_count = {}
        freq_perc = {}
        total_count = self.total_count()
        for kw, val in self.keywords.items():
            date_added = self.date_to_datetimedate(val['date_added'])
            duration = (self.date_to_datetimedate(self.today) - date_added).days
            calm_window = CONFIGS['calm_window']
            if duration <= calm_window:
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
