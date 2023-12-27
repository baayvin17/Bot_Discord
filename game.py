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




import random

class CapitalQuizGame:
    def __init__(self):
        self.all_capitals = {
            "France": "Paris",
            "Germany": "Berlin",
            "United Kingdom": "London",
            "Italy": "Rome",
            "Spain": "Madrid",
            "Japan": "Tokyo",
            "China": "Beijing",
            "Brazil": "Brasília",
            "India": "New Delhi", 
            "Australia": "Canberra",
            
        }
        self.questions = []
        self.current_question = None
        self.correct_answers = 0
        self.attempts = 0
        self.max_questions = 10  # Maximum number of questions

    def get_next_question(self):
        if self.attempts >= self.max_questions:
            return None  # Toutes les questions ont été posées

        while True:
            # Génère une question jusqu'à ce qu'une question unique soit trouvée
            question = random.choice(list(self.all_capitals.keys()))
            if question not in self.questions:
                self.questions.append(question)
                self.current_question = question
                return f"Quelle est la capitale de {self.current_question} ?"

    def check_answer(self, user_answer):
        correct_answer = self.all_capitals.get(self.current_question)
        self.attempts += 1

        if user_answer.lower() == correct_answer.lower():
            self.correct_answers += 1
            return "Correct !"
        else:
            return f"Incorrect. La bonne réponse est {correct_answer}."

    def get_score(self):
        return f"Vous avez obtenu {self.correct_answers} réponses correctes sur {self.max_questions} questions."

# Déclarez quiz_game en tant que variable globale en dehors des fonctions
quiz_game = None


class HangmanGame:
    def __init__(self):
        # Liste de joueurs de foot connus
        self.word_list = [
            "messi", "ronaldo", "neymar", "mbappe", "salah",
            "halland", "kane", "suarez", "hazard", "debruyne",
            "lewandowski", "griezzmann", "ramos", "varane", "kroos",
            "neuer", "modric", "alves", "ozil", "courtois"
        ]

        self.word_to_guess = random.choice(self.word_list).upper()
        self.guesses = []
        self.max_attempts = 11  # Changement du nombre de chances
        self.attempts_left = self.max_attempts
        self.word_display = ['_'] * len(self.word_to_guess)

        # Liste représentant le dessin du pendu à chaque étape 
        self.hangman_steps = [
            """
            ---------
            |       |
            |
            |
            |
            |
            ---------
            """,
            """
            ---------
            |       |
            |       O
            |
            |
            |
            ---------
            """,
            """
            ---------
            |       |
            |       O
            |       |
            |
            |
            ---------
            """,
            """
            ---------
            |       |
            |       O
            |      /|
            |
            |
            ---------
            """,
            """
            ---------
            |       |
            |       O
            |      /|\\
            |
            |
            ---------
            """,
            """
            ---------
            |       |
            |       O
            |      /|\\
            |      /
            |
            ---------
            """,
            """
            ---------
            |       |
            |       O
            |      /|\\
            |      / \\
            |
            ---------
            """,
            """
            ---------
            |       |
            |       O
            |      /|\\
            |      / \\
            |     /
            ---------
            """,
            """
            ---------
            |       |
            |       O
            |      /|\\
            |      / \\
            |     /   \\
            ---------
            """,
            """
            ---------
            |       |
            |       O
            |      /|\\
            |      / \\
            |     /   \\
            |    /
            ---------
            """,
            """
            ---------
            |       |
            |       O
            |      /|\\
            |      / \\
            |     /   \\
            |    /     \\
            ---------
            """
        ]
    def display_instructions(self):
        return "Devinez le joueur de football connu."
    

    def display_word(self):
        return ' '.join(self.word_display)

    def display_hangman(self):
        index = self.max_attempts - self.attempts_left
        if 0 <= index < len(self.hangman_steps):
            return self.hangman_steps[index]
        else:
            return "Erreur dans l'affichage du pendu."

    def guess(self, letter):
        letter = letter.upper()

        if letter in self.guesses:
            return "Vous avez déjà deviné cette lettre. Essayez une autre."

        self.guesses.append(letter)

        if letter in self.word_to_guess:
            for i in range(len(self.word_to_guess)):
                if self.word_to_guess[i] == letter:
                    self.word_display[i] = letter

            if '_' not in self.word_display:
                return f"Bravo ! Vous avez deviné le mot : {self.word_to_guess}"

            return f"Bien joué ! Mot partiel : {self.display_word()}"
        else:
            self.attempts_left -= 1
            if self.attempts_left == 0:
                return f"Désolé, vous avez épuisé toutes vos tentatives. Le mot était : {self.word_to_guess}"
            
            # Afficher le dessin du pendu actuel
            hangman_display = self.display_hangman()
            return f"Incorrect. Il vous reste {self.attempts_left} tentatives. Mot partiel : {self.display_word()}\n{hangman_display}"
hangman_game = None