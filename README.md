# Playlist Recommendation Demo

This project is a demo application that recommends songs based on a user-provided playlist title.  
It uses a fine-tuned transformer model trained on the Million Playlist Dataset to generate real-time suggestions that match the theme of the input.

The system is fully packaged in a Docker image and includes:
- A Flask backend API
- A clean, interactive web interface
- Preloaded data, embeddings, and model (no extra setup required)

---

## Run the demo locally

First, populate the `app/data/` directory:
- apply `transform-dataset/json2csv.py` on the [Million Playlist Dataset](https://www.kaggle.com/datasets/himanshuwagh/spotify-million) and put the three obtained csv in the directory;
- download the model in the [Zenodo repository](https://zenodo.org/records/15837980) and uncompress in the directory.

### 1. Pull the image
```bash
docker pull eleadocker/playlist-recommendation:latest
```

### 2. Run the container
```bash
docker run --rm -p 8080:8080 eleadocker/playlist-recommendation:latest
```
