import os
import shutil
import subprocess
import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage
import cv2
import threading

# Initializing Firebase
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://auto-attendance-d7a57-default-rtdb.firebaseio.com/",
    'storageBucket': "auto-attendance-d7a57.appspot.com"
})

def run_main():
    def run():
        subprocess.run(["python", "main.py"])

    threading.Thread(target=run).start()

def run_encode():
    subprocess.run(["python", "encode_gen.py"])

def save_to_firebase(student_id, data, photo_path):
    ref = db.reference('Students')
    ref.child(student_id).set(data)

    # moving photos to images directory
    image_dir = 'images'
    os.makedirs(image_dir, exist_ok=True)
    new_photo_path = os.path.join(image_dir, f"{student_id}.png")
    shutil.copy(photo_path, new_photo_path)

    # Uploading Photo to Firebase
    bucket = storage.bucket()
    blob = bucket.blob(f'images/{student_id}.png')
    blob.upload_from_filename(new_photo_path)

def open_form():
    form_window = ctk.CTkToplevel(app)
    form_window.title("Add Student Data")
    form_window.geometry("640x480")

    ctk.CTkLabel(form_window, text="Student ID:").grid(row=0, column=0, padx=10, pady=10)
    student_id_entry = ctk.CTkEntry(form_window)
    student_id_entry.grid(row=0, column=1, padx=10, pady=10)

    ctk.CTkLabel(form_window, text="Name:").grid(row=1, column=0, padx=10, pady=10)
    name_entry = ctk.CTkEntry(form_window)
    name_entry.grid(row=1, column=1, padx=10, pady=10)

    ctk.CTkLabel(form_window, text="Major:").grid(row=2, column=0, padx=10, pady=10)
    major_entry = ctk.CTkEntry(form_window)
    major_entry.grid(row=2, column=1, padx=10, pady=10)

    ctk.CTkLabel(form_window, text="Total Attendance:").grid(row=3, column=0, padx=10, pady=10)
    total_attendance_entry = ctk.CTkEntry(form_window)
    total_attendance_entry.grid(row=3, column=1, padx=10, pady=10)

    ctk.CTkLabel(form_window, text="Photo:").grid(row=4, column=0, padx=10, pady=10)
    photo_label = ctk.CTkLabel(form_window, text="No file chosen")
    photo_label.grid(row=4, column=1, padx=10, pady=10)

    def choose_photo():
        photo_path = filedialog.askopenfilename(title="Select Photo", filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
        photo_label.configure(text=os.path.basename(photo_path))
        photo_label.photo_path = photo_path

    ctk.CTkButton(form_window, text="Choose Photo", command=choose_photo).grid(row=4, column=2, padx=10, pady=10)

    def submit():
        student_id = student_id_entry.get()
        name = name_entry.get()
        major = major_entry.get()
        total_attendance = total_attendance_entry.get()
        photo_path = getattr(photo_label, 'photo_path', '')

        if not student_id or not name or not major or not total_attendance or not photo_path:
            messagebox.showerror("Error", "Please fill in all fields and choose a photo.")
            return

        data = {
            "name": name,
            "major": major,
            "Total_attendance": int(total_attendance)
        }

        save_to_firebase(student_id, data, photo_path)
        messagebox.showinfo("Success", "Student data saved successfully.")
        form_window.destroy()

    ctk.CTkButton(form_window, text="Submit", command=submit).grid(row=5, column=0, columnspan=3, pady=20)

app = ctk.CTk()
app.title("Attendify")
app.geometry("640x480")

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

frame = ctk.CTkFrame(app)
frame.pack(pady=20, padx=60, fill="both", expand=True)

label = ctk.CTkLabel(frame, text="Attendify", font=("Arial", 24))
label.pack(pady=20)

btn2 = ctk.CTkButton(frame, text="Add Student Data", command=open_form)
btn2.pack(pady=10)

btn3 = ctk.CTkButton(frame, text="Run Encoding", command=run_encode)
btn3.pack(pady=10)

btn1 = ctk.CTkButton(frame, text="Launch Attendtify", command=run_main)
btn1.pack(pady=10)

app.mainloop()
