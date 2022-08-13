# these 2 imports i didnt write
from crypt import methods
from re import A
from database import db
from app import app
from flask import Flask, redirect, render_template, request, redirect, session, url_for
from models import Account, Login, Reservation, Category, Menu, Order
import os
import datetime

app.config["IMAGE_UPLOADS"] = 'static/images'

@app.route('/', methods=['POST','GET'])
def index():
	if request.method == 'POST':
		login = Login.query.filter_by(uname=request.form['username'], password=request.form['password']).first()

		if login:
			# variable for computer to make remember id
			session["id"] = login.id

			# role A -> you are the owner of the website. A is just a variable and i can change it in phpMyAdmin
			if login.role == 'A':
				return redirect('/dashboard')
			else:
				# /reservation is for Regular Users of the website
				return redirect('/userdashboard') 

		else:
			return 'Error loggin in'

	else:
		return render_template('index.html')

@app.route('/account', methods=['POST','GET'])
def account():
	if request.method == 'POST':
		# object = class name(column = data from form[form name])
		# we dont get role "U" from form, but we shouled set role in instance/object
		login = Login(uname=request.form['uname'], password=request.form['password'], role='U')

		try:
			db.session.add(login)
			db.session.commit()
			db.session.refresh(login)

			# login_id=login.id -> login_id(foreign key) = id column from login(table after refresh)
			account = Account(login_id=login.id, first_name=request.form['fname'], last_name=request.form['lname'], email=request.form['email'], birth_date =request.form['birthdate'])
			print('test')

			db.session.add(account)
			db.session.commit()
			return redirect('/')

		except:
			return 'Error in registration'

	else:
		return render_template('account.html')

@app.route('/logout')
def logout():
	session.clear()
	return redirect('/')

@app.route('/dashboard')
def dashboard():
	current_category = Category.query.add_columns(Category.id).all()
	current_menu = Menu.query.add_columns(Menu.id).all()

	if 'id' in session:
		login_id = session['id']
		user = Login.query.filter_by(id=login_id).first()

		return render_template('dashboard.html', current_category=current_category, current_menu = current_menu, user=user)

@app.route('/userdashboard')
def userdashboard():
	if 'id' in session:
		login_id = session['id']
		user = Login.query.filter_by(id=login_id).first()

		return render_template('userdashboard.html', user = user)

@app.route('/reservation', methods=['POST','GET'])
def reservation():
	# variable to get/call the id from computer
	login_id = session["id"]

	reserved_record = Reservation.query.filter(Reservation.login_id == login_id).add_columns(Reservation.id, Reservation.res_date, Reservation.res_time, Reservation.num_guest, Reservation.login_id).all()

	if request.method == 'POST':
		# login_id -> column in Reservation table, 
		reservation = Reservation(res_date=request.form['res_date'], res_time=request.form['res_time'], num_guest=request.form['num_guest'], login_id=login_id)

		try:
			db.session.add(reservation)
			db.session.commit()
			# session['msg'] = "Reservation sucess"
			return redirect('/reservation')

		except:
			return 'Error in reservation'

	else:
		return render_template('reservation.html', reservations = reserved_record)     

@app.route('/update_reservation/<int:id>', methods =['POST','GET'])
def update_resarvation(id):
	update_reservation = Reservation.query.get_or_404(id)

	if request.method == 'POST':
		update_reservation.res_date = request.form['res_date']
		update_reservation.res_time = request.form['res_time']
		update_reservation.num_guest = request.form['num_guest']

		try:
			db.session.commit()
			return redirect('/reservation')
		except:
			return 'Error in updating the record'

	else:
		return render_template('update_reservation.html', reservations = update_reservation)

@app.route('/delete_reservation/<int:id>')
def delete_reservation(id):
	record_to_delete = Reservation.query.get_or_404(id)

	try:
		db.session.delete(record_to_delete)
		db.session.commit()
		return redirect('/reservation')
	except:
		return 'Error in deleting reservation'

@app.route('/categories', methods = ['POST', 'GET'])
def categories():
	category_record = Category.query.add_columns(Category.id, Category.category_name).all()

	if request.method == 'POST':
		category = Category(category_name=request.form['category_name'])

		try:
			db.session.add(category)
			db.session.commit()
			return redirect('/categories')
		except:
			return 'Error in registration'

	else:
		return render_template('categories.html', categories = category_record)

@app.route('/update_category/<int:id>', methods =['POST','GET'])
def update_category(id):
	category = Category.query.get_or_404(id)

	if request.method == 'POST':
		category.category_name = request.form['category_name']

		try:
			db.session.commit()
			return redirect('/categories')
		except:
			return 'Error in updating the record'

	else:
		return render_template('update_category.html', categories = category)

@app.route('/delete_category/<int:id>')
def delete_category(id):
	record_to_delete = Category.query.get_or_404(id)

	try:
		db.session.delete(record_to_delete)
		db.session.commit()
		return redirect('/categories')
	except:
		return 'Error in deleting category'

