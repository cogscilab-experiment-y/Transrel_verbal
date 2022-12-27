import random

from code.trial import Trial
from code.data import stimulus_category, stimulus_names, stimulus_types


def prepare_block(block_info: list, randomize: bool):
    trials = []
    for sub_block in block_info:
        for i in range(sub_block["n_trials"]):
            stimulus_cat = random.choice(stimulus_category)
            stimulus_names_list = random.sample(stimulus_names[stimulus_cat], sub_block["n_stimulus"])
            stimulus_type_dict = random.choice(stimulus_types[stimulus_cat])
            trial = Trial(stimulus_list=stimulus_names_list,
                          stimulus_type_dict=stimulus_type_dict,
                          correct_answer_type=sub_block["correct_answer_type"],
                          incorrect_answers_types=sub_block["incorrect_answers_types"],
                          stimulus_category=stimulus_category)
            trials.append(trial)

    if randomize:
        random.shuffle(trials)
    return trials


if __name__ == "__main__":
    test_block_info = [{"n_trials": 2, "n_stimulus": 4, "correct_answer_type": "identical",
                        "incorrect_answers_types": {"identical": 0, "reversed": 1, "distance_1": 1, "distance_2": 1}},
                       {"n_trials": 2, "n_stimulus": 4, "correct_answer_type": "reversed",
                        "incorrect_answers_types": {'identical': 1, "reversed": 0, "distance_1": 1, "distance_2": 1}}]
    test_trials = prepare_block(test_block_info, False)
    [print(trial.get_trail_description()) for trial in test_trials]
