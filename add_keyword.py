from db_helper import DBHelper


def main():
    db = DBHelper()
    today = db.today
    keywords = db.keywords
    while True:
        print('Please type your keyword and type:')
        user_input = input()
        if user_input == 'exit':
            print('Have a nice day!')
            break
        keyword, type, *others = user_input.split(' ')
        if keyword in keywords:
            print('Keyword already existed!')
            continue
        keywords[keyword] = {'date_added': today, 'review_history': [[today, 'h']], 'type': type, 'priority': 100.}

        print(f'Added keyword: {keyword} type: {type}!\n')
    db.overwrite(keywords)

if __name__=='__main__':
    main()