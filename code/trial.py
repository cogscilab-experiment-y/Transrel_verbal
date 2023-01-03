import random
from copy import deepcopy
from psychopy.visual import Window

from code.pair import Pair
from code.data import AnswerType


class Trial:
    def __init__(self, stimulus_list: list, stimulus_type_dict: dict, correct_answer_type: str, incorrect_answers_types: dict,
                 stimulus_category: str):
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

    def prepare_to_draw(self, config: dict, win: Window):
        def prepare_list_to_draw(stimulus_list: list, start_pos: list, distance: list, color: str, size: int):
            pos = [start_pos[0] - (len(stimulus_list) / 2 - 0.5) * distance[0], start_pos[1] - len(stimulus_list) / 2 * distance[1]]
            for pair in stimulus_list:
                pair.prepare_to_draw(position=pos, win=win, color=color, size=size)
                pos[0] += distance[0]
                pos[1] += distance[1]

        prepare_list_to_draw(stimulus_list=self.clues_list, start_pos=config["clue_pos"], distance=config["clue_dist"],
                             color=config["stimulus_color"], size=config["clue_size"])
        prepare_list_to_draw(stimulus_list=self.answers_list, start_pos=config["answer_pos"], distance=config["answer_dist"],
                             color=config["stimulus_color"], size=config["answer_size"])

    def set_auto_draw(self, flag: bool):
        for pair in self.clues_list:
            pair.set_auto_draw(flag)
        for pair in self.answers_list:
            pair.set_auto_draw(flag)

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
