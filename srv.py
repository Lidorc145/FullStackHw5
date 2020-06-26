from flask import Flask, request
import mysql.connector as mysql
import json
import datetime

db = mysql.connect(
	host = "localhost",
	user = "root",
	passwd = "PASSWORD",
	database = "myblog")

#######################################################################################
# How to use this REST API:
#######################################################################################
# to get all users u can send GET reques to /users/
# to get users by any attribute send GET request to /users/<attribute>/<value>
# and replace "<attribute>" and "<value>" with your required attribute and value.
#
# to get all posts u can send GET reques to /posts/
# to get users by any attribute send GET request to /posts/<attribute>/<value>
# and replace "<attribute>" and "<value>" with your required attribute and value.
#
# to add user, send POST request with the required attributes and values to /users/,
# for exmaple:
# send POST request to "/users/" 
# with this body:
# {
# 	"full_name": "Demo User",
#	"username": "demoAuther",
#	"password": "demo",
#	"type": "auther"
# }
#
#
# to add post, send POST request with the required attributes and values to /posts/,
# for exmaple:
# send POST request to "/users/" 
# with this body:
# { 
# 	"title": "Title text",
#	"summary": "This is the summary..",
#	"content": "content text..",
#	"image": "imgURL",
#	"auther_id": "6",
#	"last_update_date": "2020-06-22 22:59",
#	"publish_date": "2020-06-26 07:02",
#	"tags_list": "{ json tags list }"
# }
#####################################################################################

app = Flask(__name__)

#######################################
# Routes:
#######################################
@app.route('/users/<attribute>/<value>', methods=['GET', 'POST'])
@app.route('/users/', methods=['GET', 'POST'])
def users(attribute=None, value=None):
	if request.method == 'GET':
		return getUsers(attribute, value)
	else:
		data = request.get_json()
		return addUser(data)

@app.route('/posts/<attribute>/<value>', methods=['GET', 'POST'])
@app.route('/posts/', methods=['GET', 'POST'])
def posts(attribute=None, value=None):
	if request.method == 'GET':
		return getPosts(attribute, value)
	else:
		data = request.get_json()
		return addPost(data)
		
@app.route('/<path:path>')
def catch_all(path):
    return 'Invalid argument! %s' % path, 404
	
	

#######################################
# Functions:
#######################################
def addPost(data):
	query = "insert into posts (title, summary, content, image, auther_id, last_update_date, publish_date, num_of_views, tags_list) values (%s,%s,%s,%s,%s,STR_TO_DATE(%s,'%Y-%m-%d %H:%i'),STR_TO_DATE(%s,'%Y-%m-%d %H:%i'),0,%s)"
	values = (data['title'],data['summary'],data['content'],data['image'],data['auther_id'], data['last_update_date'], data['publish_date'],data['tags_list'])
	return postQuery(query, values)

def addUser(data):
	query = "insert into users (full_name, username, password, type) values (%s,%s,%s,%s)"
	values = (data['full_name'],data['username'],data['password'],data['type'])
	return postQuery(query, values)

def getUsers(attribute, value):
	query = "select * from users"
	header = ['id', 'full_name', 'username', 'password', 'type']
	return selectValidation(attribute, header, value, query, "users")	

def getPosts(attribute, value):
	query = "select * from posts"
	header = ['id', 'title', 'summary', 'content', 'image', 'auther_id', 'creation_date', 'last_update_date', 'publish_date', 'num_of_views', 'tags_list']
	return selectValidation(attribute, header, value, query, "posts")
	
	

def selectValidation(attribute, header, value, query, table):	
	if (attribute is not None) and (value is not None):
		if(attribute in header):
			query = "select * from "+table+" where "+attribute+"='"+value+"'"
		else:
			return "Invalid argument!", 404
	data = getQuery(query, header)
	return json.dumps(data)


def postQuery(query, values):
	cursor = db.cursor()
	print(query)
	print(values)
	cursor.execute(query, values)
	db.commit()
	new_post_id = cursor.lastrowid
	cursor.close()
	return "Added: "+str(new_post_id)
	
def getQuery(query, header):
	cursor = db.cursor()
	cursor.execute(query)
	records = cursor.fetchall()
	cursor.close()
	data = []
	for r in records:
		tmp = []
		for c in r:
				tmp.append(c.__str__()) #because of the datetime Object(Json Unsupport)
			
		data.append(dict(zip(header, tmp)))
	return data
 
	
if __name__ == "__main__":
	app.run()
