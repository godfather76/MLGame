# This will be where we create the world's dynamics
# CorpoPunk will be a move/action based game, where every one action spurs the world to do one action.
# When the player moves, the world moves.

class DynamicWorld:
    def __init__(self, root, main_game, *args, **kwargs):
        self.root = root
        self.main_game = main_game

    def move_world(self, *args, **kwargs):
        print("World taking its turn")
