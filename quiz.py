from db_helper import DBHelper
from compute_priority import ComputePriority


def main():
    db = DBHelper()
    keywords = db.keywords
    keywords_new_priorities = ComputePriority().compute(keywords)
    db.overwrite(keywords_new_priorities)

    sorted_keywords = []
    for keyword_name, keyword_data in keywords.items():
        sorted_keywords.append((keyword_name, keyword_data['priority']))
    sorted_keywords.sort(key=lambda x: x[1])

    idx = 0
    review_count = 1
    while True:
        if idx >= len(sorted_keywords):
            print('Reached the end of database, goodbye!')
            break
        keyword_pair = sorted_keywords[idx]
        # skip priority 100 or above keywords
        if keyword_pair[1] >= 100:
            idx += 1
            continue
        print(f'{review_count}. "{keyword_pair[0]}", please type your confidence level: h, m, l')
        user_input = input()

        if user_input == 'exit':
            print('Have a nice day!')
            break
        elif user_input == 'h' or user_input == 'm' or user_input == 'l':
            keywords[keyword_pair[0]]['review_history'].append([db.today, user_input])
            idx += 1
            review_count += 1
        else:
            print(f'User input: "{user_input}" not defined, please try again!\n')
    db.overwrite(keywords)


if __name__=='__main__':
    main()