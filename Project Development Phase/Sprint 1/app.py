# Store this code in 'app.py' file

from flask  import Flask, render_template, request, redirect, url_for, session
import re
import ibm_db
app = Flask(__name__)


app.secret_key = 'a'
hostname="9938aec0-8105-433e-8bf9-0fbb7e483086.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud"
uid="bnl43300"
pwd="8xP7XmqgCC97iV1a"
driver="{IBM DB2 ODBC DRIVER}"
db="bludb"
port="32459"
protocol="TCPIP"
cert="Certificate.crt"

dsn=(
      "DATABASE={0};"
      "HOSTNAME={1};"
      "PORT={2};"
      "UID={3};"
      "SECURITY=SSL;"
      "SSLServerCerttificate={4};"
      "pwd={5};"
).format(db,hostname,port,uid,cert,pwd)
print(dsn)
try:
    conn=ibm_db.connect(dsn,"","")
    print("CONNECTED")
except:
    print("Unable to connect",ibm_db.conn_errormsg())

    

@app.route('/login', methods =["GET", "POST"])
@app.route('/', methods =["GET", "POST"])
def login():
	return render_template('login.html')
	global userid
	msg = ''
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		sql="SELECT * FROM USER_DETAILS WHERE USER_NAME =? AND PASSWORD =?"
		stmt = ibm_db.prepare(conn,sql)
		ibm_db.bind_param(stmt,1,username)
		ibm_db.bind_param(stmt,2,password)
		ibm_db.execute(stmt)
		account =ibm_db.fetch_assoc(stmt)
		print(account)
		if account:
			
			msg ='logged in successfully !'

			return render_template('dashboard.html',msg = msg)
		else:
			msg = 'Incorrect username / password !'
	return render_template('login.html', msg = msg)


@app.route('/register', methods =['GET', 'POST'])
def register():
	msg = ''
	if request.method == 'POST' :
		username = request.form['username']
		password = request.form['password']
		email = request.form['email']
		sql ="SELECT * FROM USER_DETAILS WHERE USER_NAME = ?"
		stmt = ibm_db.prepare(conn,sql)
		ibm_db.bind_param(stmt,1,username)
		ibm_db.execute(stmt)
		account = ibm_db.fetch_assoc(stmt)
		print(account)
		
		if account:
			msg = 'Account already exists !'
		elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
			msg = 'Invalid email address !'
		elif not re.match(r'[A-Za-z0-9]+', username):
			msg = 'Username must contain only characters and numbers !'
		else:
			inser_sql="INSERT INTO USER_DETAILS VALUES(?,?,?)"
			prep_stmt = ibm_db.prepare(conn, inser_sql)
			ibm_db.bind_param(prep_stmt,1,username)
			ibm_db.bind_param(prep_stmt,2,email)
			ibm_db.bind_param(prep_stmt,3,password)
			ibm_db.execute(prep_stmt)
			msg = 'You have successfully registered !'
	elif request.method == 'POST':
		msg = 'Please fill out the form !'
	return render_template('register.html', msg = msg)

@app.route('/dashboard')
def dash():
		return render_template('deshboard.html')

@app.route('/apply',methods =['GET','POST'])
def apply():
		msg=''
		if request.mwthod == 'POST':
			username = request.form['username']
			email=request.form['email']
			qualification=request.form['qualification']
			skills=request.form['skills']
			jobs = request.form['s']
			################################################
			msg='YOU ARE SUCESFULLY APPLIED '
			session['loggedin']=True
		elif request.method == 'POST':
			msg='please fill the form'
			return render_template('apply.html',msg = msg)
@app.route('/display')
def display():
	##############################
 @app.route('/logout')
 def logout():
  
 
  return render_template('home.html')

if __name__=='__main__':
	app.run(host='0.0.0.0')