import sys
import pyautogui
import os
import numpy as np
import time
import pytesseract
import cv2
from PIL import Image, ImageEnhance
from skimage.metrics import structural_similarity as ssim

from data_gatherer.screen_analyzator import AnalyzeScreen
from manipulator.helper import HelperFunctions
from manipulator.scarlet_base import ScarletBase
from data_gatherer.take_screenshot import TakeScreenshot
from data_gatherer.tile_scanner import TileScanner


class Manipulator(ScarletBase):
    def __init__(self, current_level):
        super().__init__()
        self.current_level = current_level
        self.tiles = {}
        self.clickable_locations = {}
        self.tile_number_click_locations = {
            'tile_1': (733, 326),
            'tile_2': (839, 326),
            'tile_3': (947, 326),
            'tile_4': (1050, 326),
            'tile_5': (1157, 326),
            'tile_6': (733, 428),
            'tile_7': (839, 428),
            'tile_8': (947, 428),
            'tile_9': (1050, 428),
            'tile_10': (1157, 428),
            'tile_11': (733, 534),
            'tile_12': (839, 534),
            'tile_13': (947, 534),
            'tile_14': (1050, 534),
            'tile_15': (1157, 534),
            'tile_16': (733, 640),
            'tile_17': (839, 640),
            'tile_18': (947, 640),
            'tile_19': (1050, 640),
            'tile_20': (1157, 640),
            'tile_21': (733, 745),
            'tile_22': (839, 745),
            'tile_23': (947, 745),
            'tile_24': (1050, 745),
            'tile_25': (1157, 745)
        }
        self.portal_location = (0, 0)
        self.pillar_location = (0, 0)

    @property
    def current_level(self):
        return self._current_level

    @current_level.setter
    def current_level(self, value):
        try:
            value = int(value)
        except ValueError:
            raise ValueError("You must enter a number!")
        if not 1 <= value <= 10:
            raise ValueError("The current level must be between 1 and 10!")
        else:
            self._current_level = int(value)

    def worker(self):
        TakeScreenshot().take_screenshot()
        self.tiles = TileScanner(self).tile_recorder()
        self.find_clickable_tiles()
        if self.tiles:
            self.clicker()
        elif not self.tiles():
            # Complete Pillar selection
            pillar_x, pillar_y = self.pillar_location
            pyautogui.leftClick(pillar_x, pillar_y)
            options = AnalyzeScreen().pillar_finder()
            if options:
                x1, y1 = 950, 835
                x2, y2 = 0, 0
                option = options[0]
                if option == 1:
                    x2, y2 = 946, 535
                elif options == 2:
                    x2, y2 = 943, 639
                elif options == 3:
                    x2, y2 = 944, 737
                pyautogui.leftClick(x2, y2)
                time.sleep(0.5)
                pyautogui.leftClick(x1, y1)
                time.sleep(0.5)

            # Go to next level
            x, y = self.portal_location
            pyautogui.leftClick(x, y)
            self.current_level += 1
            if self.current_level != 5 and self.current_level != 10:
                self.worker()
            elif self.current_level == 5:
                pass
            elif self.current_level == 10:
                pass

    def find_clickable_tiles(self):
        to_del = []
        self.clickable_locations.clear()
        # Finds which tiles are clickable
        for tile_number, state_of_tile in self.tiles.items():
            if state_of_tile == 'gray_tile' or state_of_tile == 'thorn_tile':
                continue
            elif state_of_tile == 'portal_tile':
                self.portal_location = self.tile_number_click_locations[tile_number]
                to_del.append(tile_number)
            elif state_of_tile == 'clickable_tile':
                self.clickable_locations[tile_number] = self.tile_number_click_locations[tile_number]
            elif state_of_tile == 'home_tile':
                to_del.append(tile_number)
            elif state_of_tile == 'pillar_tile':
                to_del.append(tile_number)
                self.pillar_location = self.tile_number_click_locations[tile_number]
            else:
                self.clickable_locations[tile_number] = self.tile_number_click_locations[tile_number]

        for item in to_del:
            del self.tiles[item]
        for k, v in self.tiles.items():
            print(f"Key: {k}, Value: {v}")
        print('\n\n\n\n')

    def clicker(self):
        # Performs clicks based on analyzed data
        for tile_number, click_location in self.clickable_locations.items():
            x, y = click_location
            pyautogui.leftClick(x, y)
            if tile_number in self.tiles.keys():
                del self.tiles[tile_number]
            time.sleep(4)
            riddle = AnalyzeScreen().riddle_finder()
            if riddle:
                answer = HelperFunctions.riddle_solver(riddle)
                x1, y1 = 940,844
                x2, y2 = 0, 0
                if answer == 'A':
                    x2, y2 = 941, 493
                elif answer == 'B':
                    x2, y2 = 941, 585
                elif answer == 'C':
                    x2, y2 = 941, 669
                elif answer == 'D':
                    x2, y2 = 941, 762
                pyautogui.leftClick(x2, y2)
                time.sleep(1)
                pyautogui.leftClick(x1, y1)
                time.sleep(1)
            else:
                pyautogui.leftClick(x, y)
                time.sleep(4)
                if AnalyzeScreen().victory_finder():
                    x, y = 1210, 957
                    pyautogui.leftClick(x, y)
                    time.sleep(1)

                elif AnalyzeScreen().shop_finder():
                    if AnalyzeScreen().chest_finder():
                        x, y = 1087, 715
                        pyautogui.leftClick(x, y)
                        time.sleep(1)
                        x1, y1 = 1214, 1008
                        pyautogui.leftClick(x, y)
                        time.sleep(1)
                        x, y = 943, 851
                        pyautogui.leftClick(x, y)
                        time.sleep(1)
                    else:
                        x, y = 943, 851
                        pyautogui.leftClick(x, y)
                        time.sleep(1)

                elif AnalyzeScreen().collected_chest():
                    x, y = 1210, 957
                    pyautogui.leftClick(x, y)
                    time.sleep(1)

        # Loop back to worker to continue the program
        self.worker()

    def current_tiles(self):
        return self.tiles



