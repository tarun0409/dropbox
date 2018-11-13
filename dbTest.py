from dropboxdb import DropBoxDB
import copy

db_obj = DropBoxDB("praveen","S@gem0de")
#
# user_details = dict()
# user_details["email"] = "pra@gmail.com"
# user_details["name"] = "praveen"
# user_details["password"] = "hello123"
# db_obj.create_user(user_details)

# folder_details = {}
#
# folder_details["name"] = "dir2"
# folder_details["path"] = 9
# folder_details["owner"] = 1
# db_obj.create_folder(folder_details)

#
file = {}
file["name"] = "dummy22.jpg"
file["path"] = 9
file["size"] = 56
file["owner"] = 1
file["permission"] = "public"

db_obj.create_file(file)

# file1 = copy.deepcopy(file)
# file1["name"] = "dummy2.jpg"

# db_obj.create_file(file1)