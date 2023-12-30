import os

import cv2
import numpy as np

from data_gatherer.take_screenshot import TakeScreenshot
from manipulator.helper import HelperFunctions
from manipulator.scarlet_base import ScarletBase
from PIL import Image, ImageEnhance
import pytesseract


class AnalyzeScreen(ScarletBase):
    def __init__(self):
        super().__init__()

    def victory_finder(self):
        victory_region = (931, 307, 952, 341)
        TakeScreenshot().take_screenshot()
        open_state_screenshot = Image.open(self.current_state_path)
        victory_crop = open_state_screenshot.crop(victory_region)
        victory_crop.save(self.victory_state_path)

        similarity_index = HelperFunctions.similarity_index(self.victory_state_path, self.victory_comp_path)

        if similarity_index >= 0.8:
            return True
        else:
            return False

    def shop_finder(self):
        shop_region = (861, 177, 1026, 208)
        TakeScreenshot().take_screenshot()
        open_state_screenshot = Image.open(self.current_state_path)
        shop_crop = open_state_screenshot.crop(shop_region)
        shop_crop.save(self.shop_state_path)

        similarity_index = HelperFunctions.similarity_index(self.shop_state_path, self.shop_comp_path)

        if similarity_index >= 0.8:
            return True
        else:
            return False

    def chest_finder(self):
        chest_region = (1046, 705, 1062, 726)
        TakeScreenshot().take_screenshot()
        open_state_screenshot = Image.open(self.current_state_path)
        chest_crop = open_state_screenshot.crop(chest_region)
        chest_crop.save(self.chest_state_path)

        similarity_index = HelperFunctions.similarity_index(self.chest_state_path, self.chest_comp_path)

        if similarity_index >= 0.8:
            return False
        else:
            return True

    def pillar_finder(self):
        pillar_region = (886, 293, 1009, 404)
        options = []
        TakeScreenshot().take_screenshot()
        open_state_screenshot = Image.open(self.current_state_path)
        pillar_crop = open_state_screenshot.crop(pillar_region)
        pillar_crop.save(self.pillar_state_path)

        similarity_index = HelperFunctions.similarity_index(self.pillar_state_path, self.pillar_comp_path)

        if similarity_index >= 0.8:
            option_regions = {
                'option_1': (742, 493, 760, 508),
                'option_2': (742, 596, 760, 611),
                'option_3': (742, 699, 760, 714)
            }
            for i in range(1, 4):
                option_region = option_regions[f"option_{i}"]
                option_crop = open_state_screenshot.crop(option_region)
                save_path = os.path.join(self.pillar_option_state_path, f"option_state_{i}.png")
                option_crop.save(save_path)

                similarity_index = HelperFunctions.similarity_index(self.pillar_option_ok_path, save_path)

                if similarity_index >= 0.95:
                    options.append(i)
            return options

    def riddle_finder(self):
        # Find if the clicked tile was a riddle book, if so, extract the riddle.
        riddle_region = (886, 293, 1009, 404)
        TakeScreenshot().take_screenshot()
        riddle_question = ''
        open_state_screenshot = Image.open(self.current_state_path)
        riddle_crop = open_state_screenshot.crop(riddle_region)
        riddle_crop.save(self.riddle_book_state_path)

        similarity_index = HelperFunctions.similarity_index(self.riddle_book_state_path, self.riddle_book_comp_path)

        if similarity_index >= 0.8:
            question_region = (748, 400, 1138, 444)
            question_crop = open_state_screenshot.crop(question_region)
            question_crop.save(self.question_save_path)

            pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

            img = Image.open(self.question_save_path)
            img = img.convert('L')
            img = ImageEnhance.Contrast(img).enhance(2.0)
            _, binary_img = cv2.threshold(np.array(img), 128, 255, cv2.THRESH_BINARY)

            text = pytesseract.image_to_string(Image.fromarray(binary_img), config='--psm 6')
            riddle_question = text[:-1]
            riddle_question = riddle_question.replace('\n', ' ')
        return riddle_question

    def collected_chest(self):
        # Find if the clicked tile was a chest
        collected_region = (881, 367, 1004, 397)
        TakeScreenshot().take_screenshot()
        open_state_screenshot = Image.open(self.current_state_path)
        collected_crop = open_state_screenshot.crop(collected_region)
        collected_crop.save(self.collected_state_path)

        similarity_index = HelperFunctions.similarity_index(self.collected_state_path, self.collected_comp_path)

        if similarity_index >= 0.8:
            return True
        else:
            return False

