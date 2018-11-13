from flask import Flask, render_template, stream_with_context, request, Response, session, Session, json
import copy
from jinja2 import Environment, PackageLoader, select_autoescape
import time
from dropboxdb import DropBoxDB
import thread
import threading
db_obj = DropBoxDB("praveen","S@gem0de")
#create the application.
app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
# Session(app)

@app.route('/delete_file/<id>/')
def delete_file(id = None):
    print("In delete file{0}".format(id))
    db_obj.delete_file(id)
    return

@app.route('/delete_folder/<id>/')
def delete_folder(id = None):
    print("In delete folder {0}".format(id))
    db_obj.delete_folder(id)
    return

@app.route('/move_file/', methods = ['GET', 'POST'])
def move():
    if(request.method == "POST"):
        print("In move file")
        src_id = request.form["src_id"]
        dest_id = request.form["dest_id"]
        print("In move folder src:{0} dest{1}".format(src_id,dest_id))
        db_obj.move_file(src_id,dest_id)
        return

@app.route('/get_folder_list/<id>/', methods = ['GET', 'POST'])
def get_folder_entries(id = None):
    print("In get folder list {0}".format(id))
    files = db_obj.get_folder_entries(id)
    return files["folders"]

@app.route('/get_nav_context/<id>/', methods = ['GET', 'POST'])
def get_nav_context(id = None):
    print("In get nav list {0}".format(id))
    lock.acquire()
    files = db_obj.get_navigation_context(int(id))
    lock.release()
    return json.dumps(files)


@app.route('/view/')
@app.route('/view/<id>/')
def view(id=None):
    session['id'] = 1
    if(id == None):
        lock.acquire()
        files = db_obj.get_folder_entries(db_obj.get_root_path_id(session["id"]))
        lock.release()
        print(files)
        return Response(render_template('for-if-showall.html', data=files))
    else:
        lock.acquire()
        files = db_obj.get_folder_entries(int(id))
        lock.release()
        print(files)
        return json.dumps(files)


if __name__ == '__main__':
    lock=thread.allocate_lock()
    app.run(debug=True)
