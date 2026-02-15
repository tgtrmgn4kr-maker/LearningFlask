import logging
from datetime import datetime, timezone
from logging.handlers import RotatingFileHandler
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, url_for, redirect, render_template, request
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tea.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#app.config['SECRET_KEY'] = b'\x9c\x82\xdb\x86\x07\xa9JB\xab\x9f\xe9\x8f\xee0?`C\xf5\x17\x06\xf9\x19[5' # Using os.urandom(24)

db = SQLAlchemy(app)

def init_db():
    with app.app_context():
        db.create_all()

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(100))
    sugar = db.Column(db.String(20))
    extra = db.Column(db.String(200))
    area = db.Column(db.String(20))



# ==================================================================== #
#                      Logs                                            #
# ==================================================================== #
def configure_logging(app):

    # Avoid adding handlers repeatedly
    if app.logger.handlers:
        app.logger.handlers.clear()

    # ========================= #
    #        Error Log          #
    # ========================= #
    error_handler = RotatingFileHandler(
        "error.log",
        maxBytes=1 << 20,  # 1MB
        backupCount=3
    )
    # Information will not be printed if its level lower than "ERROR"
    error_handler.setLevel(logging.ERROR)

    error_formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
    )
    error_handler.setFormatter(error_formatter)

    app.logger.addHandler(error_handler)
    app.logger.setLevel(logging.INFO)

    # ========================= #
    #       Access Log          #
    # ========================= #
    access_logger = logging.getLogger("access")

    access_handler = RotatingFileHandler(
        "access.log",
        maxBytes=1 << 20,
        backupCount=3
    )
    access_handler.setLevel(logging.INFO)

    access_formatter = logging.Formatter(
        "%(asctime)s - %(message)s"
    )
    access_handler.setFormatter(access_formatter)

    access_logger.addHandler(access_handler)
    access_logger.setLevel(logging.INFO)

    # ========================= #
    #   Request Logging Hook    #
    # ========================= #
    @app.after_request
    def log_request(response):
        access_logger.info(
            f'{request.remote_addr} '
            f'"{request.method} {request.path}" '
            f'{response.status_code}'
        )
        return response
    

# ==================================================================== #
#                      Pages                                           #
# ==================================================================== #

# The decorator connects the route and the function
@app.route('/index.html')
@app.route('/')  # The main page
def index():  # View
    # Logger shows on terminal when its level higher than setLevel
    app.logger.debug("It's a information comes from debugger")
    app.logger.info('User get into main page')
    app.logger.warning('Caution: The API is soon to be abandoned')
    app.logger.error('Cannot connect to database')
    return render_template('index.html')


@app.route('/about')  # Only match /about
def about():
    return 'About us'  # Response


@app.route('/faq/')  # Match "/faq" and "/faq/"
def faq():
    return 'FAQ'


@app.route('/users/<user>')
def users(user):
    # Send parameter 'user' to "model.html"
    return render_template('model.html', name=user)


# Convert the attribute of parameter into integer
@app.route('/product/<int:id>')
def product(id):
    return f'#{id} Product display page'


@app.route('/test/<int:point>')
def test(point):
    # score/point --> template/program
    return render_template('score.html', score=point)


@app.route('/tea')
def tea():
    return render_template('tea_form.html')

'''
 In tea_form.html,                                                                    
 <form action="{{ url_for('order')}}" method="POST">                                  
 This attribute specifies order() as the target to submit data with method of "POST"  
'''
@app.route('/tea/order', methods=['POST'])
def order():
    user = request.form.get('user')
    sugar = request.form.get('sugar')
    extra = request.form.getlist('extra')
    area = request.form.get('area')

    new_order = Order(
    user=user,
    sugar=sugar,
    extra=",".join(extra),
    area=area
    )

    db.session.add(new_order)
    db.session.commit()

    return render_template(
        'result.html',
        user=user,
        sugar=sugar,
        extra=extra,
        area=area
    )

@app.route('/orders')
def orders():
    all_orders = Order.query.all()
    return render_template('orders.html', orders=all_orders)



@app.route('/best_seller')
def best_sell():
    # Redirect to /product/109. You can adjust as you need
    return redirect(url_for('product', id=109))


@app.route("/error")
def error():
    return 1 / 0


if __name__ == '__main__':

    configure_logging(app)

    app.run(debug=True, host='0.0.0.0', port=80)
    '''
    If you set host as "127.0.0.1", it will be only accessible for local.
    But if you set host as "0.0.0.0", it will be accessible for all devices connected to host
    '''

'''
Information printed by terminal
127.0.0.1 - - [30/Jan/2026 15:40:58] "GET / HTTP/1.1" 200 -
127.0.0.1 - - [30/Jan/2026 15:40:58] "GET /favicon.ico HTTP/1.1" 404 -(There was no icon in favicon.ico)
'''
