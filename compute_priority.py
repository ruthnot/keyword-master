import math
import datetime as dt
import json

RATE_WEIGHT = {'h': 1.5, 'm': 1.0, 'l': 0.5}


class ComputePriority(object):
    def __init__(self):
        self.today = dt.datetime.today().date()

    def compute(self, keywords):
        assert isinstance(keywords, dict)
        for key, val in keywords.items():
            last_review = val['review_history'][-1]
            last_date, last_rate = last_review[0], last_review[1]
            year, month, day = last_date.split('-')
            delta_days = (self.today - dt.date(int(year), int(month), int(day))).days
            if delta_days <= 0:
                continue
            priority = self.algorithm(delta_days)
            priority *= RATE_WEIGHT[last_rate]
            priority = round(min(100.0, priority), 1)
            val['priority'] = priority
        return keywords

    def algorithm(self, days):
        # Ebbinghaus Forgetting Curve
        c = 1.25
        k = 1.84
        t = days * 24 * 60
        b = 100 * k / (math.log(t, 10)**c + k)
        return b



