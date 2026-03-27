import cv2
import os

# Ruta a tu imagen de fondo
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RUTA_FONDO = os.path.join(BASE_DIR, "fondo_lety_ia.png")
RUTA_ICONO = os.path.join(BASE_DIR, "lety_icon.png")

if not os.path.exists(RUTA_FONDO):
    print(f"Error: No encuentro {RUTA_FONDO}")
    exit()

# Cargar la imagen y recortar la zona del Bitcoin
img = cv2.imread(RUTA_FONDO)
# Ajusta estas coordenadas (y, x) para capturar el Bitcoin en tu imagen
# En tu imagen 800x500, el Bitcoin está abajo a la derecha
# Recortar zona: y from 350 to 480, x from 550 to 680
bitcoin_crop = img[350:480, 550:680] 

# Guardar como icono
cv2.imwrite(RUTA_ICONO, bitcoin_crop)
print(f"Icono creado en {RUTA_ICONO}")
