import os
import time
import json
from gtts import gTTS
import pygame
from datetime import datetime

# --- CONFIGURACIÓN TÁCTICA ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RUTA_RESPUESTA_ELIZA = os.path.join(BASE_DIR, "eliza_output.json") 
RUTA_LOG = os.path.join(BASE_DIR, "auditoria_fqc.log") # <--- El archivo de registro
pygame.mixer.init()

def registrar_evento(mensaje):
    """Guarda el mensaje con timestamp en el log del búnker"""
    ahora = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    entrada = f"{ahora} [FQC-SYSTEM]: {mensaje}\n"
    with open(RUTA_LOG, "a", encoding="utf-8") as f:
        f.write(entrada)

def hablar(texto):
    try:
        archivo_audio = os.path.join(BASE_DIR, "temp_eliza.mp3")
        tts = gTTS(text=texto, lang='es')
        tts.save(archivo_audio)
        pygame.mixer.music.load(archivo_audio)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            time.sleep(0.1)
    except Exception as e:
        print(f"Error de audio: {e}")

def monitorear_eliza():
    print("🛡️ LETY IA: Escuchando a ElizaOS y registrando en Log...")
    registrar_evento("SISTEMA OPERATIVO - PROTOCOLO INICIADO")
    ultima_modificacion = 0
    
    while True:
        if os.path.exists(RUTA_RESPUESTA_ELIZA):
            mtime = os.path.getmtime(RUTA_RESPUESTA_ELIZA)
            if mtime > ultima_modificacion:
                try:
                    with open(RUTA_RESPUESTA_ELIZA, 'r') as f:
                        data = json.load(f)
                        mensaje = data.get("text", "")
                        if mensaje:
                            print(f"🎙️ LETY dice: {mensaje}")
                            registrar_evento(mensaje) # <--- Guardar en el log
                            hablar(mensaje)
                except: pass
                ultima_modificacion = mtime
        time.sleep(1)

if __name__ == "__main__":
    monitorear_eliza()
