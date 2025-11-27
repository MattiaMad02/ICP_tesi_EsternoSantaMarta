import os
import json
import pandas as pd

# Percorso della cartella con le pointcloud
folder_path = "pointcloud"
# Percorso del file JSON con i tempi
json_path = "pointcloud/acquisition_times.json"

# Carichiamo il JSON
with open(json_path, "r") as f:
    tempi_dict = json.load(f)  # formato: {"chiave": "seconds: ...\nnanos: ...", ...}

# Lista dei file waypoint nella cartella
files = [f for f in os.listdir(folder_path) if f.startswith("waypoint_")]

# Lista di timestamp dal JSON
timestamps = []
for key, value in tempi_dict.items():
    try:
        # Estrae secondi e nanos
        lines = value.split("\n")
        seconds = int(lines[0].split(":")[1].strip())
        nanos = int(lines[1].split(":")[1].strip())
        timestamp = seconds + nanos / 1e9
        timestamps.append(timestamp)
    except Exception as e:
        print(f"Errore con la chiave {key}: {e}")

# Controllo sul numero di file e timestamp
if len(files) != len(timestamps):
    print(f"Attenzione: ci sono {len(files)} file ma {len(timestamps)} timestamp. Verranno abbinati in ordine.")

# Creiamo DataFrame
files_sorted = sorted(files)  # ordina alfabeticamente i file
timestamps_sorted = sorted(timestamps)  # ordina i timestamp

data = [{"filename": f, "timestamp": t} for f, t in zip(files_sorted, timestamps_sorted)]
df = pd.DataFrame(data)

# Ordiniamo per timestamp
df = df.sort_values(by="timestamp").reset_index(drop=True)

# Salviamo CSV (opzionale)
df.to_csv("pointclouds_sorted.csv", index=False)

# Salviamo TXT
with open("pointclouds_sorted.txt", "w") as f:
    for _, row in df.iterrows():
        f.write(f"{row['filename']} {row['timestamp']}\n")

print("DataFrame ordinato e file TXT creati correttamente!")

