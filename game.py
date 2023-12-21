# game.py

import random

class GuessingGame:
    def __init__(self):
        self.answer = random.randint(1, 100)
        self.attempts = 0

    def guess(self, number):
        self.attempts += 1
        if number == self.answer:
            return f"Bravo ! Vous avez deviné le nombre en {self.attempts} tentatives."
        elif number < self.answer:
            return "Le nombre est plus grand. Essayez à nouveau !"
        else:
            return "Le nombre est plus petit. Essayez à nouveau !"
