# Store this code in 'app.py' file

from flask  import Flask, render_template, request, redirect, url_for, session
import re
import ibm_db
import sendgrid
import os
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
	
	

class data:
	def __init__(self, email = ''):
		self.email = email
	
	
	# setter method
	def set_email(self, x):
		self.email = x
	def set_name(self, x):
		self.name = x

data = data()




@app.route('/', methods =["GET", "POST"])
@app.route('/login', methods =['GET', 'POST'])
def login():
	print(request.form)
	msg = ''
	if request.method == 'POST':
		email = request.form['email']
		password = request.form['password']
		sql="SELECT * FROM USER_DETAILS WHERE EMAIL =? AND PASSWORD =?"
		stmt = ibm_db.prepare(conn,sql)
		ibm_db.bind_param(stmt,1,email)
		ibm_db.bind_param(stmt,2,password)
		ibm_db.execute(stmt)
		account =ibm_db.fetch_assoc(stmt)
		print(account)
		print("account--------------")
		data.set_email(email)
		print(data.email)

		
		
		if account:
			sql="SELECT * FROM USER_DETAILS WHERE EMAIL =?"
			stmt = ibm_db.prepare(conn,sql)
			ibm_db.bind_param(stmt,1,email)
			ibm_db.execute(stmt)
			username =ibm_db.fetch_assoc(stmt)
			name=username.get("USER_NAME")
			data.set_name(username.get("USER_NAME"))

			



			return render_template('home.html',name=data.name,email=data.email)
		else:
			msg = 'Incorrect username / password !'
	return render_template('login.html', msg = msg)


@app.route('/register', methods =['GET', 'POST'])
def register():
	msg = ''
	if request.method == "POST":
		username = request.form['username']
		password = request.form['password']
		email = request.form['email']
		sql ="SELECT * FROM USER_DETAILS WHERE USER_NAME = ?"
		stmt = ibm_db.prepare(conn,sql)
		ibm_db.bind_param(stmt,1,username)
		ibm_db.execute(stmt)
		account = ibm_db.fetch_assoc(stmt)
		print(account)
		print("account--------------")
		
		if account:
			msg = 'Account already exists ! Please Login'
			return render_template('login.html', msg = msg)

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
			inser_sql="INSERT INTO BALANCE VALUES(?,?,?,?)"
			prep_stmt = ibm_db.prepare(conn, inser_sql)
			ibm_db.bind_param(prep_stmt,1,0)
			ibm_db.bind_param(prep_stmt,2,0)
			ibm_db.bind_param(prep_stmt,3,0)
			ibm_db.bind_param(prep_stmt,4,email)
			ibm_db.execute(prep_stmt)
			

			msg = 'You have successfully registered !'
			return render_template('login.html', msg = msg)

	elif request.method == 'POST':
		msg = 'Please fill out the form !'
	return render_template('register.html', msg = msg)

@app.route('/home')
def dash():
	sql="SELECT * FROM USER_DETAILS WHERE EMAIL =?"
	stmt = ibm_db.prepare(conn,sql)
	ibm_db.bind_param(stmt,1,data.email)
	ibm_db.execute(stmt)
	username =ibm_db.fetch_assoc(stmt)
	name=username.get("USER_NAME")
	email=username.get("EMAIL")

	#name=data.email
	return render_template('home.html',name=name,email=email)

