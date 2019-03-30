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
    #Manejo del json que se recibe de los sensores
    return ''

if __name__ == '__main__':
    app.run('0.0.0.0')