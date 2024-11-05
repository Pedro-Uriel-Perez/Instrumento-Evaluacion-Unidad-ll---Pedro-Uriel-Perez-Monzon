import machine
from machine import Pin, PWM, I2C
import ssd1306
import dht
import time

DHT_PIN = 4      # sensor DHT11
SERVO_PIN = 16   # servo motor
BUZZER_PIN = 17  # buzzer

# Configuración de la pantalla OLED
i2c = I2C(0, scl=Pin(22), sda=Pin(21))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# Configuración de componentes
dht_sensor = dht.DHT11(Pin(DHT_PIN, Pin.PULL_UP))  
servo = PWM(Pin(SERVO_PIN))
servo.freq(50)
buzzer = PWM(Pin(BUZZER_PIN))
buzzer.freq(440)

TEMP_CRITICA = 29  # Temperatura critica
HUM_CRITICA = 40   # Humedad critica

# Posiciones del servo
VENTANA_CERRADA = 0   # ventana cerrada
VENTANA_ABIERTA = 90  # ventana abierta

# Notas para la alarma
NOTAS = {
    'C4': 262,
    'E4': 330,
    'G4': 392
}
def map_value(value, in_min, in_max, out_min, out_max):
    return (value - in_min) * (out_max - out_min) // (in_max - in_min) + out_min

def set_servo_angle(angle):
    #Controla la posicion de la ventana
    duty = map_value(angle, 0, 180, 1638, 8192)
    servo.duty_u16(duty)

def activar_alarma():
    #Activa la alarma 
    for nota in [NOTAS['C4'], NOTAS['E4'], NOTAS['G4']]:
        buzzer.freq(nota)
        buzzer.duty_u16(32768)
        time.sleep_ms(200)
        buzzer.duty_u16(0)
        time.sleep_ms(100)

def desactivar_alarma():
    #Desactiva la alarma
    buzzer.duty_u16(0)

def actualizar_oled(temp, hum, estado=""):
    #Actualiza la pantalla OLED
    oled.fill(0)
    oled.text("Invernadero", 0, 0)
    oled.text(f"Temp: {temp}C", 0, 16)
    oled.text(f"Hum: {hum}%", 0, 32)
    if estado:
        oled.text(estado, 0, 48)
    oled.show()

def leer_sensor():
    #Lee el sensor DHT11
    try:
        time.sleep_ms(50)
        dht_sensor.measure()
        time.sleep_ms(50)
        temp = dht_sensor.temperature()
        hum = dht_sensor.humidity()
        
        if temp is not None and hum is not None:
            if 0 <= temp <= 50 and 20 <= hum <= 100:
                return temp, hum
        return None, None
        
    except Exception as e:
        return None, None

def main():
    ventilacion_activa = False
    ultima_alarma = 0
    
    set_servo_angle(VENTANA_CERRADA)  # la ventana comienza cerrada
    
    print("Sistema de Alerta de Invernadero")
    print("Temperatura(°C) | Humedad(%)")
    print("-" * 30)
    
    while True:
        try:
            temperatura, humedad = leer_sensor()  
            if temperatura is not None and humedad is not None:
                
                print(f"{temperatura:^12} | {humedad:^9}")  # Mostramos valores en la consola
                
                condicion_critica = temperatura > TEMP_CRITICA or humedad > HUM_CRITICA    # Verificar condiciones críticas
                
                if condicion_critica:
                    if not ventilacion_activa:
                        print("¡ALERTA! Condiciones críticas")
                        set_servo_angle(VENTANA_ABIERTA)
                        ventilacion_activa = True
                    
                    if time.ticks_diff(time.ticks_ms(), ultima_alarma) > 3000:
                        activar_alarma()
                        ultima_alarma = time.ticks_ms()
                    
                    estado = "!ALERTA!"
                else:
                    if ventilacion_activa:
                        print("Condiciones normales")
                        set_servo_angle(VENTANA_CERRADA)
                        desactivar_alarma()
                        ventilacion_activa = False
                    estado = "Normal"
                
                actualizar_oled(temperatura, humedad, estado)   # Actualizar pantalla OLED
            time.sleep(1)
            
        except Exception as e:
            print("Error:", e)
            time.sleep(1)

if __name__ == "__main__":
    main()
