import psutil
import time
import csv
from datetime import datetime

# Configuración
DURACION_MONITOREO = 3600  # Tiempo en segundos (1 hora)
INTERVALO = 1  # Tiempo entre muestras en segundos
NOMBRE_ARCHIVO = "reporte_monitorizacion.csv"

# Crear archivo CSV y escribir encabezados
with open(NOMBRE_ARCHIVO, mode='w', newline='') as archivo:
    escritor = csv.writer(archivo)
    escritor.writerow(["Timestamp", "CPU (%)", "RAM (%)", "Disco (%)", "Red Enviados (KB)", "Red Recibidos (KB)", "Temp CPU (°C)"])

# Registro de datos
inicio = time.time()
print("Iniciando monitoreo...")

while time.time() - inicio < DURACION_MONITOREO:
    # Captura de métricas
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cpu_percent = psutil.cpu_percent(interval=INTERVALO)
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    net = psutil.net_io_counters()
    temp_cpu = psutil.sensors_temperatures().get('coretemp', [])[0].current if psutil.sensors_temperatures() else 'N/A'

    # Conversión de datos
    ram_percent = memory.percent
    disk_percent = disk.percent
    net_sent_kb = net.bytes_sent / 1024
    net_recv_kb = net.bytes_recv / 1024

    # Escribir datos en el archivo CSV
    with open(NOMBRE_ARCHIVO, mode='a', newline='') as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow([timestamp, cpu_percent, ram_percent, disk_percent, net_sent_kb, net_recv_kb, temp_cpu])

print(f"Monitoreo finalizado. Informe guardado en {NOMBRE_ARCHIVO}")
