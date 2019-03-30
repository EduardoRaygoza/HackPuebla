from flask import Flask, jsonify, render_template, request
import firebase_admin
from firebase_admin import credentials, db

app = Flask(__name__)
cred = credentials.Certificate('credenciales.json')
firebase_admin.initialize_app(cred, {
    'databaseURL' : 'https://hackpuebla-87795.firebaseio.com/'
})
root = db.reference()



@app.route('/')
def hello():
    return render_template('form.html')

@app.route('/result',methods = ['POST', 'GET'])
def apijson():
    if request.method == 'POST':
        #result = jsonify(request.form)
        #new_user = root.child('registers').push(request.form)
        distInicial = request.form.getlist('distanciaInicial')[0]
        distFinal = request.form.getlist('distanciaFinal')[0]
        sonido = request.form.getlist('sonido')[0]
        velocidad = request.form.getlist('velocidad')[0]
        diccionario = {
            'distInicial': distInicial,
            'distFinal': distFinal,
            'sonido': sonido,
            'velocidad': velocidad,
        }
        print(diccionario)
        if Arbol(4,5,120).esIntruso:
            print("intruso detectado")

    #Manejo del json que se recibe de los sensores
    return jsonify(diccionario)

def Arbol(self,horaEntrada,velocidadCaminado,tiempoPermanencia):
    explicacion = {
        esIntruso: False,
        horaEntrada: '',
        velocidadCaminado: '',
        tiempoPermanencia: ''
    }

    if(horaEntrada>=2 and horaEntrada<=4):
        if(velocidadCaminado>=9 and velocidadCaminado<=20):
            if(tiempoPermanencia>=5 and tiempoPermanencia<=120):
                print("welcome home ")
            else:
                print("welcome home")
            
        elif(tiempoPermanencia>=5 and tiempoPermanencia<=120):
            print("welcome home")
        else:
            explicacion.esIntruso = True
            print("stranger signal detected")
        
    elif(velocidadCaminado>=9 and velocidadCaminado<=20):
            if(tiempoPermanencia>=5 and tiempoPermanencia<=120):
                print("welcome home ")
            else:
                explicacion.esIntruso = True
                print("stranger signal detected")
            
    elif(tiempoPermanencia>=5 and tiempoPermanencia<=120):
        explicacion.esIntruso = True
        print("stranger signal detected")
    else:
        explicacion.esIntruso = True
        print("stranger signal detected")
    return explicacion


if __name__ == '__main__':
    app.run('0.0.0.0')