@app.route('/users')
def users():
	user_info = Account.query.join(Login, Account.login_id == Login.id).add_columns(Login.id, Login.uname, Account.first_name, Account.last_name, Account.email, Account.birth_date).filter(Account.login_id == Login.id).all()

	return render_template('users.html', users_info = user_info)

@app.route('/update_user_info/<int:id>', methods=['POST','GET'])
def update_user_info(id):
	user = Account.query.get_or_404(id)

	if request.method =='POST':
		user.first_name = request.form['fname']
		user.last_name = request.form['lname']
		user.email = request.form['email']
		user.birth_date = request.form['birthdate']

		try:
			db.session.commit()
			return redirect('/users')
		except:
			return 'Error in updating record'
	else:
		return render_template('update_user_info.html', users = user)

@app.route('/delete_user_info/<int:id>')
def delete_user_info(id):
	record_to_delete = Account.query.get_or_404(id)

	try:
		db.session.delete(record_to_delete)
		db.session.commit()
		return redirect('/users')

	except:
		return 'Error in deleting reservation'

@app.route('/reservations')
def reservations():
	reservation_info = Reservation.query.join(Account, Reservation.login_id == Account.login_id).add_columns(Reservation.id, Reservation.res_date, Reservation.res_time, Reservation.num_guest, Reservation.login_id, Account.id, Account.first_name, Account.last_name).filter(Reservation.login_id == Account.login_id).all()

	reservation_info_new = list()
	today = datetime.date.today()
	for r in reservation_info:
		if r[2] >= today:
			reservation_info_new.append(r)
		
	# return render_template('reservations.html', reservations_info = reservation_info)
	return render_template('reservations.html', reservations_info = reservation_info_new)

@app.route('/update_reserve_info/<int:id>', methods=['POST','GET'])
def update_reserve_info(id):
	reserve_info = Reservation.query.get_or_404(id)

	if request.method == 'POST':
		reserve_info.res_date = request.form['res_date']
		reserve_info.res_time = request.form['res_time']
		reserve_info.num_guest = request.form['num_guest']

		try:
			db.session.commit()
			return redirect('/reservations')
		except:
			return 'Error in updating the record'

	else:
		return render_template('update_reserve_info.html', reserve_infos = reserve_info)

@app.route('/delete_reserve_info/<int:id>')
def delete_reserve_info(id):
	record_to_delete = Reservation.query.get_or_404(id)

	try:
		db.session.delete(record_to_delete)
		db.session.commit()
		return redirect('/reservations')
	except:
		return 'Error in deleting reservation'

@app.route('/add_menu', methods=['POST','GET'])
def add_menu():
	all_category = Category.query.add_columns(Category.id, Category.category_name).all()

	menu_record = Menu.query.join(Category, Menu.category_id == Category.id).add_columns(Menu.id, Menu.menu_name, Menu.menu_price, Menu.menu_pic, Menu.category_id, Category.category_name, Category.id).all()

	if request.method == 'POST':
		images = request.files['menu_pic']
		pic_name = images.filename
		menu = Menu(menu_name=request.form['menu_name'], menu_price=request.form['menu_price'], menu_pic=pic_name, category_id=request.form['category_id'])

		images.save(os.path.join(app.config["IMAGE_UPLOADS"], pic_name))

		try:
			db.session.add(menu)
			db.session.commit()
			return redirect('/add_menu')
		except:
			return 'Error in registration'

	else:
		return render_template('add_menu.html', all_categories = all_category, menus = menu_record)

@app.route('/update_menu/<int:id>', methods=['POST','GET'])
def update_menu(id):
	all_category = Category.query.add_columns(Category.id, Category.category_name).all()

	selected_menu = Menu.query.get_or_404(id)

	if request.method == 'POST':
		selected_menu.menu_name = request.form['menu_name']
		selected_menu.menu_price = request.form['menu_price']
		selected_menu.menu_pic = request.form['menu_pic']
		selected_menu.category_id = request.form['category_id']

		try:
			db.session.commit()
			return redirect('/add_menu')
		except:
			return 'Error in updating the record'

	else:
		return render_template('update_menu.html', all_categories = all_category, selected_menus = selected_menu)

@app.route('/delete_menu/<int:id>')
def delete_menu(id):
	record_to_delete = Menu.query.get_or_404(id)

	try:
		db.session.delete(record_to_delete)
		db.session.commit()
		return redirect('/add_menu')
	except:
		return 'Error in deleting menu'

@app.route('/select_category')
def select_category():
	categories = Category.query.add_columns(Category.id, Category.category_name).all()
	return render_template('select_category.html', categories = categories)

@app.route('/display_menu/<int:id>')
def display_menu(id):
	category = Category.query.get_or_404(id)
	menus = Menu.query.filter(Menu.category_id==id)

	return render_template('display_menu.html', category = category, menus = menus)

