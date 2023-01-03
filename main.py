import atexit
import random
from os.path import join
import csv
from psychopy import visual, event, core

from code.show_info import show_instructions, part_info, show_stim, draw_stim_list, show_timer, show_clock
from code.load_data import load_config
from code.screen_misc import get_screen_res
from code.prepare_block import prepare_block
from code.check_exit import check_exit
from code.trial import Trial

RESULTS = []
PART_ID = ""


@atexit.register
def save_beh_results():
    num = random.randint(100, 999)
    with open(join('results', '{}_beh_{}.csv'.format(PART_ID, num)), 'w', newline='') as beh_file:
        dict_writer = csv.DictWriter(beh_file, RESULTS[0].keys(), delimiter=';')
        dict_writer.writeheader()
        dict_writer.writerows(RESULTS)


def run_trial(win: visual.Window, trial: Trial, config: dict, fixation: visual.TextBox2, clock: core.Clock, extra_text: list,
              clock_image: visual.ImageStim, timer: visual.TextBox2, show_feedback: bool, feedback: dict, block_type: str, n: int):
    chosen_key = None
    reaction_time = None
    chosen_answer = None
    acc = -1

    # fixation
    if config["fixation_time"] > 0:
        show_stim(fixation, config["fixation_time"], clock, win)

    draw_stim_list(extra_text, True)
    win.callOnFlip(clock.reset)
    win.callOnFlip(event.clearEvents)
    trial.set_auto_draw(True)
    while clock.getTime() < config["trial_time"]:
        show_clock(clock_image, clock, config)
        show_timer(timer, clock, config)

        chosen_key = event.getKeys(keyList=config["reaction_keys"].values())
        if chosen_key:
            reaction_time = clock.getTime()
            chosen_key = chosen_key[0]
            break
        check_exit()
        win.flip()

    if chosen_key:
        answer_idx = [answer_idx for answer_idx in config["reaction_keys"] if config["reaction_keys"][answer_idx] == chosen_key][0] - 1
        chosen_answer = trial.answers_list[answer_idx]
        if chosen_answer == trial.correct_answer:
            acc = 1
        else:
            acc = 0
    correct_key = config["reaction_keys"][trial.answers_list.index(trial.correct_answer)+1]

    trial_results = {"n": n,
                     "block_type": block_type,
                     "rt": reaction_time,
                     "acc": acc,
                     "chosen_answer": chosen_answer,
                     "chosen_key": chosen_key,
                     "correct_key": correct_key}
    trial_results.update(trial.get_trail_description())

    RESULTS.append(trial_results)

    trial.set_auto_draw(False)
    draw_stim_list(extra_text, False)
    if show_feedback:
        show_stim(feedback[acc], config["fdbk_show_time"], clock, win)

    wait_time = config["wait_time"] + random.random() * config["wait_jitter"]
    show_stim(None, wait_time, clock, win)


def run_block(win: visual.Window, config: dict, screen_res: dict, block_type: str, trials: list, clock: core.Clock, fixation: visual.TextBox2,
              clock_image: visual.ImageStim, timer: visual.TextBox2, extra_text: list, feedback: dict):
    # instructions
    show_instructions(win=win, config=config, screen_res=screen_res, block_type=block_type)
    show_feedback = config[f"fdbk_{block_type}"]
    for n, trial in enumerate(trials):
        run_trial(trial=trial, win=win, config=config, clock=clock, fixation=fixation, clock_image=clock_image, timer=timer, extra_text=extra_text,
                  feedback=feedback, block_type=block_type, show_feedback=show_feedback, n=n)


def main():
    global PART_ID
    config = load_config()
    info, PART_ID = part_info()

    screen_res = dict(get_screen_res())
    win = visual.Window(list(screen_res.values()), fullscr=True, units='pix', screen=0, color=config["screen_color"])
    mouse = event.Mouse()
    mouse.setVisible(False)

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

    experiment_trials = prepare_block(block_info=config["experiment_trials"], randomize=config["experiment_randomize"], config=config, win=win)

    # training
    if config["do_training"]:
        training_trials = prepare_block(block_info=config["training_trials"], randomize=config["training_randomize"], config=config, win=win)
        run_block(win=win, config=config, screen_res=screen_res, block_type="training", trials=training_trials, clock=clock, fixation=fixation,
                  clock_image=clock_image, timer=timer, extra_text=extra_text, feedback=feedback)

    # experiment
    run_block(win=win, config=config, screen_res=screen_res, block_type="experiment", trials=experiment_trials, clock=clock, fixation=fixation,
              clock_image=clock_image, timer=timer, extra_text=extra_text, feedback=feedback)

    # end
    show_instructions(win=win, config=config, screen_res=screen_res, block_type="end")


if __name__ == "__main__":
    main()
