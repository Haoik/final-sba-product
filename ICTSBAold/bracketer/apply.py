from bracketer import app
from bracketer.subprograms import addteam
from flask import render_template,redirect,url_for,session , request
from bracketer.forms import apply

@app.route('/form', methods=['GET', 'POST'])
def form():
    session.pop('flash', None)
    if 'applyopen' not in session:
        session['applyopen'] = True
    form = apply()
    if form.validate_on_submit() and session['applyopen'] == True:
        addteam(form)
        return redirect(url_for('submitted'))
    elif request.method == 'POST':
        flash = []
        for fieldName, errorMessages in form.errors.items():
            for error in errorMessages:   
                flash.append(error)
        if flash:
            session['flash'] = flash[0]
        
    flash = session.pop('flash', None)
    return render_template('form.html', form = form , flash=flash)
         
@app.route('/success') 
def submitted():
    stuid = session.pop('STUID',None)
    passwords = session.pop('passwords', None)
    return render_template('submitted.html' , stuid = stuid , passwords = passwords)

