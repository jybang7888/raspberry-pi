from flask import Flask, render_template, Response, stream_with_context
from threading import Thread
from lab.streamer import Streamer

app = Flask(__name__)
app_2 = Flask(__name__)

version = '0.1.0'

@app.route('/index')
def index():
    return render_template('index.html')

streamer = Streamer()

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

def run_app(app, port):
    app.run(host='192.168.1.144', port=port)

if __name__ == '__main__':
    print('------------------------------------------------')
    print('Wandlab CV - version ' + version)
    print('------------------------------------------------')
    
    # 멀티쓰레딩으로 두 개의 애플리케이션을 동시에 실행
    thread_app1 = Thread(target=run_app, args=(app, 5000))
    thread_app2 = Thread(target=run_app, args=(app_2, 7000))

    thread_app1.start()
    thread_app2.start()
    
    # 두 쓰레드가 종료될 때까지 대기
    thread_app1.join()
    thread_app2.join()
