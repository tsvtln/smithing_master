from manipulator.manipulator import Manipulator

current_level = input('What is your current level?\n')
auto_scarlet = Manipulator(current_level)
auto_scarlet.worker()
input("Press Enter to continue...")
