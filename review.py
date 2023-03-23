from db_helper import DBHelper
from compute_priority import ComputePriority

def main():
    db = DBHelper()
    keywords = db.keywords
    keywords_new_priorities = ComputePriority().compute(keywords)
    db.overwrite(keywords_new_priorities)


if __name__=='__main__':
    main()