import random
from psychopy.visual import Window

from code.trial import Trial
from code.data import stimulus_category, stimulus_names, stimulus_types


def prepare_block(block_info: list, randomize: bool, config: dict, win: Window):
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
                          stimulus_category=stimulus_cat)
            trial.prepare_to_draw(config=config, win=win)
            trials.append(trial)

    if randomize:
        random.shuffle(trials)
    return trials
