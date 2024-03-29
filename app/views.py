import os
from flask import render_template,request,flash,redirect,url_for,session,Response,send_from_directory,send_file
from app import app 
from dropboxdb import DropBoxDB
from flask import Flask, render_template, stream_with_context, request, Response, session, Session, json
import copy
from jinja2 import Environment, PackageLoader, select_autoescape
import time
from dropboxdb import DropBoxDB
import thread
import threading
#DropBoxDB
#import dropboxdb
#127.0.0.1 localhost
# lock=thread.allocate_lock()
#db_obj = DropBoxDB("praveen","S@gem0de")
# db_obj = DropBoxDB("praveen","S@gem0de")
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
@app.before_request
def require_login():
    allowed_routes = ['login' , 'register']
    if request.endpoint not in allowed_routes and 'email' not in session:
        return redirect(url_for('login'))

@app.errorhandler(404) 
def not_found(e): 
  return render_template("404.html")

@app.route('/permission/',methods=['GET'])
def change_permission():
    file_id = int(request.args.get("file_id"))
    perm = request.args.get("new_permission")
    db_obj = DropBoxDB("praveen","S@gem0de")
    db_obj.modify_file_permission(file_id, perm)
    return "dummy"

@app.route('/search/', methods = ['GET'])
def search_files():
    s_string = request.args.get("search_string")
    db_obj = DropBoxDB("praveen","S@gem0de")
    search_list = db_obj.search_files(session['id'], s_string)
    files = dict()
    files["files"] = search_list
    files["folders"] = list()
    print(files)
    return json.dumps(files)

@app.route('/modify_permission/<id>', methods = ['GET'])
def modifyPermission(id=None):
    db_obj = DropBoxDB("praveen","S@gem0de")



@app.route('/used_space', methods=['GET'])
def get_file_size():
    db_obj = DropBoxDB("praveen","S@gem0de")
    file_size = db_obj.get_used_space(session['id'])
    print("file size is ",file_size)
    return str(file_size)


@app.route('/delete_file/<id>/')
def delete_file(id = None):
    db_obj = DropBoxDB("praveen","S@gem0de")
    print("In delete file{0}".format(id))
    print("Getting file path in delete file {0}".format(db_obj.get_file_path(id)))
    target = "/".join([APP_ROOT,"uploaded"])
    target = "/".join([target,session['email']])
    target = "/".join([target,db_obj.get_file_path(id)])
    print("Deleting file: {0}".format(target))
    db_obj.delete_file(id)
    os.remove(target)
    return "Dsadsadas"

def deltree(target):
    print("deltree", target)
    for d in os.listdir(target):
        try:
            deltree(target + '/' + d)
        except OSError:
            os.remove(target + '/' + d)

    os.rmdir(target)


@app.route('/delete_folder/<id>/')
def delete_folder(id = None):
    db_obj = DropBoxDB("praveen","S@gem0de")
    print("In delete folder {0}".format(id))
    target = "/".join([APP_ROOT,"uploaded"])
    target = "/".join([target,session['email']])
    print("In delte folder path: ".format(db_obj.get_folder_path(id)))
    target = "/".join([target,db_obj.get_folder_path(id)])
    db_obj.delete_folder(id)
    deltree(target)
    return "Dsadsadas"

@app.route('/move_file/', methods = ['GET', 'POST'])
def move():
    if(request.method == "POST"):
        db_obj = DropBoxDB("praveen","S@gem0de")
        print("In move file")
        src_id = request.form["src_id"]
        dest_id = request.form["dest_id"]
        print("In move folder src:{0} dest{1}".format(src_id,dest_id))
        src_path = db_obj.get_file_path(src_id)
        print("src id ",src_path)
        dest_path = db_obj.get_folder_path(dest_id)
        print("destn path ",dest_path)
        target = "/".join([APP_ROOT,"uploaded"])
        target = "/".join([target,session['email']])
        full_src_path = "".join([target,src_path])
        full_dest_path = "".join([target,dest_path])
        print("full src path:",full_src_path )
        f_name = full_src_path.split('/')
        x = f_name[len(f_name)-1]
        print(x)
        full_dest_path = "/".join([full_dest_path,x])
        print("full destn path:",full_dest_path)
        os.rename(full_src_path,full_dest_path)
        db_obj.move_file(src_id,dest_id)
        return "dsadsadsa"

