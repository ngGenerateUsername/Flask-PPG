from App import app, db
from App.forms import loginForm, RegisterForm
from flask import render_template, redirect, url_for, flash, request
from App.models import task, admin, directeur, employee
from flask_login import login_user, logout_user, login_required, current_user
from flask import session


@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login_direc():
    if current_user.is_authenticated:
        return redirect(url_for('Dashboard_direc'))

    form = loginForm()
    if form.validate_on_submit():
        attempted_user = directeur.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(attempted_password=form.password.data):
            if int(attempted_user.get_state()) == 0:
                flash(f'Your account is awaiting Admin decision to accept',category='info')
                return  render_template('directeur/Login_direc.html', form=form)
            login_user(attempted_user)
            session['user_type'] = 'directeur'
            flash(f'Success! Your are loged in as: {attempted_user.username} ', category='success')
            return redirect(url_for('Dashboard_direc'))
        else:
            flash('Username and password are not match! Please try again', category='danger')

    return render_template('directeur/Login_direc.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register_direc():
    if current_user.is_authenticated:
        return redirect(url_for('Dashboard_direc'))
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = directeur(email_adress=form.email_adress.data,
                                  name = form.nom.data,
                                  lastName = form.lastName.data,
                                  phone = form.phone.data,
                                  departement = form.phone.data,
                                  poste = form.poste.data,
                                  username=form.username.data,
                                  password=form.password1.data,
                                  state = 0)
        db.session.add(user_to_create)
        db.session.commit()
        flash(f'Account created successfuly! You are loged in as : {user_to_create.username} ', category='success')
        return redirect(url_for('login_direc'))
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', category='danger')
    return render_template('directeur/Register_direc.html', form=form)


@app.route('/dashboard')
@login_required
def Dashboard_direc():
    if session.get('user_type') == 'admin':
        logout_user()
        session.pop('user_type') if session.get('user_type') != None else None
        return redirect(url_for('login_direc'))
    return render_template('directeur/Dashboard_direc.html')






#Admin routes
@app.route('/admin/',methods=['GET', 'POST'])
@app.route('/admin/login', methods=['GET', 'POST'])
def login_admin():
    if current_user.is_authenticated:
        return redirect(url_for('Dashboard_admin'))
    form = loginForm()
    if form.validate_on_submit():

        ad = admin.query.filter_by(username=form.username.data).first()
        if ad and ad.check_password_correction(attempted_password=form.password.data):
            login_user(ad)
            session['user_type'] = 'admin'
            flash(f'Success! Your are loged in as: {ad.username} ', category='success')
            return redirect(url_for('Dashboard_admin'))
        else:
            flash('Username and password are not match! Please try again', category='danger')

    return render_template('admin/Login_admin.html', form=form)


@app.route('/admin/dashboard')
@login_required
def Dashboard_admin():
    if session.get('user_type') == 'directeur':
        logout_user()
        session.pop('user_type')
        return redirect(url_for('login_direc'))

    inProgressAccounts = directeur.query.filter_by(state = 0).all()
    return render_template('admin/Dashboard_admin.html',inProgressAccounts = inProgressAccounts)


@app.route('/admin/<decision>/<idDirecteur>/')
def direcMakeDecision(decision,idDirecteur):
    dirctrToUpdateState = directeur.query.filter_by(id_directeur = idDirecteur ).first()
    if decision == 'accept':
       dirctrToUpdateState.state = 1
       db.session.commit()
    elif decision == 'refuse':
       db.session.delete(dirctrToUpdateState)
       db.session.commit()
    return redirect(url_for('Dashboard_admin'))
    


@app.route('/logout')
def logout_page():
    if(session.get('user_type') == 'admin'):
        logout_user()
        flash("You have been logged out!", category='info')
        if session.get('user_type') != None : session.pop('user_type') 
        return redirect(url_for("login_admin"))
    else:
        logout_user()
        flash("You have been logged out!", category='info')
        session.pop('user_type') if session.get('user_type') != None else None
        return redirect(url_for("login_direc"))


#Api routes