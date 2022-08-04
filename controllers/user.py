from flask import request, render_template, flash, redirect, url_for, session
from .blueprint import user
from .blueprint import product
from models.user import User

# 회원가입 페이지 API
@user.route('/form')
def form():
    return render_template('user_form.html')

# 회원가입 API
@user.route('/signup', methods=['POST'])
def signup():
    form_data = request.form

    if not form_data['password'] == form_data['password_confirmation']:
        flash("비밀번호가 일치하지 않습니다.")
        return render_template('user_form.html')

    if not User.check_email(form_data['email']):
        flash('사용 중인 이메일입니다.')
        return render_template('user_form.html')

    User.insert_one(form_data)
    return redirect(url_for('product.get_products'))

# 로그인 페이지 API
@user.route('/signin')
def signin_forn():
    return render_template('user_signin.html')

# 로그인 API
@user.route('/signin', methods=['POST'])
def signin():
    form_data = request.form
    user = User.sign_in(form_data)

    if not user:
        flash("이메일 주소 또는 비밀번호를 확인해주세요.")
        return render_template('user_signin.html')
    else:
        session['user_id'] = str(user['_id'])
        return redirect(url_for('product.get_products'))

# 로그아웃
@user.route('/signout')
def signout():
    session.pop('user_id', None) # 없애기
    return redirect(url_for('product.get_products'))