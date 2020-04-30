from flask import Flask, url_for, render_template, request
from markupsafe import escape
from APP import app
from APP import scrape
import copy
from summarize_model.Prediction import prediction
import jsonify

from flask import flash, redirect
from APP.form import RegistrationForm, LoginForm

urls =[]
data = []



@app.route('/', methods =['POST', 'GET'] )
def home():
    # for key, value in request.form.items():
    #     print(key, ':',  value)
    if request.method == 'POST':
        if 'url' in request.form.keys():
            if request.form['url'] not in urls and request.form['url']:
                urls.append(request.form['url'])  
        elif 'Delete' in request.form.keys():
            print(urls)
            print(request.form['Delete'])
            deleter = request.form['Delete']
            if deleter in urls:
                print(True)
                urls.remove(deleter)
    if request.method == 'GET':
        data.clear()
        urls.clear()
    return render_template('home.html', urls=urls)
# def index():
#     return render_template('chart.html')
@app.route('/data_scrape/', methods =['POST', 'GET'])
def Scrape():
    if request.method == 'POST':
        for i, url in enumerate(urls):
            temp_scrape = scrape(url,i)
            if temp_scrape not in data:
                data.append(scrape(url,i))
        tr_urls = copy.copy(urls)
        return render_template('DataDis.html', data= data, tr_urls= tr_urls, range= range(len(tr_urls)))
    return url_for('home')


@app.route('/data_scrape/reviews', methods=['POST', 'GET'])
def Text_Reviews():
    if request.method == 'POST':
        temp_reviews = copy.copy(request.form['Reviews'])
        Reviews = request.form['Reviews'].replace('[', '').replace(']','').replace('"', '').replace(",", ' ').replace("'",'').split('$$$') 
        Reviews = ['    '+str(num+1)+'.'+i for num, i in enumerate(Reviews) if len(i)>1]
        return render_template('reviews_text.html', Reviews= Reviews, temp_reviews=temp_reviews )
    if request.method == 'GET':
        return 'not implement get function'


@app.route('/data_scrape/reviews/summarize', methods=['POST', 'GET'])
def summarize():
    if request.method == 'POST': 
        summarized_Reviews=[]
        Reviews = request.form['Reviews'].replace('[', '').replace(']','').replace('"', '').replace(",", ' ').replace("'",'').split('$$$')
        Reviews = [i for  i in Reviews if len(i)>1]
        for i in Reviews:
            if len(i)>30:
                summarized_Reviews.append(prediction(i))
            else:
                summarized_Reviews.append(i)

        summarized_Reviews = ['    '+str(num+1)+'.'+i  for num, i in enumerate(summarized_Reviews)]
        return render_template('summarize.html', summarized_Reviews =summarized_Reviews)
    return 'no sum_reviews'


@app.route('/data_scrape/reviews/chart', methods=['POST', 'GET'])
def chart():
    if request.method == 'POST': 
        star_ifo = request.form['Star']
        star_ifo = star_ifo.replace('[','').replace(']', '').replace(',', '').split(' ')
        star_ifo = [float(i) for i in star_ifo]
        star_ifo = [j/100 for i,j in enumerate(star_ifo) if i%2!=0]
  
    return render_template('chart.html',  score= star_ifo)
# /////////////////////////////////////////////////////////////////////////
@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash('Account created for {}!'.format(form.username.data), 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)