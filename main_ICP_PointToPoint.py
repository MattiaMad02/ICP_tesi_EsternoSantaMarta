import open3d as o3d
import numpy as np
import os
import time
import pandas as pd
start_time = time.time()
project_folder = os.path.dirname(__file__)
folder = os.path.join(project_folder, "pointcloud")
df_file = os.path.join(project_folder, "pointclouds_sorted.txt")
df = pd.read_csv(df_file, sep=" ", header=None, names=["base_name", "timestamp"])
df["file"] = df["base_name"].apply(lambda x: os.path.join(folder, x))
voxel_size = 0.02
threshold = 0.1
target_file = df.loc[0, "file"]
print("Caricamento mappa iniziale:", target_file)
map_pcd = o3d.io.read_point_cloud(target_file)
map_pcd = map_pcd.voxel_down_sample(voxel_size)
source_files = df.loc[1:, "file"].tolist()
point_clouds = [o3d.io.read_point_cloud(f) for f in source_files]
for i in range(len(point_clouds)):
    point_clouds[i] = point_clouds[i].voxel_down_sample(voxel_size)
save_folder = os.path.join(project_folder, "icp_point_to_point_noFilter_results")
os.makedirs(save_folder, exist_ok=True)
transformations = []
summary_lines = []
print("\nAvvio ICP Point-to-Point...\n")
for i, source in enumerate(point_clouds):
    print(f"Allineamento nuvola {i+1}/{len(point_clouds)}")
    reg_icp = o3d.pipelines.registration.registration_icp(
        source,
        map_pcd,
        threshold,
        np.eye(4),
        o3d.pipelines.registration.TransformationEstimationPointToPoint()
    )
    print(f"  Fitness: {reg_icp.fitness:.4f}, RMSE: {reg_icp.inlier_rmse:.4f}")
    source.transform(reg_icp.transformation)
    transformations.append(reg_icp.transformation)
    np.savetxt(
        os.path.join(save_folder, f"transformation_{i+1}.txt"),
        reg_icp.transformation
    )
    o3d.io.write_point_cloud(
        os.path.join(save_folder, f"aligned_{i+1}.ply"),
        source
    )
    summary_lines.append(
        f"Frame {i+1}: {source_files[i]}, "
        f"Fitness={reg_icp.fitness:.4f}, "
        f"RMSE={reg_icp.inlier_rmse:.4f}\n"
    )
    map_pcd += source
    map_pcd = map_pcd.voxel_down_sample(voxel_size)
merged_file = os.path.join(save_folder, "merged_icp_point_to_point_map.ply")
o3d.io.write_point_cloud(merged_file, map_pcd)
total_time = time.time() - start_time
summary_lines.append(f"\nTempo totale: {total_time:.2f} secondi\n")
summary_file = os.path.join(save_folder, "icp_point_to_point_summary.txt")
with open(summary_file, "w") as f:
    f.writelines(summary_lines)
print(f"\nICP completato in {total_time:.2f} secondi")
print(f"Risultati salvati in: {save_folder}")
o3d.visualization.draw_geometries([map_pcd])
