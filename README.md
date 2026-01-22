# 🛡️ Deepfake-Check: Metadata & Signal Analyzer

Deepfake-Check is a digital forensics tool designed to identify AI-generated media. Unlike typical AI detectors that use "black-box" neural networks, this tool focuses on **forensic artifacts**: digital fingerprints, metadata anomalies, and biological signal inconsistencies left behind by generative models.

---

## 📁 Project Structure

```
deepfake_check/
├── backend/
│   ├── main.py              # FastAPI application entry point
│   ├── requirements.txt     # Python dependencies
│   ├── api/                  # API route handlers
│   └── core/                 # Analysis modules
│       ├── audio.py          # Audio frequency analysis
│       ├── metadata.py       # ExifTool metadata extraction
│       └── video.py          # Visual noise analysis
├── frontend/                 # Next.js web interface (see frontend/README.md)
├── snapshots/                # Test media files directory
├── docs/                     # Documentation
├── docker-compose.yml        # Docker orchestration
├── requirements.txt          # Root-level dependencies
└── README.md
```

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
You must have exiftool installed on your OS for the backend to function.

```bash
brew install exiftool
```

### 2. Backend Setup
You will need two terminal tabs open to run the full application.

**Tab A: Backend (API)**

```bash
cd backend
source venv/bin/activate
uvicorn main:app --reload --port 8000
```

### 3. Frontend Setup

**Tab B: Frontend (Next.js)**

```bash
cd frontend
npm install
npm run dev
```

Visit http://localhost:3000 to access the dashboard. The frontend is configured to send requests to the FastAPI server at http://localhost:8000.

---

### Running the Metadata Extractor (CLI)

You can also run the metadata extractor directly on a specific file:

```bash
python3 -m core.metadata snapshots/your_test_file.mp4
```

## 🧪 Testing the Analysis

To test the system, place sample files in the snapshots/ folder. Use the following for comparison:

- **Authentic Sample:** A video or audio file recorded directly from your iPhone/Android hardware.
- **AI Sample:** A file generated via ElevenLabs (audio), Sora, or HeyGen (video).

### Running the CLI Test

Before using the web UI, you can verify the backend logic directly via the terminal:

```bash
cd backend
python3 -m core.metadata ../snapshots/your_test_file.mp4
python3 -m core.audio ../snapshots/your_test_file.mp4
python3 -m core.video ../snapshots/your_test_file.mp4
```

---

## 🐳 Docker Setup (Optional)

To run the entire stack with Docker:

```bash
docker-compose up --build
```

---

## 📄 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET`  | `/` | Health check - returns backend status |

> More endpoints will be added as the API develops.

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -m 'Add your feature'`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Open a Pull Request

---
