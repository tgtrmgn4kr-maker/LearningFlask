import logging
from flask import Flask, url_for, redirect, render_template
from logging.handlers import RotatingFileHandler


app = Flask(__name__)


#The decorator connects the route and the function
@app.route('/index.html')
@app.route('/') #The main page
def index():  #View
    #Logger shows on terminal when its level higher than setLevel
    app.logger.debug("It's a information comes from debugger")      
    app.logger.info('User get into main page')                      
    app.logger.warning('Caution: The API is soon to be abandoned')  
    app.logger.error('Cannot connect to database')                  
    return render_template('index.html')  

@app.route('/about') #Only match /about
def about():
    return 'About us'#Response

@app.route('/faq/') #Match "/faq" and "/faq/" 
def faq():
    return 'FAQ'

@app.route('/users/<user>')
def users(user):
    return render_template('model.html', name=user) #Send parameter 'user' to "model.html"


@app.route('/product/<int:id>')
def product(id):
    return f'#{id} Product display page'

@app.route('/test/<int:point>')
def test(point):
    return render_template('score.html', score=point)
    

@app.route('/best_seller')
def best_sell():
    return redirect(url_for('product', id=109)) #Redirect to /product/109. You can adjust as you need

if __name__ == '__main__':
    app.logger.setLevel(logging.DEBUG) 
    '''
    Messages will not show if its level lower than "DEBUG"
    Showing in terminal
    '''
    
    handler = RotatingFileHandler('app.log', maxBytes= 1<<17, backupCount=3) #Setting the log
    handler.setLevel(logging.WARNING)
    
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s - [%(filename)s:%(lineno)d]') #The format written in app.log
    handler.setFormatter(formatter) #Although nothing wrong occurred, the logger still be written

    app.logger.addHandler(handler) #Add archive function for the app

    app.run(debug=True, host='0.0.0.0', port=80)
    '''
    If you set host as "127.0.0.1", it will be only accessible for local.
    But if you set host as "0.0.0.0", it will be accessible for all devices connected to host
    '''




'''
Information printed by terminal
127.0.0.1 - - [30/Jan/2026 15:40:58] "GET / HTTP/1.1" 200 -
127.0.0.1 - - [30/Jan/2026 15:40:58] "GET /favicon.ico HTTP/1.1" 404 -(There is no icon in favicon.ico)
'''
