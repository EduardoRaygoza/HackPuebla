from flask import Flask, jsonify, render_template, request
import firebase_admin
from firebase_admin import credentials, db
from twilio.rest import Client
import datetime

app = Flask(__name__)
cred = credentials.Certificate('credenciales.json')
firebase_admin.initialize_app(cred, {
    'databaseURL' : 'https://hackpuebla-87795.firebaseio.com/'
})
root = db.reference()
account_sid = 'AC0a3be5dbb6651e4b4ce9705aee1c4cc0'
auth_token = 'b5800ed4844663933197be8596141c5e'
client = Client(account_sid, auth_token)


@app.route('/')
def hello():
    return render_template('form.html')

@app.route('/result',methods = ['POST', 'GET'])
def apijson():
    if request.method == 'POST':
        #result = jsonify(request.form)
        new_user = root.child('registers').push(request.form)
        distInicial = int(request.form.getlist('distanciaInicial')[0])
        distFinal = int(request.form.getlist('distanciaFinal')[0])
        sonido = int(request.form.getlist('sonido')[0])
        velocidad = float(request.form.getlist('velocidad')[0])
        diccionario = {
            'distInicial': distInicial,
            'distFinal': distFinal,
            'sonido': sonido,
            'velocidad': velocidad,
        }
        print(diccionario)
        if Arbol(4, velocidad, 121).get('esIntruso'):
            print("intruso detectado")
            #sendText()

    #Manejo del json que se recibe de los sensores
    return jsonify(diccionario)

def Arbol(horaEntrada,velocidadCaminado,tiempoPermanencia):
    explicacion = {
        'esIntruso': False,
        'horaEntrada': '',
        'velocidadCaminado': '',
        'tiempoPermanencia': ''
    }
    if velocidadCaminado <= 0 :
        return explicacion
    if(horaEntrada>=2 and horaEntrada<=4):
        if(velocidadCaminado>=9 and velocidadCaminado<=28):
            if(tiempoPermanencia>=5 and tiempoPermanencia<=120):
                print("welcome home")
            else:
                print("welcome home")
    
        elif(tiempoPermanencia>=5 and tiempoPermanencia<=120):
            print("welcome home")
        else:
            explicacion['esIntruso'] = True
            print("stranger signal detected")
        
    elif(velocidadCaminado>=9 and velocidadCaminado<=20):
            if(tiempoPermanencia>=5 and tiempoPermanencia<=120):
                print("welcome home ")
            else:
                explicacion['esIntruso'] = True
                print("stranger signal detected")
            
    elif(tiempoPermanencia>=5 and tiempoPermanencia<=120):
        explicacion['esIntruso'] = True
        print("stranger signal detected")
    else:
        explicacion.esIntruso = True
        print("stranger signal detected")
    return explicacion

def sendText():
    message = client.messages \
        .create(
        body='Se detecto una anomalia en tu hogar a las ' + str(datetime.datetime.now()) + ' ¿Quieres que llame a la policia?',
        from_='+17242574614',
        to='+524772301826'
        )

if __name__ == '__main__':
    app.run('0.0.0.0')