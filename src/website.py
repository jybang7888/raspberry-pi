from flask import Flask, render_template

app = Flask(__name__)

version = '0.1.0'

@app.route('/index')
def index():
    return render_template('index.html')

def run_app(app, port):
    app.run(host='192.168.1.144', port=port)

if __name__ == '__main__':
    print('------------------------------------------------')
    print('Wandlab CV - version ' + version)
    print('------------------------------------------------')

    # 멀티쓰레딩으로 애플리케이션 실행
    thread_app1 = Thread(target=run_app, args=(app, 7000))
    thread_app1.start()

    # 두 쓰레드가 종료될 때까지 대기
    thread_app1.join()
