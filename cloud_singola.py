import open3d as o3d
file_path = "icp_noFilter_results/merged_icp_no_filter_map.ply"
pcd = o3d.io.read_point_cloud(file_path)
o3d.visualization.draw_geometries([pcd])