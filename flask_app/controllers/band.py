from flask import render_template,redirect,session,request, flash
from flask_app import app
from flask_app.models.bands import Bands
from flask_app.models.user import User
import json


@app.route('/new/bands')
def new_bands():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":session['user_id']
    }
    return render_template('new_bands.html',user=User.get_by_id(data))


@app.route('/create/bands',methods=['POST'])
def create_bands():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Bands.validate_bands(request.form):
        return redirect('/new/bands')
    data = {
        "name": request.form["name"],
        "Founding": request.form["Founding"],
        "Genre": request.form["Genre"],
        "user_id": session["user_id"]
    }
    Bands.save(data)
    return redirect('/dashboard')

@app.route('/edit/bands/<int:bands_id>')
def edit_bands(bands_id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":bands_id
    }
    user_data = {
        "id":session['user_id']
    }
    return render_template("edit_bands.html",edit=Bands.get_one(data),user=User.get_by_id(user_data))

@app.route('/update/bands',methods=['POST'])
def update_bands():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Bands.validate_bands(request.form):
        return redirect('/new/bands')
    data = {
        "name": request.form["name"],
        "Founding": request.form["Founding"],
        "Genre": request.form["Genre"],
        "id": request.form['id']
    }
    Bands.update(data)
    return redirect('/dashboard')



@app.route('/mybands/')
def show_bands():
    if 'user_id' not in session:
        return redirect('/logout')
    user_data = {
        "id":session['user_id']
    }
    return render_template("show_bands.html",bands=Bands.getBands_by_user(user_data), user=User.get_by_id(user_data))


@app.route('/destroy/bands/<int:id>')
def destroy_bands(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    Bands.destroy(data)
    return redirect('/dashboard')

@app.route('/saveJoin/<int:id>')
def save_join(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id,
        "user":session['user_id']
    }
    Bands.saveJoin(data)
    return redirect('/dashboard')

@app.route('/quitJoin/<int:bands_id>')
def quit_join(bands_id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":bands_id,
        "user":session['user_id']
    }
    Bands.quitJoin(data)
    return redirect('/dashboard')