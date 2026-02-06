import tkinter 
import math

button_values = [["AC","+/-","%","/"],["7","8","9","x"],["4","5","6","-"],["1","2","3","+"],["0",".","sqrt","="]]

rigth_symbols = ["/","x","-","+","=","sqrt"]
top_symbols = ["AC","+/-","%"]

row_count = len(button_values)
column_count = len(button_values[0])

color_turquoise = "#73BDB0"
color_blue = "#396192"
color_red = "#B86969"
color_sultan = "#E69F67"
color_pastel_yellow = "#EBE4C3"

#Window Setup

window = tkinter.Tk()
window.title("Calculator")
window.geometry("400x500")
window.resizable(False,False)

frame = tkinter.Frame(window)
label = tkinter.Label(frame,text="0", font=("Arial",45), background=color_pastel_yellow, foreground=color_blue, anchor="e", width=column_count)

label.grid(row=0, column=0, columnspan=column_count, sticky="we")

for row in range (row_count):
    for column in range (column_count):
        value = button_values[row][column]
        button = tkinter.Button(frame, text=value, font=("Arial",30), background=color_turquoise, width= column_count-1, height=1, command=lambda value=value: button_clicked(value))

        if value in top_symbols:
          button.config(background=color_blue, foreground=color_pastel_yellow)
        elif value in rigth_symbols:
          button.config(background=color_red, foreground=color_pastel_yellow)
        else:
          button.config(background=color_pastel_yellow, foreground=color_blue)

        button.grid(row=row+1, column=column)
        
frame.pack()

#A+B, A-B, A*B, A/B
A = 0
operator = None
B = None

#Functions
def remove_zero_decimal(num):
  if num.is_integer():
    return int(num)
  return num
  

def clear_all():
  global A, operator, B
  A = 0
  operator = None
  B = None

def button_clicked(value):
  global rigth_symbols, top_symbols,label, A, operator, B

  if value in rigth_symbols:
    if value == "=":
      if A is not None and operator is not None:
        B = label["text"]
        num_A = float(A)
        num_B = float(B)

        if operator == "+":
          label["text"] = remove_zero_decimal(num_A + num_B)
        elif operator == "-":
          label["text"] = remove_zero_decimal(num_A - num_B)
        elif operator == "x":
          label["text"] = remove_zero_decimal(num_A * num_B)
        elif operator == "/":
          label["text"] = remove_zero_decimal(num_A / num_B)
    elif value == "sqrt":
      num = float(label["text"])
      if num < 0:
        label["text"] = "Error"
        return
      result = math.sqrt(num)
      if result.is_integer():
        label["text"] = remove_zero_decimal(result)
      else:
        label["text"] = f"{result:.3f}"

    
    elif value in ["+","-","x","/"]:
      if operator is None:
        A = label["text"]
        label["text"] = "0"
        B = "0"
      operator = value
    else:
      B = label["text"]



  elif value in top_symbols:
    if value == "AC":
      clear_all()
      label["text"] = "0"
    elif value == "+/-":
      result = float(label["text"])*-1
      label["text"] = remove_zero_decimal(result)
    elif value == "%":
      result = float(label["text"])/100
      label["text"] = remove_zero_decimal(result)
    
        
  
  else: 
    if value == ".":
      if value not in label["text"]:
        label["text"] += value
    elif value in "0123456789":
      if label["text"] == "0":
        label["text"] = value
      else:
          label["text"] += value          
#Center Window
window.update()
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

window_x = int((screen_width/2) - (window_width/2))
window_y = int((screen_height/2) - (window_height/2))

window.geometry(f"{window_width}x{window_height}+{window_x}+{window_y}")

window.mainloop()