@app.route('/get_folder_list/<id>/', methods = ['GET', 'POST'])
def get_folder_entries(id = None):
    db_obj = DropBoxDB("praveen","S@gem0de")
    print("In get folder list {0}".format(id))
    files = db_obj.get_folder_entries(id)
    return files["folders"]

@app.route('/get_nav_context/<id>/', methods = ['GET', 'POST'])
def get_nav_context(id = None):
    db_obj = DropBoxDB("praveen","S@gem0de")
    print("In get nav list {0}".format(id))
    # lock.acquire()
    files = db_obj.get_navigation_context(int(id))
    # lock.release()
    return json.dumps(files)


@app.route('/')
@app.route('/view/')
@app.route('/view/<id>/')
def view(id=None):
    #session['id'] = 1
    print("before accessing session print")
    print(session['id'])
    print("In view, id= {0}".format(id))
    if(id == None):
        # lock.acquire()
        db_obj = DropBoxDB("praveen","S@gem0de")
        files = db_obj.get_folder_entries(db_obj.get_root_path_id(int(session['id'])))
        # lock.release()
        print(files)
        return Response(render_template('homePage.html', data=files))
    else:
        # lock.acquire()
        db_obj = DropBoxDB("praveen","S@gem0de")
        files = db_obj.get_folder_entries(int(id))
        # lock.release()
        # print(files)
        return json.dumps(files)


@app.route("/homePage/")
def homePage():
    return render_template('homePage.html')

@app.route('/download/', methods = ['GET', 'POST'])
def download():
    db_obj = DropBoxDB("praveen","S@gem0de")
    if(request.method == "POST"):
    #if(True):
        print("In dload file")
        f_name = request.form["f_name"]
        #return f_name
        file_path = db_obj.get_file_path(int(f_name))
        print("fp is ",file_path)
        target = "/".join([APP_ROOT,"uploaded"])
        dest_path = request.form["dest_path"]
        print("In download: " + dest_path)

        if dest_path.find("@") != -1:
            print("dsadsadsadsa")
            target = "/".join([target,dest_path])
        else:
            target = "/".join([target,session['email']])
        final_path = "".join([target,file_path])
        

        # print("received dest_path ",dest_path)
        # full_path = ""
        # if(dest_path!=""):
        #     full_path = db_obj.get_folder_path(int(dest_path))
        # print("after query completes ")
        # #f_name = request.args.get('f_name')
        # print("please dload ",f_name," from ",full_path)
        # print("app root is ",APP_ROOT)
        # target = "/".join([APP_ROOT,"uploaded"])
        
        
        # print(target)
        # target = "/".join([target,session['email']])
        # # if(full_path!="/"):
        # target = "".join([target,full_path])
        # final_path = "/".join([target,f_name])
        
        print "For download: ",final_path
        #return final_path
        try:
            return send_file(final_path , as_attachment=True)
        except Exception as e:
            print e 
            #send_from_directory(directory=target, filename=f_name)
        #print("In move folder src:{0} dest{1}".format(src_id,dest_id))
    return "dummy val"

@app.route("/upload", methods=['GET','POST'])
def upload():
    db_obj = DropBoxDB("praveen","S@gem0de")
    print("app root is ",APP_ROOT)
    target = "/".join([APP_ROOT,"uploaded"])
    #target = APP_ROOT
    target = "/".join([target,session['email']])
    #path here
    print("In python recieved path = " + str(request.form["pathID"]))
    received_pathid = request.form["pathID"]
    full_path = ""
    path_for_file_in_db = received_pathid
    if(received_pathid ==""):
        path_for_file_in_db =1
        print("received_pathid is None")    
    if(received_pathid !=""):
        print("received_pathid is not None") 
        print(received_pathid)   
        print("In python recieved path id = " + str(db_obj.get_folder_path(request.form["pathID"])))
        full_path = db_obj.get_folder_path(request.form["pathID"])
    target = "".join([target,full_path])
    #formkdir = "-p "+target
    print(os.path.isdir(session['email']))
    if (not os.path.isdir(target)):
        os.makedirs(target)
    for file in request.files.getlist("file"):
        #print(file)
        filename = file.filename
        destn = "/".join([target,filename])
        file.save(destn)
        file_length = os.stat(destn).st_size
        print("file len is",file_length)
        file_details = dict()
        file_details["name"] = filename
        file_details["path"] = path_for_file_in_db
        print("for uploading ")
        print(path_for_file_in_db)
        file_details["size"] = file_length
        owner_id = db_obj.get_user_id(session['email'])
        file_details["owner"] = owner_id
        file_details["permission"] = "private"
        db_obj.create_file(file_details)
        #return "success"
        return redirect(url_for('view'))
        #return view()
    #return render_template('upload.html')
    return "dummy value"

