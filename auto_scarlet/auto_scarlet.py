from manipulator.manipulator import Manipulator

try:
    current_level = input('What is your current level?\n')
    auto_scarlet = Manipulator(current_level)
    auto_scarlet.worker()
    input("Press Enter to continue...")
except Exception as e:
    print(f"An error was encountered: {e}")
    input("Press Enter to continue...")
