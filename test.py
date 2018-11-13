from dropboxdb import DropBoxDB

db_obj = DropBoxDB("ateam","password")


# user_details = dict()
# user_details["email"] = "tar@gmail.com"
# user_details["name"] = "Tarun"
# user_details["password"] = "hello123"
# db_obj.create_user(user_details)
# db_obj.modify_file_permission(1, 'private')

# file_details = dict()
# file_details["name"] = "daenaryfile123.sha"
# file_details["path"] = 1
# file_details["size"] = 98
# file_details["owner"] = 2
# file_details["permission"] = 'private'
# db_obj.create_file(file_details)

# fe = db_obj.search_files(1, "file1")
# print str(fe)

res = db_obj.get_navigation_context(4)
print str(res)