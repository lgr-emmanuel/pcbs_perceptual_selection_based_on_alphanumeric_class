""" This program is the main ; many side functions are defined in < useful_functions_perceptual_decision.py >
The purpose of the program is to design the experiment run by Duncan in 1983. In this experiment, participants are briefly shown 6 characters (one *or* three of them are digits) and must report
	- only digits while ignoring letters in the partial report
	- every character in the whole report
Participants randomly begin with the partial (resp whole) report.

The purpose of Duncan's experiment is then to compare the responses and accuracy/validity of the responses between partial and whole report. 

 This program does six things : 
	1. Set all the constants/characters that are used
	2. For each participant, randomly decide which set of characters, which characters and digits themselves are to be used (and store them)
	3. Design all the trials
	4. Define the function that runs half the experiment (id est partial report experiment or whole report experiment)
	5. Run the function defined in (4.) for partial and whole report in good order
	6. Save all the relevant data (responses, RT, validity of the responses...) in an .xpd file

There is nothing to do for the user but to run the main program in a shell.
I have coded and run my script under Python 3.6.5 ; PyGame 1.9.3; Expyriment 0.10
"""

from expyriment import design, control, stimuli, io
import useful_functions_perceptual_decision as usf
import random

N_TRIALS = 4
DISTANCE_TO_ORIGIN = 400
SPACE_BAR = 32

""" Each participant is stimulated with one of the following sets of characters, and with one only """
set_1 = [['1', '3', '4', '5', '6', '8'], ['C', 'J', 'P', 'Q', 'X', 'R']]
set_2 = [['2', '3', '5', '6', '7', '8'], ['E', 'J', 'L', 'N', 'P', 'U']]
set_3 = [['2', '4', '5', '6', '7', '7'], ['D', 'B', 'G', 'S', 'T', 'H']]

dict_char_to_keyboardconstants = usf.dict_map_char_to_keyboard_constant()

nb_set, set_chosen_for_exp = usf.which_set_of_characters(set_1, set_2, set_3)


exp = design.Experiment(name = 'Perceptual decision based on alphanumeric class', text_size = 40)
#control.set_develop_mode(on=True)

control.initialize(exp)

block_1 = design.Block(name = "Partial report")

choice_nb_digits_p = [] # For each trial, remember whether there are a single or three digits presented
all_lists_of_keyboard_constants_p = [] # For each trial, remember the list of keyboard constants used
all_lists_of_allowed_digits_p = [] # When we check validity, we need to compare responses with 'allowed' digits

for k in range(N_TRIALS): # We design the N_TRIALS = 4 trials for partial report
	nb_digits, list_of_characters_used = usf.make_list(set_chosen_for_exp)
	single_trial = usf.design_trial_drawing_characters(list_of_characters_used, DISTANCE_TO_ORIGIN)
	
	choice_nb_digits_p.append(nb_digits)
	
	list_of_keyboardconstants_used = usf.characters2keyboard_constants(list_of_characters_used, dict_char_to_keyboardconstants)
	all_lists_of_keyboard_constants_p.append(list_of_keyboardconstants_used)
	
	list_of_allowed_digits = usf.remove_letters_from_list_of_char(list_of_characters_used)
	all_lists_of_allowed_digits_p.append(list_of_allowed_digits)
	
	block_1.add_trial(single_trial)


block_2 = design.Block(name = "Whole report")

choice_nb_digits_w = [] # Same as for partial report
all_lists_of_keyboard_constants_w = [] # Same as for partial report
all_lists_of_char_w = []

for j in range(N_TRIALS): # We design the trials for whole report
	nb_digits, list_of_characters_used = usf.make_list(set_chosen_for_exp)
	single_trial = usf.design_trial_drawing_characters(list_of_characters_used, DISTANCE_TO_ORIGIN)
	block_2.add_trial(single_trial)
	
	choice_nb_digits_w.append(nb_digits)
	
	list_of_keyboardconstants_used = usf.characters2keyboard_constants(list_of_characters_used, dict_char_to_keyboardconstants)
	all_lists_of_keyboard_constants_w.append(list_of_keyboardconstants_used)
	
	all_lists_of_char_w.append(list_of_characters_used)
	
	
exp.add_block(block_1)
exp.add_block(block_2)


