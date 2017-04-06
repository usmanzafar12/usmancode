from flask import Flask, render_template, request, redirect, url_for
from flask import jsonify, Blueprint
from sqlalchemy import create_engine
from database_setup import make_db, Item, Category
import logging
from flask import session as login_session

bp_item = Blueprint('item', __name__,
                    template_folder='templates')
session = make_db()


@bp_item.route('/item/create', methods=['GET', 'POST'])
def create_item():
    if session_check():
        return redirect('/login')
    if request.method == 'GET':
        cats = session.query(Category)
        return render_template('createitem.html', cats_view=cats,
                               login_session=login_session)
    else:
        newItem = Item(name=request.form['name'],
                       desc=request.form['description'],
                       category_id=request.form['categories'],
                       user=login_session['id'])
        session.add(newItem)
        session.commit()
        return redirect(url_for('main'))


@bp_item.route('/item/edit/<id>', methods=['GET', 'POST'])
def edit_item(id):
    if session_check():
        return redirect('/login')
    
    if user_check(id):
        return redirect('/error2')       
    
    if request.method == 'GET':
        cats = session.query(Category)
        item = session.query(Item).filter(Item.id == id).one()
        return render_template('edititem.html', cats_view=cats, item_view=item,
                               login_session=login_session)
    if request.method == 'POST':
        item = session.query(Item).filter(Item.id == id).one()
        item.name = request.form['name']
        item.desc = request.form['description']
        item.category_id = request.form['categories']
        session.add(item)
        session.commit()
        return redirect('/item/view/' + str(id))


@bp_item.route('/item/view/<id>')
def view_item(id):
    session_check()
    try:
        item = session.query(Item).filter(Item.id == id).one()
        return render_template('viewitem.html', name=item.name, desc=item.desc,
                               login_session=login_session)
    except:
        return redirect("/error1")


@bp_item.route('/item/delete/<id>')
def delete_item(id):
    if session_check():
        return redirect('/login')
    if user_check(id):
        return redirect('/error2')   
    try:
        item = session.query(Item).filter(Item.id == id).one()
        session.delete(item)
        session.commit()
        return redirect(url_for('main'))
    except:
        return redirect('/error1')


@bp_item.route('/item/view/<id>/json')
def get_item_json(id):
    """ generates a json file when requested """
    if session_check():
        return redirect('/login')
    try:
        i = session.query(Item).filter(Item.id == id).one()
        data = {'name': i.name, 'id': i.id, 'desc': i.desc,
                'category_id': i.category_id, 'user': i.user}
        return jsonify(item=data)
    except:
        return redirect("/error1")

def user_check(post_id):
    item = session.query(Item).filter(Item.id == post_id).one()
    if(item.user == login_session['id']):
        return False
    else:
        return True
    
def session_check():
    """ checks if the id tag was set in the session object or not """
    login_session['path'] = request.path
    if login_session.get('id', False):
        return False
    else:
        return True
