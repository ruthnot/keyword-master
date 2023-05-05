from db_helper import DBHelper


def main():
    db = DBHelper()
    today = db.today
    keywords = db.keywords

    while True:
        print('Please type your keyword:')
        user_input = input()
        if user_input == '-q' or user_input == 'exit':
            print('Have a nice day!')
            break
        if '-t' in user_input:
            keyword = user_input.split('-t')[0].strip()
            type = user_input.split('-t')[1].strip()
        else:
            keyword = user_input.strip()
            type = None
        db.add(keyword, type)

        # if len(keyword) == 0:
        #     print('Error: Empty keyword, input again!\n')
        #     continue
        # if keyword in keywords:
        #     print('Warning: Keyword already existed!\n')
        #     continue
        # keywords[keyword] = {'date_added': today, 'review_history': [[today, 'm']], 'type': type, 'priority': 100.}
        #
        # print(f'Added keyword: "{keyword}", with type: "{type}"!\n')
    db.overwrite(keywords)


if __name__=='__main__':
    main()