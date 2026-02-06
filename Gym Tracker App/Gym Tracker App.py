#Gym Tracker App
import tkinter as tk
import sqlite3 

#Create a database connection and cursor including a table for workouts
conn = sqlite3.connect('gym_tracker.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS workouts
                  (id INTEGER PRIMARY KEY AUTOINCREMENT,
                   exercise TEXT NOT NULL,
                   muscle_group TEXT NOT NULL,
                   intensity TEXT NOT NULL)
               ''')

#Set up the main window
window = tk.Tk()
window.title("Gym Tracker App")
window.geometry("400x500")
window.resizable(False,False)
window.configure(background="#DE8471")
window.configure(padx=20, pady=20)
window.configure(bg="#E0BBE4")
window.grid_columnconfigure(0, weight=1)
window.grid_columnconfigure(1, weight=1)


#Create variables to store user input
sets_var = tk.StringVar()
reps_var = tk.StringVar()
total_reps_var = tk.StringVar()
# Create labels and entry fields for workout details
exercise_label = tk.Label(window, text="Exercise:")
exercise_label.grid(row=0, column=0)
exercise_entry = tk.Entry(window)
exercise_entry.grid(row=0, column=1)

sets_label = tk.Label(window, text="Sets:")
sets_label.grid(row=1, column=0)
sets_entry = tk.Entry(window, textvariable=sets_var)
sets_entry.grid(row=1, column=1)

reps_label = tk.Label(window, text="Reps:")
reps_label.grid(row=2, column=0)
reps_entry = tk.Entry(window, textvariable=reps_var)
reps_entry.grid(row=2, column=1)

weight_label = tk.Label(window, text="Weight (kg):")
weight_label.grid(row=3, column=0)
weight_entry = tk.Entry(window)
weight_entry.grid(row=3, column=1)

total_reps_label = tk.Label(window, text="Total Reps:")
total_reps_label.grid(row=4, column=0)
total_reps_entry = tk.Entry(window, textvariable=total_reps_var, state='readonly')
total_reps_entry.grid(row=4, column=1)

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
    global exercise, sets, reps, weight, total_reps_var
    exercise = exercise_entry.get()
    sets = sets_entry.get()
    reps = reps_entry.get()
    weight = weight_entry.get()
    print(f"Saved workout: {exercise}, {sets} sets, {reps} reps, {weight} kg, {total_reps_var.get()} total reps")
save_button = tk.Button(window, text="Save Workout", command=save_workout)
save_button.grid(row=6, column=1, columnspan=2)

window.mainloop()