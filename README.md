# Playlist Recommendation Demo

This project is a demonstration system for generating music playlists based on a user-provided playlist name. It uses transformer-based language models to find similar playlists and recommend the most relevant tracks. The demo includes a backend API (Flask + Docker) and a web interface for interacting with the system.

---

## 📁 Repository Structure

```
.
├── recommend_backend.py         # Flask backend server
├── Dockerfile                   # Docker container configuration
├── requirements.txt             # Python dependencies
├── index.html                   # Web interface (static)
└── data/                        # (expected path for metadata files)
```

---

## ⚙️ Requirements

- Docker installed locally
- At least **9 GB of RAM**
- No GPU required (runs on CPU)

---

## 📦 Setup Instructions

### 1. Clone the repository

```bash
git@github.com:elea-vellard/DEMO-playlist-continuation.git
cd playlist-demo
```

### 2. Download required files

The following files are **not included** in the repository and must be manually added in the /data folder:

- Fine-tuned model directories:
  - `data/fine_tuned_model_no_scheduler_2/`
  - `data/final_triplet_model/`

- Precomputed embeddings:
  - `data/playlists_embeddings_scheduler.pkl`
  - `data/playlists_embeddings_triplet.pkl`
  - `data/playlists_embeddings_pretrained.pkl`

- Metadata files:
  - `data/tracks.csv`
  - `data/items.csv`
  - `data/playlists.csv`

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