@app.route("/about")
def about():
    return render_template('about.html')


@app.route("/changepassword/",methods=['GET','POST'])
def changepassword():
    db_obj = DropBoxDB("praveen","S@gem0de")
    user_details = dict()
    user_details["email"] = session['email']
    
    user_details["old_password"] = request.form['oldpassword']
    print user_details["old_password"]
    user_details["new_password"] = request.form['newpassword']
    
    db_obj.modify_password(user_details)
    print("password changed successfully")
    return "Dsadsa"


@app.route("/createFolder/",methods=['GET','POST'])
def createFolder():
    db_obj = DropBoxDB("praveen","S@gem0de")
    folder_details = dict()
    folder_details['name'] = request.form['foldername']
    print folder_details['name']
    folder_details["path"] = request.form['pathID']
    print("In create folder, path = {0}".format(folder_details["path"]))
    folder_path = db_obj.get_folder_path(folder_details["path"])
    target = "/".join([APP_ROOT,"uploaded"])
    target = "/".join([target,session['email']])
    target = "/".join([target,folder_path])
    target = "/".join([target,folder_details['name']])
    print("target for folder create ",target)
    if (not os.path.isdir(target)):
        os.makedirs(target)
    owner_id = db_obj.get_user_id(session['email'])
    print(owner_id)
    folder_details["owner"] = owner_id
    db_obj.create_folder(folder_details)
    print("succesfully created folder")
    return "ousdaiudsy"

@app.route("/get_root_path/",methods=['GET','POST'])
def getRootPath():
    db_obj = DropBoxDB("praveen","S@gem0de")
    print("In get root path, returning: " + str(db_obj.get_root_path_id(session["id"])))
    return json.dumps(db_obj.get_root_path_id(session["id"]))

@app.route("/register", methods=['GET','POST'])
def register():
    db_obj = DropBoxDB("praveen","S@gem0de")
    error=''
    try:
        if(request.method == "POST"):
            print("in register")
            print("in register 1")           
            to_register_email = request.form["email"]
            print("in register 2")
            print(to_register_email)
            to_register_pwd = request.form['password']
            print("in register 3")
            print(to_register_pwd)
            to_register_name = request.form['name']
            print("in register 4")
            user_details = dict()
           
            
            print(to_register_name)
            user_details["email"] = to_register_email
            user_details["name"] = to_register_name
            user_details["password"] = to_register_pwd
            db_obj.create_user(user_details)
            print("Before flash")
            flash(to_register_email)
            flash(to_register_name)
            print("Create user successful")
            return redirect(url_for('login'))
            # return Response(render_template('login.html',title='login',fromreg="user registered successfully"))
            

    except Exception as e:
        print("Exception!")
        print(e)
        # flash(e)
        return render_template('register.html',title='register',error=error)

    #return render_template('login.html',title='login',error=error)
    
    return render_template('register.html',title='register',error=error)
    


@app.route("/login",methods=['GET','POST'])
def login():
    db_obj = DropBoxDB("praveen","S@gem0de")
    error=''
    try:
        if(request.method == "POST"):
            print("Debug 1")
            attempted_email = request.form["email"]
            attempted_pwd = request.form['password']
            flash(attempted_email)
            flash(attempted_pwd)
            print("Debug 2, after flash")
            user_details = dict()
            user_details["email"] = attempted_email
            #user_details["name"] = "Tarun"
            user_details["password"] = attempted_pwd
            #db_obj.authenticate_user(user_details)        

            #if(attempted_email=="chitta.vssut@gmail.com" and attempted_pwd=="123"):
            if(db_obj.authenticate_user(user_details)):
                print("Authentication success!")
                session['email'] = attempted_email
                session['id'] = db_obj.get_user_id(attempted_email)
                print("while setting session id ",session['id'])
                print("In login session id: {0}".format(session['id']))
                return redirect(url_for('view'))
            else:
                print("Authentication Fail!")
                error = "Invalid try again"
                print("invalid user")
                return render_template('login.html',title='login',wrongPassword=error)
    except Exception as e:
        flash(e)
        return render_template('login.html',title='login',error=error)

    return render_template('login.html',title='login',error=error)
    
@app.route("/logout")
def logout():
    del session['email']
    return redirect(url_for('login'))