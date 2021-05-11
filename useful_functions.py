import numpy as np
import random
from expyriment import design, control, stimuli, io

MAX_DELAY_RESPONSE = 3000
ENTER = 13
SPACE_BAR = 32

def dict_map_char_to_keyboard_constant():
	""" For instance, the constant of A is 98. *Careful* : this mapping holds 
	for a French "azerty" keyboard ; it might not hold for foreign keyboards"""
	
	dictionnaire = {}
	dictionnaire['1'] = 38
	dictionnaire['2'] = 233
	dictionnaire['3'] = 34
	dictionnaire['4'] = 39
	dictionnaire['5'] = 40
	dictionnaire['6'] = 45
	dictionnaire['7'] = 232
	dictionnaire['8'] = 95
	dictionnaire['9'] = 231

	for k in range(26):
		dictionnaire[chr(65+k)] = 97+k
	
	return dictionnaire


def which_set_of_characters(set_1, set_2, set_3):
	""" The set of characters a subject shall use is set for the entire duration of the experiment """
	n = random.randint(1, 3)
	if n == 1:
		return n, set_1
	elif n == 2:
		return n, set_2
	else:
		return n, set_3

def begin_with_partial_report():
	n = random.randint(0,1)
	if n == 0:
		return True
	return False

def choose_three_digits(liste):
	""" The list given in argument has two elements : a list of digits and a list of letters
	It returns a list of six characters, including three digits"""
	indexes = [k for k in range(6)]
	chosen_indexes = np.random.choice(indexes, 3, replace = False)
	chosen_digits =  [liste[0][k] for k in chosen_indexes]
	chosen_indexes = np.random.choice(indexes, 3, replace = False)
	chosen_letters = [liste[1][k] for k in chosen_indexes]
	
	chosen_characters = chosen_digits + chosen_letters
	random.shuffle(chosen_characters)
	return chosen_characters


def choose_one_digit(liste):
	""" The list given in argument has two elements : a list of digits and a list of letters
	It returns a list of six characters, including one digit"""
	indexes = [k for k in range(6)]
	chosen_indexes = np.random.choice(indexes, 5, replace = False)
	chosen_letters =  [liste[1][k] for k in chosen_indexes]
	chosen_indexes = np.random.choice(indexes, 1)
	chosen_digit = [liste[0][k] for k in chosen_indexes]
	
	chosen_characters = chosen_digit + chosen_letters
	random.shuffle(chosen_characters)
	return chosen_characters
	
		

def make_list(set_exp):
	""" It returns a list of characters randomly chosen, with equal chance to have 1 and 3 digits ;
	it returns also True if there are three digits in the liste, False otherwise"""
	index = random.randint(0, 1)
	if index == 0:
		boolean = 3
		liste = choose_three_digits(set_exp)
	else:
		liste = choose_one_digit(set_exp)
		boolean = 1
	return boolean, liste


def remove_letters_from_list_of_char(list_of_char):
	list_of_digits = []
	for char in list_of_char:
		try:
			int(char)
			list_of_digits.append(char)
		except:
			pass
	return list_of_digits


def design_trial_drawing_characters(list_of_used_characters, distance_to_origin):
	""" Given a list of characters, it designs the trial which will allow us to display
	 the characters on the screen. It returns the trial. The variable DISTANCE_TO_ORIGIN
	 is the radius of the circle on which the characters are drawn """
	
	if len(list_of_used_characters) != 6:
		return "The length of the list does not match the experimental design"
	
	trial = design.Trial()
	for k, char in enumerate(list_of_used_characters):
		location = (np.cos(k*np.pi/3)*distance_to_origin, np.sin(k*np.pi/3)*distance_to_origin)
		stim = stimuli.TextLine(char, location)
		stim.preload()
		trial.add_stimulus(stim)
	return trial

def characters2keyboard_constants(list_characters, dict_char_to_keyboardconstants):
	"""Given a list of characters, returns the list of associated constants"""
	list_keyboard_constants = []
	for element in list_characters:
		value = dict_char_to_keyboardconstants[str(element)]
		list_keyboard_constants.append(value)
	return list_keyboard_constants

			
def design_circle():
	"""It designs the fixation point on the screen"""
	trial_circle = design.Trial()
	circle = stimuli.Circle(3)
	circle.preload()
	trial_circle.add_stimulus(circle)
	return circle

def design_unique_transition(index, n_trials):
	if index == n_trials -1:
		msg_waiting = stimuli.TextLine("The first part of the experiment is over. Press space bar to continue")
		msg_waiting.preload()
		return msg_waiting
	msg_waiting = stimuli.TextLine("Press space bar when ready for trial #{}".format(index+2))
	msg_waiting.preload()
	return msg_waiting

def design_all_transitions(n_trials):
	list_stimuli = []
	for k in range(n_trials):
		stim = design_unique_transition(k, n_trials)
		list_stimuli.append(stim)
	return list_stimuli


def message_reporting_mistake():
	message = stimuli.TextLine('This digit was not presented on the screen')
	message.preload()
	return message

def display_answer(trial, char, index, total_nb_of_digits): # il faut peut-être que je crée le stimulus *avant* de commencer l'expérience
	if total_nb_of_digits == 3:
		location = (-200 + index*200, 0)
		character = stimuli.TextLine(char, location)
		character.present(clear = False)
	else:
		character = stimuli.TextLine(char, (0, 0))
		character.present()
		
def keyboard_constant2character(constant, dict_char_to_keyboardconstants):
	"""Given a single keyboard constant, returns the associated character"""
	for char, val in dict_char_to_keyboardconstants.items():
		if val == constant:
			return char		

""" Je ferais mieux de faire un get_data, un remember_data un display data / error """

def get_data_of_single_trial(exp, trial, list_licit_char, nb_digits, n_trial, n_set):
	""" Returns the list of the responses of the participant and the total reponse time of the trial """
	
	key = 'a'
	n = 0
	response = []
	rt_trial = 0
	while key != ENTER and n < nb_digits:
		key, rt = exp.keyboard.wait()
		rt_trial += rt
		if key == SPACE_BAR or key == ENTER:
			pass
		else:
			char = keyboard_constant2character(key, dict_map_char_to_keyboard_constant())
			response.append(char)
			display_answer(trial, char, n, nb_digits)
			if key in list_licit_char:
				list_licit_char.remove(key)
			n += 1
			
	exp.clock.wait(1000)
	return response, rt_trial

def check_validity_of_response(response, list_valid_responses, nb_digits):
	results_validity = []
	for element in response:
		if element in list_valid_responses:
			results_validity.append('H')
		else:
			results_validity.append('FA')
	for j in range(nb_digits - len(response)):
		results_validity.append('M')
	
	return results_validity

	
def display_transition_intertrials(blankscreen, msg_waiting, exp):
	blankscreen.present()
	exp.clock.wait(200)
	msg_waiting.present()
	exp.keyboard.wait()
	blankscreen.present()


""" Réfléchir à ne pas enregistrer le RT ; par contre enregistrer si la réponse est bonne """
	
