from dropboxdb import DropBoxDB

db_obj = DropBoxDB("ateam","password")


user_details = dict()
user_details["email"] = "tar@gmail.com"
user_details["name"] = "Tarun"
user_details["password"] = "hello123"
db_obj.create_user(user_details)