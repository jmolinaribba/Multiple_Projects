# Gym Tracker App
import sys
import os
import tkinter as tk
import sqlite3
import pandas as pd
import tkinter.ttk as ttk
import matplotlib.pyplot as plt
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

# ==============================
# CONFIGURACIÓN DE RUTAS (PyInstaller Fix)
# ==============================

def obtener_ruta_recurso(ruta_relativa):
    """Devuelve la ruta para archivos de solo lectura empaquetados (CSV, imágenes, iconos)."""
    try:
        # PyInstaller guarda los recursos en la carpeta temporal sys._MEIPASS
        ruta_base = sys._MEIPASS
    except Exception:
        ruta_base = os.path.abspath(".")
    return os.path.join(ruta_base, ruta_relativa)

def obtener_ruta_datos(nombre_archivo):
    """Devuelve la ruta segura para guardar datos persistentes (Base de datos)."""
    if getattr(sys, 'frozen', False):
        # Si estamos ejecutando desde el .exe, guarda la DB al lado del .exe
        ruta_base = os.path.dirname(sys.executable)
    else:
        # Si estamos en desarrollo (.py), guarda al lado del script
        ruta_base = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(ruta_base, nombre_archivo)

# Asignar rutas correctas
CSV_PATH = obtener_ruta_recurso("exercises.csv")
DB_PATH = obtener_ruta_datos("workouts.db")

# Cargar el archivo CSV usando la ruta segura
try:
    df = pd.read_csv(CSV_PATH)
except FileNotFoundError:
    messagebox.showerror("Error Crítico", f"No se encontró el archivo: {CSV_PATH}")
    sys.exit()

# ==============================
# BASE DE DATOS
# ==============================
# Crear conexión y tabla para los entrenamientos
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS workouts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,
    exercise TEXT,
    muscle_group TEXT,
    training_type TEXT,
    difficulty TEXT,
    equipment TEXT,
    sets INTEGER,
    reps INTEGER,
    weight REAL,
    total_reps INTEGER
)
""")
conn.close()

# ==============================
# INTERFAZ GRÁFICA PRINCIPAL
# ==============================
window = tk.Tk()
window.title("Gym Tracker App")
title_label = tk.Label(window, text="Gym Tracker App",
                       font=("Helvetica", 16, "bold"), bg="#3032BB", fg="white")
title_label.grid(row=0, column=0, columnspan=2, pady=(0,10))
window.geometry("400x350")
window.resizable(False,False)
window.configure(padx=20, pady=20)
window.configure(bg="#3032BB")
window.grid_columnconfigure(0, weight=1)
window.grid_columnconfigure(1, weight=1)

# Variables para almacenar inputs
sets_var = tk.StringVar()
reps_var = tk.StringVar()
total_reps_var = tk.StringVar()
exercise_var = tk.StringVar()

# Campos de entrada
exercise_list = df["name"].tolist()
exercise_combo = ttk.Combobox(
    window,
    textvariable=exercise_var,
    values=exercise_list,
    state="readonly"
)
exercise_combo.grid(row=1, column=1)
exercise_label = tk.Label(window, text="Choose Exercise:", font=("Helvetica", 12,"bold"), bg="#3032BB", fg="white")
exercise_label.grid(row=1, column=0)

sets_label = tk.Label(window, text="Sets:", font=("Helvetica", 12,"bold"), bg="#3032BB", fg="white")
sets_label.grid(row=2, column=0)
sets_entry = tk.Entry(window, textvariable=sets_var)
sets_entry.grid(row=2, column=1)

reps_label = tk.Label(window, text="Reps:", font=("Helvetica", 12,"bold"), bg="#3032BB", fg="white")
reps_label.grid(row=3, column=0)
reps_entry = tk.Entry(window, textvariable=reps_var)
reps_entry.grid(row=3, column=1)

weight_label = tk.Label(window, text="Weight (kg):", font=("Helvetica", 12,"bold"), bg="#3032BB", fg="white")
weight_label.grid(row=4, column=0)
weight_entry = tk.Entry(window)
weight_entry.grid(row=4, column=1)

total_reps_label = tk.Label(window, text="Total Reps:", font = ("Helvetica", 12,"bold"), bg="#3032BB", fg="white")
total_reps_label.grid(row=5, column=0)
total_reps_entry = tk.Entry(window, textvariable=total_reps_var, state='readonly')
total_reps_entry.grid(row=5, column=1)

# Calcular repeticiones totales dinámicamente
def calculate_total_reps(*args):
    try:
        sets = int(sets_var.get())
        reps = int(reps_var.get())
        total_reps_var.set(str(sets * reps))
    except ValueError:
        total_reps_var.set("Invalid input")

sets_var.trace_add("write", calculate_total_reps)
reps_var.trace_add("write", calculate_total_reps)

# Guardar entrenamiento
def save_workout():
    from datetime import datetime
    today = datetime.now().strftime("%Y-%m-%d")

    try:
        sets = int(sets_var.get())
        reps = int(reps_var.get())
        weight = float(weight_entry.get())
    except ValueError:
        messagebox.showerror("Error", "Enter valid numbers")
        return

    exercise = exercise_var.get()
    sets = sets_var.get()
    reps = reps_var.get()
    weight = weight_entry.get()
    total_reps = total_reps_var.get()

    # Obtener información del ejercicio desde el DataFrame
    row = df[df["name"] == exercise]

    if not row.empty:
        muscle = row["muscle_group"].values[0]
        training_type = row["training_type"].values[0]
        difficulty = row["difficulty"].values[0]
        equipment = row["equipment"].values[0]
    else:
        muscle = "Unknown"
        training_type = "Unknown"
        difficulty = "Unknown"
        equipment = "Unknown"

    # Guardar en base de datos usando DB_PATH
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO workouts (
            date, exercise, muscle_group, training_type,
            difficulty, equipment, sets, reps, weight, total_reps
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        today, exercise, muscle, training_type,
        difficulty, equipment, sets, reps, weight, total_reps
    ))

    conn.commit()
    conn.close()

    tk.messagebox.showinfo("Saved", "Workout saved successfully!")

    # Limpiar campos
    sets_var.set("")
    reps_var.set("")
    weight_entry.delete(0, tk.END)
    total_reps_var.set("")

    print(f"""
