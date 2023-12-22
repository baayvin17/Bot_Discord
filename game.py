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
