from flask import Flask, request, render_template, Response, stream_with_context
from threading import Thread
from lab.streamer_dont_touch import Streamer
from lab.streamer_2_dont_touch import Streamer2
from lab.streamer_3_dont_touch import Streamer3

app = Flask(__name__)

version = '0.1.0'

@app.route('/index')
def index():
    return render_template('push_up.html')

@app.route('/index2')
def index2():
    return render_template('squat.html')

@app.route('/index3')
def index3():
    return render_template('burpee.html')

streamer = Streamer()
streamer2 = Streamer2()
streamer3 = Streamer3()

@app.route('/stream')
def stream():
    src = request.args.get('src', default=0, type=int)
    return Response(stream_with_context(stream_gen(src)), mimetype='multipart/x-mixed-replace; boundary=frame')

def stream_gen(src):
    try:
        streamer2.stop()
        streamer.run(src)
        while True:
            frame = streamer.bytescode()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    except GeneratorExit:
        print('[wandlab]', 'disconnected stream')
        streamer.stop()


@app.route('/stream2')
def stream2():
    src2 = request.args.get('src', default=0, type=int)
    return Response(stream_with_context(stream2_gen(src2)), mimetype='multipart/x-mixed-replace; boundary=frame')

def stream2_gen(src2):
    try:
        streamer.stop()
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
        streamer.stop()
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