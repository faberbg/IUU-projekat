from flask import Flask, render_template, Response, request, send_from_directory
from kamera import VideoCamera
import os
import motor

pi_camera = VideoCamera(flip=False) # flip pi camera if upside down.
z,e,t=motor.setup()
# App Globals (do not edit)
app = Flask(__name__)

@app.route('/')
def index():
    dis = motor.distance(e,t)
    poruka = "Zona je bezbedna"
    if(dis >20):
        
        
        poruka="Zona je bezbedna"
        
    else:
        poruka="OPREZ! NEKO JE U OPASNOJ ZONI"
        motor.pokreni(z)
        motor.zvuk2()
        
    templateData = {
      'poruka' : poruka
      }
    return render_template('index.html', **templateData) #you can customze index.html here

def gen(camera):
    #get camera frame
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(pi_camera),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

# Take a photo when pressing camera button
@app.route('/picture')
def take_picture():
    pi_camera.take_picture()
    return "None"

@app.route('/klikupali')
def upali():
    motor.pokreni(z)
    motor.zvuk1()
    
    
@app.route('/klikugasi')
def ugasi():
    
    motor.prekini(z)
    

if __name__ == '__main__':

    app.run(host='0.0.0.0', debug=False)

