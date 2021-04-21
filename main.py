""" First script for my PCBS project """
""" This for the partial report """


from expyriment import design, control, stimuli, io
import useful_functions as usf
import random

MAX_DELAY_RESPONSE = 10000
N_TRIALS = 4
DISTANCE_TO_ORIGIN = 400


set_1 = [['1', '3', '4', '5', '6', '8'], ['C', 'J', 'P', 'Q', 'X', 'Y']]
set_2 = [['2', '3', '5', '6', '7', '8'], ['E', 'J', 'L', 'N', 'P', 'U']]
set_3 = [['2', '4', '5', '6', '7', '7'], ['A', 'B', 'G', 'S', 'T', 'Z']]

dictionnaire = usf.dictionnaire()
exposure_conditions = [90, 120, 150] # à vérifier

n_set, set_exp = usf.which_set_of_characters(set_1, set_2, set_3)



exp = design.Experiment(name = 'Partial report of characters', text_size = 40)
control.initialize(exp)
block_1 = design.Block(name = "Partial report")

choice_nb_digits = []
for k in range(N_TRIALS):
	index, liste = usf.make_list(set_exp)
	choice_nb_digits.append(index)
	trial = usf.draw_characters(liste, DISTANCE_TO_ORIGIN)
	liste_constantes = usf.characters2constants(liste, dictionnaire) # ça ne va pas marcher ça
	block_1.add_trial(trial)

trial_circle = design.Trial()
circle = stimuli.Circle(3)
circle.preload()
trial_circle.add_stimulus(circle)

trial_waiting = design.Trial()
msg_waiting = stimuli.TextLine("Press when ready for the next trial")

exp.add_block(block_1)
blankscreen = stimuli.BlankScreen()

instructions_partial = stimuli.TextScreen("Instructions", f"""Letters and digits will be displayed on the screen 
		Your task is to report as many digits as possible while ignoring letters""")
instructions_whole = stimuli.TextScreen("Instructions", f""" Letters and digits will be displayed on the screen.
Your task is to report as many characters as possible, be they letters or digits""")



exp.add_data_variable_names(['n_set', 'partial', '3_digits','trial', 'respkey', 'RT']) # int, y/n, y/n, int, int, int

control.start(skip_ready_screen = True)

instructions_partial.present()
exp.keyboard.wait()
blankscreen.present()

circle.present()
exp.clock.wait(100)
i = 0
for trial in block_1.trials:
	for stimulus in trial.stimuli:
		stimulus.present(clear = False)
	exp.clock.wait(1000) # temps de présentation du stimulus
	blankscreen.present()
	usf.get_data(exp, trial, liste_constantes, choice_nb_digits[i], i+1, n_set)
	i+= 1
	msg_waiting.present()
	exp.keyboard.wait()
	blankscreen.present()


control.end()