instructions_partial = stimuli.TextScreen("Instructions", f"""Letters and digits will be displayed on the screen. 
Your task is to report as many digits as possible while ignoring letters. There are either 1 or 3 digits. You must report only digits you are fairly certain of. You have as much time as yuo want. If you have not caught as many digits as there were displayed, report those you noticed and then press ENTER to continue. Press SPACE BAR when ready""")

instructions_whole = stimuli.TextScreen("Instructions", f""" Letters and digits will be displayed on the screen.
Your task is to report as many characters as possible, be they letters or digits. You must report only characters you are fairly certain of. You have as much time as you want. If you have not caught as many characters as there were displayed, report those you noticed and then press ENTER to continue. Press SPACE BAR when ready""")


exp.add_data_variable_names(['n_set', ' is_partial', ' is_3_digits',' #trial', ' response', ' validity', ' RT']) # int, boolean, boolean, int, list, list, int

control.start(skip_ready_screen = True)


def run_session(exp, block, is_partial, list_exposure_duration, all_lists_of_keyboard_constants, all_lists_validity, choice_nb_digits, instructions, nb_set):
	""" This is the most important function of the project : it runs half the experiment : either the partial 
	experiment or the whole experiment """
	
	""" The variable < all_lists_validity > is called to check the validity of the responses at each trial.
	For partial report : it is the list of the list of allowed digits at each trial
	For whole report : it is the list of the list of the characters that are displayed at each trial """
	
	circle = usf.design_circle()
	blankscreen = stimuli.BlankScreen()
	list_transitions = usf.design_all_transitions(N_TRIALS)
	
	instructions.present()
	exp.keyboard.wait(SPACE_BAR)
	blankscreen.present()
	
	careful_msg = stimuli.TextScreen("Careful :", f""" When reporting digits, do not use a numpad, but use the keys on top of your keyboard. Moreover, if you want to report a '1', press *only* '&'. Do not press Shift + '&', it is not necessary. Press SPACE BAR when ready""")
	careful_msg.present()
	exp.keyboard.wait(SPACE_BAR)
	blankscreen.present()	
	
	i = 0
	exposure_duration = list_exposure_duration[i]
	for trial in block.trials: 
		# Run one trial and ask for responses, checks them and store
		circle.present()
		exp.clock.wait(200)
		
		for stimulus in trial.stimuli:
			stimulus.present(clear = False)
		exp.clock.wait(exposure_duration) 
		blankscreen.present()
		
		response_to_one_trial, rt_trial = usf.get_data_of_single_trial(exp, is_partial, trial, 		all_lists_of_keyboard_constants[i], choice_nb_digits[i], i+1, nb_set)
		validity_of_one_trial = usf.check_validity_of_response(is_partial, response_to_one_trial, all_lists_validity[i], choice_nb_digits[i])
	
		exp.data.add([nb_set, is_partial, choice_nb_digits[i] == 3, i+1, response_to_one_trial, validity_of_one_trial, rt_trial])
		usf.display_transition_intertrials(blankscreen, list_transitions[i], exp)
		i+=1


""" From here, the program consists in the experiment : we call the function that runs it"""
order = usf.begin_with_partial_report()
exposure_conditions = [90, 120, 150, 500]

if order is True:
	run_session(exp, block_1, True, exposure_conditions, all_lists_of_keyboard_constants_p, all_lists_of_allowed_digits_p, choice_nb_digits_p, instructions_partial, nb_set)
	run_session(exp, block_2, False, exposure_conditions, all_lists_of_keyboard_constants_w, all_lists_of_char_w, choice_nb_digits_w, instructions_whole, nb_set)

else:
	run_session(exp, block_2, False, exposure_conditions, all_lists_of_keyboard_constants_w, all_lists_of_char_w, choice_nb_digits_w, instructions_whole, nb_set)
	run_session(exp, block_1, True, exposure_conditions, all_lists_of_keyboard_constants_p, all_lists_of_allowed_digits_p, choice_nb_digits_p, instructions_partial, nb_set)
	
goodbye_message = stimuli.TextScreen("Thank you very much for participating to this experiment", f"""We wish you a nice day""")

goodbye_message.present()
exp.clock.wait(3000)

control.end()
