#-----ACCESSIBLE PARKING-----
#NAOMI YAMILE SÁNCHEZ ANDRADE


#CASO: UN CARRO QUE TRANSPORTA A UN PASAJERO CON DISCAPACIDAD DEBE BUSCAR UN LUGAR DE ESTACIONAMIENTO ACCESIBLE PARA QUE
#SU PASAJERO PUEDA BAJAR DEL VEHÍCULO SIN PROBLEMA.

#SE TOMA EN CUENTA QUE:
#-EL CARRO YA SE ENCUENTRA FRENTE A UN LUGAR DE ESTACIONAMIENTO. 
#-LOS ESTACIONAMIENTOS ACCESIBLES (O RESERVADOS) TIENEN SEÑALAMIENTOS EN COLORES AZULES




#LIBS
import RPi.GPIO as GPIO
import time
import cv2
import numpy as np


GPIO.setwarnings(False)


#SENSOR
trig = 5
echo = 6

#MOTORES DERECHA
in1 = 24
in2 = 23
enA = 25

#MOTORES IZQUIERDA
in3 = 17
in4 = 27
enB = 22

temp = 1


#SETUP
GPIO.setmode(GPIO.BCM) #MODO BCM

#SENSOR
GPIO.setup(trig, GPIO.OUT)
GPIO.setup(echo, GPIO.IN)

#MOTORES
#-DERECHA
GPIO.setup(in1, GPIO.OUT)
GPIO.setup(in2, GPIO.OUT)
GPIO.setup(enA, GPIO.OUT)
GPIO.output(in1, GPIO.LOW) #AL INICIAR EL PROGRAMA EL OUTPUT DE IN1 E IN2 ES = 0, O LOW
GPIO.output(in2, GPIO.LOW)
pwmA = GPIO.PWM(enA, 1000)

#IZQUIERDA
GPIO.setup(in3, GPIO.OUT)
GPIO.setup(in4, GPIO.OUT)
GPIO.setup(enB, GPIO.OUT)
GPIO.output(in3, GPIO.LOW) #AL INICIAR EL PROGRAMA EL OUTPUT DE IN1 E IN2 ES = 0, O LOW
GPIO.output(in4, GPIO.LOW)
pwmB = GPIO.PWM(enB, 1000)

pwmA.start(20)
pwmB.start(20)


#FUNCION
def forward(): #MOVER MOTORES
    if(temp==1):
        GPIO.output(in1, GPIO.HIGH)
        GPIO.output(in2, GPIO.LOW)
            
        GPIO.output(in3, GPIO.HIGH)
        GPIO.output(in4, GPIO.LOW)
        
    print("ESTACIONANDO...")
            #time.sleep(1)
        

def motorsOff(): #MOTORES EN LOW
    GPIO.output(in1, GPIO.LOW)
    GPIO.output(in2, GPIO.LOW)
    GPIO.output(enA, GPIO.LOW)
    GPIO.output(in3, GPIO.LOW)
    GPIO.output(in4, GPIO.LOW)
    GPIO.output(enB, GPIO.LOW)
    
    print('ESTACIONADO')
    
    #time.sleep(1)
    
#CÁMARA    
cam = cv2.VideoCapture(0)
w  = cam.get(3) # float
h = cam.get(4) # float


#MAIN
while(1):
    
    #BUSCAR COLOR
    # FRAME POR FRAME
    ret, frame = cam.read() #IMAGEN O FRAMES GUARDADOS EN VARIABLE FRAME
    
    #-----RGB-----
    #RANGO AZUL RGB
    blueMin = np.array([10, 0, 0], np.uint8) #AJUSTAR, MAYBE
    blueMax = np.array([255, 0, 0], np.uint8)

    #MASK
    blueMask = cv2.inRange(frame, blueMin, blueMax)
    blueColor = cv2.countNonZero(blueMask) #CONTAR PIXELES != 0
    print(blueColor)

    #MERGE MASK AND ORIGNIAL IMAGE
    blue = cv2.bitwise_and(frame, frame, mask = blueMask)
    
    #cv2.imshow('ORIGINAL', frame)
    cv2.imshow("BLUE MASK", blueMask) #BNW
    cv2.imshow("BLUE", blue)

    
    if blueColor > 36000: #SI LA CANTIDAD DE PIXELES AZULES ES MAYOR
        
        GPIO.output(trig, False)
        print('Midiendo...')
        time.sleep(2)
        
        #SEÑAL
        GPIO.output(trig, True) #SET TRIG HIGH POR 10uS
        time.sleep(0.00001) #
        GPIO.output(trig, False) #SET TRIG LOW
        
        #TIEMPO INICIO PULSO
        while GPIO.input(echo)==0:
            pulseStart = time.time() #TIMESTAMP CUANDO PIN ECHO = 0      
                    
        #TIEMPO FIN PULSO                
        while GPIO.input(echo)==1:
            pulseEnd = time.time()   #TIMESTAMP CUANDO PIN ECHO = 1
                                   
                
        pulseDuration = pulseEnd - pulseStart #DURACIÓN DE PULSO
        
        
        #SPEED = DISTANCE/TIME ; SOUND SPEED = 343M/S = 34300 CM/S
        #PARA SENSOR US, EL TIEMPO ES DE IDA Y VUELTA DE PULSO: SPEED = (DISTANCE)/(TIME/2)
        #17150 = DISTANCE/TIME
        #DISTANCE = 17150*TIME
        
        dist = pulseDuration * 17150 
        dist = round(dist, 2) #REDONDEAR 2 DECIM 
        print('Distancia: ', dist, 'cm')
        
        #-----SENSOR
        
        
        #MOVER MOTORES
        d = dist #ADAPTAR PARA VARS DE SENDOR US, CREO K PARA 
        
        if d >= 6.50: #conviene if o while??
            forward()    
                #GPIO.output(in1, GPIO.HIGH)
                #GPIO.output(in2, GPIO.LOW)
                #GPIO.output(in3, GPIO.HIGH)
                #GPIO.output(in4, GPIO.LOW)
                #print("FORWARD")
        else:
            motorsOff()
    
    else:
        print("Seguir buscando")
    

#MOVER MOTORES
#LEER DISTANCIA
#SI DISTANCIA >= x, AVANZA. DISTANCIA <=Y, STOP

