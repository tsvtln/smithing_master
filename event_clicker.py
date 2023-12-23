import pyautogui
import os
from PIL import Image
from skimage.metrics import structural_similarity as ssim
import numpy as np
import time
import pytesseract

time.sleep(3)
start_time = time.time()
# duration = 999999999999999999999999999999  # test
duration = 120  # 2min

QUAD = False
MOVED = False
targets = []
target_numbers = {}
board_icon_coordinates = {
    'wrap': [],
    'ball': [],
    'ginger': [],
    'pine_cone': [],
    'circ': [],
    'cane': [],
    'party': [],
    'sock': [],
    'star': [],
    'pandelka': []
}

icon_coordinates = {
    'icon_01': (782, 471),
    'icon_02': (860, 471),
    'icon_03': (942, 471),
    'icon_04': (1024, 471),
    'icon_05': (1104, 471),
    'icon_06': (782, 554),
    'icon_07': (860, 554),
    'icon_08': (942, 554),
    'icon_09': (1024, 554),
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

while True:
    # Take a screenshot
    working_dir = os.path.dirname(os.path.abspath(__file__))
    target_directory = 'screenshots'
    level_screen = 'level_screen.png'
    screenshot_dir = os.path.join(working_dir, target_directory)
    if not os.path.exists(screenshot_dir):
        os.makedirs(screenshot_dir)

    screenshot = pyautogui.screenshot()
    screenshot.save(os.path.join(screenshot_dir, level_screen))


    def find_triple_or_quad(screenshot_path):
        global QUAD
        # (831, 318, 848, 406)
        screenshot_path = os.path.join(screenshot_path, 'level_screen.png')
        scns = Image.open(screenshot_path)  # scns = screenshot
        target_region = [
            (831, 318, 848, 406)
        ]
        # Extract and save region
        for i, region in enumerate(target_region):
            cropped = scns.crop(region)
            cropped_path = os.path.join(screenshot_dir, f'crop.png')
            cropped.save(cropped_path)

        icd = 'imgs_comp'
        tfd = 'to_find'
        tfp = os.path.join(working_dir, icd, tfd)
        crop_path = os.path.join(screenshot_dir, 'crop.png')
        to_compare_if_quad = os.path.join(icd, tfp, 'quad.png')
        crop_image_open = Image.open(crop_path)
        to_compare_if_quad_image_open = Image.open(to_compare_if_quad)

        # Convert to np array
        crop_image_np = np.array(crop_image_open)
        to_compare_np = np.array(to_compare_if_quad_image_open)

        # Calculate Structural Similarity Index (SSI) with a smaller win_size
        smaller_side = min(to_compare_np.shape[0], to_compare_np.shape[1], crop_image_np.shape[0],
                           crop_image_np.shape[1])
        win_size = min(smaller_side, 3)
        similarity_index, _ = ssim(to_compare_np, crop_image_np, win_size=win_size, full=True)
        # Print the similarity index for each image
        similarity_index_formatted = float(f"{similarity_index:.2f}")
        # print(f"Similarity index with Crop: {similarity_index_formatted:.2f}")

        if similarity_index_formatted < 0.80:
            QUAD = False
        else:
            QUAD = True


    # print(f"THIS IS QUAD STATE {QUAD}")

    class TripleImageManipulator:
        """
        img info
        3ple image/target
        IMG1 -> X 794 / Y 318 / W 87 / H 75
        IMG2 -> X 900 / Y 319 / W 87 / H 75
        IMG3 -> X1003 / Y 318 / W 87 / H 75
        """

        # Set targets from the screenshot
        @staticmethod
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


        @staticmethod
        def extract_targets_plus_4(screenshot_path, td):  # td = targets dir
            # Load the screenshot
            screenshot_path = os.path.join(screenshot_path, 'level_screen.png')
            scns = Image.open(screenshot_path)  # scns = screenshot
            target_regions = [
                (796, 318, 885, 393),
                (904, 319, 991, 394),
                (1007, 318, 1094, 393)
            ]
            # Extract and save target images
            for i, region in enumerate(target_regions):
                target_image = scns.crop(region)
                target_image_path = os.path.join(td, f'target_{i + 1}.png')
                target_image.save(target_image_path)

        @staticmethod
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
                    if similarity_index >= 0.77:
                        if similarity_index >= 0.77:
                            filename = filename[:-4]
                            if filename == 'pandelk':
                                filename = 'pandelka'
                            elif filename == 'ginge':
                                filename = 'ginger'
                            elif filename == 'can':
                                filename = 'cane'
                            targets.append(filename)
                        break

        @staticmethod
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

        @staticmethod
        def extract_number_of_targets_plus_4(screenshot_path, tdn):  # td = targets numbers dir
            """
            3ple target info
            X 822 / Y 396 / W 35 / H 18
            X 925 / Y 396 / W 35 / H 18
            X 1030 / Y 396 / W 35 / H 18"""
            # Load the screenshot
            screenshot_path = os.path.join(screenshot_path, 'level_screen.png')
            scns = Image.open(screenshot_path)  # scns = screenshot
            target_regions = [
                (822, 396, 861, 414),
                (929, 396, 968, 414),
                (1034, 396, 1073, 414)
            ]

            # Extract and save target number images
            for i, region in enumerate(target_regions):
                target_image = scns.crop(region)
                target_image_path = os.path.join(tdn, f'target_number_{i + 1}.png')
                target_image.save(target_image_path)

        @staticmethod
        def extract_numbers_of_targets_to_values():
            global working_dir
            targets_directory = 'targets'
            targets_path = os.path.join(working_dir, targets_directory)
            target_numbers.clear()
            # Extract targets numbers
            tar_dir = 'target_numbers'
            targets_number_path = os.path.join(working_dir, tar_dir)
            if not os.path.exists(targets_number_path):
                os.makedirs(targets_path)
            TripleImageManipulator.extract_number_of_targets(screenshot_dir, targets_number_path)

            # Set the path to the Tesseract executable
            # (modify this based on your installation; bellow is the default location
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

                # try:
                target_numbers[f"{targets[i - 1]}"] = int(text[-2])
                # except (ValueError, IndexError):
                #     print('GO')
                #     triple_clicker()

                # test of this text to find what it gives
                # print(f"Extracted Text {i}:", text)


    class QuadImageManipulator:

        @staticmethod
        def extract_targets(screenshot_path, td):  # td = targets dir
            # Load the screenshot
            screenshot_path = os.path.join(screenshot_path, 'level_screen.png')
            scns = Image.open(screenshot_path)  # scns = screenshot
            target_regions = [
                (744, 318, 832, 393),  # Example: (left, top, right, bottom)
                (847, 318, 935, 393),
                (951, 318, 1039, 393),
                (1055, 318, 1143, 393)
            ]
            # Extract and save target images
            for i, region in enumerate(target_regions):
                target_image = scns.crop(region)
                target_image_path = os.path.join(td, f'target_{i + 1}.png')
                target_image.save(target_image_path)

        @staticmethod
        def compare_targets_with_to_find(target_path, tfd):  # tfd = to find dir
            global targets
            targets = []
            for i in range(1, 5):
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
                    if similarity_index >= 0.77:
                        filename = filename[:-4]
                        if filename == 'pandelk':
                            filename = 'pandelka'
                        elif filename == 'ginge':
                            filename = 'ginger'
                        elif filename == 'can':
                            filename = 'cane'
                        targets.append(filename)
                        break

        @staticmethod
        def extract_number_of_targets(screenshot_path, tdn):  # td = targets numbers dir
            """
            quad target info
            X 771 Y 396 W 34 H 18
            X 875 Y 396 W 34 H 18
            X 980 Y 396 W 34 H 18
            X 1083 Y 396 W 34 H 18
            """
            # Load the screenshot
            screenshot_path = os.path.join(screenshot_path, 'level_screen.png')
            scns = Image.open(screenshot_path)  # scns = screenshot
            target_regions = [
                (771, 396, 805, 414),
                (875, 396, 909, 414),
                (980, 396, 1014, 414),
                (1083, 396, 1117, 414)
            ]
            # Extract and save target number images
            for i, region in enumerate(target_regions):
                target_image = scns.crop(region)
                target_image_path = os.path.join(tdn, f'target_number_{i + 1}.png')
                target_image.save(target_image_path)

        @staticmethod
        def extract_numbers_of_targets_to_values():
            global working_dir
            targets_directory = 'targets'
            targets_path = os.path.join(working_dir, targets_directory)
            target_numbers.clear()
            # Extract targets numbers
            tar_dir = 'target_numbers'
            targets_number_path = os.path.join(working_dir, tar_dir)
            if not os.path.exists(targets_number_path):
                os.makedirs(targets_path)
            QuadImageManipulator.extract_number_of_targets(screenshot_dir, targets_number_path)

            # Set the path to the Tesseract executable
            # (modify this based on your installation; bellow is the default location
            # for windows). Get the installation from: https://github.com/tesseract-ocr/tesseract
            pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

            # 3ple target loader
            # Load the images
            for i in range(1, 5):
                target_numbers_path = 'target_numbers'
                image_path = os.path.join(working_dir, target_numbers_path)
                open_image = os.path.join(image_path, f"target_number_{i}.png")
                img = Image.open(open_image)

                # Preprocess the image (convert to grayscale)
                img = img.convert("L")

                # Use Tesseract OCR to extract text
                text = pytesseract.image_to_string(img, config='--psm 6')
                # try:
                target_numbers[f"{targets[i - 1]}"] = int(text[-2])
                # except (ValueError, IndexError):
                #     print("GO")
                #     quad_clicker()


                # test of this text to find what it gives
                # print(f"Extracted Text {i}:", text)


    find_triple_or_quad(screenshot_dir)


    def triple_clicker():
        # Bellow is 3ple target initialization
        # Extract targets
        targets_directory = 'targets'
        targets_path = os.path.join(working_dir, targets_directory)
        if not os.path.exists(targets_path):
            os.makedirs(targets_path)
        TripleImageManipulator.extract_targets(screenshot_dir, targets_path)

        # Compare targets to images in the to_find directory
        imgs_comp_directory = 'imgs_comp'
        to_find_directory = 'to_find'
        to_find_path = os.path.join(working_dir, imgs_comp_directory, to_find_directory)
        TripleImageManipulator.compare_targets_with_to_find(targets_path, to_find_path)

        # Extract the numbers from the target values
        TripleImageManipulator.extract_numbers_of_targets_to_values()

    def triple_clicker_plus_4():
        # Bellow is 3ple target initialization + 4 px
        # Extract targets
        targets_directory = 'targets'
        targets_path = os.path.join(working_dir, targets_directory)
        if not os.path.exists(targets_path):
            os.makedirs(targets_path)
        TripleImageManipulator.extract_targets_plus_4(screenshot_dir, targets_path)

        # Compare targets to images in the to_find directory
        imgs_comp_directory = 'imgs_comp'
        to_find_directory = 'to_find'
        to_find_path = os.path.join(working_dir, imgs_comp_directory, to_find_directory)
        TripleImageManipulator.compare_targets_with_to_find(targets_path, to_find_path)

        # Extract the numbers from the target values
        TripleImageManipulator.extract_numbers_of_targets_to_values()


    def quad_clicker():
        targets_directory = 'targets'
        targets_path = os.path.join(working_dir, targets_directory)
        if not os.path.exists(targets_path):
            os.makedirs(targets_path)
        QuadImageManipulator.extract_targets(screenshot_dir, targets_path)
        imgs_comp_directory = 'imgs_comp'
        to_find_directory = 'to_find'
        to_find_path = os.path.join(working_dir, imgs_comp_directory, to_find_directory)
        QuadImageManipulator.compare_targets_with_to_find(targets_path, to_find_path)
        QuadImageManipulator.extract_numbers_of_targets_to_values()
        # print(target_numbers)


    if not QUAD:
        triple_clicker()
    elif QUAD:
        quad_clicker()


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
            board_image_path = os.path.join(dump_dir, f'board_icon_{str(i + 1).zfill(2)}.png')
            board_image.save(board_image_path)


    get_board_images(screenshot_dir)
    targets_to_hit = targets.copy()


    def get_coordinates_of_board_icons(board_path, to_find_path):
        board_icons = os.listdir(board_path)
        to_find_icons = os.listdir(to_find_path)

        for board_icon in board_icons:
            board_icon_path = os.path.join(board_path, board_icon)
            board_image = Image.open(board_icon_path)
            if not targets:
                break

            for to_find_icon in to_find_icons:
                to_find_icon_path = os.path.join(to_find_path, to_find_icon)
                to_find_image = Image.open(to_find_icon_path)

                board_image_resized = board_image.resize(to_find_image.size)

                board_np = np.array(board_image_resized)
                to_find_np = np.array(to_find_image)

                # Calculate Structural Similarity Index (SSI) with a smaller win_size
                smaller_side = min(board_np.shape[0], board_np.shape[1], to_find_np.shape[0], to_find_np.shape[1])
                win_size = min(smaller_side, 3)
                similarity_index, _ = ssim(board_np, to_find_np, win_size=win_size, full=True)

                # Print the similarity index for each image
                similarity_index_formatted = float(f"{similarity_index:.2f}")
                if similarity_index_formatted >= 0.90:
                    # print(f"Similarity index between {board_icon} and {to_find_icon}: {similarity_index_formatted:.2f}")
                    found_icon_name = to_find_icon[:-4]
                    if found_icon_name in targets:
                        target_numbers[found_icon_name] -= 1
                        if target_numbers[found_icon_name] == 0:
                            target_numbers.pop(found_icon_name)
                            targets.remove(found_icon_name)

                        parts = board_icon.split("_")[1:]
                        icon_number = "_".join(parts)[:-4]
                        icon_number = str(icon_number)
                        coordinates_of_icon = icon_coordinates.get(icon_number)
                        # print(f"Coordinates of icon: {coordinates_of_icon}")
                        # print(f"Found icon name: {found_icon_name}")
                        board_icon_coordinates[found_icon_name].append(coordinates_of_icon)
                    break

    def test_if_moved_board(screenshot_path):
        global MOVED
        screenshot_path = os.path.join(screenshot_path, 'board_icon_01.png')
        scns = Image.open(screenshot_path)  # scns = screenshot
        target_region = [
            (0, 0, 4, 74)
        ]
        # Extract and save region
        for i, region in enumerate(target_region):
            cropped = scns.crop(region)
            cropped_path = os.path.join(screenshot_dir, f'crop_board.png')
            cropped.save(cropped_path)

        icd = 'imgs_comp'
        tfd = 'to_find_board_moved'
        tfp = os.path.join(working_dir, icd, tfd)
        crop_path = os.path.join(screenshot_dir, 'crop_board.png')
        to_compare_if_moved = os.path.join(icd, tfp, 'compare_crop.png')
        crop_image_open = Image.open(crop_path)
        to_compare_if_moved = Image.open(to_compare_if_moved)

        # Convert to np array
        crop_image_np = np.array(crop_image_open)
        to_compare_np = np.array(to_compare_if_moved)

        # Calculate Structural Similarity Index (SSI) with a smaller win_size
        smaller_side = min(to_compare_np.shape[0], to_compare_np.shape[1], crop_image_np.shape[0],
                           crop_image_np.shape[1])
        win_size = min(smaller_side, 3)
        similarity_index, _ = ssim(to_compare_np, crop_image_np, win_size=win_size, full=True)
        # Print the similarity index for each image
        similarity_index_formatted = float(f"{similarity_index:.2f}")
        # print(f"Similarity index with Crop: {similarity_index_formatted:.2f}")

        if similarity_index_formatted < 0.80:
            MOVED = False
        else:
            MOVED = True

    moved_dir_board = os.path.join(working_dir, 'board_dump')
    test_if_moved_board(moved_dir_board)

    # Set the paths to the board and to_find directories
    board_icons_directory = 'board_dump'
    if MOVED:
        to_find_icons_directory = 'to_find_board_moved'
    else:
        to_find_icons_directory = 'to_find_board'
    board_icons_path = os.path.join(working_dir, board_icons_directory)
    to_find_icons_path = os.path.join(working_dir, 'imgs_comp', to_find_icons_directory)
    # Compare board icons with to_find icons
    get_coordinates_of_board_icons(board_icons_path, to_find_icons_path)

    for target in targets_to_hit:
        for click in range(len(board_icon_coordinates[target])):
            target_x = board_icon_coordinates[target][-1][0]
            target_y = board_icon_coordinates[target][-1][1]
            board_icon_coordinates[target].pop()
            pyautogui.leftClick(target_x, target_y)
            # time.sleep(0.5)

    elapsed_time = time.time() - start_time
    if elapsed_time >= duration:
        break
    time.sleep(2)

# print(f"Targets: {targets}")
# print(f"Target numbers: {target_numbers}")
# print(f"Icon coordinates: {board_icon_coordinates}")
end_time = time.time()
execution_time = end_time - start_time
print(f"Execution time: {execution_time} seconds")
