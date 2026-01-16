import open3d as o3d
import numpy as np
import os
file_path = "icp_point_to_point_noFilter_results/merged_icp_point_to_point_map.ply"
pcd = o3d.io.read_point_cloud(file_path)
o3d.visualization.draw_geometries([pcd])
