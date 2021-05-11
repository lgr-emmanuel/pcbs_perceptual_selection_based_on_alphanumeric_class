""" First script for my PCBS project """


from expyriment import design, control, stimuli, io
import useful_functions as usf
import random

MAX_DELAY_RESPONSE = 10000
N_TRIALS = 4
DISTANCE_TO_ORIGIN = 400
SPACE_BAR = 32

""" Each participant is stimulated with one of the following sets of characters, and with one only """
set_1 = [['1', '3', '4', '5', '6', '8'], ['C', 'J', 'P', 'Q', 'X', 'Y']]
set_2 = [['2', '3', '5', '6', '7', '8'], ['E', 'J', 'L', 'N', 'P', 'U']]
set_3 = [['2', '4', '5', '6', '7', '7'], ['A', 'B', 'G', 'S', 'T', 'Z']]

dict_char_to_keyboardconstants = usf.dict_map_char_to_keyboard_constant()
exposure_conditions = [90, 120, 150] # à vérifier

nb_set, set_chosen_for_exp = usf.which_set_of_characters(set_1, set_2, set_3)


exp = design.Experiment(name = 'Perceptual decision based on alphanumeric class', text_size = 40)
#control.set_develop_mode(on=True)

control.initialize(exp)

block_1 = design.Block(name = "Partial report")

choice_nb_digits_p = [] # For each trial, remember whether there are a single or three digits presented
list_of_lists_keyboard_constants_p = [] # For each trial, remember the list of keyboard constants used
list_of_lists_allowed_digits_p = [] # When we check validity, we need to compare responses with 'allowed' digits

for k in range(N_TRIALS): # We design the N_TRIALS = 4 trials for partial report
	nb_digits, list_of_characters_used = usf.make_list(set_chosen_for_exp)
	single_trial = usf.design_trial_drawing_characters(list_of_characters_used, DISTANCE_TO_ORIGIN)
	
	choice_nb_digits_p.append(nb_digits)
	
	list_of_keyboardconstants_used = usf.characters2keyboard_constants(list_of_characters_used, dict_char_to_keyboardconstants)
	list_of_lists_keyboard_constants_p.append(list_of_keyboardconstants_used)
	
	list_of_allowed_digits = usf.remove_letters_from_list_of_char(list_of_characters_used)
	list_of_lists_allowed_digits_p.append(list_of_allowed_digits)
	
	block_1.add_trial(single_trial)


block_2 = design.Block(name = "Whole report")

choice_nb_digits_w = [] # Same as for partial report
list_of_lists_keyboard_constants_w = [] # Same as for partial report
list_of_lists_char_w = []

for j in range(N_TRIALS): # We design the trials for whole report
	nb_digits, list_of_characters_used = usf.make_list(set_chosen_for_exp)
	single_trial = usf.design_trial_drawing_characters(list_of_characters_used, DISTANCE_TO_ORIGIN)
	block_2.add_trial(single_trial)
	
	choice_nb_digits_w.append(nb_digits)
	
	list_of_keyboardconstants_used = usf.characters2keyboard_constants(list_of_characters_used, dict_char_to_keyboardconstants)
	list_of_lists_keyboard_constants_w.append(list_of_keyboardconstants_used)
	
	list_of_lists_char_w.append(list_of_characters_used)
	
	
exp.add_block(block_1)
exp.add_block(block_2)


circle = usf.design_circle()
blankscreen = stimuli.BlankScreen()
list_transitions = usf.design_all_transitions(N_TRIALS)

instructions_partial = stimuli.TextScreen("Instructions", f"""Letters and digits will be displayed on the screen 
		Your task is to report as many digits as possible while ignoring letters. Press space bar when ready""")
instructions_whole = stimuli.TextScreen("Instructions", f""" Letters and digits will be displayed on the screen.
Your task is to report as many characters as possible, be they letters or digits. Press space_bar when ready""")



exp.add_data_variable_names(['n_set', ' partial', ' 3_digits',' #trial', ' response', ' validity', ' RT']) # int, boolean, boolean, int, list, list, int

control.start(skip_ready_screen = True)

instructions_partial.present()
exp.keyboard.wait(SPACE_BAR)
blankscreen.present()

circle.present()
exp.clock.wait(100)
i = 0
for trial in block_1.trials:
	for stimulus in trial.stimuli:
		stimulus.present(clear = False)
	exp.clock.wait(1000) # temps de présentation du stimulus jusque là ça tourne
	blankscreen.present()
	response_to_one_trial, rt_trial = usf.get_data_of_single_trial(exp, trial, list_of_lists_keyboard_constants_p[i], choice_nb_digits_p[i], i+1, nb_set)
	validity_of_one_trial = usf.check_validity_of_response(response_to_one_trial, list_of_lists_allowed_digits_p[i], choice_nb_digits_p[i])
	
	exp.data.add([nb_set, True, choice_nb_digits_p[i] == 3, i+1, response_to_one_trial, validity_of_one_trial, rt_trial])
	usf.display_transition_intertrials(blankscreen, list_transitions[i], exp)
	i+=1

control.end()

