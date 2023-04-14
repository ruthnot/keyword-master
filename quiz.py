from db_helper import DBHelper
from compute_priority import ComputePriority


def main():
    db = DBHelper()
    keywords = db.keywords
    keywords_new_priorities = ComputePriority().compute(keywords)
    db.overwrite(keywords_new_priorities)

    sorted_keywords = []
    for keyword_name, keyword_data in keywords.items():
        sorted_keywords.append((keyword_data['priority'], keyword_name, keyword_data))
    sorted_keywords.sort(key=lambda x: x[0])

    idx = 0
    review_count = 1
    while True:
        if idx >= len(sorted_keywords):
            print('Reached the end of database, goodbye!')
            break
        keyword_tuple = sorted_keywords[idx]
        # skip priority 100 or above keywords
        if keyword_tuple[0] >= 100:
            idx += 1
            continue
        kw_type = keyword_tuple[2]['type']
        print(f'{review_count}. "{keyword_tuple[1]}", type[{kw_type}]. Type confidence level: h, m, l')
        user_input = input()

        if user_input == '-q' or user_input == 'exit':
            print('Have a nice day!')
            break
        elif '-t' in user_input:
            new_type = user_input.split('-t')[-1].strip()
            if 'vocab' in new_type:
                new_type = 'vocabulary'
            keyword_tuple[2]['type'] = new_type
            print(f'You updated type: "{new_type}"')
        elif user_input == 'h' or user_input == 'm' or user_input == 'l':
            keyword_tuple[2]['review_history'].append([db.today, user_input])
            idx += 1
            review_count += 1
        else:
            print(f'User input: "{user_input}" not defined, please try again!\n')
    db.overwrite(keywords)


if __name__=='__main__':
    main()