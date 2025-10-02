import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import warnings
warnings.filterwarnings('ignore')
import joblib
import os

df_musicas = None
kmeans_model = None
scaler = None
scaled_features = None
feature_columns = None


def treinar_modelo(df, features_cols, n_clusters=10, nome_col='name', artista_col='artists'):
    global df_musicas, kmeans_model, scaler, scaled_features, feature_columns
    
    
    if nome_col not in df.columns:
        raise ValueError(f"Coluna '{nome_col}' não encontrada. Colunas disponíveis: {df.columns.tolist()}")
    
    if os.path.exists("backend/data/k_means.pkl") and os.path.exists("backend/data/scaler.pkl"):
        print("Carregando modelo existente...")
        kmeans_model = joblib.load("backend/data/k_means.pkl")
        scaler = joblib.load("backend/data/scaler.pkl")
        
        df_musicas = df.copy()
        df_musicas['name'] = df_musicas[nome_col]
        if artista_col in df.columns:
            df_musicas['artists'] = df_musicas[artista_col]
        feature_columns = features_cols
        
        features = df_musicas[feature_columns].values
        scaled_features = scaler.transform(features)
        df_musicas['cluster'] = kmeans_model.predict(scaled_features)
        
        print(f"Modelo carregado com sucesso")
        print(f"Total de músicas: {len(df_musicas)}")
        return
    
    df_musicas = df.copy()
    df_musicas['name'] = df_musicas[nome_col]
    if artista_col in df.columns:
        df_musicas['artists'] = df_musicas[artista_col]
    feature_columns = features_cols
    
    scaler = StandardScaler()
    features = df_musicas[feature_columns].values
    scaled_features = scaler.fit_transform(features)
    
    kmeans_model = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    df_musicas['cluster'] = kmeans_model.fit_predict(scaled_features)
    
    joblib.dump(kmeans_model, "backend/data/k_means.pkl")
    joblib.dump(scaler, "backend/data/scaler.pkl")
    
    print(f"Modelo treinado com {n_clusters} clusters")
    print(f"Total de músicas: {len(df_musicas)}")


def recomendar_musicas(nome_musica, n_recomendacoes=10):
    global df_musicas, kmeans_model, scaler, scaled_features
    
    if df_musicas is None or kmeans_model is None:
        raise ValueError("Modelo não treinado. Execute treinar_modelo() primeiro.")
    
    if '-' in nome_musica:
        musica = nome_musica.split('-')[0].strip()
        artistas = nome_musica.split('-')[1].strip()
        song_match = df_musicas[(df_musicas['name'].str.contains(musica, case=False, na=False)) & (df_musicas['artists'].str.contains(artistas, case=False, na=False))]
    else:
        song_match = df_musicas[df_musicas['name'].str.contains(nome_musica, case=False, na=False)]
    
    if song_match.empty:
        print(f"Música '{nome_musica}' não encontrada no dataset.")
        return []
    
    song = song_match.iloc[0]
    song_cluster = song['cluster']
    song_index = song.name
    
    print(f"\nMúsica encontrada: {song['name']}")
    if 'artists' in df_musicas.columns:
        print(f"Artista: {song['artists']}")
    print(f"Cluster: {song_cluster}\n")
    
    cluster_songs = df_musicas[df_musicas['cluster'] == song_cluster].copy()
    cluster_songs = cluster_songs[cluster_songs.index != song_index]
    
    if len(cluster_songs) == 0:
        print("Nenhuma outra música encontrada no mesmo cluster.")
        return []

    cluster_songs = cluster_songs.drop_duplicates(subset=['name', 'artists'])
    
    song_features = scaled_features[song_index].reshape(1, -1)
    cluster_indices = cluster_songs.index
    cluster_features = scaled_features[cluster_indices]
    
    distances = np.sqrt(np.sum((cluster_features - song_features) ** 2, axis=1))
    cluster_songs['distance'] = distances

    cluster_songs = cluster_songs.sort_values(by='distance')

    cluster_songs = cluster_songs[cluster_songs['distance'] > 0]
    
    recommendations = cluster_songs.nsmallest(n_recomendacoes, 'distance')
    lista_recomendacoes = recommendations['name'].tolist()
    
    print(f"{'='*60}")
    print(f"Top {len(lista_recomendacoes)} Recomendações:")
    print(f"{'='*60}\n")
    
    for i, musica in enumerate(lista_recomendacoes, 1):
        artista = ""
        if 'artists' in recommendations.columns:
            artista = f" - {recommendations.iloc[i-1]['artists']}"
        print(f"{i:2d}. {musica}{artista}")
    
    return lista_recomendacoes
