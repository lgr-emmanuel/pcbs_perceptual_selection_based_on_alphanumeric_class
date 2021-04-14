""" First script for my PCBS project """
""" This for the partial report """


from expyriment import design, control, stimuli, io
import useful_functions as usf

MAX_DELAY_RESPONSE = 10000
N_TRIALS = 4
DISTANCE_TO_ORIGIN = 400


set_1 = [['1', '3', '4', '5', '6', '8'], ['C', 'J', 'P', 'Q', 'X', 'Y']]
set_2 = [['2', '3', '5', '6', '7', '8'], ['E', 'J', 'L', 'N', 'P', 'U']]
set_3 = [['2', '4', '5', '6', '7', '7'], ['A', 'B', 'G', 'S', 'T', 'Z']]

exposure_conditions = [90, 120, 150] # à vérifier

exp = design.Experiment(name = 'Partial report of characters', text_size = 40)
control.initialize(exp)

trial = design.Trial()

circle = stimuli.Circle(3)
circle.preload()
trial.add_stimulus(circle)

blankscreen = stimuli.BlankScreen()
instructions = stimuli.TextScreen("Instructions", f"""Letters and digits will be displayed on the screen 
		Your task is to report as many digits as possible while ignoring letters""")

""" essayons de faire un essai qui soit joli """

liste = usf.choose_three_digits(set_1)
print(liste)
trial = usf.draw_characters_on_screen(liste, trial, DISTANCE_TO_ORIGIN)


control.start()

instructions.present()
exp.keyboard.wait()
blankscreen.present()

circle.present()
exp.clock.wait(100)

for stimulus in trial.stimuli:
	stimulus.present(clear = False)

exp.clock.wait(3000)

""" C'est ici qu'il faut récupérer ce que les gens ont vu, de préférence avec une jolie fonction """

control.end()

