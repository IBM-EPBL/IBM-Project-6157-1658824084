
# importing Flask and other modules
import email
from tkinter import N
from flask import Flask, request, render_template
 
# Flask constructor
app = Flask(__name__)  
 
# A decorator used to tell the application
# which URL is associated function
@app.route('/', methods =["GET", "POST"])
def gfg():
    if request.method == "POST":
       # getting input with name = fname in HTML form
       first_name = request.form.get("fname")
       # getting input with name = lname in HTML form
       email = request.form.get("email")
       phone = request.form.get("phone")

       return "Name: "+first_name + "\nEmail: \n"+email+"Phone no: "+phone
    return render_template("register.html")
 
if __name__=='__main__':
   app.run()