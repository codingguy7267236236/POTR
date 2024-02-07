from flask import Flask, session, render_template, url_for,request,redirect,flash,redirect,jsonify, make_response,session
import os
from flask import Flask
from funcs import *
import jwt
import datetime
from functools import wraps

#secret key variable
skey = "YOUR SECRET KEY"

#decorator for ensuring token
def token_required(f):
  @wraps(f)
  def decorated(*args,**kwargs):
    try:
      token = session["token"]
      if not token:
        return redirect(url_for("login"))

      try:
        data = jwt.decode(jwt=token,key=app.config["SECRET_KEY"],algorithms=["HS256"])
      except:
        session["name"] = None
        session["token"] = None
        return redirect(url_for('index'))
      return f(*args,**kwargs)
    except KeyError:
      session["name"] = None
      session["token"] = None
      return redirect(url_for('login'))
  return decorated

def token_required2(f):
  @wraps(f)
  def decorated(*args,**kwargs):
    try:
      token = request.args.get("token")
      if not token:
        return redirect(url_for("login"))
  
      try:
        data = jwt.decode(jwt=token,key=app.config["SECRET_KEY"],algorithms=["HS256"])
      except:
        session["name"] = None
        session["token"] = None
        return redirect(url_for('index'))
      return f(*args,**kwargs)
    except KeyError:
      session["name"] = None
      session["token"] = None
      return redirect(url_for('login'))
  return decorated


usrData = JSON("userdata.json")
states = JSON("states.json")


#getting environmental variable
#os.environ['secret']
secret = skey
app = Flask(__name__)
app.config["SECRET_KEY"] = secret
app.secret_key = secret


dat = JSON("data.json")
data = dat.data


#token work stuff
def get_token():
  try:
    token = session["token"]
  except KeyError:
    token = None
  return token

def createToken(user,pw):
  info = usrData.data
  token = None
  #checking passwords match
  #try:
  da = usrData.data[user]
  stored = da["password"]
  salt = da["salt"]
  
  #checking hashed passwords
  valid = checkEncryption(pw,stored,salt)
  if valid == False:
    print("Passwords do not match")

  #getting data if exists and creating token if 
  else:
    for i in info:
      if i == user:
        data = info[i]
        token = jwt.encode({'user': user, "data":data, "exp":datetime.datetime.utcnow()+datetime.timedelta(minutes=30)}, app.config["SECRET_KEY"])
        break
      else:
        data = None
        token=None
    
  #except:
    #print("User does not exist")
  return token


def decodeToken():
  token = session["token"]
  try:
    data = jwt.decode(jwt=token,key=app.config["SECRET_KEY"],algorithms=["HS256"])
  except:
    data = None
  return data


@app.route('/')
def index():
  token = get_token()
  return render_template("home.html")

@app.route('/login',methods=["POST","GET"])
def login():
  token = get_token()
  if token == None:
    if request.method == "POST":
      name=request.form.get("name")
      pw=request.form.get("password")
      
      #if its signup form add to db if username not already in use
      #creating user data if the username doesn't exist
      if "signup" in request.form:
        try:
          uData = usrData.data[str(name)]

        #if key error then the username doesn't exist so add it
        except KeyError:
          hashed,salt = hashPassword(pw)
          usrData.data[str(name)] = {"role":"Citizen","password":hashed.decode("utf-8"),"salt":salt.decode("utf-8")}
          usrData.save()
      
      #processing token stuff. even on signup
      #creating token
      token = createToken(name,pw)
      if token != None:
        session["token"] = token
        session["name"] = name
          #usrData.data[name]={"role":"Citizen","password":str(pw)}
          #usrData.save()
          #redirecting bakc here if invalid
        return redirect(url_for('profile'))
    
    return render_template("login.html")
  else:
    return redirect(url_for('profile'))

@app.route('/news')
def news():
  dat = JSON("data.json")
  newsdata = dat.data["news"]
  return render_template("news.html",dat=newsdata)

@app.route('/about')
def about():
  return render_template("about.html")

@app.route('/logout')
def logout():
  session["token"] = None
  session["name"] = None
  return redirect(url_for("index"))

@app.route('/contact')
def contact():
  return render_template("contact.html")

@app.route('/clubs')
def governance():
  dat = JSON("data.json")
  cab = dat.data["clubs"]
  return render_template("clubs.html",dat=cab)

@app.route('/map')
@token_required
def map():
  token = get_token()
  data = decodeToken()
  sts = states.data
  return render_template("map.html",dat=sts,usrinfo=data)


@app.route('/profile')
@token_required
def profile():
  data = usrData.data[session["name"]]
  token = get_token()
  dat = decodeToken()
  return render_template("profile.html",data=data,user=dat)

@app.route('/store')
def store():
  dat = JSON("data.json")
  items = dat.data["store"]
  return render_template("store.html",items=items)

@app.route('/article/<string:id>')
def article(id):
  try:
    dat = JSON("data.json")
    newsdata = dat.data["news"][id]
    return render_template("article.html",dat=newsdata)
  except KeyError:
    return render_template("404.html")


###API METHODS THAT CAN BE CALLED
@app.route('/editarticle/<string:id>',methods=["POST"])
def editarticle(id):
  if request.method == "POST":
    #converting the form data to a dictionary
    output = request.form.to_dict()
    dat = JSON("data.json")
    newsdata = dat.data["news"][id]["description"] = output["content"]
    dat.save()
  return jsonify(0),200


@app.route('/postarticle',methods=["POST"])
def postarticle():
  if request.method == "POST":
    #converting the form data to a dictionary
    output = request.form.to_dict()
    dat = JSON("data.json")
    cab = dat.data["news"]
    id = len(cab)
    cab[str(id+1)] = {"title":output["title"],"description":output["content"],"image":output["img"]}
    dat.data["news"] = cab
    dat.save()
  msg = "Posted article to the JE Times"
  return jsonify(msg)


app.run(host='0.0.0.0', port=8080)