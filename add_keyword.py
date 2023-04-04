from db_helper import DBHelper


def main():
    db = DBHelper()
    today = db.today
    keywords = db.keywords

    while True:
        print('Please type your keyword:')
        user_input = input()
        if user_input == 'exit':
            print('Have a nice day!')
            break
        # keyword, type, *others = user_input.split(' ')
        keyword = user_input.strip(' ')  # prevent space at beginning or end
        if len(keyword) == 0:
            print('Error: Empty keyword, input again!\n')
            continue
        if keyword in keywords:
            print('Warning: Keyword already existed!\n')
            continue
        keywords[keyword] = {'date_added': today, 'review_history': [[today, 'm']], 'type': None, 'priority': 100.}

        print(f'Added keyword: "{keyword}"!\n')
    db.overwrite(keywords)


if __name__=='__main__':
    main()