import atexit
import random
from os.path import join
import csv
from psychopy import visual, event, core

from code.show_info import show_instructions, part_info
from code.load_data import load_config
from code.screen_misc import get_screen_res
from code.prepare_block import prepare_block

RESULTS = []
PART_ID = ""


@atexit.register
def save_beh_results():
    num = random.randint(100, 999)
    with open(join('results', '{}_beh_{}.csv'.format(PART_ID, num)), 'w', newline='') as beh_file:
        dict_writer = csv.DictWriter(beh_file, RESULTS[0].keys(), delimiter=';')
        dict_writer.writeheader()
        dict_writer.writerows(RESULTS)


def run_trial(trial):
    pass


def run_block(win, config, screen_res, block_type, trials):
    # instructions
    show_instructions(win=win, config=config, screen_res=screen_res, block_type=block_type)
    for trial in trials:
        run_trial(trial)


def main():
    global PART_ID
    config = load_config()
    info, PART_ID = part_info()

    screen_res = dict(get_screen_res())
    win = visual.Window(list(screen_res.values()), fullscr=True, units='pix', screen=0, color=config["screen_color"])
    mouse = event.Mouse()

    clock = core.Clock()

    fixation = visual.TextBox2(win, color=config["fixation_color"], text=config["fixation_text"],
                               letterHeight=config["fixation_size"], pos=config["fixation_pos"],
                               alignment="center")

    clock_image = visual.ImageStim(win, image=join('images', 'clock.png'), interpolate=True,
                                   size=config['clock_size'], pos=config['clock_pos'])

    timer = visual.TextBox2(win, color=config["timer_color"], text=config["trial_time"],
                            letterHeight=config["timer_size"], pos=config["timer_pos"], alignment="center")

    extra_text = [visual.TextBox2(win, color=text["color"], text=text["text"], letterHeight=text["size"],
                                  pos=text["pos"], alignment="center")
                  for text in config["extra_text_to_show"]]

    feedback_text = (config["fdbk_incorrect"], config["fdbk_no_answer"], config["fdbk_correct"])
    feedback = {i: visual.TextBox2(win, color=config["fdbk_color"], text=text, letterHeight=config["fdbk_size"],
                                   alignment="center")
                for (i, text) in zip([0, -1, 1], feedback_text)}

    experiment_trials = prepare_block(block_info=config["experiment_trials"], randomize=config["experiment_randomize"])

    # training
    if config["do_training"]:
        training_trials = prepare_block(block_info=config["training_trials"], randomize=config["training_randomize"])
        run_block(win=win, config=config, screen_res=screen_res, block_type="training", trials=training_trials)

    # experiment
    run_block(win=win, config=config, screen_res=screen_res, block_type="experiment", trials=experiment_trials)

    # end
    show_instructions(win=win, config=config, screen_res=screen_res, block_type="end")


if __name__ == "__main__":
    main()