Workout Saved!
Date: {today}
Exercise: {exercise}
Muscle: {muscle}
Training Type: {training_type}
Difficulty: {difficulty}
Equipment: {equipment}
Sets: {sets}
Reps: {reps}
Weight: {weight}
Total reps: {total_reps}
""")
    
save_button = tk.Button(window, text="Save Workout", command=save_workout)
save_button.grid(row=6, column=1, columnspan=2, pady=10)

def show_all_workouts():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM workouts")
    rows = cursor.fetchall()
    conn.close()

    for row in rows:
        print(row)

show_all_workouts()

# ==============================
# DASHBOARD WINDOW
# ==============================

def open_dashboard():
    dash = tk.Toplevel(window)
    dash.title("Training Dashboard")
    dash.geometry("1100x650")
    dash.configure(bg="white")

    # Layout
    top = tk.Frame(dash, bg="white")
    top.pack(fill="x", pady=10)

    mid = tk.Frame(dash, bg="white")
    mid.pack(fill="both", expand=True)

    left = tk.Frame(mid, bg="white")
    left.pack(side="left", fill="both", expand=True, padx=10)

    right = tk.Frame(mid, bg="white")
    right.pack(side="right", fill="both", expand=True, padx=10)

    load_dashboard(top, left, right)

# ==============================
# LOAD DATA
# ==============================

def load_dashboard(top, left, right):
    conn = sqlite3.connect(DB_PATH)
    df_db = pd.read_sql("SELECT * FROM workouts", conn)
    conn.close()

    # Convert to numeric
    df_db["weight"] = pd.to_numeric(df_db["weight"], errors="coerce")
    df_db["sets"]   = pd.to_numeric(df_db["sets"], errors="coerce")
    df_db["reps"]   = pd.to_numeric(df_db["reps"], errors="coerce")

    # Remove invalid rows
    df_db = df_db.dropna(subset=["weight", "sets", "reps"])

    if df_db.empty:
        tk.Label(
            top,
            text="No training data yet",
            font=("Helvetica", 14, "bold"),
            bg="white"
        ).pack()
        return

    df_db["date"] = pd.to_datetime(df_db["date"])

    show_kpis(top, df_db)
    plot_volume(left, df_db)
    plot_muscles(right, df_db)

# ==============================
# KPIs
# ==============================

def show_kpis(frame, df_db):
    for w in frame.winfo_children():
        w.destroy()

    sessions = df_db["date"].nunique()
    workouts = len(df_db)
    volume = (df_db["weight"] * df_db["sets"] * df_db["reps"]).sum()

    box_style = {
        "font": ("Helvetica", 12, "bold"),
        "bg": "#f1f3f5",
        "padx": 20,
        "pady": 10,
        "bd": 1,
        "relief": "solid"
    }

    tk.Label(frame, text=f"Sessions\n{sessions}", **box_style).pack(side="left", padx=15)
    tk.Label(frame, text=f"Exercises\n{workouts}", **box_style).pack(side="left", padx=15)
    tk.Label(frame, text=f"Total Volume\n{int(volume)} kg", **box_style).pack(side="left", padx=15)

# ==============================
# VOLUME CHART
# ==============================

def plot_volume(frame, df_db):
    for w in frame.winfo_children():
        w.destroy()

    volume = df_db.groupby("date").apply(
        lambda x: (x["weight"] * x["sets"] * x["reps"]).sum()
    )

    fig = Figure(figsize=(5,4))
    ax = fig.add_subplot(111)

    ax.plot(volume.index, volume.values, marker="o")
    ax.set_title("Daily Training Volume")
    ax.set_xlabel("Date")
    ax.set_ylabel("Volume (kg)")
    ax.grid(True)

    canvas = FigureCanvasTkAgg(fig, frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)

# ==============================
# MUSCLE GROUP CHART
# ==============================

def plot_muscles(frame, df_db):
    for w in frame.winfo_children():
        w.destroy()

    muscles = df_db["muscle_group"].value_counts()

    fig = Figure(figsize=(5,4))
    ax = fig.add_subplot(111)

    ax.bar(muscles.index, muscles.values)
    ax.set_title("Muscle Group Distribution")
    ax.set_ylabel("Sessions")
    ax.tick_params(axis="x", rotation=45)

    canvas = FigureCanvasTkAgg(fig, frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)


dashboard_btn = tk.Button(
    window,
    text="Open Dashboard",
    font=("Helvetica", 12, "bold"),
    command=open_dashboard
)

dashboard_btn.grid(row=8, column=0, columnspan=2, pady=10)

window.mainloop()