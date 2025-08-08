# Playlist Recommendation Demo

This project is a demo application that recommends songs based on a user-provided playlist title.
It uses a fine-tuned transformer model trained on the Million Playlist Dataset to generate real-time suggestions that match the theme of the input.

The system is fully packaged in a Docker image and includes:

- A Flask backend API
- A clean, interactive web interface
- Preloaded data, embeddings, and model (no extra setup required)

**Related links**

- [Main project repository](https://github.com/elea-vellard/LLM-Playlist-Recommender) with the main method
- [Online demo](https://playlist-recommendation.tools.eurecom.fr/)

---

## Run the demo locally
### 1. Download the data

First, populate the `app/data/` directory:]

- apply `transform-dataset/json2csv.py` on the [Million Playlist Dataset](https://www.kaggle.com/datasets/himanshuwagh/spotify-million) and put the three obtained csv in the directory;
- download the model in the [Zenodo repository](https://zenodo.org/records/15837980) and decompress in the directory.

Make sure your project follows this structure:

```bash
project-root/
├── app/
│   ├── recommend_backend.py                  # Back-end logic (Flask API)
│   ├── templates/
│   │   └── index.html                        # Front-end (UI)
│   ├── static/
│   │   └── images/
│   │       ├── eurecom-logo.png
│   │       ├── github-logo.png
│   │       └── spotify.png
│   └── data/
│       ├── tracks.csv
│       ├── items.csv
│       ├── playlists.csv
│       ├── playlists_embeddings_scheduler.pkl
│       └── fine_tuned_model_no_scheduler_2/  # Fine-tuned model
├── Dockerfile
├── requirements.txt
└── README.md
```

### 2. Build the image

From the root of the project, run:

```bash
docker build -t playlist-recommendation:latest .
```

### 3. Run the container

```bash
docker run --rm -p 8080:8080 playlist-recommendation:latest
```

---

## Citation

If you use this software, please cite ([bib file](https://raw.githubusercontent.com/elea-vellard/LM-Playlist-Recommender/refs/heads/main/vellardcharolois2025demo.bib)):

Eléa Vellard, Enzo Charolois–Pasqua, Youssra Rebboud, Pasquale Lisena,
and Raphael Troncy. 2025. Interactive Playlist Generation from Titles. In
Proceedings of the Nineteenth ACM Conference on Recommender Systems
(RecSys ’25), September 22–26, 2025, Prague, Czech Republic. ACM, New York,
NY, USA, 3 pages. https://doi.org/10.1145/3705328.3759336