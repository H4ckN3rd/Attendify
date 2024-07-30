<div align="center">

# Attendify 📸

Attendify is a Facial Recognition Attendance System built using Python, OpenCV (cv2), face_recognition, and Firebase for real-time database integration. This application allows the registration of students with their photos, encodes the facial features, and marks attendance by recognizing the student's face in real-time.

</div>

## Features ✨

- Add new students with their photos and details.
- Encode and save facial features for recognition.
- Real-time attendance marking using facial recognition.
- Store and retrieve data using Firebase real-time database.
- Upload and download student photos from Firebase storage.

## Prerequisites 🛠️

Make sure you have the following installed:

- Python 3.x
- OpenCV
- face_recognition
- customtkinter
- Pillow
- firebase-admin
- numpy
- cvzone

You can install the required Python packages using the following command:

```bash
pip install -r requirements.txt
```

## Installation ⚙️

1. Clone the repository:

```bash
git clone https://github.com/jatink2004/Attendify.git
cd attendify
```

2. Set up Firebase:
   - Go to the Firebase Console and create a new project.
   - Navigate to the "Project settings" and click on "Service accounts".
   - Generate a new private key and download the `serviceAccountKey.json` file.
   - Place the `serviceAccountKey.json` file in the root directory of the project.

3. Update Firebase configuration:
   - In `attendify.py`, `encode_gen.py`, and `main.py`, make sure the Firebase database URL and storage bucket URL match your Firebase project.

## Usage 🚀

1. Run the Attendify application:

```bash
python attendify.py
```
<div align="center">
    <img src="https://github.com/jatink2004/Attendify/blob/3d4167f073d6ce2c86e5312ac04912b3af1a26fe/images_for_readme/1.png?raw=true" alt="Attendify GUI">
</div>

2. Use the GUI to:
   - Add new student data and photos.
   - Run the encoding process by clicking "Run Encoding".
   - Launch the real-time attendance system by clicking "Launch Attendify".

<div align="center">
    <img src="https://github.com/jatink2004/Attendify/blob/3d4167f073d6ce2c86e5312ac04912b3af1a26fe/images_for_readme/2.png?raw=true" alt="Attendify GUI 2">
</div>

## Project Structure 📂

- `attendify.py`: Main GUI application for adding student data, running encoding, and launching the attendance system.
- `encode_gen.py`: Script to encode facial features of the students and save them for recognition.
- `main.py`: Script to run the real-time facial recognition and mark attendance.
- `serviceAccountKey.json`: Firebase service account key file.
- `images/`: Directory where student photos are stored.
- `Resources/`: Directory containing background and mode images for the GUI.

## Contributing 🤝

Contributions are welcome! Please feel free to submit a Pull Request.

Feel free to customize the content further as per your project's specifics and preferences.

