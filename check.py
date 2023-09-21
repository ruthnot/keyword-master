from db_helper import DBHelper

if __name__=='__main__':
    obj = DBHelper()
    obj.total_count()
    obj.review_freq()
    obj.type_count()