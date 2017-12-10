from flask import Flask, render_template, flash, request
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
from werkzeug import secure_filename
import os
import smtplib
import sqlite3
import db
 
# App  config.
DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'
file_name = "c:\\Users\\LOKESH\\tryscribe\\campaign.csv";
UPLOAD_FOLDER = 'c:\\Users\\LOKESH\\tryscribe\\uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

conn = sqlite3.connect('database.db')
#print ("Opened database successfully");
#conn.execute('DROP TABLE campaign')
conn.execute('CREATE TABLE if not exists campaign (id integer primary key AUTOINCREMENT, name TEXT NOT NULL, stages integer NOT NULL, schedule integer NOT NULL, subject TEXT NOT NULL, body TEXT NOT NULL, email TEXT )')

class ReusableForm(Form):
    name = TextField('Name:', validators=[validators.required()])
    stages = TextField('Stages:', validators=[validators.required()])
    schedule = TextField('Schedule:', validators=[validators.required()])
    subject = TextField('Subject:', validators=[validators.required()])
    body = TextField('Body:', validators=[validators.required()])

@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        fp = open(app.config['UPLOAD_FOLDER'] + '\\' + filename)
        emails = fp.read()
        db.saveRecipients(emails)		
        return emails

@app.route("/hello", methods=['GET', 'POST'])
def hello():
    form = ReusableForm(request.form) 
    print (form.errors)
    if request.method == 'POST':
        name=request.form['name']
        stages=request.form['stages']
        schedule=request.form['schedule']
        subject=request.form['subject']
        body=request.form['body']
        #print (name + ' ' + stages + ' ' + schedule + ' ' + subject + ' ' + body)
 
        if form.validate():
            # Save the comment here.
            msg = name + "\\t" + stages + "\\t" + schedule + "\\t" + subject + "\\t" + body
            #save(msg)
            saveCampaign(request)
            with open(file_name) as f:
                content = ""
                for line in f.readlines():
                    flash(line)
            return render_template('recipients.html', form=form)
        else:
            flash('All the form fields are required. ')
 
    return render_template('hello.html', form=form)
 
@app.route("/list", methods=['GET', 'POST'])
def list():
	return render_template("list.html",rows = db.list())


@app.route("/sendmail/<id>", methods=['GET', 'POST'])
def sendmail(id):
	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.ehlo()
	server.starttls()
	server.login("babureddy1969@gmail.com", "babs331969")
	campaign = db.list(id)
	subject = campaign[0]['subject']
	body = campaign[0]['body']
	emails = campaign[0]['email']
	#Send the mail
	for email in emails.split("\t"):
		msg = "\r\n".join([
		  "From: babureddy1969@gmail",
		  "To: " + email,
		  "Subject: " + subject,
		  "",
		  body
		  ])
		server.sendmail("babureddy1969@gmail",email, msg)
	return "mail sent ok"

def saveCampaign(request):
    r = {"name":request.form["name"],"stages":request.form["stages"],"schedule":request.form["schedule"],"subject":request.form["subject"],"body":request.form["body"]}
    db.saveCampaign(r)
    return "Campaign created successfully"

if __name__ == "__main__":
    app.run()
