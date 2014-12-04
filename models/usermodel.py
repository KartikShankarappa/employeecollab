import MySQLdb, md5
from flask import session
from user_objects import *
class UserModel:
	def __init__(self):
		self.db = MySQLdb.connect(host="localhost",
		                     user="root",
		                      passwd="ron",
		                      db="employee_network")

		self.runquery = self.db.cursor()

	def register_user(self, user):
		users_query = "insert into users(password,\
										 first_name,\
										 last_name,\
										 email_id,\
										 join_date,\
										 friends_visibility_id,\
										 post_visibility_id) values('%s', '%s', '%s', '%s', '%s', '%s', '%s')"\
										%(md5.md5(user.password).hexdigest(),
										  user.first_name,
										  user.last_name,
										  user.email_id,
										  user.join_date,
										  user.friends_visibility_id,
										  user.post_visibility_id)
		self.runquery.execute(users_query)
		self.db.commit()
		return None

	def login(self, user):
		users_query = "select user_id,\
							  first_name,\
							  last_name,\
							  email_id,\
							  current_location,\
							  relationship_status,\
							  date_of_birth,\
							  profile_pic,\
							  friends_visibility_id,\
							  post_visibility_id from users where \
							email_id = '%s' and \
							password = '%s'" %(user.email_id, md5.md5(user.password).hexdigest())
		self.runquery.execute(users_query)
		data = self.runquery.fetchone()
		if data:
			user_data = {}
			user_data["user_id"] = data[0]
			user_data["first_name"] = data[1]
			user_data["last_name"] = data[2]
			user_data["email_id"] = data[3]
			user_data["current_location"] = data[4]
			user_data["relationship_status"] = data[5]
			user_data["date_of_birth"] = data[6]
			user_data["profile_pic"] = data[7]
			user_data["friends_visibility_id"] = data[8]
			user_data["post_visibility_id"] = data[9]
			session['user'] = user_data
			return True
		return False
