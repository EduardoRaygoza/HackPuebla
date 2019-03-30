#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <FirebaseArduino.h>

// Se inicializa la base de datos.
#define FIREBASE_HOST "smart-report-a7c43.firebaseio.com"
#define FIREBASE_AUTH "yPrkD62N92M5YcuMMeQ3TbicWb3z0gqBWPDApHTc"
#define WIFI_SSID "Juan PC"
#define WIFI_PASSWORD "123456789a"

const char* host = "192.168.137.97";
const uint16_t port = 5000;

const int pinAdc = A0;
long distancia = 0;
int distanciaAnt = 0;
void setup() {
  Serial.begin(115200);
  // connect to wifi.
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  Serial.print("connecting");
  while (WiFi.status() != WL_CONNECTED) {
    Serial.print(".");
    delay(500);
  }
  Serial.println();
  Serial.print("connected: ");
  Serial.println(WiFi.localIP());



  // pin D2 es trigger
  pinMode(D2, OUTPUT);
  //pin D3 es echo
  pinMode(D3, INPUT);
  //inicializamos el pin con 0
  digitalWrite(D2, LOW);

}

void loop() {
  
  //delay(100);
  //Serial.print("Distancia: ");
  int datoSensorUltrasonico = SensorUltrasonico();
  delay(1000);
  //Serial.print(datoSensorUltrasonico);
  //Serial.print("\n");
  //delay(10);
  int datoSoundSensor = SoundSensor();
  //Serial.print(datoSoundSensor);
  //Serial.print("\n");
  double velocidad=calcularVelocidad(datoSensorUltrasonico, distanciaAnt);
  distanciaAnt = datoSensorUltrasonico;
  enviarDatosAlServidor(distanciaAnt,datoSensorUltrasonico ,datoSoundSensor,velocidad);
  
}



long SoundSensor() {
  long sum = 0;
  for (int i = 0; i < 32; i++) {
    sum += analogRead(pinAdc);
  }
  sum >>= 5;
  return sum;
}


long SensorUltrasonico() {
  long t; //tiempo que demora en llegar el eco
  int d; //distancia en centimetros

  digitalWrite(D2, HIGH);
  delayMicroseconds(10);          //Enviamos un pulso de 10us
  digitalWrite(D2, LOW);

  t = pulseIn(D3, HIGH); //obtenemos el ancho del pulso
  d = t / 59;
  return d;
  //escalamos el tiempo a una distancia en cm
  //Serial.print(d);
}

//petición POST con los datos de los sensores al servidor
void enviarDatosAlServidor(int distanciaIni,int distanciaFin, int sonido,double velocidad) {
  String post = "distanciaInicial=" + String(distanciaIni) + "&distanciaFinal=" + String(distanciaFin) +
                "&sonido="+String(sonido)+"&velocidad="+String(velocidad);
  HTTPClient http;
  http.begin("http://192.168.137.97:5000/result");
  http.addHeader("Content-Type", "application/x-www-form-urlencoded");
  http.addHeader("Content-Length", String(post.length()));
  http.POST(post);
  http.writeToStream(&Serial);
  http.end();
}

double calcularVelocidad(int distancia1, int distancia2){
  double velocidad=0;
  double distanciaIni=distancia1;
  double distanciaFini=distancia2;
  if(distanciaIni<distanciaFini){
       velocidad=(distanciaFini-distanciaIni);
  }else{
    velocidad=(distanciaIni-distanciaFini);
  }
  return velocidad;
}

