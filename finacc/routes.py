from flask_login import current_user
from flask import render_template, request, g, redirect, url_for, flash, jsonify
from flask_login import login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

from finacc import app, db
from finacc.models import User, Project, Transaction
from finacc.validator import Validator


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template('login.html')
    elif request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if not username or not password:
            flash("Please fill all fields", "error")
            return render_template("login.html")
        else:
            user = User.query.filter_by(username=username).first()

            if not user or not check_password_hash(user.password, password):
                flash("Incorrect login or password", "error")
                return render_template("login.html")
            else:
                login_user(user)
                return redirect(url_for("project"))


@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template('register.html')
    elif request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        password2 = request.form.get("password2")

        if not username or not email or not password or not password2:
            flash("Please fill all fields", "error")
            return render_template('register.html')
        elif password != password2:
            flash("Passwords need to match", "error")
            return render_template('register.html')
        elif User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first():
            flash("User already exists", "error")
            return render_template("register.html")
        else:
            user = User(username=username, email=email, password=generate_password_hash(password))
            db.session.add(user)
            db.session.commit()
            flash("Successfully registered", "success")
            return redirect(url_for("login"))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/project', methods=["GET", "POST"])
@login_required
def project():
    user_id = current_user.id
    if request.method == "POST":
        project_name = request.form.get("project_name")
        if Project.query.filter_by(name=project_name).first():
            flash(f"Project {project_name} already exists", "error")
        else:
            new_project = Project(user_id=user_id, name=project_name)
            db.session.add(new_project)
            db.session.commit()
            flash(f"Project {project_name} created successfully", "success")
    projects = Project.query.filter_by(user_id=user_id).all()
    return render_template("project.html", projects=projects)


@app.route('/project_data', methods=["GET"])
@login_required
def project_data():
    user_id = current_user.id
    project_id = request.args.get("id")
    project = Project.query.filter_by(id=project_id).first()
    if not project or project.user_id != user_id:
        flash("Project not found", "error")
        return redirect(url_for('project'))
    transactions = Transaction.query.filter_by(project_id=project.id).all()
    return render_template("project_data.html", transactions=transactions, project=project)


@app.route('/add_transaction', methods=["POST"])
@login_required
def add_transaction():
    user_id = current_user.id
    req_data = request.form.to_dict()
    print(req_data)
    validator = Validator()
    if not validator.validate_new_transaction(req_data):
        flash("Enter correct transaction data", "error")
        return redirect(url_for('project'))
    project = Project.query.filter_by(id=req_data['project_id']).first()
    if not project or project.user_id != user_id:
        flash("Project not found", "error")
        return redirect(url_for('project'))
    new_trans = Transaction(project_id=req_data["project_id"], name=req_data["name"],
                            freq_type=req_data["freq_type"], value=req_data["value"],
                            comment=req_data["comment"], trans_type=req_data["trans_type"])
    db.session.add(new_trans)
    db.session.commit()
    flash(f"Transaction {new_trans.name} added successfully", "success")
    return redirect(url_for('project_data', id=req_data["project_id"]))


@app.route('/delete_transaction', methods=["GET"])
@login_required
def delete_transaction():
    user_id = current_user.id
    trans_id = request.args.get('trans_id')
    trans = Transaction.query.filter_by(id=trans_id).first()
    project = Project.query.filter_by(id=trans.project_id).first()
    if not project or project.user_id != user_id:
        flash("Project not found", "error")
        return redirect(url_for('project'))
    db.session.delete(trans)
    db.session.commit()
    flash(f"Income {trans.name} was deleted successfully", "warning")
    return redirect(url_for('project_data', id=project.id))


@app.after_request
def redirect_to_login(response):
    if response.status_code == 401:
        return redirect(url_for("login"))

    return response