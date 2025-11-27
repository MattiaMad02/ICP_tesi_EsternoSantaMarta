import open3d as o3d
import numpy as np
import os
import time
import pandas as pd

# --- TIMER INIZIALE ---
start_time = time.time()

# --- CARTELLA PROGETTO E POINT CLOUD ---
project_folder = os.path.dirname(__file__)
folder = os.path.join(project_folder, "pointcloud")

# --- LETTURA DATAFRAME ORDINATO ---
df_file = os.path.join(project_folder, "pointclouds_sorted.txt")
# Il TXT ha due colonne: filename timestamp
df = pd.read_csv(df_file, sep=" ", header=None, names=["base_name", "timestamp"])

# Ricostruzione percorsi completi dei file
df["file"] = df["base_name"].apply(lambda x: os.path.join(folder, x))

# --- PARAMETRI ICP ---
voxel_size = 0.02
threshold = 0.1  # distanza massima per ICP

# --- CARICAMENTO MAPPA INIZIALE (TARGET) ---
target_file = df.loc[0, "file"]
print("Caricamento mappa iniziale:", target_file)
map_pcd = o3d.io.read_point_cloud(target_file)
map_pcd = map_pcd.voxel_down_sample(voxel_size)
map_pcd.estimate_normals()

# --- CARICAMENTO DELLE ALTRE POINT CLOUD -
source_files = df.loc[1:, "file"].tolist()
point_clouds = [o3d.io.read_point_cloud(f) for f in source_files]

# --- PREPROCESSING ---
for i in range(len(point_clouds)):
    pcd = point_clouds[i].voxel_down_sample(voxel_size)
    pcd.estimate_normals()
    point_clouds[i] = pcd

# --- CREAZIONE CARTELLA RISULTATI ---
save_folder = os.path.join(project_folder, "icp_results")
os.makedirs(save_folder, exist_ok=True)

# --- ICP ---
transformations = []
summary_lines = []

print("\nAvvio ICP...\n")
for i, source in enumerate(point_clouds):
    print(f"Allineamento nuvola {i+1}/{len(point_clouds)}")

    reg_icp = o3d.pipelines.registration.registration_icp(
        source, map_pcd, threshold, np.eye(4),
        o3d.pipelines.registration.TransformationEstimationPointToPlane()
    )

    print(f"  Fitness: {reg_icp.fitness:.4f}, RMSE: {reg_icp.inlier_rmse:.4f}")

    # Applica trasformazione alla nuvola
    source.transform(reg_icp.transformation)
    transformations.append(reg_icp.transformation)

    # Salva trasformazione e nuvola
    np.savetxt(os.path.join(save_folder, f"transformation_{i+1}.txt"), reg_icp.transformation)
    o3d.io.write_point_cloud(os.path.join(save_folder, f"aligned_{i+1}.ply"), source)

    summary_lines.append(
        f"Frame {i+1}: {source_files[i]}, Fitness={reg_icp.fitness:.4f}, RMSE={reg_icp.inlier_rmse:.4f}\n"
    )

    # Aggiorna la mappa cumulativ
    map_pcd += source
    map_pcd = map_pcd.voxel_down_sample(voxel_size)
    map_pcd.estimate_normals()

# --- SALVATAGGIO MAPPA COMPLETA ---
merged_file = os.path.join(save_folder, "merged_icp_map.ply")
o3d.io.write_point_cloud(merged_file, map_pcd)

# --- TEMPO TOTALE ---
total_time = time.time() - start_time
summary_lines.append(f"\nTempo totale: {total_time:.2f} secondi\n")

summary_file = os.path.join(save_folder, "icp_summary.txt")
with open(summary_file, "w") as f:
    f.writelines(summary_lines)

print(f"\nICP completato in {total_time:.2f} secondi")
print(f"Risultati salvati in: {save_folder}")

# --- VISUALIZZAZIONE ---
o3d.visualization.draw_geometries([map_pcd])
