from dropboxdb import DropBoxDB

db_obj = DropBoxDB("ateam","password")


# user_details = dict()
# user_details["email"] = "chit@gmail.com"
# user_details["name"] = "Chittr"
# user_details["password"] = "iiit123"
# db_obj.create_user(user_details)

user_details = dict()
user_details["email"] = "chit@gmail.com"
user_details["old_password"] = "iiit123"
user_details["new_password"] = "hello123"

print db_obj.get_root_path_id(1)