import os

import numpy as np
from PIL import Image

from manipulator.scarlet_base import ScarletBase
from skimage.metrics import structural_similarity as ssim


class TileScanner(ScarletBase):
    def __init__(self, manipulator_instance):
        super().__init__()
        self.state_img = Image.open(self.current_state_path)
        self.manipulator_instance = manipulator_instance
        self.tiles = self.manipulator_instance.current_tiles()

    def tile_scan(self):
        # Tile regions to crop
        tile_regions = [
            # row 1
            (699, 300, 764, 338),
            (805, 300, 870, 338),
            (910, 300, 975, 338),
            (1016, 300, 1081, 338),
            (1122, 300, 1187, 338),
            # row 2
            (699, 406, 764, 444),
            (805, 406, 870, 444),
            (910, 406, 975, 444),
            (1016, 406, 1081, 444),
            (1122, 406, 1187, 444),
            # row 3
            (699, 512, 764, 550),
            (805, 512, 870, 550),
            (910, 512, 975, 550),
            (1016, 512, 1081, 550),
            (1122, 512, 1187, 550),
            # row 4
            (699, 618, 764, 656),
            (805, 618, 870, 656),
            (910, 618, 975, 656),
            (1016, 618, 1081, 656),
            (1122, 618, 1187, 656),
            # row 5
            (699, 724, 764, 762),
            (805, 724, 870, 762),
            (910, 724, 975, 762),
            (1016, 724, 1081, 762),
            (1122, 724, 1187, 762)
        ]

        # extract tile state
        for i, region in enumerate(tile_regions):
            tile_region_crop = self.state_img.crop(region)
            tile_save_path = os.path.join(self.tiles_state_path, f'tile_{i + 1}.png')
            tile_region_crop.save(tile_save_path)

    def tile_recorder(self):
        self.tile_scan()
        if not self.tiles:
            self.tiles = {f'tile_{i}': '' for i in range(1, 26)}
        else:
            self.tiles = self.manipulator_instance.current_tiles()
        if self.tiles:
            for tile_number in range(1, 26):
                # Load tile state image and convert to np array
                tile_state_image = Image.open(os.path.join(self.tiles_state_path, f'tile_{tile_number}.png'))
                tile_state_image_np = np.array(tile_state_image)

                # Loop through comparing images
                for filename in os.listdir(self.comparing_images_tiles):
                    comparable_image = Image.open(os.path.join(self.comparing_images_tiles, filename))
                    comparable_image_np = np.array(comparable_image)

                    # Calculate Structural Similarity Index (SSI) with a smaller win_size
                    smaller_side = min(tile_state_image_np.shape[0], tile_state_image_np.shape[1],
                                       comparable_image_np.shape[0], comparable_image_np.shape[1])
                    win_size = min(smaller_side, 3)
                    similarity_index, _ = ssim(tile_state_image_np, comparable_image_np, win_size=win_size, full=True)
                    similarity_index = float(f"{similarity_index:.2f}")

                    if similarity_index > 0.8:
                        filename = filename[:-4]
                        # if filename == 'home_tile_2':
                        #     filename = 'home_tile'
                        # elif filename == 'pillar_tile_2':
                        #     filename = 'pillar_tile'
                        if f"tile_{tile_number}" in self.tiles:
                            self.tiles[f"tile_{tile_number}"] = filename
                            break
        return self.tiles
