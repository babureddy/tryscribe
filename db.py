import sqlite3 
conn = sqlite3.connect('database.db')
	
def read():
    with open(file_name) as f:
        content = f.readlines()
    return content

def campaigns():
	conn = sqlite3.connect('database.db')
	conn.row_factory = sqlite3.Row
	cur = conn.cursor()
	cur.execute("SELECT * FROM campaign ORDER BY id DESC")
	rows = cur.fetchall(); 
	return rows

def list(id):
	conn = sqlite3.connect('database.db')
	conn.row_factory = sqlite3.Row
	cur = conn.cursor()
	cur.execute("SELECT * FROM campaign where id = " + id)
	rows = cur.fetchall(); 
	return rows

def saveCampaign(request):
	with sqlite3.connect("database.db") as con:
		cur = con.cursor()
		sql = "INSERT INTO campaign (name,stages,schedule,subject,body) VALUES (?,?,?,?,?)"
		cur.execute(sql,(request['name'],request['stages'],request['schedule'],request['subject'],request['body']) )            
		con.commit()
	return "Campaign created successfully"

def saveRecipients(email):
	with sqlite3.connect("database.db") as con:
		cur = con.cursor()
		sql = "UPDATE campaign set email='" + email + "' where id = (select max(id) from campaign)"
		cur.execute(sql)            
		con.commit()
	return "email list updated successfully"
def init():	
	conn = sqlite3.connect('database.db')
	conn.execute('DROP TABLE campaign')
	conn.execute('CREATE TABLE campaign (id integer primary key AUTOINCREMENT, name TEXT NOT NULL, stages integer NOT NULL, schedule integer NOT NULL, subject TEXT NOT NULL, body TEXT NOT NULL)')

#request = {"name":"name1","stages":"2","schedule":"2","subject":"s1","body":"msg1"}	
#saveCampaign(request)
#list()

