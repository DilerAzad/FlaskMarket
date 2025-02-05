from market import app, db
from flask import render_template, redirect, url_for, flash, request
from market.models import Item, User
from market.forms import RegisterForm, LoginForm, PurchaseItemForm, SellItemForm
from flask_login import login_user, logout_user, login_required, current_user


@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/market', methods=['GET',"POST"])
@login_required
def market_page():
    purchase_form = PurchaseItemForm()
    selling_form = SellItemForm()

    if request.method == "POST":
        purchased_item = request.form.get('purchased_item')
        p_item_object = Item.query.filter_by(name=purchased_item).first()
        if p_item_object:
            # Purchase Item Logic
            if current_user.can_purchase(p_item_object):
                p_item_object.buy(current_user)
                flash(f"Congratulation! You purchased {p_item_object.name} for {p_item_object.price}$", category='success')
            else:
                flash(f"Unfortunatly, you don't have enoug money to purchase {p_item_object.name} for {p_item_object.price}$ ", category='danger')

        # Sell Item Logic
        sold_item = request.form.get('sold_item')
        s_item_obj = Item.query.filter_by(name=sold_item).first()
        if s_item_obj:
            if current_user.can_sell(s_item_obj):
                flash(f"Conratulation! You sold {s_item_obj.name} back to the Market for {s_item_obj.price}", category='success')
                s_item_obj.sell(current_user)
                
            else:
                flash(f"Something went worng! With sell {s_item_obj.name}", category='danger')

        return redirect(url_for('market_page'))
    

    if request.method == "GET":
        item = Item.query.filter_by(owner = None)
        owned_item = Item.query.filter_by(owner=current_user.id)
        return render_template('market.html', items=item, purchase_form=purchase_form, selling_form = selling_form,  owned_items=owned_item)

@app.route("/register", methods=['GET',"POST"])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_1 = User(username=form.username.data,
                    email_address=form.email_address.data,
                    password=form.password1.data)
         
        db.session.add(user_1)
        db.session.commit()

        login_user(user_1)
        flash(f'Account has been created! {user_1.username}', category='success')
        return redirect(url_for('market_page')) 
     
    if form.errors != {}:
        for er in form.errors.values():
            flash(f'There is an error : {er[0]}', category='danger')

    return render_template('register.html',form=form)

@app.route('/login', methods=['GET','POST'])
def login_page():
    form = LoginForm()

    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username = form.username.data).first()
        if attempted_user and attempted_user.check_password(
            attempted_password=form.password.data
            ):
                login_user(attempted_user)
                flash(f'You have Signed in successfully! {attempted_user.username}', category='success')
                return redirect(url_for('market_page')) 
        
        else:
            flash('Username and password are not matched! Please try again.', category='danger')

    return render_template('login.html',form = form)


@app.route('/logout')
def logout_page():
    logout_user()
    flash('You have been logged out!', category='info')
    return redirect(url_for('home_page'))