import os
import random
import string
import pyautogui
import subprocess
from bottle import run, get, post, request, template, \
		   redirect, route, static_file, response, \
                   abort

iid = "http://0.0.0.0:5000"

def check_dir(*args):
    if not args:
        pass
    else:    
        for make in args:
            try:
                os.makedirs(make)
            except FileExistsError:
                continue

def check_login(username, password):
    if username == "admin" and password == "qwert":
        return True
    
    else:
        return False

    # Return a random alphanumerical id

def random_id():
  rid = ''
  for x in range(8):
      rid += random.choice(string.ascii_letters + string.digits)
  return rid

@route('/upload')
def do_upload():
    return template('test.html', error_page="")

@route('/upload', method='POST')
def upload():
    global iid
    upload = request.files.get('upload')
    save_path = "download" 
    try:
        file_path = "{path}/{file}".format(path=save_path, file=upload.filename)
    except AttributeError:
        return template("test.html", error_page="No file selected")
    try:
        upload.save(file_path)
    except OSError:
        return template("test.html", error_page="Select another file. This file already exists.")
    return "File successfully saved to '{}'.<br><p><a href='{}'>home page</a></p>"\
            .format(save_path, iid)

@route('/download/<filepath:path>')
def download_static_files(filepath):
     static_dir = "static_files"
     return static_file(filepath, root=static_dir, download=filepath)

@route('/static/<filepath:path>')
def static_files(filepath):
    return static_file(filepath, root="")

@route('/list/<path_dir>')
def files(path_dir):
    global iid
    path_file = path_dir
    for file in os.listdir(path_file):
        if os.path.isdir(path_file+file):
            continue
        else:
            path = "/".join(path_file.split("/"))+"/"
            yield '<p><a href="{}/static/{}">{}</a></p>' \
                .format(iid, \
                 path.replace("//", "/")+file, file)

@get('/')
def login():
    global iid
    try:
        options = open("options.txt", "r")
    except FileNotFoundError:
        options = open("options.txt", "w")
        options.write("admin=false\n")
        options.close
        options = open("options.txt", "r")
    if options.read() == 'admin=false\n':
        return template('based.tpl', css_file="default.css", iid=iid)
    else:    
        return '''
        <form action="/login" method="post">
             Username: <input name="username" type="text" />
             Password: <input name="password" type="password" />
             <input value="Login" type="submit" />
        </form>
        '''

@post('/login') # or @route('/login', method='POST')
def do_login():
    global iid
    username = request.forms.get('username')
    password = request.forms.get('password')
    if check_login(username, password):
        return template('based.tpl', css_file="default.css", iid=iid)
    else:
       	return '''
        <form action="/login" method="post">
            Username: <input name="username" type="text" />
            Password: <input name="password" type="password" />
            <input value="Login" type="submit" />
        </form>
	<b>Incorrect username or password</b>
    '''

@post('/comm_run') # or @route('/login', method='POST')
def check_command():
    global iid
    data_forms = request.forms.decode()
    kill = data_forms["comm"]
    history = open("history.txt", "a")
    history.write(kill + "\n")
    if kill == "prints -d":
        rai = random_id()
        scr = pyautogui.screenshot("static_files/"+rai+".png")
        redirect(iid+"/download/"+rai+".png")

    elif kill == "prints":
        rai = random_id()
        scr = pyautogui.screenshot("static_files/"+rai+".png")
        redirect(iid + "/static/static_files/"+rai+".png")

    else:
        try:
            res = subprocess.check_output(kill.split(), universal_newlines=True)
            return "<pre>%s<pre>" % res
        except:
            if not kill:
                return "No Command"
            else:
                return 'Command: %s' % kill
        return "Command: %s" % kill
    history.close()

if __name__ == "__main__":
    check_dir("download", "static_files")
    run(host='0.0.0.0', port=5000, reloading=True)
