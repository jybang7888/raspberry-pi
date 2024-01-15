from flask import Flask, render_template
from threading import Thread

app = Flask(__name__)

version = '0.1.0'

@app.route('/index')
def index():
    return render_template('start_count.html')

@app.route('/web')
def web():
    return 'Hi'

if __name__ == '__main__':
    print('------------------------------------------------')
    print('Wandlab CV - version ' + version)
    print('------------------------------------------------')

    app.run(host='192.168.1.144',port=7000)
