from flask import Flask, request, render_template, Response, stream_with_context
from threading import Thread
from lab.streamer import Streamer

app = Flask(__name__)

version = '0.1.0'

@app.route('/index')
def index():
    return render_template('start_count.html')

streamer = Streamer()
streamer2 = Streamer2()

@app.route('/stream')
def stream():
    src = request.args.get('src', default=0, type=int)
    return Response(stream_with_context(stream_gen(src)), mimetype='multipart/x-mixed-replace; boundary=frame')

def stream_gen(src):
    try:
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
    return Response(stream_with_context(stream_gen(src2)), mimetype='multipart/x-mixed-replace; boundary=frame')

def stream2_gen(src2):
    try:
        streamer2.run(src2)
        while True:
            frame2 = streamer2.bytescode()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame2 + b'\r\n')
    except GeneratorExit:
        print('[wandlab]', 'disconnected stream')
        streamer2.stop()


if __name__ == '__main__':
    print('------------------------------------------------')
    print('Wandlab CV - version ' + version)
    print('------------------------------------------------')
    
    app.run(host='192.168.1.144',port=5000)
