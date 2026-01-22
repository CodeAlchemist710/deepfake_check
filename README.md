Markdown
```markdown
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
3. Frontend Setup
Bash

cd frontend
npm install
🏃 How to Run
You will need two terminal tabs open:

Tab A: Backend (API)

Bash

cd backend
source venv/bin/activate
uvicorn main:app --reload --port 8000
Tab B: Frontend (UI)

Bash

cd frontend
npm run dev
Visit http://localhost:3000 to access the dashboard.

🧪 Testing the Analysis
To test the system, place sample files in the snapshots/ folder:

Authentic Sample: A video/audio file recorded directly from your iPhone/Android.

AI Sample: A file generated via ElevenLabs, Sora, or HeyGen.

Running the CLI Test:

Bash

# Example script to test metadata extraction
python3 backend/core/metadata.py snapshots/test_video.mp4
🤝 Contributor Workflow
To avoid merge conflicts, please follow this flow:

Pull latest changes: git pull origin main

Create a feature branch: git checkout -b feature/your-feature-name

Commit changes: git commit -m "Add: Noise residue extraction logic"

Push and PR: git push origin feature/your-feature-name (then create a Pull Request on GitHub).

🗺️ Roadmap
[ ] Implement rPPG (Remote Photoplethysmography) to detect heartbeats in video faces.

[ ] Add Spectral Centroid analysis for audio.

[ ] Generate PDF Forensic Reports.

Disclaimer: This tool is for educational and forensic research purposes. No detector is 100% accurate; always use manual verification for critical evidence.


---

### Why this README works
* **Scientific Credibility:** It explains *how* it detects fakes (PRNU, Spectral gaps), which makes it a high-level portfolio piece.
* **Clear Instructions:** Your partner can clone the repo and be running in under 5 minutes.
* **Standardization:** It defines the port numbers ($8000$ for backend, $3000$ for frontend) so your API calls don't break.



### Next Step for you:
Now that the README is set, would you like the **Python code for the `metadata.py` module** so you can actually start extracting "Suspicion Scores" from files?