import math
import datetime as dt
import random

RATE_WEIGHT = {'h': 1.5, 'm': 1.0, 'l': 0.5}
CALM_WINDOW = 5
RANDOM_BOMBING = {'prob': 0.2, 'weight': 0.5}


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

            # Calm Window: for newly reviewed/created keywords
            if delta_days <= CALM_WINDOW:
                val['priority'] = 100
                continue

            # Base Priority: is based on algorithm function
            base_priority = self.algorithm(delta_days)

            # Review Adjusted Priority: is based on latest review
            adjusted_priority = base_priority * RATE_WEIGHT[last_rate]
            adjusted_priority = round(min(100.0, adjusted_priority), 1)
            val['priority'] = adjusted_priority

            # Random bombing: toss a coin and decide if random bomb
            coin = random.random()
            if coin < RANDOM_BOMBING['prob']:
                val['priority'] *= RANDOM_BOMBING['weight']

        return keywords

    def algorithm(self, days):
        # Ebbinghaus Forgetting Curve
        c = 1.25
        k = 1.84
        t = days * 24 * 60
        b = 100 * k / (math.log(t, 10)**c + k)
        return b



