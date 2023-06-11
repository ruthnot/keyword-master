import random
from db_helper import DBHelper
from compute_priority import ComputePriority

TOPIC = "ALL"
SHUFFLE = True


def main():
    db = DBHelper()
    if TOPIC == "ALL":
        keywords = db.keywords
    else:
        keywords = db.get_keywords_subset(TOPIC)
    keywords_new_priorities = ComputePriority().compute(keywords)
    db.update(keywords_new_priorities)

    sorted_keywords = []
    for keyword_name, keyword_data in keywords.items():
        sorted_keywords.append([keyword_data['priority'], keyword_name, keyword_data])

    if SHUFFLE:
        random.shuffle(sorted_keywords)
    else:
        sorted_keywords.sort(key=lambda x: x[0])

    idx = 0
    review_count = 1
    total_count = len(sorted_keywords)
    while True:
        if idx >= len(sorted_keywords):
            print('Reached the end of database, goodbye!')
            break
        keyword_tuple = sorted_keywords[idx]
        # skip priority 100 or above keywords (only when topic is all)
        if keyword_tuple[0] >= 100 and TOPIC == "ALL":
            idx += 1
            continue
        kw_type = keyword_tuple[2]['type']
        print(f'{review_count}/{total_count}. "{keyword_tuple[1]}", [type: {kw_type}]. Type confidence level: h, m, l')
        user_input = input()

        if user_input == '-q' or user_input == 'exit':
            print('Have a nice day!')
            break
        elif '-delete' in user_input:
            del keywords[keyword_tuple[1]]
            idx += 1
            continue
        elif '-e' in user_input:
            new_name = user_input.split('-e')[-1].strip()
            old_name = keyword_tuple[1]
            keywords[new_name] = keywords.pop(old_name)
            keyword_tuple[1] = new_name
            print(f'Change name to {new_name}!')
        elif '-t' in user_input and '-a' not in user_input:
            new_type = user_input.split('-t')[-1].strip()
            keyword_tuple[2]['type'] = DBHelper.type_convert(new_type)
            print(f'You updated type: "{new_type}"')
        elif '-a' in user_input:
            word_idx = user_input.index('-a') + 2
            type_idx = None
            if '-t' in user_input:
                type_idx = user_input.index('-t')
            if type_idx is None:
                new_word = user_input[word_idx:].strip()
                new_type = None
            else:
                new_word = user_input[word_idx:type_idx].strip()
                new_type = user_input[type_idx+2:].strip()
            db.add(new_word, new_type)
        elif user_input == 'h' or user_input == 'm' or user_input == 'l':
            keyword_tuple[2]['review_history'].append([db.today, user_input])
            idx += 1
            review_count += 1
        else:
            print(f'User input: "{user_input}" not defined, please try again!\n')
    db.update(keywords)


if __name__=='__main__':
    main()