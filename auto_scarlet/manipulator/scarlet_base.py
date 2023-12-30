import os

from manipulator.helper import HelperFunctions


class ScarletBase:
    def __init__(self):
        self.workdir = HelperFunctions.workdir()
        self.current_state_path = os.path.join(self.workdir, 'collector', 'current_state.png')
        # tiles:
        self.tiles_state_path = os.path.join(self.workdir, 'collector', 'tiles_state')
        self.comparing_images_tiles = os.path.join(self.workdir, 'collector', 'comp', 'tiles')
        # victory:
        self.victory_comp_path = os.path.join(self.workdir, 'collector', 'comp', 'analyze_board', 'victory.png')
        self.victory_state_path = os.path.join(self.workdir, 'collector', 'analyzation_state', 'victory_state.png')
        # shop:
        self.shop_comp_path = os.path.join(self.workdir, 'collector', 'comp', 'analyze_board', 'shop.png')
        self.shop_state_path = os.path.join(self.workdir, 'collector', 'analyzation_state', 'shop_state.png')
        # chest:
        self.chest_comp_path = os.path.join(self.workdir, 'collector', 'comp', 'analyze_board', 'chest.png')
        self.chest_state_path = os.path.join(self.workdir, 'collector', 'analyzation_state', 'chest_state.png')
        # pillar:
        self.pillar_comp_path = os.path.join(self.workdir, 'collector', 'comp', 'analyze_board', 'pillar.png')
        self.pillar_state_path = os.path.join(self.workdir, 'collector', 'analyzation_state', 'pillar_state.png')
        self.pillar_option_state_path = os.path.join(self.workdir, 'collector', 'analyzation_state')
        self.pillar_option_nok_path = os.path.join(self.workdir, 'collector', 'comp', 'analyze_board', 'option_nok.png')
        self.pillar_option_ok_path = os.path.join(self.workdir, 'collector', 'comp', 'analyze_board', 'option_ok.png')
        # riddle book
        self.riddle_book_comp_path = os.path.join(self.workdir, 'collector', 'comp', 'analyze_board', 'riddle.png')
        self.riddle_book_state_path = os.path.join(self.workdir, 'collector', 'analyzation_state', 'riddle_state.png')
        self.question_save_path = os.path.join(self.workdir, 'collector', 'analyzation_state', 'question.png')
        # collected chest
        self.collected_comp_path = os.path.join(self.workdir, 'collector', 'comp', 'analyze_board', 'collected.png')
        self.collected_state_path = os.path.join(self.workdir, 'collector', 'analyzation_state', 'collected_state.png')
