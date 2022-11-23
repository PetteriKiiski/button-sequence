class FinishLine:
    def __init__(self, player, x):
        self.vel = player.vel
        self.x = x
    def move(self):
        self.x -= self.vel