import math
import datetime as dt
import json


class ComputePriority(object):
    def __init__(self):
        self.today = dt.datetime.today().date()

    def compute(self, keywords):
        assert isinstance(keywords, dict)
        for key, val in keywords.items():
            last_review = val['review_history'][-1]
            last_date, last_conf = last_review[0], last_review[1]
            year, month, day = last_date.split('-')
            delta_days = (self.today - dt.date(int(year), int(month), int(day))).days
            if delta_days <= 0:
                continue
            priority = self.algorithm(delta_days)
            val['priority'] = priority

    def algorithm(self, days):
        # Ebbinghaus Forgetting Curve
        c = 1.25
        k = 1.84
        t = days * 24 * 60
        b = 100 * k / (math.log(t, 10)**c + k)
        return round(b, 1)

if __name__=='__main__':
    x = ComputePriority()

