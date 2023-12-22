import pyautogui
import os
from PIL import Image
from skimage.metrics import structural_similarity as ssim
import numpy as np
import time

time.sleep(5)
start_time = time.time()

targets = []

# Take a screenshot
working_dir = os.path.dirname(os.path.abspath(__file__))
target_directory = 'screenshots'
level_screen = 'level_screen.png'
screenshot_dir = os.path.join(working_dir, target_directory)
if not os.path.exists(screenshot_dir):
    os.makedirs(screenshot_dir)

screenshot = pyautogui.screenshot()
screenshot.save(os.path.join(screenshot_dir, level_screen))

"""
img info
3ple image/target
IMG1 -> X 794 / Y 318 / W 87 / H 75
IMG2 -> X 900 / Y 319 / W 87 / H 75
IMG3 -> X1003 / Y 318 / W 87 / H 75
"""


# Set targets from the screenshot
def extract_targets(screenshot_path, td):  # td = targets dir
    # Load the screenshot
    screenshot_path = os.path.join(screenshot_path, 'level_screen.png')
    scns = Image.open(screenshot_path)  # scns = screenshot
    target_regions = [
        (796, 318, 881, 393),  # Example: (left, top, right, bottom)
        (900, 319, 987, 394),
        (1003, 318, 1090, 393)
    ]
    # Extract and save target images
    for i, region in enumerate(target_regions):
        target_image = scns.crop(region)
        target_image_path = os.path.join(td, f'target_{i + 1}.png')
        target_image.save(target_image_path)


# Extract targets
targets_directory = 'targets'
targets_path = os.path.join(working_dir, targets_directory)
if not os.path.exists(targets_path):
    os.makedirs(targets_path)
extract_targets(screenshot_dir, targets_path)


def compare_targets_with_to_find(target_path, tfd): # tfd = to find dir
    global targets
    targets = []
    for i in range(1, 4):
        # Load the target image
        tp = os.path.join(target_path, f"target_{i}.png")
        target_image = Image.open(tp)

        # Loop through images in the to_find directory
        for filename in os.listdir(tfd):
            image_path = os.path.join(tfd, filename)

            # Load the image from to_find directory
            to_find_image = Image.open(image_path)

            # Resize the target image to match the dimensions of the to_find image
            target_image_resized = target_image.resize(to_find_image.size)

            # Convert images to numpy arrays
            target_np = np.array(target_image_resized)
            to_find_np = np.array(to_find_image)

            # Calculate Structural Similarity Index (SSI) with a smaller win_size
            smaller_side = min(target_np.shape[0], target_np.shape[1], to_find_np.shape[0], to_find_np.shape[1])
            win_size = min(smaller_side, 3)  # Set to 5 or any odd value less than or equal to the smaller side
            similarity_index, _ = ssim(target_np, to_find_np, win_size=win_size, full=True)

            # Print the similarity index for each image
            # print(f"Similarity index with {filename}: {similarity_index}")

            # You can store the results in the 'targets' list if needed
            # targets.append((f"target_{i}.png", filename, similarity_index))
            similarity_index = float(f"{similarity_index:.2f}")
            if similarity_index >= 0.80:
                targets.append(filename[:-4])
                break

    # return targets


# Compare targets to images in the to_find directory
imgs_comp_directory = 'imgs_comp'
to_find_directory = 'to_find'
to_find_path = os.path.join(working_dir, imgs_comp_directory, to_find_directory)

compare_targets_with_to_find(targets_path, to_find_path)

# Example: Print the results
# print(targets)

end_time = time.time()
execution_time = end_time - start_time
print(f"Execution time: {execution_time} seconds")
