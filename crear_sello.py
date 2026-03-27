import os
from PIL import Image, ImageDraw, ImageFont

# Configuración
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RUTA_SALIDA = os.path.join(BASE_DIR, "marca_agua_fqc.png")

def crear_marca_agua():
    # Crear una imagen transparente
    img = Image.new('RGBA', (300, 100), (255, 255, 255, 0))
    d = ImageDraw.Draw(img)
    
    try:
        # Intentar cargar una fuente Arial o Roboto, si no, usa la predeterminada
        font = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf", 20)
        font_sub = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf", 12)
    except:
        font = ImageFont.load_default()
        font_sub = ImageFont.load_default()

    # Color Cian Neón (#00FFFF) con opacidad (alfa) de 150 (semi-transparente)
    color_cian = (0, 255, 255, 150)
    color_blanco = (255, 255, 255, 120)

    # Dibujar el texto
    d.text((10, 10), "FQC - LETY IA", fill=color_cian, font=font)
    d.text((10, 40), "PROPIEDAD: LUIS F. SANTIESTEBAN G.", fill=color_blanco, font=font_sub)
    d.text((10, 60), "JALISCO, MÉXICO", fill=color_blanco, font=font_sub)

    # Guardar la imagen
    img.save(RUTA_SALIDA)
    print(f"Marca de agua creada en: {RUTA_SALIDA}")

if __name__ == "__main__":
    crear_marca_agua()
