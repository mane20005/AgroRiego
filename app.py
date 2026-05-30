import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import random  # Simula la API de clima para la demostración

# --- BASE DE DATOS INTERNA DE ETAPAS ---
ETAPAS_CULTIVOS = {
    "Soya": [
        {"max_dias": 20, "estado": "Inicial", "riego_critico": False},
        {"max_dias": 50, "estado": "Vegetativo", "riego_critico": False},
        {"max_dias": 90, "estado": "Floración y Llenado", "riego_critico": True},
        {"max_dias": 120, "estado": "Maduración", "riego_critico": False, "suspender": True}
    ],
    "Caña": [
        {"max_dias": 30, "estado": "Brotación", "riego_critico": False},
        {"max_dias": 120, "estado": "Macollaje", "riego_critico": False},
        {"max_dias": 270, "estado": "Gran Crecimiento", "riego_critico": True},
        {"max_dias": 360, "estado": "Maduración", "riego_critico": False, "suspender": True}
    ]
}

# --- FUNCIONES DE LA LOGICA ---

def registrar_riego():
    """Captura automáticamente fecha y hora al presionar el botón"""
    ahora = datetime.now()
    fecha = ahora.strftime("%Y-%m-%d")
    hora = ahora.strftime("%H:%M:%S")
    
    # Insertar en la tabla visual de la interfaz
    tabla_riegos.insert("", "end", values=(fecha, hora))
    messagebox.showinfo("Éxito", f"Riego registrado automáticamente:\nFecha: {fecha}\nHora: {hora}")

def calcular_prediccion():
    """Calcula la decisión de la IA basada en el cultivo y el clima"""
    tipo_cultivo = combo_cultivo.get()
    fecha_str = entry_fecha.get()
    
    try:
        # Validar el formato de fecha que ingresó el usuario
        fecha_siembra = datetime.strptime(fecha_str, "%Y-%m-%d").date()
        dias_transcurridos = (datetime.now().date() - fecha_siembra).days
    except ValueError:
        messagebox.showerror("Error", "Por favor use el formato de fecha AAAA-MM-DD")
        return

    # Simulación de la API de clima (Probabilidad de lluvia entre 10% y 90%)
    probabilidad_lluvia = random.randint(10, 90)
    
    # Buscar la etapa del cultivo
    etapa_actual = None
    for etapa in ETAPAS_CULTIVOS[tipo_cultivo]:
        if dias_transcurridos <= etapa["max_dias"]:
            etapa_actual = etapa
            break

    # Mostrar variables analizadas en la interfaz
    lbl_analisis.config(
        text=f"Analizando: {tipo_cultivo} ({dias_transcurridos} días de vida)\n"
             f"Pronóstico del Clima: {probabilidad_lluvia}% de probabilidad de lluvia"
    )

    # Lógica de decisión
    if not etapa_actual:
        lbl_resultado.config(text="RECOMENDACIÓN: El ciclo del cultivo ya finalizó.", fg="gray")
    elif etapa_actual.get("suspender"):
        lbl_resultado.config(
            text=f"❌ NO REGAR\nCultivo en {etapa_actual['estado']}.\nSe debe estresar la planta antes de la cosecha.", 
            fg="red"
        )
    elif probabilidad_lluvia > 55:
        lbl_resultado.config(
            text=f"❌ NO REGAR\nProbabilidad de lluvia alta ({probabilidad_lluvia}%).\nAproveche el agua de lluvia.", 
            fg="red"
        )
    elif etapa_actual["riego_critico"]:
        lbl_resultado.config(
            text=f"🚨 SÍ REGAR INDISPENSABLE\nCultivo en {etapa_actual['estado']}.\nFase crítica de alta demanda hídrica.", 
            fg="green"
        )
    else:
        lbl_resultado.config(
            text=f"⚠️ RIEGO MODERADO / OPCIONAL\nCultivo en {etapa_actual['estado']}.\nSin alertas climáticas.", 
            fg="orange"
        )

# --- CONFIGURACIÓN DE LA INTERFAZ GRÁFICA (TKINTER) ---
ventana = tk.Tk()
ventana.title("AgroRiego Santa Cruz - Prototipo Hackatón")
ventana.geometry("500x650")
ventana.resizable(False, False)

# Título Principal
lbl_titulo = tk.Label(ventana, text="🌾 Sistema de Riego Inteligente", font=("Arial", 16, "bold"))
lbl_titulo.pack(pady=10)

# SECCIÓN 1: REGISTRO DE SIEMBRA
frame_siembra = tk.LabelFrame(ventana, text=" 1. Registro de Siembra ", padx=10, pady=10)
frame_siembra.pack(fill="x", padx=15, pady=5)

tk.Label(frame_siembra, text="Tipo de Cultivo:").grid(row=0, column=0, sticky="w", pady=5)
combo_cultivo = ttk.Combobox(frame_siembra, values=["Soya", "Caña"], state="readonly")
combo_cultivo.current(0)
combo_cultivo.grid(row=0, column=1, pady=5, padx=5)

tk.Label(frame_siembra, text="Fecha Siembra (AAAA-MM-DD):").grid(row=1, column=0, sticky="w", pady=5)
entry_fecha = tk.Entry(frame_siembra)
entry_fecha.insert(0, datetime.now().strftime("%Y-%m-%d"))  # Pone la fecha de hoy por defecto
entry_fecha.grid(row=1, column=1, pady=5, padx=5)

# SECCIÓN 2: REGISTRO DE RIEGO
frame_riego = tk.LabelFrame(ventana, text=" 2. Control de Riego en Campo ", padx=10, pady=10)
frame_riego.pack(fill="x", padx=15, pady=5)

btn_riego = tk.Button(frame_riego, text="💧 REGISTRAR RIEGO ACTUAL", font=("Arial", 10, "bold"), bg="#4CAF50", fg="white", command=registrar_riego)
btn_riego.pack(fill="x", pady=5)

# Tabla para mostrar el historial de riegos automáticos
tabla_riegos = ttk.Treeview(frame_riego, columns=("Fecha", "Hora"), show="headings", height=4)
tabla_riegos.heading("Fecha", text="Fecha de Riego")
tabla_riegos.heading("Hora", text="Hora Automática")
tabla_riegos.column("Fecha", width=120, anchor="center")
tabla_riegos.column("Hora", width=120, anchor="center")
tabla_riegos.pack(fill="x", pady=5)

# SECCIÓN 3: PREDICCIÓN CON IA
frame_ia = tk.LabelFrame(ventana, text=" 3. Inteligencia de Riego ", padx=10, pady=10)
frame_ia.pack(fill="both", expand=True, padx=15, pady=5)

btn_ia = tk.Button(frame_ia, text="🤖 CALCULAR PREDICCIÓN", font=("Arial", 11, "bold"), bg="#2196F3", fg="white", command=calcular_prediccion)
btn_ia.pack(fill="x", pady=5)

lbl_analisis = tk.Label(frame_ia, text="Presione el botón para evaluar las condiciones.", font=("Arial", 9, "italic"), fg="gray")
lbl_analisis.pack(pady=5)

lbl_resultado = tk.Label(frame_ia, text="Esperando datos...", font=("Arial", 12, "bold"), justify="center")
lbl_resultado.pack(pady=10)

# Arrancar la aplicación
ventana.mainloop()
