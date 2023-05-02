import math
import datetime as dt
import random
import yaml

with open('config.yml', 'r') as file:
    configs = yaml.safe_load(file)

RATE_WEIGHT = configs['rate_weight']
CALM_WINDOW = configs['calm_window']
RANDOM_BOMBING = configs['random_bombing']
RANDOM_WEIGHT = configs['random_weight']
NEW_WORD_WEIGHT = configs['new_word_weight']


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

            # Random weight: toss a coin and decide the random weight
            # This is to avoid 2 similar keywords always stick together
            coin2 = random.randint(0, len(RANDOM_WEIGHT)-1)
            random_weight = RANDOM_WEIGHT[coin2]
            val['priority'] *= random_weight

            # Promote new words:
            # Words passed calm window but hasn't been reviewed yet
            if len(val['review_history']) <= 1:
                val['priority'] *= NEW_WORD_WEIGHT

        return keywords

    def algorithm(self, days):
        # Ebbinghaus Forgetting Curve
        c = 1.25
        k = 1.84
        t = days * 24 * 60
        b = 100 * k / (math.log(t, 10)**c + k)
        return b



