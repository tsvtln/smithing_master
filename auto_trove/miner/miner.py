import pyautogui
import os
import numpy as np
import time
import pytesseract
import cv2
from PIL import Image
from skimage.metrics import structural_similarity as ssim


class Miner:
    def __init__(self, mine_counter: int):
        self.mine_counter = mine_counter
        self.workdir = Miner.workdir()
        self.collected_gems = {}
        self.collected_sundries = {}
        self.gem = False
        self.unlucky = False

    @staticmethod
    def workdir():
        cd = os.path.dirname(os.path.abspath(__file__))
        pd = os.path.abspath(os.path.join(cd, os.pardir))
        return pd

    def worker(self):
        self.take_screenshot()
        self.unlucky_finder()
        if not self.unlucky:
            gem_name = self.get_gem_name()
            self.sort_collected_gems(gem_name)
            upgrade_finder = self.upgrade_finder()
            if not upgrade_finder:
                if self.gem:
                    # sell item
                    x, y = 833, 831
                    pyautogui.leftClick(x, y)
                else:
                    # sell item
                    x, y = 924, 831
                    pyautogui.leftClick(x, y)
        if self.mine_counter == 0:
            print('Mining operation completed.\n')

            if self.collected_gems:
                # Print Gems found
                print('#### Gems found ####')
                for i, (gem_type, gem_data) in enumerate(self.collected_gems.items()):
                    if i > 0:
                        print()
                    print(f'{gem_type} gems:')
                    for gem_name, count in gem_data.items():
                        print(f'{gem_name}: {count}')

            if self.collected_sundries:
                # Print Sundries found
                print('\n#### Sundries found ####')
                for sundry_name, count in self.collected_sundries.items():
                    print(f'{sundry_name}: {count}')
        else:
            time.sleep(3)
            self.click()

    def click(self):
        click_x = 1024
        click_y = 875
        self.mine_counter -= 1
        pyautogui.leftClick(click_x, click_y)
        time.sleep(3)
        self.worker()

    def take_screenshot(self):
        screenshot_dir = 'collector'
        screenshot_name = 'current_state.png'
        screenshot_path = os.path.join(self.workdir, screenshot_dir, screenshot_name)
        take_screenshot = pyautogui.screenshot()
        take_screenshot.save(screenshot_path)

    def get_gem_name(self):
        # Crop the gem name
        name_region = (856, 400, 1034, 431)
        state_screenshot_path = os.path.join(self.workdir, 'collector', 'current_state.png')
        open_state_screenshot = Image.open(state_screenshot_path)
        crop_gem_name = open_state_screenshot.crop(name_region)
        crop_gem_name.save(os.path.join(self.workdir, 'collector', 'cropped_gem_name.png'))

        # Find the gem name
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        cropped_gem_name_png = os.path.join(self.workdir, 'collector', 'cropped_gem_name.png')
        img = Image.open(cropped_gem_name_png)
        img = img.convert('L')
        _, binary_img = cv2.threshold(np.array(img), 128, 255, cv2.THRESH_BINARY)
        text = pytesseract.image_to_string(Image.fromarray(binary_img), config='--psm 6')
        text = text[:-1]
        return text

    def sort_collected_gems(self, gem_name):
        gem_name_lower = gem_name.lower()
        # gems
        gems = [
            'anemo',
            'pyro',
            'electro',
            'geo',
            'hydro'
        ]
        found_gem = next((gem for gem in gems if gem in gem_name_lower), None)
        if found_gem:
            self.gem = True
            found_gem = found_gem.capitalize()
            if found_gem not in self.collected_gems.keys():
                self.collected_gems[found_gem] = {gem_name: 1}
            else:
                if gem_name not in self.collected_gems[found_gem].keys():
                    self.collected_gems[found_gem][gem_name] = 1
                else:
                    self.collected_gems[found_gem][gem_name] += 1
        else:
            # sundries
            self.gem = False
            sundries = [
                'Mushroom',
                'Mushroom Cluster',
                'Tattered Boot',
                'Plain Boot',
                'Patterned Boot',
                'Glass Bottle',
                'Silvered Bottle',
                'Gilded Bottle',
                'Moneybag',
                'Money Chest',
                'Eggshell',
                'Rusty Hammer',
                'Battered Forging',
                'Ore Shard'
            ]
            sundry_found = next((sundry for sundry in sundries if sundry in gem_name), None)
            if sundry_found:
                if sundry_found not in self.collected_sundries.keys():
                    self.collected_sundries[sundry_found] = 1
                else:
                    self.collected_sundries[sundry_found] += 1

    def upgrade_finder(self):
        # crop region where upgrade indicator is
        upgrade_region = (992, 538, 1044, 578)
        state_screenshot_path = os.path.join(self.workdir, 'collector', 'current_state.png')
        open_state_screenshot = Image.open(state_screenshot_path)
        crop_upgrade_region = open_state_screenshot.crop(upgrade_region)
        crop_upgrade_region.save(os.path.join(self.workdir, 'collector', 'upgrade_region.png'))

        # check if upgradable
        load_image = os.path.join(self.workdir, 'collector', 'upgrade_region.png')
        load_image = Image.open(load_image)
        tfd = os.path.join(self.workdir, 'collector', 'comp')

        for filename in os.listdir(tfd):
            image_path = os.path.join(tfd, filename)
            compare_to_image = Image.open(image_path)

            compare_to_image = compare_to_image.resize(load_image.size)

            # Convert to np
            upgrade_crop = np.array(load_image)
            compare_image = np.array(compare_to_image)

            # Calculate Structural Similarity Index (SSI) with a smaller win_size
            smaller_side = min(compare_image.shape[0], compare_image.shape[1],
                               upgrade_crop.shape[0], upgrade_crop.shape[1])
            win_size = min(smaller_side, 3)
            similarity_index, _ = ssim(upgrade_crop, compare_image, win_size=win_size, full=True)
            similarity_index = float(f"{similarity_index:.2f}")
            if similarity_index >= 0.80:
                if filename == 'have_upgrade.png':
                    print(input("Found upgradable gem. Press enter to continue."))
                    return True
                elif filename == 'no_upgrade.png':
                    return False

    def unlucky_finder(self):
        map_region = (671, 724, 764, 809)
        open_state_screenshot = Image.open(os.path.join(self.workdir, 'collector', 'current_state.png'))
        crop_map_region = open_state_screenshot.crop(map_region)
        crop_map_region.save(os.path.join(self.workdir, 'collector', 'map_region.png'))

        load_unlucky_compare = Image.open(os.path.join(self.workdir, 'collector', 'comp', 'unlucky_compare.png'))
        load_cropped_image = Image.open(os.path.join(self.workdir, 'collector', 'map_region.png'))

        # Convert to np
        load_unlucky_compare_np = np.array(load_unlucky_compare)
        load_cropped_np = np.array(load_cropped_image)

        # Calculate Structural Similarity Index (SSI) with a smaller win_size
        smaller_side = min(load_cropped_np.shape[0], load_cropped_np.shape[1],
                           load_unlucky_compare_np.shape[0], load_unlucky_compare_np.shape[1])
        win_size = min(smaller_side, 3)
        similarity_index, _ = ssim(load_unlucky_compare_np, load_cropped_np, win_size=win_size, full=True)
        similarity_index = float(f"{similarity_index:.2f}")
        if similarity_index >= 0.80:
            self.unlucky = True
        else:
            self.unlucky = False
