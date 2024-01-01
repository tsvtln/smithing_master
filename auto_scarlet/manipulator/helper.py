import os
import sys
import numpy as np
from PIL import Image
from skimage.metrics import structural_similarity as ssim


class HelperFunctions:
    @staticmethod
    def workdir():
        if getattr(sys, 'frozen', False):
            # Find if program is running as a standalone executable
            return os.path.abspath(os.path.join(os.path.dirname(sys.executable)))
        else:
            # Return this path if program is in dev mode or .py instance.
            return os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))

    @staticmethod
    def similarity_index(state_path, comp_path):
        state_open = Image.open(state_path)
        comp_open = Image.open(comp_path)

        comp_open = comp_open.resize(state_open.size)

        state_np = np.array(state_open)
        comp_np = np.array(comp_open)

        smaller_side = min(comp_np.shape[0], comp_np.shape[1],
                           state_np.shape[0], state_np.shape[1])

        win_size = min(smaller_side, 3)

        similarity_index, _ = ssim(state_np, comp_np, win_size=win_size, full=True)
        return float(f"{similarity_index:.2f}")

    @staticmethod
    def riddle_solver(riddle):
        changers = ['{', '}', "'", "(", ")"]
        for char in changers:
            if char in riddle:
                riddle = (riddle.replace
                          ("{", "[").replace("}", "]").replace("'", "’").replace("(", "[").replace(")", "]"))
                break
        question = {
            "At what level is [Demon Invasion] system unlocked?": "D",
            "At what level is [Secret Stone] system unlocked?": "C",
            "At what level is the [Artifact] system unlocked?": "D",
            "At what level is the [Guild] system unlocked?": "B",
            "At what level is the [Trove Hunt] system unlocked?": "C",
            "At what level is [Wing] system unlocked?": "A",
            "How long does the Pinnacle Arena take each season?": "B",
            "How many Anemo Gems can you collect at most in the Gem Collection?": "D",
            "How many Artifacts can be placed in the Treasure House at most?": "B",
            "How many Bosses are there at most on each floor of the Scarlet Corridor?": "A",
            "How many Chests can be claimed at most in each Chapter during the adventure?": "C",
            "How many free chances do you have to challenge the Solo Arena every day?": "B",
            "How many players can u ask for help with boosting the Forging Anvil upgrade?": "B",
            "How many products are sold in the Grocery Stall at most?": "B",
            "How many Secret Stones can be inlaid at most?": "B",
            "How many times can you refine Secret Stones for free every day?": "D",
            "How many times can you smash the world Boss for free every day?": "A",
            "In Guild League, what are the minimum points required for claiming the Guild Rank Reward?": "D",
            "In the [Solo Arena], what does it cost if a player wants to challenge another player?": "C",
            "In the [Solo Arenal, what does it cost if a player wants to challenge another player?": "C",
            "What are some of the hunt tools?": "A",
            "What’s the name of the first unlocked pair of wings?": "B",
            "Which attributes of Wings can be purified?": "A",
            "Which attribute can be obtained when the [Clothing] part is enhanced to +5?": "B",
            "Which attribute can be obtained when the [Helmet] part is enhanced to +5?": "C",
            "Which attribute can be obtained when the [Pauldron] part is enhanced to +5?": "A",
            "Which attribute can be obtained when the [Weapon] part is enhanced to +5?": "D",
            "Which currency can be used in Tower Shop?": "B",
            "Which event doesn’t allow Spirit Pets in battles?": "A",
            "Which is a Spirit Pet type?": "D",
            "Which is the highest equipment quality?": "D",
            "Which is the highest Tier in the Solo Arena?": "D",
            "Which item can speed up the Forging Anvil upgrade?": "A",
            "Which item is needed for equipment forging?": "C",
            "Which item is required to upgrade a Spirit Pet?": "A",
            "Which item is required to obtain [Blazing Wings]": "C",
            "Which item is used to refresh quests in the [Trove Hunt] - [Daily Bounty]?": "A",
            "Which items are required to start a Trove Hunt?": "C",
            "Which monster is not in the Scarlet Corridor?": "B",
            "Which of the following attributes can the wings [Eternal Fire] provide?": "A",
            "Which of the following gems cannot be obtained from Trove Hunt?": "D",
            "Which of the following methods can you take to get [Arena Ticket]?": "C",
            "Which of the following methods can you take to get [Stormlight Plume]?": "A",
            "Which of the following rewards can be obtained by building the Guild?": "D",
            "Which part of appearance cannot be changed in Skin feature?": "C",
            "Which product is unlocked at the Guild Shop when Guild is Lv. 3?": "A",
            "Which product is unlocked at the Guild Shop when Guild is Lv. 5?": "C",
            "Which quality of equipment has only 1 sub-entry attribute?": "D",
            "Which reward is unavailable to the first place on the Taboo Tower ranking?": "D",
            "Which Spirit Pet can’t be synthesized?": "A",
            "What’s the highest title available in Master’s Path?": "C",
            "Which of the following attributes can the wing [Light of Holy Dome] provide?": "B",
            "How long does the [Pinnacle Arena] take each season?": "B"
        }

        if riddle in question.keys():
            return question[riddle]
        else:
            print(f"FAIL-SAVE HANDLER TO RIDDLE: {riddle}")
            return "A"
