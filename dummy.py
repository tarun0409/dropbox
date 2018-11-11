from flask import Flask, render_template, stream_with_context, request, Response
import copy
from jinja2 import Environment, PackageLoader, select_autoescape
import time
from dropboxdb import DropBoxDB

db_obj = DropBoxDB("praveen","S@gem0de")

#create the application.
app = Flask(__name__)

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
        dest_path = request.form["dest_path"]
        print("In move folder src:{0} dest{1}".format(src_id,dest_path))
        db_obj.move_file(src_id,dest_path)
        return


@app.route('/view/')
@app.route('/view/<id>/')
def view(id=None):
    if(id == None):
        files = db_obj.get_folder_entries(5)
        return Response(render_template('for-if-showall.html', data=files))
    else:
        files = db_obj.get_folder_entries(id)
        return Response(render_template('for-if-showall.html', data=files))


if __name__ == '__main__':

    app.run(debug=True)
