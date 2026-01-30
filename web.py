import logging
from flask import Flask, url_for, redirect
from logging.handlers import RotatingFileHandler


app = Flask(__name__)



#The decorator connects the route and the function
@app.route('/') #The main page
def index():  #View
    #Logger shows on terminal when its level higher than setLevel
    app.logger.debug("It's a information comes from debugger")      
    app.logger.info('User get into main page')                      
    app.logger.warning('Caution: The API is soon to be abandoned')  
    app.logger.error('Cannot connect to database')                  
    return "Welcome!"  #Response

@app.route('/about') #Only match /about
def about():
    return 'About us'

@app.route('/faq/') #Match "/faq" and "/faq/" 
def faq():
    return 'FAQ'

@app.route('/product/<int:id>')
def product(id):
    return f'#{id} Product display page'

@app.route('/best_seller')
def best_sell():
    return redirect(url_for('product', id=109)) #Redirect to /product/109

if __name__ == '__main__':
    app.logger.setLevel(logging.DEBUG) 
    '''
    Messages will not show if its level lower than "DEBUG"
    Showing in terminal
    '''
    
    handler = RotatingFileHandler('app.log', maxBytes= 128*1024, backupCount=3) #Setting the log
    handler.setLevel(logging.WARNING)
    
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s - [%(filename)s:%(lineno)d]') #The format written in app.log
    handler.setFormatter(formatter)

    app.logger.addHandler(handler) #Add archive function for the app

    app.run(debug=True, host='0.0.0.0', port=80)



'''
Information printed by terminal
127.0.0.1 - - [30/Jan/2026 15:40:58] "GET / HTTP/1.1" 200 -
127.0.0.1 - - [30/Jan/2026 15:40:58] "GET /favicon.ico HTTP/1.1" 404 -(There is no icon in favicon.ico)
'''
