import random
from copy import deepcopy

from code.pair import Pair
from code.data import AnswerType


class Trial:
    def __init__(self, stimulus_list: list, stimulus_type_dict: dict, correct_answer_type: str, incorrect_answers_types: dict, stimulus_category: str):
        self.stimulus_n = len(stimulus_list)
        self.stimulus_list = stimulus_list
        self.stimulus_type_dict = stimulus_type_dict

        self.clues_list = None
        self.create_clues_list()

        self.answers_n = None
        self.answers_list = None
        self.correct_answer = None

        self.correct_answer_type = correct_answer_type
        self.incorrect_answers_types = incorrect_answers_types
        self.create_answers(correct_answer_type=self.correct_answer_type, incorrect_answers_types=self.incorrect_answers_types)

        self.stimulus_category = stimulus_category

    def create_clues_list(self):
        self.clues_list = []
        for i in range(self.stimulus_n - 1):
            pair = Pair(first_stimulus=self.stimulus_list[i], symbol=self.stimulus_type_dict["lower"],
                        second_stimulus=self.stimulus_list[i + 1], stimulus_type_dict=self.stimulus_type_dict)
            if random.random() < 0.5:
                pair.reverse_pair()
            self.clues_list.append(pair)
        random.shuffle(self.clues_list)

    def create_answers_identical(self):
        return [deepcopy(pair) for pair in self.clues_list]

    def create_answers_reversed(self):
        possible_answers = self.create_answers_identical()
        [pair.reverse_pair() for pair in possible_answers]
        return possible_answers

    def create_answers_distance_n(self, distance):
        assert 0 < distance < self.stimulus_n - 1, f"cant create answers with distance {distance} for answers_n = {self.answers_n}"
        possible_answers = []
        for i in range(self.stimulus_n - 1 - distance):
            pair = Pair(first_stimulus=self.stimulus_list[i], symbol=self.stimulus_type_dict["lower"],
                        second_stimulus=self.stimulus_list[i + 1 + distance], stimulus_type_dict=self.stimulus_type_dict)
            possible_answers.append(pair)
            pair = Pair(first_stimulus=self.stimulus_list[i], symbol=self.stimulus_type_dict["lower"],
                        second_stimulus=self.stimulus_list[i + 1 + distance], stimulus_type_dict=self.stimulus_type_dict)
            pair.reverse_pair()
            possible_answers.append(pair)
        return possible_answers

    @staticmethod
    def create_answers_incorrect(answers_list):
        [pair.reverse_symbol() for pair in answers_list]

    def choose_answers_to_create(self, answer_type: str):
        if answer_type == AnswerType.identical:
            return self.create_answers_identical()
        elif answer_type == AnswerType.reversed:
            return self.create_answers_reversed()
        elif answer_type == AnswerType.distance_1:
            return self.create_answers_distance_n(distance=1)
        elif answer_type == AnswerType.distance_2:
            return self.create_answers_distance_n(distance=2)
        elif answer_type == AnswerType.distance_3:
            return self.create_answers_distance_n(distance=3)
        else:
            raise Exception(f"answer_type={answer_type} is not implemented.")

    def create_answers(self, correct_answer_type: str, incorrect_answers_types: dict):
        self.correct_answer = random.choice(self.choose_answers_to_create(correct_answer_type))
        self.answers_list = [self.correct_answer]
        for answer_type, n in incorrect_answers_types.items():
            possible_answers = self.choose_answers_to_create(answer_type)
            self.create_answers_incorrect(possible_answers)
            self.answers_list += random.sample(possible_answers, n)
        random.shuffle(self.answers_list)
        self.answers_n = len(self.answers_list)

    def get_trail_description(self):
        return {"stimulus_n": self.stimulus_n,
                "stimulus_list": self.stimulus_list,
                "clues_list": self.clues_list,
                "answers_n": self.answers_n,
                "answers_list": self.answers_list,
                "correct_answer": self.correct_answer,
                "correct_answer_type": self.correct_answer_type,
                "incorrect_answers_types": self.incorrect_answers_types,
                "stimulus_category": self.stimulus_category}


if __name__ == "main":
    stim_list = [1, 2, 3, 4, 5] # list(string.ascii_letters[:4].upper())
    t = Trial(stimulus_list=stim_list,
              correct_answer_type=AnswerType.distance_2,
              incorrect_answers_types={AnswerType.identical: 1, AnswerType.reversed: 1, AnswerType.distance_1: 1, AnswerType.distance_2: 0})
    print(t.get_trail_description())