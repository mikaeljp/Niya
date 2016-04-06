from pprint import pprint
from random import shuffle
from numpy.core.multiarray import ndarray


class Node(object):
    """
    All tile nodes have one front feature and one back feature and there are no duplicate tiles
    """
    # front features
    SUN = 'SUN'
    ANIMAL = 'ANIMAL'
    POEM = 'POEM'
    CLOUD = 'CLOUD'
    FRONT_FEATURES = [SUN, ANIMAL, POEM, CLOUD]

    # back features
    FLOWER = 'FLOWER'
    BLOSSOM = 'BLOSSOM'
    PINE = 'PINE'
    LEAF = 'LEAF'
    BACK_FEATURES = [FLOWER, BLOSSOM, PINE, LEAF]

    def __init__(self, feature_front, feature_back):
        self.feature_front = feature_front
        self.feature_back = feature_back
        self.feature_pairs = set()
        self.address = None
        self.player = None

    def set_address(self, address):
        self.address = address

    def add_feature_pair(self, node):
        if node not in self.feature_pairs:
            self.feature_pairs.add(node)
            node.feature_pairs.add(self)

    def is_playable(self):
        return not bool(self.player)

    def play(self, color):
        if not self.player:
            self.player = color
        else:
            return False

    def __str__(self):
        return "({r}:{c}) {front} {back}".format(r=self.address[0], c=self.address[1], front=self.feature_front, back=self.feature_back)


class Board(object):
    """
    The board is a 4x4 grid
    """
    addresses = ((0, 0), (0, 1), (0, 2), (0, 3),
                 (1, 0), (1, 1), (1, 2), (1, 3),
                 (2, 0), (2, 1), (2, 2), (2, 3),
                 (3, 0), (3, 1), (3, 2), (3, 3))

    RED = 1
    BLACK = -1

    def __init__(self):
        """
        construct the tile nodes
        """
        self.move_counter = 0
        self.active_player = self.RED
        self.tile_stack = []
        self.feature_map = self._feature_map()
        self.grid = [[None, None, None, None],
                     [None, None, None, None],
                     [None, None, None, None],
                     [None, None, None, None]]
        for f_feature in Node.FRONT_FEATURES:
            for b_feature in Node.BACK_FEATURES:
                tile = Node(f_feature, b_feature)
                for n in self.feature_map[f_feature] | self.feature_map[b_feature]:
                    tile.add_feature_pair(n)
                self.feature_map[f_feature].add(tile)
                self.feature_map[b_feature].add(tile)
                self.tile_stack.append(tile)
        shuffle(self.tile_stack)
        for tile, address in zip(self.tile_stack, self.addresses):
            tile.set_address(address)
            row, col = address
            self.grid[row][col] = tile

        # Initial playable moves are border tiles.
        self.playable_moves = [(0, 0), (0, 1), (0, 2), (0, 3), (1, 0), (1, 3), (2, 0), (2, 3), (3, 0), (3, 1), (3, 2), (3, 3)]

    def get_feature_matches(self, tile):
        return self.feature_map[tile.feature_front] | self.feature_map[tile.feature_back]

    def play(self, address):
        row, col = address
        tile = self.grid[row][col]
        # check that the tile is a legal play that hasn't been played yet
        if address in self.playable_moves and not tile.player:
            tile.player = self.active_player
            self.playable_moves = [t.address for t in tile.feature_pairs if t.is_playable()]
            if self.active_player == self.RED:
                self.active_player = self.BLACK
            else:
                self.active_player = self.RED
            self.move_counter += 1

    def evaluate_board(self):
        """
        The active player wins if:
            there are no playable moves for the next player
            the active player has 4 continuous pieces in any row, column, or diagonal
            the active player has a square of 4 pieces in any position on the board
        """
        if len(self.playable_moves) == 0:
            return self.active_player


    @staticmethod
    def _feature_map():
        feature_map = {}
        for feature in Node.FRONT_FEATURES:
            feature_map[feature] = set()
        for feature in Node.BACK_FEATURES:
            feature_map[feature] = set()
        return feature_map


def main():
    b = Board()
    while len(b.playable_moves) > 0:
        row, col = b.playable_moves[0]
        print(b.grid[row][col])
        b.play((row, col))
        pprint(b.playable_moves)
    print(b.move_counter)


if __name__ == '__main__':
    main()