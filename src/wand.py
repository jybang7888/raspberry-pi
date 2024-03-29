from flask import Flask, request, render_template, Response, stream_with_context
from threading import Thread
from lab.streamer_1 import Streamer1
from lab.streamer_2 import Streamer2
from lab.streamer_3 import Streamer3

app = Flask(__name__)

@app.route('/main')
def main():
    return render_template('main.html')
    
@app.route('/count')
def count_name():
    username = request.args.get('username')
    return render_template('count.html',username=username)

@app.route('/count/index1')
def index1():
    username = request.args.get('username')
    return render_template('count_pushup.html',username=username)
        
@app.route('/count/index2')
def index2():
    username = request.args.get('username')
    return render_template('count_squat.html',username=username)

@app.route('/count/index3')
def index3():
    username = request.args.get('username')
    return render_template('count_burpee.html',username=username)

@app.route('/record')
def record():
    return render_template('record.html')

@app.route('/record_wrong')
def record_wrong():
    return render_template('record_wrong.html')
    
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

@app.route('/sign_up_exist')
def sign_up_exist():
    return render_template('sign_up_exist.html')

@app.route('/ranking')
def ranking():
    return render_template('ranking.html')

streamer1 = Streamer1()
streamer2 = Streamer2()
streamer3 = Streamer3()

@app.route('/stream1')
def stream1():
    src1 = request.args.get('src', default=0, type=int)
    return Response(stream_with_context(stream1_gen(src1)), mimetype='multipart/x-mixed-replace; boundary=frame')

def stream1_gen(src1):
    try:
        streamer1.stop()
        streamer2.stop()
        streamer3.stop()
        streamer1.run(src1)
        while True:
            frame = streamer1.bytescode()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    except GeneratorExit:
        streamer1.stop()


@app.route('/stream2')
def stream2():
    src2 = request.args.get('src', default=0, type=int)
    return Response(stream_with_context(stream2_gen(src2)), mimetype='multipart/x-mixed-replace; boundary=frame')

def stream2_gen(src2):
    try:
        streamer1.stop()
        streamer2.stop()
        streamer3.stop()
        streamer2.run(src2)
        while True:
            frame = streamer2.bytescode()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    except GeneratorExit:
        streamer2.stop()

@app.route('/stream3')
def stream3():
    src3 = request.args.get('src', default=0, type=int)
    return Response(stream_with_context(stream3_gen(src3)), mimetype='multipart/x-mixed-replace; boundary=frame')

def stream3_gen(src3):
    try:
        streamer1.stop()
        streamer2.stop()
        streamer3.stop()
        streamer3.run(src3)
        while True:
            frame = streamer3.bytescode()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    except GeneratorExit:
        streamer3.stop()

if __name__ == '__main__':
    app.run(host='192.168.210.77',port=5000)
