import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

root = tk.Tk()
root.title("BMI Calculator")
root.geometry("520x700")
root.configure(bg="white")

# ---------------- HEADER ----------------
title_label = tk.Label(root, text="BMI CALCULATOR", font=("Arial Black", 20), bg="white")
title_label.pack(pady=10)

# ---------------- INPUT SECTION ----------------
frame_inputs = tk.Frame(root, bg="white")
frame_inputs.pack(pady=10, fill="x")

# Load box image
try:
    box_img = Image.open("Assets/biglable.png").resize((180, 130))
    box_photo = ImageTk.PhotoImage(box_img)
except FileNotFoundError:
    messagebox.showerror("Missing Image", "biglable.png not found! Please add it to the same folder.")
    root.destroy()
    raise SystemExit

# Labels
tk.Label(frame_inputs, text="Height (cm)", font=("Arial", 14, "bold"), bg="white").grid(row=0, column=0, padx=30)
tk.Label(frame_inputs, text="Weight (kg)", font=("Arial", 14, "bold"), bg="white").grid(row=0, column=1, padx=30)

# Variables
height_var = tk.StringVar()
weight_var = tk.StringVar()

# Entry background boxes
tk.Label(frame_inputs, image=box_photo, bg="white").grid(row=1, column=0, padx=20, pady=5)
tk.Label(frame_inputs, image=box_photo, bg="white").grid(row=1, column=1, padx=20, pady=5)

# Entry fields
height_entry = tk.Entry(frame_inputs, textvariable=height_var, font=("Arial", 34, "bold"),
                        width=5, justify="center", bd=0, bg="white")
height_entry.place(x=90, y=70)

weight_entry = tk.Entry(frame_inputs, textvariable=weight_var, font=("Arial", 34, "bold"),
                        width=5, justify="center", bd=0, bg="white")
weight_entry.place(x=300, y=70)

# ---------------- SLIDERS ----------------
height_slider = tk.Scale(frame_inputs, from_=1, to=250, orient="horizontal", length=180,
                         bg="white", highlightthickness=0, troughcolor="#b3e5fc")
height_slider.grid(row=2, column=0, pady=5)

weight_slider = tk.Scale(frame_inputs, from_=1, to=300, orient="horizontal", length=180,
                         bg="white", highlightthickness=0, troughcolor="#b3e5fc")
weight_slider.grid(row=2, column=1, pady=5)

# ---------------- SYNC FUNCTIONS ----------------
def sync_from_slider(event=None):
    height_var.set(str(height_slider.get()))
    weight_var.set(str(weight_slider.get()))

def sync_from_entry(event=None):
    try:
        h = float(height_var.get())
        w = float(weight_var.get())
        if 1 <= h <= 250:
            height_slider.set(h)
        if 1<= w <= 300:
            weight_slider.set(w)
    except ValueError:
        pass  # ignore invalid typing

height_slider.bind("<B1-Motion>", sync_from_slider)
weight_slider.bind("<B1-Motion>", sync_from_slider)
height_slider.bind("<ButtonRelease-1>", sync_from_slider)
weight_slider.bind("<ButtonRelease-1>", sync_from_slider)

height_entry.bind("<KeyRelease>", sync_from_entry)
weight_entry.bind("<KeyRelease>", sync_from_entry)

# ---------------- CALCULATION FUNCTION ----------------
def show_report():
    try:
        height_cm = float(height_var.get())
        weight = float(weight_var.get())
    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numeric values for height and weight.")
        return

    # sanity checks
    if not (1 <= height_cm <= 250):
        messagebox.showerror("Input Error", "Height must be between 1 cm and 250 cm.")
        return
    if not (1 <= weight <= 300):
        messagebox.showerror("Input Error", "Weight must be between 1 kg and 300 kg.")
        return

    height = height_cm / 100
    bmi = weight / (height ** 2)
    bmi_value_label.config(text=f"{bmi:.1f}")

    if bmi < 18.5:
        status, advice, color = "Underweight", "Eat more and gain some weight.", "#0288d1"
    elif bmi < 25:
        status, advice, color = "Normal", "You are healthy! Keep it up.", "#2e7d32"
    elif bmi < 30:
        status, advice, color = "Overweight", "Try to exercise regularly.", "#fbc02d"
    else:
        status, advice, color = "Obese", "Health may be at risk. Try to lose weight.", "#d32f2f"

    status_label.config(text=status, fg=color)
    message_label.config(text=advice)
    bmi_value_label.config(fg=color)

# ---------------- BUTTON ----------------
tk.Button(root, text="CHECK BMI", font=("Arial Black", 16), bg="#0288d1", fg="white",
          padx=40, pady=10, relief="flat", activebackground="#0277bd",
          command=show_report).pack(pady=20)

# ---------------- RESULT SECTION ----------------
frame_result = tk.Frame(root, bg="#99defe", height=320)
frame_result.pack(fill="both", expand=True)
frame_result.pack_propagate(False)

bmi_value_label = tk.Label(frame_result, text="0.0", font=("Arial Black", 64),
                           bg="#99defe", fg="#01579b")
bmi_value_label.pack(pady=(40, 5))

status_label = tk.Label(frame_result, text="", font=("Arial Black", 22), bg="#99defe")
status_label.pack()

message_label = tk.Label(frame_result, text="", font=("Arial", 12),
                         bg="#99defe", wraplength=450)
message_label.pack(pady=10)

root.mainloop()