@app.route('/expenditure',methods =['GET','POST'])
def expenditure():
	account=[]
	if request.method == "GET":
		sql ="SELECT EMAIL FROM EXPENSE"
		stmt = ibm_db.prepare(conn,sql)
		#ibm_db.bind_param(stmt,1,data.email)
		ibm_db.execute(stmt)
		#account.append(ibm_db.fetch_assoc(stmt))
		account=ibm_db.free_result(stmt)
		print(account)
		print("get")
		print(request.form)
		sql="SELECT * FROM BALANCE WHERE EMAIL =?"
		stmt = ibm_db.prepare(conn,sql)
		ibm_db.bind_param(stmt,1,data.email)
		ibm_db.execute(stmt)
		username =ibm_db.fetch_assoc(stmt)
		expense=username.get("EXPENSE")
		balance=username.get("BALANCE")	
		return render_template('expenditure.html',expense=expense,balance=balance)

		
	else:
		print("------------POST------------------")
		print(request.form)
		expense=request.form["expense"]
		etype=request.form["type"]
		sql="UPDATE BALANCE SET EXPENSE=EXPENSE+?,BALANCE=BALANCE-? WHERE EMAIL=?"
		prep_stmt = ibm_db.prepare(conn,sql)
		ibm_db.bind_param(prep_stmt,1,expense)
		ibm_db.bind_param(prep_stmt,2,expense)
		ibm_db.bind_param(prep_stmt,3,data.email)
		ibm_db.execute(prep_stmt)
		inser_sql="INSERT INTO EXPENSE VALUES(?,?,?)"
		prep_stmt = ibm_db.prepare(conn, inser_sql)
		ibm_db.bind_param(prep_stmt,1,data.email)
		ibm_db.bind_param(prep_stmt,2,etype)
		ibm_db.bind_param(prep_stmt,3,expense)
		ibm_db.execute(prep_stmt)
        

		sql="SELECT * FROM BALANCE WHERE EMAIL =?"
		stmt = ibm_db.prepare(conn,sql)
		ibm_db.bind_param(stmt,1,data.email) 
		ibm_db.execute(stmt)
		username =ibm_db.fetch_assoc(stmt)
		balance=username.get("BALANCE")
		expense=username.get("EXPENSE")	
		limit=username.get("LIMIT")
		if expense > limit:
			sg = sendgrid.SendGridAPIClient(api_key='{{api key}}')
			dat = {
              "personalizations": [
                {
                  "to": [
                    {
                      "email":data.email
                    }
                  ],
                  "subject": "EXPENDITURE LIMIT Alert!"
                }
              ],
              "from": {
                "email": "{{sender mail}}"
              },
              "content": [
                {
                  "type": "text/plain",
                  "value": "Your monthly expense limit exit your balance:"+balance+" expense:"+expense+" limit:"+limit
                }
              ]
            }
			response = sg.client.mail.send.post(request_body=dat)
			print(response.status_code)
			print(response.body)
			print(response.headers)
            
	return render_template('expenditure.html',expense=expense,balance=balance)
		
	


    

@app.route('/wallet',methods =['GET','POST'])
def wallet():
	if request.method == "GET":
		print("get")
		print(request.form)
		sql="SELECT * FROM BALANCE WHERE EMAIL =?"
		stmt = ibm_db.prepare(conn,sql)
		ibm_db.bind_param(stmt,1,data.email)
		ibm_db.execute(stmt)
		username =ibm_db.fetch_assoc(stmt)
		limit=username.get("LIMIT")
		balance=username.get("BALANCE")	
		return render_template('wallet.html',limit=limit,balance=balance)

		
	else:
		print("post")
		print(request.form)
		limit=request.form["limit"]
		balance=request.form["balance"]
		if limit!='':
			sql="UPDATE BALANCE SET LIMIT=? WHERE EMAIL=?"
			prep_stmt = ibm_db.prepare(conn,sql)
			ibm_db.bind_param(prep_stmt,1,limit)
			ibm_db.bind_param(prep_stmt,2,data.email)
			ibm_db.execute(prep_stmt)
			sql="SELECT * FROM BALANCE WHERE EMAIL =?"
			stmt = ibm_db.prepare(conn,sql)
			ibm_db.bind_param(stmt,1,data.email)
			ibm_db.execute(stmt)
			username =ibm_db.fetch_assoc(stmt)
			limit=username.get("LIMIT")
			balance=username.get("BALANCE")	
			return render_template('wallet.html',limit=limit,balance=balance)
		elif balance!='':
			sql="UPDATE BALANCE SET BALANCE=BALANCE+? WHERE EMAIL=?"
			prep_stmt = ibm_db.prepare(conn,sql)
			ibm_db.bind_param(prep_stmt,1,balance)
			ibm_db.bind_param(prep_stmt,2,data.email)
			ibm_db.execute(prep_stmt)
			sql="SELECT * FROM BALANCE WHERE EMAIL =?"
			stmt = ibm_db.prepare(conn,sql)
			ibm_db.bind_param(stmt,1,data.email)
			ibm_db.execute(stmt)
			username =ibm_db.fetch_assoc(stmt)
			limit=username.get("LIMIT")
			balance=username.get("BALANCE")	
			return render_template('wallet.html',limit=limit,balance=balance)
		else:
			sql="SELECT * FROM BALANCE WHERE EMAIL =?"
			stmt = ibm_db.prepare(conn,sql)
			ibm_db.bind_param(stmt,1,data.email)
			ibm_db.execute(stmt)
			username =ibm_db.fetch_assoc(stmt)
			limit=username.get("LIMIT")
			balance=username.get("BALANCE")	
			return render_template('wallet.html',limit=limit,balance=balance)

			

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
@app.route('/logout')
def logout():
  return render_template('home.html')

if __name__=='__main__':
	app.run(host='0.0.0.0')
