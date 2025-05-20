from flask import Flask, request, jsonify
import os
import torch
import pickle
from sklearn.metrics.pairwise import cosine_similarity
from tqdm import tqdm
from collections import Counter
import csv
from transformers import AutoTokenizer, AutoModel
import math
from gensim.models import KeyedVectors
import numpy as np

app = Flask(__name__)

print("Loading static data (track metadata)...")

# Static paths
ITEMS_CSV = "./csvs/items.csv"
TRACKS_CSV = "./csvs/tracks.csv"
PLAYLISTS_CSV = "./csvs/playlists.csv"

# Models paths + pretrained config
MODEL_CONFIGS = {
    "1": {
        "pretrained": True,
        "base_model_name": "sentence-transformers/all-MiniLM-L6-v2",
        "embeddings_file": "./data/playlists_embeddings_pretrained.pkl"
    }#,
    #"2": {
    #    "model_dir": "./data/fine_tuned_model_no_scheduler_2",
    #    "embeddings_file": "./data/playlists_embeddings_scheduler.pkl"
    #},
    #"3": {
    #    "model_dir": "./data/final_triplet_model",
    #    "embeddings_file": "./data/playlists_embeddings_triplet.pkl"
    #}
}

# Cache loaded models
loaded_models = {}

# Load static data
track_metadata = {}
with open(TRACKS_CSV, 'r', encoding='utf8') as f:
    reader = csv.DictReader(f)
    for row in tqdm(reader, desc="Loading track metadata", unit="track"):
        track_metadata[row["track_uri"]] = {
            "track_name": row["track_name"],
            "artist_name": row["artist_name"],
        }

playlist_tracks = {}
with open(ITEMS_CSV, 'r', encoding='utf8') as f:
    reader = csv.DictReader(f)
    for row in tqdm(reader, desc="Loading playlist tracks", unit="playlist"):
        pid_str = row["pid"].strip()
        track_uri = row["track_uri"]
        if pid_str not in playlist_tracks:
            playlist_tracks[pid_str] = []
        if track_uri in track_metadata:
            playlist_tracks[pid_str].append(track_metadata[track_uri])

playlist_titles = {}
with open(PLAYLISTS_CSV, 'r', encoding='utf8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        playlist_titles[row["pid"].strip()] = row["name"]

print("Static data loaded.")

# Load model + embeddings (cached by model id)
def load_model(model_id):
    if model_id in loaded_models:
        return loaded_models[model_id]

    if model_id not in MODEL_CONFIGS:
        raise ValueError("Invalid model id")

    config = MODEL_CONFIGS[model_id]

    if config.get("pretrained"):
        tokenizer = AutoTokenizer.from_pretrained(config["base_model_name"])
        model = AutoModel.from_pretrained(config["base_model_name"])
    else:
        tokenizer = AutoTokenizer.from_pretrained('sentence-transformers/all-MiniLM-L6-v2')
        model = AutoModel.from_pretrained(config["model_dir"])

    model.eval()
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)

    with open(config["embeddings_file"], 'rb') as f:
        playlist_embeddings = pickle.load(f)

    keys = list(playlist_embeddings.keys())
    vectors = np.stack([playlist_embeddings[key]["embedding"] for key in keys])
    playlist_embeddings_kv = KeyedVectors(vector_size=vectors.shape[1])
    playlist_embeddings_kv.add_vectors(keys, vectors)

    loaded_models[model_id] = (tokenizer, model, playlist_embeddings_kv)
    return tokenizer, model, playlist_embeddings_kv

# Helper functions
def get_playlist_embedding(playlist_name, tokenizer, model):
    with torch.no_grad():
        inputs = tokenizer(playlist_name, return_tensors='pt', truncation=True, padding=True).to(model.device)
        outputs = model(**inputs)
        last_hidden = outputs.last_hidden_state
        embedding = last_hidden.mean(dim=1).squeeze().cpu().numpy()
    return embedding

def find_similar_playlists(playlist_name, playlist_embeddings_kv, tokenizer, model, top_k=50):
    playlist_embedding = get_playlist_embedding(playlist_name, tokenizer, model)
    sims = playlist_embeddings_kv.similar_by_vector(playlist_embedding, topn=top_k)
    return sims

def get_top_songs(similar_playlists, top_k=10):
    song_counter = Counter()
    for pid, _ in similar_playlists:
        pid_str = str(pid)
        if pid_str in playlist_tracks:
            for track in playlist_tracks[pid_str]:
                song_counter[(track["track_name"], track["artist_name"])] += 1
    return song_counter.most_common(top_k)

@app.route("/recommend")
def recommend():
    playlist_name = request.args.get("playlist_name")
    model_id = request.args.get("model_id", "1")  # Default model = 1

    if not playlist_name:
        return jsonify({"error": "Missing playlist_name parameter"}), 400

    try:
        tokenizer, model, playlist_embeddings_kv = load_model(model_id)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    similar_playlists = find_similar_playlists(playlist_name, playlist_embeddings_kv, tokenizer, model)
    top_songs = get_top_songs(similar_playlists)

    response = {
        "model_id": model_id,
        "recommendations": [{"song": song, "artist": artist, "count": count} for (song, artist), count in top_songs]
    }

    return jsonify(response)

print("Preloading all models for fast first request...")
for model_id in ["1"]#, "2", "3"]:
    print(f"Loading model {model_id}...")
    load_model(model_id)
print("All models preloaded and ready!")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
