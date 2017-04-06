from item import *


bp_cat = Blueprint('category', __name__, template_folder='templates')
session = make_db()


@bp_cat.route('/category/create', methods=['GET', 'POST'])
def create_category():
    if session_check():
        return redirect('/login')
    try:
        if request.method == 'GET':
            return render_template('createcategory.html',
                                   login_session=login_session)
        elif request.method == 'POST':
            cat = Category(name=request.form['name'])
            session.add(cat)
            session.commit()
            return redirect('/')
    except:
        return redirect("/error")


@bp_cat.route('/category/edit/<id>', methods=['GET', 'POST'])
def edit_category(id):
    if session_check():
        return redirect('/login')
    try:
        if request.method == 'GET':
            cat = session.query(Category).filter(Category.id == id).one()
            return render_template('editcat.html', cat_view=cat,
                                   login_session=login_session)
        elif request.method == 'POST':
            cat = session.query(Category).filter(Category.id == id).one()
            cat.name = request.form['name']
            session.add(cat)
            session.commit()
            return redirect('/category/view/' + str(id))
    except:
        return redirect("/error")


@bp_cat.route('/category/view/<id>', methods=['GET'])
def view_category(id):
    session_check()
    try:
        cats = session.query(Category).all()
        cat_items = session.query(Item).filter(Item.category_id == id)
        main_cat = session.query(Category).filter(Category.id == id).one()
        index = cats.index(main_cat)
        return render_template('viewcategory.html', categories=cats,
                               items=cat_items, login_session=login_session,
                               index=index)
    except:
        return redirect("/error")


@bp_cat.route('/category/delete/<id>')
def delete_category(id):
    if session_check():
        return redirect('/login')
    if cat_user_check(id):
        return redirect('/error3')
    try:
        items = session.query(Item).filter(Item.category_id == id)
        items.delete()
        cat = session.query(Category).filter(Category.id == id).one()
        session.delete(cat)
        session.commit()
        return redirect(url_for('main'))
    except:
        return redirect("/error")


def cat_user_check(id):
    other_items = session.query(Item).\
                  filter(Item.category_id == id,
                         Item.user != login_session['id']).all()
    if not other_items:
        return False
    else:
        return True
