from engine.gameobject import GameObject
from game.card import Card
import pygame


class Tape(GameObject):
    def __init__(self, cards, coords, app):
        GameObject.__init__(self, None, coords, None, app, -10)
        self.cards = []
        for c in cards:
            self.cards.append(Card(c, "green", 1, app.images[c + ".jpg"], (0, 0), self.transform, app))
        self.index = 3
        cursor = app.images["cursor.png"]
        GameObject(cursor, (-25, 220), self.transform, app, -2)
        GameObject(pygame.transform.flip(cursor, False, True), (-25, -60), self.transform, app, 10)
        self.init_cards()
        self.old = self.index + 1
        self.fast_mode = False

    def init_cards(self):
        for i in range(len(self.cards)):
            distance_head = i - self.index
            if distance_head <= 0:
                self.cards[i].color = "green"
                self.cards[i].power = -distance_head + 2
                if distance_head == 0:
                    self.cards[i].move_local_y(20)
            else:
                if distance_head == 1:
                    self.cards[i].flip()
                self.cards[i].color = "white"
                self.cards[i].power = distance_head + 2

    def update(self, delta_time):
        GameObject.update(self, delta_time)
        if self.fast_mode:
            return
        for i in range(len(self.cards)):
            if self.cards[i] is None:
                continue
            distance_head = i - self.index
            if distance_head == 0:
                self.cards[i].move_local_y(20)
            self.cards[i].transform.move_to((distance_head * 120 - 60, self.cards[i].transform.local_y), delta_time)

    def play_infest(self):
        for c in self.cards:
            if c is not None:
                c.power -= 2

    def read_head(self):
        c = self.cards[self.index]
        self.app.game_objects.remove(c)
        self.app.game_objects.remove(c.info)

    def write_head(self, new_head):
        new_head.flip()
        self.cards[self.old].flip()
        self.cards[self.index] = new_head
        self.old = self.index

    def remove_infest(self):
        for c in self.cards:
            if c is not None and c is not self.cards[self.index]:
                c.power += 2

    def play_cleansing(self):
        for c in self.cards:
            if c.color == self.cards[self.index].color:
                c.power += 2

    def play_coalition(self):
        pass

    def play_eteigneur(self):
        for c in self.cards:
            c.power -= 1

    def move_index(self):
        if 0 <= self.index < len(self.cards):
            card = self.cards[self.index]
            card.move_local_y(0)
        self.index += 1 if self.cards[self.index].color == "green" else -1

    def fast_update(self, symbol, offset):
        color = "green" if offset == 1 else "white"
        card = Card(symbol, color, 2, self.app.images[symbol + ".jpg"], (-60, 0),
                    self.transform, self.app)
        self.read_head()
        self.write_head(card)
        self.index += offset
        for i in range(len(self.cards)):
            distance_head = i - self.index
            if distance_head == 0:
                self.cards[i].move_local_y(20)
            self.cards[i].power = abs(distance_head) + 2
            self.cards[i].transform.local_x = distance_head * 120 - 60
