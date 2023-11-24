import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# Función para generar un único id_ubicacion para cada id_usuario
def generar_id_ubicacion_para_usuario():
    return np.random.randint(1, 973)  # 972 ubicaciones posibles

# Función para generar datos aleatorios para un usuario específico
def generar_datos_aleatorios(id_usuario, distancia_acumulada_anterior, fecha_hora_anterior, fuente_registro_anterior, tipo_actividad, id_ubicacion):
    fecha_hora = fecha_hora_anterior + timedelta(seconds=5)

    # Reiniciar la distancia acumulada a 0 para cada usuario
    distancia_acumulada = 0 if fecha_hora.date() != fecha_hora_anterior.date() else distancia_acumulada_anterior

    ritmo_cardiaco = random.randint(80, 160)
    velocidad = round(random.uniform(5, 15), 2)
    distancia = round(velocidad * random.uniform(0.5, 2.0), 2)  # Distancia aleatoria basada en velocidad
    distancia_acumulada += distancia

    # Fuente de registro constante para el mismo usuario durante el mismo día
    fuente_registro = fuente_registro_anterior if fecha_hora.date() == fecha_hora_anterior.date() else random.choice(['Celular', 'Reloj', 'Otros'])

    # Asignar tipo de terreno en función del tipo de actividad
    tipo_terreno = 'Agua' if tipo_actividad == 'Swimming' else 'Tierra'

    # Mapear tipo_actividad a números enteros
    id_tipo_actividad = {
        "Running": 1,
        "Cycling": 2,
        "Swimming": 3,
        "Basketball": 4
    }[tipo_actividad]

    return {
        'fecha_hora': fecha_hora,
        'ritmo_cardiaco': ritmo_cardiaco,
        'velocidad': velocidad,
        'distancia': distancia_acumulada,
        'tipo_terreno': tipo_terreno,
        'fuente_registro': fuente_registro,
        'id_tipo_actividad': id_tipo_actividad,  # Cambiado de 'tipo_actividad' a 'id_tipo_actividad'
        'id_usuario': id_usuario,
        'id_ubicacion': id_ubicacion
    }, distancia_acumulada, fecha_hora, fuente_registro

# Generar datos aleatorios para múltiples usuarios y almacenar en un DataFrame
num_usuarios = 100
num_registros_por_usuario = 500
datos = []
id_ubicacion_por_usuario = {id_usuario: generar_id_ubicacion_para_usuario() for id_usuario in range(1, num_usuarios + 1)}
fecha_hora_anterior_por_usuario = {id_usuario: datetime.now() for id_usuario in range(1, num_usuarios + 1)}
fuente_registro_anterior_por_usuario = {id_usuario: random.choice(['Celular', 'Reloj', 'Otros']) for id_usuario in range(1, num_usuarios + 1)}

for usuario in range(1, num_usuarios + 1):
    distancia_acumulada_anterior = 0  # Reiniciar distancia acumulada para cada usuario
    tipo_actividad_usuario = random.choice(["Running", "Cycling", "Swimming", "Basketball"])
    id_ubicacion = id_ubicacion_por_usuario[usuario]  # Obtener el id_ubicacion para este usuario
    for _ in range(num_registros_por_usuario):
        registro, distancia_acumulada_anterior, fecha_hora_anterior, fuente_registro_anterior = generar_datos_aleatorios(
            usuario, distancia_acumulada_anterior, 
            fecha_hora_anterior_por_usuario[usuario], fuente_registro_anterior_por_usuario[usuario],
            tipo_actividad_usuario, id_ubicacion  # Pasar el tipo de actividad y el id_ubicacion
        )
        datos.append(registro)
        fecha_hora_anterior_por_usuario[usuario] = fecha_hora_anterior
        fuente_registro_anterior_por_usuario[usuario] = fuente_registro_anterior

df = pd.DataFrame(datos)

# Mostrar el DataFrame
print(df)
df.to_csv('datos_simulados.csv', index=False)