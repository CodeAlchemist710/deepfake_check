# 🛡️ Deepfake-Check: Metadata & Signal Analyzer

Deepfake-Check is a digital forensics tool designed to identify AI-generated media. Unlike typical AI detectors that use "black-box" neural networks, this tool focuses on **forensic artifacts**: digital fingerprints, metadata anomalies, and biological signal inconsistencies left behind by generative models.

---

## 🚀 The Forensic Approach

This project implements three primary layers of analysis:

1. **Container Forensics (ExifTool):** Identifying missing hardware signatures, non-standard quantization tables, and software-specific metadata (e.g., FFmpeg traces in "original" footage).
2. **Audio Frequency Analysis (Librosa):** Detecting "spectral gaps" and robotic pitch consistency in AI-synthesized voices.
3. **Visual Noise Analysis (OpenCV):** Extracting the "Noise Floor" or PRNU (Photo Response Non-Uniformity) to check for GAN-generated checkerboard artifacts.

---

## 🛠️ Tech Stack

- **Backend:** Python 3.12+, FastAPI, OpenCV, Librosa, PyExifTool.
- **Frontend:** Next.js 15, TypeScript, Tailwind CSS, Lucide Icons.
- **System Dependencies:** ExifTool (Perl-based forensic engine).

---

## ⚙️ Installation & Setup

### 1. System Prerequisites (Mac/Linux)

You must have `exiftool` installed on your OS for the backend to function.

```bash
brew install exiftool
```

### 2. Backend Setup
```

Bash

cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

```
3. Frontend Setup

```
Bash

cd frontend
npm install

```
## 🏃 How to Run

You will need two terminal tabs open:

### Tab A: Backend (API)

Visit http://localhost:3000 to access the dashboard.

🧪 Testing the Analysis
To test the system, place sample files in the snapshots/ folder:

Authentic Sample: A video/audio file recorded directly from your iPhone/Android.

AI Sample: A file generated via ElevenLabs, Sora, or HeyGen.

Running the CLI Test:


---
