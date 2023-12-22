import pyautogui
import os
from PIL import Image
from skimage.metrics import structural_similarity as ssim
import numpy as np
import time
import pytesseract

time.sleep(5)
start_time = time.time()

targets = []
target_numbers = {}
board_icon_coordinates = {
    'ball': [],
    'circ': [],
    'ginger': [],
    'party': [],
    'pine_cone': [],
    'sock': [],
    'warp': []
}

icon_coordinates = {
    'icon_1': (782, 471),
    'icon_2': (860, 471),
    'icon_3': (942, 471),
    'icon_4': (1024, 471),
    'icon_5': (1104, 471),
    'icon_6': (782, 554),
    'icon_7': (860, 554),
    'icon_8': (942, 554),
    'icon_9': (1024, 554),
    'icon_10': (1104, 554),
    'icon_11': (782, 633),
    'icon_12': (860, 633),
    'icon_13': (942, 633),
    'icon_14': (1024, 633),
    'icon_15': (1104, 633),
    'icon_16': (782, 711),
    'icon_17': (860, 711),
    'icon_18': (942, 711),
    'icon_19': (1024, 711),
    'icon_20': (1104, 711),
    'icon_21': (782, 792),
    'icon_22': (860, 792),
    'icon_23': (942, 792),
    'icon_24': (1024, 792),
    'icon_25': (1104, 792),
    'icon_26': (782, 869),
    'icon_27': (860, 869),
    'icon_28': (942, 869),
    'icon_29': (1024, 869),
    'icon_30': (1104, 869),
}

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


def compare_targets_with_to_find(target_path, tfd):  # tfd = to find dir
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



def extract_number_of_targets(screenshot_path, tdn):  # td = targets numbers dir
    """
    3ple target info
    X 822 / Y 396 / W 35 / H 18
    X 925 / Y 396 / W 35 / H 18
    X 1030 / Y 396 / W 35 / H 18"""
    # Load the screenshot
    screenshot_path = os.path.join(screenshot_path, 'level_screen.png')
    scns = Image.open(screenshot_path)  # scns = screenshot
    target_regions = [
        (822, 396, 857, 414),
        (925, 396, 960, 414),
        (1030, 396, 1065, 414)
    ]
    # Extract and save target number images
    for i, region in enumerate(target_regions):
        target_image = scns.crop(region)
        target_image_path = os.path.join(tdn, f'target_number_{i + 1}.png')
        target_image.save(target_image_path)


def extract_numbers_of_targets_to_values():
    target_numbers.clear()
    # Extract targets numbers
    targets_directory = 'target_numbers'
    targets_number_path = os.path.join(working_dir, targets_directory)
    if not os.path.exists(targets_number_path):
        os.makedirs(targets_path)
    extract_number_of_targets(screenshot_dir, targets_number_path)

    # Set the path to the Tesseract executable (modify this based on your installation; bellow is the default location
    # for windows). Get the installation from: https://github.com/tesseract-ocr/tesseract
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

    # 3ple target loader
    # Load the images
    for i in range(1, 4):
        target_numbers_path = 'target_numbers'
        image_path = os.path.join(working_dir, target_numbers_path)
        open_image = os.path.join(image_path, f"target_number_{i}.png")
        img = Image.open(open_image)

        # Preprocess the image (convert to grayscale)
        img = img.convert("L")

        # Use Tesseract OCR to extract text
        text = pytesseract.image_to_string(img, config='--psm 6')

        target_numbers[f"{targets[i-1]}"] = text[-2]

        # test of this text to find what it gives
        # print(f"Extracted Text {i}:", text)


extract_numbers_of_targets_to_values()
# print(target_numbers)


# get board images locations
def get_board_images(screenshot_path):
    screenshot_path = os.path.join(screenshot_path, 'level_screen.png')
    scns = Image.open(screenshot_path)  # scns = screenshot
    target_regions = [
        (746, 434, 820, 508),
        (826, 434, 900, 508),
        (906, 434, 980, 508),
        (986, 434, 1060, 508),
        (1066, 434, 1140, 508),
        (746, 514, 820, 588),
        (826, 514, 900, 588),
        (906, 514, 980, 588),
        (986, 514, 1060, 588),
        (1066, 514, 1140, 588),
        (746, 594, 820, 668),
        (826, 594, 900, 668),
        (906, 594, 980, 668),
        (986, 594, 1060, 668),
        (1066, 594, 1140, 668),
        (746, 594, 820, 668),
        (826, 594, 900, 668),
        (906, 594, 980, 668),
        (986, 594, 1060, 668),
        (1066, 594, 1140, 668),
        (746, 675, 820, 749),
        (826, 675, 900, 749),
        (906, 675, 980, 749),
        (986, 675, 1060, 749),
        (1066, 675, 1140, 749),
        (746, 755, 820, 829),
        (826, 755, 900, 829),
        (906, 755, 980, 829),
        (986, 755, 1060, 829),
        (1066, 755, 1140, 829),
        (746, 835, 820, 909),
        (826, 835, 900, 909),
        (906, 835, 980, 909),
        (986, 835, 1060, 909),
        (1066, 835, 1140, 909)
    ]

    dump_dir = os.path.join(working_dir, 'board_dump')

    # Extract and save board images
    for i, region in enumerate(target_regions):
        board_image = scns.crop(region)
        board_image_path = os.path.join(dump_dir, f'board_icon_{i + 1}.png')
        board_image.save(board_image_path)


get_board_images(screenshot_dir)

def get_coordinates_of_board_icons():
    pass

end_time = time.time()
execution_time = end_time - start_time
print(f"Execution time: {execution_time} seconds")