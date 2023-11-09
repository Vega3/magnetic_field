import tkinter as tk
import math
import time
import numpy as np

# Variables para el tiempo
start_time = 0
end_time = 0

# Radio de la circunferencia en metros (supongamos 150 metros)
radio_metros = 350

# Convertir el radio de metros a kilómetros
radio_kilometros = radio_metros / 1000

# Calcular la velocidad lineal en km/h
speed = int(input("Ingresa la velocidad en grados por segundo: "))
velocidad_lineal_km_h = (speed * radio_kilometros * 3.1416) / 180

print(f"Velocidad lineal: {velocidad_lineal_km_h} km/h")

# Función para calcular el campo magnético en un punto específico
def calculate_magnetic_field(Q, L, omega, r, theta, angle, user_point):
    mu_0 = 4 * np.pi * 1e-7
    num_points = 1000
    B = np.array([0.0, 0.0, 0.0])

    for i in range(num_points):
        dtheta = 2 * np.pi / num_points
        angle_i = angle + i * dtheta
        dl = np.array([-L * np.sin(angle_i), L * np.cos(angle_i), 0.0])
        r_vec = np.array([r * np.cos(theta), r * np.sin(theta), 0.0]) - dl
        r_mag = np.linalg.norm(r_vec)
        dl_cross_r = np.cross(dl, r_vec)
        dI = Q * omega * L / num_points  # Pequeño tramo de corriente
        dB = (mu_0 / (4 * np.pi)) * (dI / r_mag**2) * dl_cross_r
        B += dB

    # No actualizamos B aquí, solo calculamos la magnitud y la almacenamos en user_point
    B_mag = np.linalg.norm(B)
    user_point[0] = B_mag


# Ingrese las coordenadas del punto donde desea calcular el campo magnético
x_user = float(input("Ingresa la coordenada x del punto: "))
y_user = float(input("Ingresa la coordenada y del punto: "))

user_point = [0.0]  # Lista para almacenar la magnitud del campo magnético en el punto

theta_degrees = float(input("Ingresa el ángulo theta en grados: "))
theta = math.radians(theta_degrees)  # Convertir de grados a radianes

# Función para rotar la elipse y calcular el campo magnético
def rotate_ellipse(angle):
    global start_time
    global velocidad_lineal_km_h
    
    circle_radius_x = 150
    bar_length = 2 * circle_radius_x
    ellipse_angle = math.radians(angle)
    bar_x0 = 200 - bar_length / 2 * math.cos(ellipse_angle)
    bar_y0 = 200 - bar_length / 2 * math.sin(ellipse_angle)
    bar_x1 = 200 + bar_length / 2 * math.cos(ellipse_angle)
    bar_y1 = 200 + bar_length / 2 * math.sin(ellipse_angle)
    canvas.coords(bar, bar_x0, bar_y0, bar_x1, bar_y1)
    
    if angle == 0:
        start_time = time.time()
    
    new_angle = angle + 1
    
    if new_angle <= 360:
        r = radio_metros
        B = calculate_magnetic_field(1.0, 1.0, math.radians(speed), r, theta, angle, user_point)
        B_mag = user_point[0]
        
        # Imprimir la magnitud del campo magnético en el punto especificado por el usuario
        print(f"Magnitud del campo magnético en el punto ({x_user}, {y_user}) en el ángulo {theta_degrees} grados: {user_point} T")
        
        end_time = time.time()
        time_elapsed = end_time - start_time
        
        window.after(speed, rotate_ellipse, new_angle)
    else:
        end_time = time.time()
        time_elapsed = end_time - start_time
        print(f"Tiempo para una vuelta: {time_elapsed:.2f} segundos")
        print(f"Velocidad lineal: {velocidad_lineal_km_h} km/h")

# Crear una ventana
window = tk.Tk()
window.title("Elipse con Tkinter")
window.geometry("400x600")

# Crear un lienzo (canvas)
canvas = tk.Canvas(window, width=400, height=400, bg="lightblue")
canvas.pack()

# Dibujar el círculo
circle = canvas.create_oval(50, 50, 350, 350, outline="red", width=5)

# Dibujar la elipse (barra)
bar = canvas.create_line(200, 200, 350, 200, fill="black", width=10)

# Dibujar ejes de un plano cartesiano
canvas.create_line(200, 0, 200, 400, fill="black", width=2)  # Eje Y
canvas.create_line(0, 200, 400, 200, fill="black", width=2)  # Eje X

# Flechas y etiquetas
canvas.create_polygon(195, 5, 200, 0, 205, 5, fill="black")  # Flecha superior del eje Y
canvas.create_polygon(395, 195, 400, 200, 395, 205, fill="black")  # Flecha derecha del eje X
canvas.create_text(215, 10, text="Y", font=("Helvetica", 16))
canvas.create_text(385, 215, text="X", font=("Helvetica", 16))

# Flecha para el campo magnético
field_arrow = canvas.create_line(200, 200, 200, 200, fill="blue", width=3)

# Etiqueta para mostrar el tiempo transcurrido
time_label = tk.Label(window, text="Tiempo para una vuelta: 0.00 segundos", font=("Helvetica", 12))
time_label.pack()

# Iniciar la animación de la rotación de la elipse
rotate_ellipse(0)

# Ejecutar la aplicación
window.mainloop()
