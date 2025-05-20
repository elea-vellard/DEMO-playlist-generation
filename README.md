# Playlist Recommendation Demo

This project is a demonstration system for generating music playlists based on a user-provided playlist name. It uses transformer-based language models to find similar playlists and recommend the most relevant tracks. The demo includes a backend API (Flask + Docker) and a web interface for interacting with the system.

---

## 🧠 Overview

The system encodes the input playlist name into a vector using a transformer model, compares it to precomputed embeddings of existing playlists, and returns the most frequently occurring tracks from the most similar ones.

Three models are supported:

- **Model 1**: Pretrained MiniLM (`sentence-transformers/all-MiniLM-L6-v2`)
- **Model 2**: Fine-tuned with Cross-Entropy loss
- **Model 3**: Fine-tuned with Triplet Loss

---

## 📁 Repository Structure

```
.
├── recommend_backend.py         # Flask backend server
├── Dockerfile                   # Docker container configuration
├── requirements.txt             # Python dependencies
├── index.html                   # Web interface (static)
├── playlist_continuation/      # (expected path for models and embeddings)
└── data/csvs/                   # (expected path for metadata files)
```

---

## ⚙️ Requirements

- Docker installed locally
- At least **9 GB of RAM**
- No GPU required (runs on CPU)
- Internet browser to open the frontend (`index.html`)

---

## 📦 Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/your-username/playlist-demo.git
cd playlist-demo
```

### 2. Download required files

The following files are **not included** in the repository and must be manually added:

- Fine-tuned model directories:
  - `playlist_continuation/fine_tuned_model_no_scheduler_2/`
  - `playlist_continuation/final_triplet_model/`

- Precomputed embeddings:
  - `playlist_continuation/playlists_embeddings/final_embeddings/playlists_embeddings_scheduler.pkl`
  - `playlist_continuation/playlists_embeddings/final_embeddings/playlists_embeddings_triplet.pkl`
  - `playlist_continuation/playlists_embeddings/final_embeddings/playlists_embeddings_pretrained.pkl`

- Metadata files:
  - `data/csvs/tracks.csv`
  - `data/csvs/items.csv`
  - `data/csvs/playlists.csv`

Once downloaded, place them as follows:

```
playlist_continuation/
├── fine_tuned_model_no_scheduler_2/
├── final_triplet_model/
└── playlists_embeddings/
    └── final_embeddings/
        ├── playlists_embeddings_scheduler.pkl
        ├── playlists_embeddings_triplet.pkl
        └── playlists_embeddings_pretrained.pkl

data/csvs/
├── tracks.csv
├── items.csv
├── playlists.csv
```

---

## 🐳 Running the Demo (Docker)

### Step-by-step:

1. Open a terminal and go to the root of the project.
2. Make sure the folders `playlist_continuation/` and `data/csvs/` contain the required files.
3. Build the Docker image:

```bash
docker build -t playlist-recommendation .
```

4. Run the container:

```bash
docker run -p 8080:8080 \
  -v $(pwd)/playlist_continuation:/app/playlist_continuation \
  -v $(pwd)/data/csvs:/app/csvs \
  playlist-recommendation
```

5. Keep this terminal open — the backend Flask server is now running on http://localhost:8080.

---

## 🌐 Using the Web Interface

1. Open the `index.html` file in your browser.
2. Select a model, enter a playlist name, and press Enter.
3. The page will send an HTTP request to the backend and display the recommended tracks.

> The interface dynamically communicates with the backend via JavaScript.

---

## 🔌 API Reference (for developers)

**Endpoint:**

```
GET /recommend?playlist_name=<name>&model_id=<1|2|3>
```

**Response:**

```json
{
  "model_id": "2",
  "recommendations": [
    {"song": "Song A", "artist": "Artist A", "count": 5},
    {"song": "Song B", "artist": "Artist B", "count": 4}
  ]
}
```

---

## 🖥️ System Requirements

- RAM: ~9 GB
- GPU: Not required
- Docker: Required

---

## 📬 Contact

For access to the data files or further assistance, contact:

**Éléa Vellard**  
EURECOM  
[youremail@domain.com]
