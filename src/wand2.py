from flask import Flask
from flask import request
from flask import Response
from flask import stream_with_context
from flask import render_template

from lab.streamer import Streamer

app = Flask( __name__ )

version = '0.1.0'

@app.route('/index')
def index():
    return render_template('index.html')

streamer = Streamer()
@app.route('/stream')
def stream():
    src = request.args.get( 'src', default = 0, type = int )
    return Response(stream_with_context( stream_gen( src ) ), mimetype='multipart/x-mixed-replace; boundary=frame' )


def stream_gen( src ):   
  
    try : 
        
        streamer.run( src )
        
        while True :
            
            frame = streamer.bytescode()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
                    
    except GeneratorExit :
        #print( '[wandlab]', 'disconnected stream' )
        streamer.stop()

if __name__ == '__main__' :
    
    print('------------------------------------------------')
    print('Wandlab CV - version ' + version )
    print('------------------------------------------------')
    app.run( host='192.168.1.143', port=5000 )
