from __future__ import unicode_literals
import os
import datetime
import MySQLdb
import sys
import random

con=MySQLdb.connect("localhost","root","root","t")
cursor=con.cursor()
from flask import Flask,request,render_template,session,redirect,jsonify,send_from_directory
from werkzeug import secure_filename
# from database import insert,select,update,delete
now = datetime.datetime.now().strftime('%d-%m-%Y')
now1 = datetime.datetime.now()
app=Flask(__name__)
app.secret_key = "tam"
app.config['UPLOAD_FOLDER'] = 'static/img/new'
#LOGIN SESSION
@app.route("/")
def login():
	return render_template("user.html")
@app.route("/view")
def log():
	return render_template("view.html")
@app.route("/update")
def update():
	return render_template("update.html")		
@app.route("/view.json")
def subject_handler_json():
	con.set_character_set('utf8')
	cursor.execute('SET NAMES utf8;')
	cursor.execute('SET CHARACTER SET utf8;')
	cursor.execute('SET character_set_connection=utf8;')
	cursor.execute("SELECT * FROM new")
	des=[]
	for x in cursor.description:
	  des.append(x[0])
	i=[]
	for x in cursor.fetchall():
	  i.append({des[0]:x[0],des[1]:x[1],des[2]:x[2],des[3]:x[3],des[4]:x[4]})	
	return jsonify(i)

# @app.route("/login_validate",methods=['POST'])
# def login_validate():
# 	data= request.get_json()
# 	user_id=data.get("user_name")
# 	password=data.get("password")
# 	cursor.execute("SELECT *FROM  WHERE Mobile='%s' AND password='%s'" %(user_id,password))
# 	data=cursor.fetchone()
# 	if data==None:
# 		re="n"	
# 	else:
# 		session['user_id']=user_id
# 		re="s"
# 	return re
	# quantity=data['quantity']	
	# file = request.files['file']
	# file.filename.encode("utf8")	
	# filename = secure_filename(file.filename)
	# file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
	# file=filename
	# print(file)	
@app.route("/addd",methods=["POST"])
def addd():
	data=request.form
	name=data['name']
	price=data['price']
	nprice=data['nprice']
	tamil_name=data['tamil_name']
	con.set_character_set('utf8')
	cursor.execute('SET NAMES utf8;')
	cursor.execute('SET CHARACTER SET utf8;')
	cursor.execute('SET character_set_connection=utf8;')	
	cursor.execute("INSERT INTO new(`name`,`price`,`newprice`,`tamil_name`) VALUES('%s','%s','%s','%s')" %(name,price,nprice,tamil_name))
	con.commit()	
	return redirect("/")	
@app.route("/userupdate",methods=["POST"])
def userupdate():
	data=request.get_json()
	name=data.get('name')
	price=data.get('price')	
	newprice=data.get('newprice')		
	con.set_character_set('utf8')
	cursor.execute('SET NAMES utf8;')
	cursor.execute('SET CHARACTER SET utf8;')
	cursor.execute('SET character_set_connection=utf8;')	
	cursor.execute("UPDATE new SET price = '%s' , newprice = '%s' WHERE name = '%s'" %(price,newprice,name))
	con.commit()	
	return "success"		 			 
@app.route("/delete.json/<id>",methods=['POST'])
def sdata_delete(id):	
	print id
	cursor.execute("DELETE FROM new WHERE ID='%s'" %(id))
	con.commit()
	return "deleted success"
@app.route("/balance")
def balance():
	return render_template("balance.html")
@app.route("/balance_amount",methods=['POST'])
def balance_amount():
	data=request.get_json()
	name=data.get('name')
	balance_amount=data.get('balance_amount')
	total_amount=data.get('total_amount')
	cursor.execute("INSERT INTO balance(`name`,`balance_amount`,`total_amount`,`date`) VALUES('%s','%s','%s',now())" %(name,balance_amount,total_amount))	
	con.commit()
	return "success"
@app.route("/balance.json")
def balance_json():
	cursor.execute("SELECT *FROM balance")
	datas=cursor.fetchall()
	t=[]
	for data in datas:
		y={"id":data[0],"name":data[1],"balance_amount":data[2],"total_amount":data[3],"date":data[4]}
		t.append(y)
	return jsonify(t)
@app.route("/balupdate",methods=['POST'])
def balupdate():
	data=request.get_json()	
	id=data.get('id')
	name=data.get('name')
	bal=data.get('balance_amount')
	total_amount=data.get('total_amount')
	con.set_character_set('utf8')
	cursor.execute('SET NAMES utf8;')
	cursor.execute('SET CHARACTER SET utf8;')
	cursor.execute('SET character_set_connection=utf8;')	
	cursor.execute("UPDATE balance SET name = '%s' , balance_amount = '%s' , total_amount = '%s'  WHERE id = '%s'" %(name,bal,total_amount,id))
	con.commit()	
	return "success"	
@app.route("/report_update",methods=["POST"])
def report_update():
	data=request.get_json()
	name=data.get("name")
	total=data.get("total")
	print name,total
	cursor.execute("INSERT INTO report(`name`,`total_amount`,`date`) VALUES('%s','%s',now())" %(name,total))
	con.commit()
	return "s"
@app.route("/report")
def report():
	return render_template("report.html")
@app.route("/report_get")
def report_get():
	cursor.execute("SELECT *FROM report")
	data=cursor.fetchall()
	t=[]
	for x in data:
		t.append({"name":x[1],"amount":x[2],"date":x[3],"id":x[0]})
	return jsonify(t)
@app.route("/bal_delete/<id>",methods=['POST'])
def bal_delete(id):	
	print id
	cursor.execute("DELETE FROM balance WHERE id='%s'" %(id))
	con.commit()
	return "deleted success"	
@app.route("/report_delete/<id>",methods=['POST'])
def report_delete(id):	
	print id
	cursor.execute("DELETE FROM report WHERE id='%s'" %(id))
	con.commit()
	return "deleted success"	

if __name__=="__main__":
	# print dep()
	# app.run("192.168.137.41",88,debug=True)
	# app.run("172.16.193.52",88,debug=True)
	# app.run("192.168.43.50",debug=True)
	app.run("tamizh",800,debug=True)



	
