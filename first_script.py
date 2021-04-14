""" First script for my PCBS project """
""" This for the partial report """


from expyriment import design, control, stimuli
import useful_functions as usf

set_of_characters_1 = [['1', '3', '4', '5', '6', '8'], ['C', 'J', 'P', 'Q', 'X', 'Y']]
set_of_characters_2 = [['2', '3', '5', '6', '7', '8'], ['E', 'J', 'L', 'N', 'P', 'U']]
set_of_characters_3 = [['2', '4', '5', '6', '7', '7'], ['A', 'B', 'G', 'S', 'T', 'Z']]

print(usf.choose_three_digits(set_of_characters_1))

exp = design.Experiment(name = 'Partial report of characters', text_size = 40)
control.initialize(exp)

trial = design.Trial()

circle = stimuli.Circle(3)
circle.preload()
trial.add_stimulus(circle)

blankscreen = stimuli.BlankScreen()

for k in range(len(set_of_characters_1)//2):
	stim = stimuli.TextLine(set_of_characters_1[2*k], (100 + 100*k, 200))
	stim.preload()
	trial.add_stimulus(stim)

	



instructions = stimuli.TextScreen("Instructions", f"""Letters and digits will be displayed on the screen 
		Your task is to report as many digits as possible while ignoring letters""")





control.start()

instructions.present()
exp.keyboard.wait()
blankscreen.present()

circle.present()
exp.clock.wait(100)

for stimulus in trial.stimuli:
	stimulus.present(clear = False)

exp.clock.wait(3000)

control.end()

