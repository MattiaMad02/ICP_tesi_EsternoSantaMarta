import open3d as o3d
import numpy as np
import os
file_path = "icp_results/merged_icp_map.ply"
pcd = o3d.io.read_point_cloud(file_path)
o3d.visualization.draw_geometries([pcd])
vis = o3d.visualization.Visualizer()
vis.create_window(visible=True)
vis.add_geometry(pcd)
opt = vis.get_render_option()
opt.background_color = np.asarray([1, 1, 1])  # sfondo bianco
opt.point_size = 2.0
vis.poll_events()
vis.update_renderer()
output_folder = "screenshots"
os.makedirs(output_folder, exist_ok=True)
screenshot_path = os.path.join(output_folder, "parco_pointcloud_filter.png")
vis.capture_screen_image(screenshot_path)
print(f"Screenshot salvato in: {screenshot_path}")
vis.run()
vis.destroy_window()