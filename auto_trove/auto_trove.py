import time
from miner.miner import Miner

trove_hunt_counter = int(input("How many hunts would you like to perform?\n"))
trove_miner = Miner(trove_hunt_counter)
time.sleep(2)
trove_miner.click()
