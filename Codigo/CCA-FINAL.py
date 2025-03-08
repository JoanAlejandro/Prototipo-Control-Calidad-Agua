from tcs3200 import TCS3200
from machine import Pin, PWM, ADC, I2C
import time
import ssd1306

tcs3200 = TCS3200(OUT=13 ,S0=27, S1=26, S2=12, S3=14, LED=23)
Sen_Tb_pin=Pin(34,Pin.IN) #entrada tur
i2c = I2C(0, scl=Pin(22), sda=Pin(21))#pines oled
adc=ADC(Sen_Tb_pin, atten=ADC.ATTN_11DB) #atenuacion tur
oled_width = 128
oled_height = 64
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)

bom1=PWM(Pin(25))
bom2=PWM(Pin(18))
motor=PWM(Pin(19))
bom1.freq(500)
bom2.freq(500)
motor.freq(500)


val1_cl=[103, 100, 89]
val2_cl=[76, 59, 54]
val3_cl=[73, 57, 41]
val4_cl=[67, 52, 42]
val5_cl=[88, 74, 61]

val1_ph=[52, 37, 36]
val2_ph=[62, 38, 36]
val3_ph=[69, 43, 38]
val4_ph=[71, 51, 43]
val5_ph=[83, 70, 58]

val_cloro=[6775897, 4100000]
val_ph=[5457466, 3417380]


def rgb_a_hex(color):
    return '#{:02x}{:02x}{:02x}'.format(color[0], color[1], color[2])

def hex_dec(num1, num2):
    return (int(num1, 16) - int(num2, 16))

def compa(valor, lista):
    if lista[0]>valor>lista[1]:
        return True
    else:
        return False

def turbiedad(tur):
    if tur<15:
        return True
    else:
        return False

def bienvenida():#mensaje de bienvenida
    oled.fill(0)  # Limpia la pantalla
    oled.text("Bienvenido", 30, 8)
    oled.text("Control Calidad", 10, 25)
    oled.text("del Agua", 40, 40)
    oled.show()
    
# Pantalla de carga de 0 a 100%
def pantalla_carga():
    oled.fill(0)
    oled.text("Cargando...", 30, 20)
    oled.show()
    
    
def pantalla_tur():
    oled.fill(0)
    oled.text("midiendo", 30, 15)
    oled.text("turbiedad", 28, 22)
    oled.show()
    
def pantalla_cl():
    oled.fill(0)
    oled.text("midiendo", 30, 15)
    oled.text("cloro", 34, 22)
    oled.show()
    
def pantalla_ph():
    oled.fill(0)
    oled.text("midiendo", 30, 15)
    oled.text("ph", 34, 30)
    oled.show()
    
def pantala_datos(tur, cl, ph):
    oled.fill(0)
    if tur==True and cl==True and ph== True:
        oled.text("agua potable", 30, 10)
    else:
        oled.text("agua no potable", 30, 8)
    oled.show()
    
        
def fin():
    oled.fill(0)
    oled.text("fin del analisis", 30, 15)
    oled.show()
    time.sleep(10)
    
    
def iniciacion_colorimetria():
    # Activar el modo de depuración
    tcs3200.debugging = tcs3200.ON

    # Encender los LEDs del sensor
    tcs3200.led = tcs3200.ON

    # Establecer el divisor de frecuencia al 2% y leerlo
    tcs3200.freq_divider = tcs3200.TWO_PERCENT
    print(tcs3200.freq_divider)
    if tcs3200.freq_divider == tcs3200.TWO_PERCENT:
        print("Divisor de frecuencia establecido al 2%")
    else:
        print("Error al establecer el divisor de frecuencia")

    # Establecer el número de ciclos a medir
    tcs3200.cycles = 500
    tcs3200.calibrate()
    black_freq = tcs3200.calib(tcs3200.BLACK)
    print("Frecuencias de calibración para negro:", black_freq)
    white_freq = tcs3200.calib(tcs3200.WHITE)
    print("Frecuencias de calibración para blanco:", white_freq)
    return
        
        
while True:
    bienvenida()
    X=input("Presione la tecla x para iniciar la medicion: ")
    time.sleep(2)
    if X=="x":
        iniciacion_colorimetria()
        time.sleep(2)
        pantalla_carga()
        time.sleep(1)
        pantalla_tur()
        print("tomando tur")
        lectura_sensor=adc.read()
        porcentaje=abs((-0.083333*lectura_sensor)+100)
        time.sleep(1)
        print(porcentaje, "%")
        time.sleep(2)
        resul_tur=turbiedad(porcentaje)
        
        pantalla_cl()
        bomb1.duty(900)
        time.sleep(1)
        bomba1.duty(0)
        
        
        rgb_cloro=tcs3200.rgb
        color_hex_cloro = rgb_a_hex(rgb_cloro)
        color_hex_cloro= color_hex_cloro.replace("#","")
        color_cloro=hex_dec(color_hex_cloro, "000000")
        resul_cl=compa(color_cloro,val_cloro)
        time.sleep(10)
        motor.duty(1023)
        time.sleep(3)
        motor.duty(0)
        
        
        pantala_carga()
        time.sleep(1)
        print("Vuelva a llenar la muestra")
        time.sleep(1)
        Y=input("Presione la tecla x para iniciar la segunda medicion: ")
        time.sleep(2)
        if Y=="x":
            pantalla_ph()
            bomba2.duty(900)
            time.sleep(1)
            bomba2.duty(0)
            rgb_ph=tcs3200.rgb
            color_hex_ph = rgb_a_hex(rgb_ph)
            color_hex_ph = color_hex_ph.replace("#","")
            color_ph=hex_dec(color_hex_ph, "000000")
            resul_ph=compa(color_ph,val_ph)
            time.sleep(10)
            
            motor.duty(1023)
            time.sleep(3)
            motor.duty(0)
            
            pantalla.datos(resul_tur, resul_cl, resul_ph)
            time.sleep(15)
            fin()   
    break







