import tkinter as tk
from tkinter import messagebox
import yfinance as yf
import pandas as pd
import mplfinance as mpf
from datetime import datetime
import os
from PIL import Image, ImageTk
from gtts import gTTS
import pygame
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# --- CONFIGURACIÓN ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RUTA_IMAGEN = os.path.join(BASE_DIR, "fondo_lety_ia.png")
RUTA_BITACORA = os.path.join(BASE_DIR, "bitacora_velas.csv")
RUTA_MARCA = os.path.join(BASE_DIR, "marca_agua_fqc.png") # <--- Nueva Ruta

pygame.mixer.init()

def hablar(texto):
    try:
        archivo_audio = os.path.join(BASE_DIR, "temp_voz.mp3")
        tts = gTTS(text=texto, lang='es')
        tts.save(archivo_audio)
        pygame.mixer.music.load(archivo_audio)
        pygame.mixer.music.play()
    except: pass

def obtener_datos_vela():
    try:
        ticker = yf.Ticker("BTC-USD")
        hist = ticker.history(period="1d", interval="1m")
        if hist.empty: return None
        ultima = hist.iloc[-1]
        # Simulamos variación para el cuerpo de la vela
        return {
            "Date": datetime.now(),
            "Open": ultima['Open'] * 0.9998,
            "High": ultima['High'] * 1.0002,
            "Low": ultima['Low'] * 0.9997,
            "Close": ultima['Close']
        }
    except: return None

def ejecutar_analisis():
    datos = obtener_datos_vela()
    if datos:
        df_nuevo = pd.DataFrame([datos])
        if not os.path.isfile(RUTA_BITACORA):
            df_nuevo.to_csv(RUTA_BITACORA, index=False)
        else:
            df_nuevo.to_csv(RUTA_BITACORA, mode='a', header=False, index=False)
        
        hablar(f"Luis, análisis completo. Bitcoin en {int(datos['Close'])}.")
        actualizar_grafica_velas()
    else:
        messagebox.showerror("Búnker Offline", "No hay conexión.")

def actualizar_grafica_velas():
    for widget in frame_grafica.winfo_children(): widget.destroy()
    if os.path.exists(RUTA_BITACORA):
        try:
            df = pd.read_csv(RUTA_BITACORA)
            df['Date'] = pd.to_datetime(df['Date'])
            df.set_index('Date', inplace=True)
            df = df.tail(15)

            mc = mpf.make_marketcolors(up='#00FFFF', down='#FF0000', edge='inherit', wick='inherit', volume='in')
            s  = mpf.make_mpf_style(marketcolors=mc, facecolor='#101010', gridcolor='#222222', edgecolor='#00FFFF')

            fig, axlist = mpf.plot(df, type='candle', style=s, figsize=(4.5, 3), 
                                   returnfig=True, xrotation=20, datetime_format='%H:%M',
                                   update_width_config=dict(candle_width=0.8))
            fig.patch.set_facecolor('#101010') 
            
            canvas_plot = FigureCanvasTkAgg(fig, master=frame_grafica)
            canvas_plot.draw()
            canvas_plot.get_tk_widget().pack()
            plt.close(fig)
        except:
            tk.Label(frame_grafica, text="DATOS DAÑADOS, REGENERANDO...", fg="white", bg="#101010").pack()

# --- INTERFAZ LETY V3.9 (CON MARCA DE AGUA) ---
root = tk.Tk()
root.title("LETY IA - FQC V3.9")
root.geometry("800x650")

canvas = tk.Canvas(root, width=800, height=650, highlightthickness=0)
canvas.pack()

# CARGA DE FONDO Y MARCA DE AGUA
if os.path.exists(RUTA_IMAGEN):
    fondo_img = Image.open(RUTA_IMAGEN).resize((800, 650))
    
    # Intentar poner la marca de agua
    if os.path.exists(RUTA_MARCA):
        marca_img = Image.open(RUTA_MARCA)
        # Pegar en la esquina inferior izquierda (x=10, y=fondo.height - marca.height - 10)
        fondo_img.paste(marca_img, (10, 540), marca_img) # Usar marca_img como máscara de transparencia
        
    img = ImageTk.PhotoImage(fondo_img)
    canvas.create_image(0, 0, image=img, anchor="nw")
    canvas.image = img

# Título y Botones
label_titulo = tk.Label(root, text="SISTEMA LETY - FQC V3.9", fg="#00FFFF", bg="black", font=("Courier", 20, "bold"))
canvas.create_window(400, 60, window=label_titulo)

btn_ejecutar = tk.Button(root, text="GENERAR VELA TÁCTICA", command=ejecutar_analisis, 
                         bg="#00FFFF", fg="black", font=("Arial", 10, "bold"), bd=4)
canvas.create_window(400, 150, window=btn_ejecutar)

btn_exit = tk.Button(root, text="X", command=root.destroy, bg="red", fg="white", font=("Arial", 8, "bold"))
canvas.create_window(780, 20, window=btn_exit)

frame_grafica = tk.Frame(root, bg="#101010")
canvas_window = canvas.create_window(780, 580, window=frame_grafica, anchor="se")

actualizar_grafica_velas()
root.mainloop()
