#!/bin/bash
# Protocolo de Inicio LETY IA - FQC
echo "🛡️ Iniciando Protocolo LETY IA x ElizaOS..."
source bin/activate

# Inicia el Puente de Voz en segundo plano
python3 escuchar_eliza.py & 

# Inicia la Interfaz Gráfica de Velas
python3 lety_app.py

# Al cerrar la interfaz, mata el proceso de voz
kill $!
echo "Búnker en reposo. Todo entra, nada sale."
