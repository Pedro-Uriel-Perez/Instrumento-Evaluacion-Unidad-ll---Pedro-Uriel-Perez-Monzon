from machine import Pin, PWM, time_pulse_us
import time

# Sensor
trigger = Pin(32, Pin.OUT)
echo = Pin(33, Pin.IN)

# Servos
brazo_der = PWM(Pin(4), freq=50)
brazo_izq = PWM(Pin(15), freq=50)

# LEDs originales
led1 = Pin(13, Pin.OUT)
led2 = Pin(17, Pin.OUT)
led3 = Pin(18, Pin.OUT)

# LEDs adicionales
led4 = Pin(5, Pin.OUT)
led5 = Pin(16, Pin.OUT)
led6 = Pin(19, Pin.OUT)


led7 = Pin(21, Pin.OUT)
led8 = Pin(2, Pin.OUT)



# Inicializar servos y LEDs
brazo_der.duty(20)
brazo_izq.duty(20)

# Apagar todos los LEDs
for led in [led1, led2, led3, led4, led5, led6, led7, led8]:
    led.value(0)
time.sleep(0.5)

def medir_distancia():
    trigger.value(0)
    time.sleep_us(2)
    trigger.value(1)
    time.sleep_us(10)
    trigger.value(0)
    
    try:
        duracion = time_pulse_us(echo, 1, 30000)
        if duracion > 0:
            return (duracion * 0.0343) / 2
        return None
    except:
        return None

def mover_brazos(inicio, fin):
    """Mover ambos brazos simultáneamente"""
    direccion = 1 if fin > inicio else -1
    for duty in range(inicio, fin, direccion):
        brazo_der.duty(duty)
        brazo_izq.duty(duty)
        time.sleep(0.02)

def parpadeo_leds():
    """Efecto de parpadeo rápido - LEDs originales"""
    for _ in range(3):
        led1.value(1)
        led2.value(1)
        led3.value(1)
        time.sleep(0.1)
        led1.value(0)
        led2.value(0)
        led3.value(0)
        time.sleep(0.1)

def efecto_secuencial():
    """Efecto de luces secuencial - LEDs originales"""
    for _ in range(2):
        led1.value(1)
        time.sleep(0.1)
        led1.value(0)
        led2.value(1)
        time.sleep(0.1)
        led2.value(0)
        led3.value(1)
        time.sleep(0.1)
        led3.value(0)

def efecto_escalera():
    """Efecto de escalera con los nuevos LEDs"""
    # Encender uno por uno
    for led in [led4, led5, led6]:
        led.value(1)
        time.sleep(0.1)
    # Apagar uno por uno
    for led in [led6, led5, led4]:
        led.value(0)
        time.sleep(0.1)

def efecto_alternado_nuevo():
    """Efecto alternado con los nuevos LEDs"""
    for _ in range(4):
        led4.value(1)
        led5.value(0)
        led6.value(1)
        time.sleep(0.1)
        led4.value(0)
        led5.value(1)
        led6.value(0)
        time.sleep(0.1)

def efecto_todos():
    """Efecto usando todos los LEDs"""
    todos_leds = [led1, led2, led3, led4, led5, led6, led7, led8]
    # Encender desde el centro
    for i in range(3):
        todos_leds[2-i].value(1)
        todos_leds[3+i].value(1)
        time.sleep(0.1)
    # Apagar desde los extremos
    for i in range(3):
        todos_leds[i].value(0)
        todos_leds[5-i].value(0)
        time.sleep(0.1)

def efecto_ola():
    """Efecto de ola con todos los LEDs"""
    todos_leds = [led1, led2, led3, led4, led5, led6, led7, led8]
    # Ola de ida
    for i in range(len(todos_leds)):
        todos_leds[i].value(1)
        time.sleep(0.1)
        if i > 0:
            todos_leds[i-1].value(0)
    # Ola de vuelta
    for i in range(len(todos_leds)-1, -1, -1):
        todos_leds[i].value(1)
        time.sleep(0.1)
        if i < len(todos_leds)-1:
            todos_leds[i+1].value(0)
    # Apagar el último
    todos_leds[0].value(0)

def apagar_leds():
    """Apagar todos los LEDs"""
    for led in [led1, led2, led3, led4, led5, led6, led7, led8 ]:
        led.value(0)

def brazos_arriba():
    """Subir brazos con todos los efectos"""
    print("¡Brazos arriba!")
    parpadeo_leds()      # Efecto original
    efecto_escalera()
    mover_brazos(20, 50)
    efecto_todos()       # Efecto con todos
    efecto_ola()         # Efecto final
    # Mantener todos encendidos
    for led in [led1, led2, led3, led4, led5, led6, led7, led8]:
        led.value(1)

def brazos_abajo():
    """Bajar brazos con todos los efectos"""
    print("Brazos abajo...")
    efecto_alternado_nuevo()
    mover_brazos(50, 20)
    efecto_secuencial()
    efecto_todos()
    apagar_leds()

print("Iniciando Oogie Boogie - Versión Completa")
print("Esperando movimiento...")

brazos_levantados = False
ultimo_movimiento = time.time()

while True:
    try:
        distancia = medir_distancia()
        tiempo_actual = time.time()
        
        if distancia is not None:
            print("Distancia:", distancia, "cm")
            
            if tiempo_actual - ultimo_movimiento >= 1:
                if distancia < 50 and not brazos_levantados:
                    brazos_arriba()
                    brazos_levantados = True
                    ultimo_movimiento = tiempo_actual
                    
                elif distancia >= 50 and brazos_levantados:
                    brazos_abajo()
                    brazos_levantados = False
                    ultimo_movimiento = tiempo_actual
        
        time.sleep(0.05)
        
    except Exception as e:
        print("Error:", e)
        brazo_der.duty(20)
        brazo_izq.duty(20)
        apagar_leds()
        time.sleep(0.5)
