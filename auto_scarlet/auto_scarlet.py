from manipulator.manipulator import Manipulator
from data_gatherer.tile_scanner import TileScanner
from data_gatherer.take_screenshot import TakeScreenshot
from data_gatherer.screen_analyzator import AnalyzeScreen

# current_level = input('What is your current level\n')
current_level = 3
auto_scarlet = Manipulator(current_level)
# tile_scanner = TileScanner(auto_scarlet)
# auto_scarlet.worker()
# input("Press Enter to continue...")
# print(tile_scanner.tile_recorder())

screenshooter = TakeScreenshot()
screenshooter.take_screenshot()
# #
# screen_anal = AnalyzeScreen()
# # #
# print(screen_anal.riddle_finder())
