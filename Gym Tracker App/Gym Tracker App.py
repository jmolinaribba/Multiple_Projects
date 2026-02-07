#Gym Tracker App
import tkinter as tk
import sqlite3
import pandas as pd
import tkinter.ttk as ttk

#Read workout data from a CSV file and store it in a DataFrame
df = pd.read_csv('Gym Tracker App/exercises.csv')

#Create a database connection and cursor including a table for workouts
conn = sqlite3.connect('Gym Tracker App/workouts.db')
cursor = conn.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS workouts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
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
''')

conn.close()

#Set up the main window
window = tk.Tk()
window.title("Gym Tracker App")
title_label = tk.Label(window, text="Gym Tracker App",
                       font=("Helvetica", 16, "bold"), bg="#3032BB", fg="white")
title_label.grid(row=0, column=0, columnspan=2, pady=(0,10))
window.geometry("400x300")
window.resizable(False,False)
window.configure(padx=20, pady=20)
window.configure(bg="#3032BB")
window.grid_columnconfigure(0, weight=1)
window.grid_columnconfigure(1, weight=1)


#Create variables to store user input
sets_var = tk.StringVar()
reps_var = tk.StringVar()
total_reps_var = tk.StringVar()
exercise_var = tk.StringVar()

# Create labels and entry fields for workout details
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

#Define a function to calculate total reps
def calculate_total_reps(*args):
    try:
        sets = int(sets_var.get())
        reps = int(reps_var.get())
        total_reps_var.set(str(sets * reps))
    except ValueError:
        total_reps_var.set("Invalid input")
sets_var.trace_add("write", calculate_total_reps)
reps_var.trace_add("write", calculate_total_reps)

# Create a button to save workout details
def save_workout():

    exercise = exercise_var.get()
    sets = sets_entry.get()
    reps = reps_entry.get()
    weight = weight_entry.get()
    total_reps = total_reps_var.get()

    # Get exercise info
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

    # Save to database
    conn = sqlite3.connect("Gym Tracker App/workouts.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO workouts (exercise, muscle_group, training_type, difficulty, equipment, sets, reps, weight, total_reps)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (exercise, muscle, training_type, difficulty, equipment, sets, reps, weight, total_reps))

    conn.commit()
    conn.close()

    print(f"""
Workout Saved!
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
save_button.grid(row=6, column=1, columnspan=2)

window.mainloop()