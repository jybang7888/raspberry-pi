from flask import Flask, request, render_template, Response, stream_with_context
from threading import Thread
from lab.streamer_1 import Streamer1
from lab.streamer_2 import Streamer2
from lab.streamer_3 import Streamer3
from DB import Database

app = Flask(__name__)

version = '0.1.0'

@app.route('/test')
def test():
    return render_template('jun_test.html')

@app.route('/main')
def main():
    return render_template('main.html')

@app.route('/count')
def count():
    return render_template('count.html')
    
@app.route('/count/<username>')
def count_name(username):
    return render_template('count.html',username=username)

@app.route('/show_record')
def show_record():
    return render_template('show_record.html')

@app.route('/sign_in')
def sign_in():
    return render_template('sign_in.html')

@app.route('/sign_in_wrong')
def sign_in_wrong():
    return render_template('sign_in_wrong.html')

@app.route('/sign_up')
def sign_up():
    return render_template('sign_up.html')

@app.route('/sign_up_wrong')
def sign_up_wrong():
    return render_template('sign_up_wrong.html')

@app.route('/count/index1/<username>')
def index1(username):
    return render_template('count_pushup.html',username=username)
    
@app.route('/index1/result',methods=['GET','POST'])
def index1_r():
    if request.method == 'GET':
        db1 = Database()
        sql = db1.show_1()   
        return render_template('data.html',list=sql)
        
@app.route('/index2')
def index2():
    return render_template('count_squat.html')

@app.route('/index2/result',methods=['GET','POST'])
def index2_r():
    if request.method == 'GET':
        db2 = Database()
        sql = db2.show_2()   
        return render_template('data.html',list=sql)

@app.route('/clock_save.php',methods=['GET','POST'])
def index2_c():
    return render_template('clock_save.php')

@app.route('/index3')
def index3():
    return render_template('count_burpee.html')

streamer1 = Streamer1()
streamer2 = Streamer2()
streamer3 = Streamer3()

@app.route('/stream1')
def stream1():
    src1 = request.args.get('src', default=0, type=int)
    return Response(stream_with_context(stream1_gen(src1)), mimetype='multipart/x-mixed-replace; boundary=frame')

def stream1_gen(src1):
    try:
        streamer2.stop()
        streamer3.stop()
        streamer1.run(src1)
        while True:
            frame = streamer1.bytescode()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    except GeneratorExit:
        print('[wandlab]', 'disconnected stream')
        streamer1.stop()


@app.route('/stream2')
def stream2():
    src2 = request.args.get('src', default=0, type=int)
    return Response(stream_with_context(stream2_gen(src2)), mimetype='multipart/x-mixed-replace; boundary=frame')

def stream2_gen(src2):
    try:
        streamer1.stop()
        streamer3.stop()
        streamer2.run(src2)
        while True:
            frame = streamer2.bytescode()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    except GeneratorExit:
        print('[wandlab]', 'disconnected stream')
        streamer2.stop()

@app.route('/stream3')
def stream3():
    src3 = request.args.get('src', default=0, type=int)
    return Response(stream_with_context(stream3_gen(src3)), mimetype='multipart/x-mixed-replace; boundary=frame')

def stream3_gen(src3):
    try:
        streamer1.stop()
        streamer2.stop()
        streamer3.run(src3)
        while True:
            frame = streamer3.bytescode()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    except GeneratorExit:
        print('[wandlab]', 'disconnected stream')
        streamer3.stop()

if __name__ == '__main__':
    print('------------------------------------------------')
    print('Wandlab CV - version ' + version)
    print('------------------------------------------------')
    
    app.run(host='192.168.1.144',port=5000)
