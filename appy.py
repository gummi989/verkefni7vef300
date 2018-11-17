from bottle import run, route, get, post, request, template, response, redirect
import os

@route('/')
@get('/login') # or @route('/login')
def login():
    return '''
        <form action="/login" method="post">
            Username: <input name="username" type="text" />
            Password: <input name="password" type="password" />
            <input value="Login" type="submit" />
        </form>
    '''

@post('/login') # or @route('/login', method='POST')
def do_login():
    username = request.forms.get('username')
    password = request.forms.get('password')

    # hér væri hægt að nota csv skrá til að bera saman við notendur og lykilorð
    # harðkóðuð lausn
    if username == "admin" and password == "4321":
        response.set_cookie("account", username, secret='some-secret-key')
        return redirect("/restricted")
    else:
        return "<p>Login failed.</p>"

@route('/restricted')
def restricted_area():
    username = request.get_cookie("account", secret='some-secret-key')
    if username:
        return template("<a href='/logout'>Logout</a><br><br>{{name}}. You are logged in! <br> Welcome to secret page.", name=username)
    else:
        return "You are not logged in. Access denied."

@route('/logout')
def logout():
    response.set_cookie("account", "", secret='some-secret-key', expires=0)
    return redirect('/login')


run(host='0.0.0.0', port=os.environ.get('PORT'), debug=True)