@app.route('/order/<int:id>', methods=['POST','GET'])
def order(id):
	selected_menu = Menu.query.get_or_404(id)
	# get the id from session
	login_id = session["id"]
	# query the reservation table using the session id
	reservation = Reservation.query.filter(Reservation.login_id == login_id).add_columns(Reservation.id, Reservation.res_date, Reservation.res_time, Reservation.num_guest,Reservation.login_id).all()
	if request.method== 'POST':
		order1 = Order(menu_id=id, reservation_id=request.form['reservation_id'], login_id=login_id)

		try:
			db.session.add(order1)
			db.session.commit()
			return redirect('/select_category')
		except:
			return 'Error in saving the order'

	else:
		return render_template ('order.html', selected_menu=selected_menu, reservation=reservation)

@app.route('/order_history')
def order_history():
	login_id = session['id']

	ordered_menu = Order.query.join(Menu, Order.menu_id==Menu.id).join(Reservation, Order.reservation_id==Reservation.id).add_columns(Order.id, Order.menu_id, Order.reservation_id, Order.login_id, Menu.id, Menu.menu_name, Menu.menu_price, Menu.menu_pic, Reservation.id, Reservation.res_date, Reservation.res_time, Reservation.num_guest).filter(Order.login_id==login_id).all()

	return render_template('/order_history.html', ordered_menu=ordered_menu)

@app.route('/update_order/<int:id>', methods=['POST','GET'])
def update_order(id):
	selected_order = Order.query.get_or_404(id)
	menu = Menu.query.filter(Menu.id==selected_order.menu_id).add_columns(Menu.id, Menu.menu_name, Menu.menu_price, Menu.menu_pic).first()

	reservation = Reservation.query.filter(Reservation.login_id==selected_order.login_id).add_columns(Reservation.id, Reservation.res_date, Reservation.res_time, Reservation.num_guest).all()

	if request.method=='POST':
		selected_order.reservation_id = request.form['reservation_id']

		try:
			db.session.commit()
			return redirect('/order_history')
		except:
			return 'Error in updating order'

	else:
		return render_template('/update_order.html', selected_order=selected_order, menu=menu, reservation=reservation)

@app.route('/delete_order/<int:id>')
def delete_order(id):
	selected_order = Order.query.get_or_404(id)

	try:
		db.session.delete(selected_order)
		db.session.commit()
		return redirect('/order_history')
	except:
		'Error in deleting order'

@app.route('/reservation_details/<int:id>')
def reservation_details(id):
	selected_res = Reservation.query.get_or_404(id)
	user = Login.query.filter(Login.id==selected_res.login_id).add_columns(Login.id, Login.uname).first()
	# last id in filter is selected_res.id
	details = Order.query.join(Reservation, Order.reservation_id==Reservation.id).join(Menu, Order.menu_id==Menu.id).add_columns(Order.id, Order.reservation_id, Order.menu_id, Reservation.res_date, Reservation.res_time, Reservation.num_guest, Menu.menu_name, Menu.menu_price, Menu.menu_pic).filter(Order.reservation_id==id).all()

	return render_template('reservation_details.html', selected_res=selected_res, user=user, details=details)

@app.route('/delete_res_order/<int:id>')
def delete_res_order(id):
	selected_order = Order.query.get_or_404(id)
	res_id = Reservation.query.filter(Reservation.id==selected_order.reservation_id).first().id
	# .get(Reservation.id==selected_order.reservation_id) --> get only one row

	try:
		db.session.delete(selected_order)
		db.session.commit()
		return redirect(url_for('reservation_details', id=res_id))

	except Exception as e:
		print(e)
		return 'Error in deleting the order'
	

@app.route('/update_res_order/<int:id>', methods=['POST', 'GET'])
def update_res_order(id):
	selected_order = Order.query.get_or_404(id)
	res_info = Order.query.join(Reservation, Order.reservation_id==Reservation.id).join(Login, Order.login_id==Login.id).filter(selected_order.id==Order.id).add_columns(Reservation.res_date, Reservation.res_time, Reservation.num_guest, Login.uname).first()
	menus = Menu.query.add_columns(Menu.id, Menu.menu_name, Menu.menu_price).all()
	
	if request.method=='POST':
		selected_order.menu_id = request.form['menus_id']
		try:
			db.session.commit()
			return redirect(url_for('reservation_details', id=id))
		except:
			'Error in updating reserved order'
	else:
		return render_template('update_res_order.html', res_info=res_info, menus=menus)

@app.route('/menu_details/<int:id>')
def menu_details(id):
	selected_menu = Menu.query.get_or_404(id)

	orders = Order.query.filter(id==Order.menu_id).join(Reservation, Order.reservation_id==Reservation.id).add_columns(Order.id, Order.reservation_id, Reservation.res_date, Reservation.res_time, Reservation.num_guest).all()

	return render_template('/menu_details.html', selected_menu=selected_menu, orders=orders)