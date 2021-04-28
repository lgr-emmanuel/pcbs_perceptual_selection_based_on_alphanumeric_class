import numpy as np
import random
from expyriment import design, control, stimuli, io

MAX_DELAY_RESPONSE = 3000
ENTER = 13

def dictionnaire():
	""" It maps the characters we use to the associated key constant of the keyboard
	for instance, the constant of A is 98"""
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
	""" It returns a list of characters randomly chosen, with equal chance to have 1 and 3 digits ; it returns also True if there are three digits in the liste, False otherwise"""
	index = random.randint(0, 1)
	if index == 0:
		boolean = 3
		liste = choose_three_digits(set_exp)
	else:
		liste = choose_one_digit(set_exp)
		boolean = 1
	return boolean, liste

def draw_characters(liste, distance_to_origin):
	""" Given a list of characters, it designs the trial which will allow us to display the characters on the screen. It returns the trial."""
	
	if len(liste) != 6:
		return "The length of the list does not match the experimental design"
	
	trial = design.Trial()
	for k, char in enumerate(liste):
		location = (np.cos(k*np.pi/3)*distance_to_origin, np.sin(k*np.pi/3)*distance_to_origin)
		stim = stimuli.TextLine(char, location)
		stim.preload()
		trial.add_stimulus(stim)
	return trial

def characters2constants(liste, dictionnaire):
	"""Given a list of characters, returns the list of associated constants"""
	liste_constantes = []
	for element in liste:
		value = dictionnaire[str(element)]
		liste_constantes.append(value)
	return liste_constantes

			
def circle():
	"""It designs the fixation point on the screen"""
	trial_circle = design.Trial()
	circle = stimuli.Circle(3)
	circle.preload()
	trial_circle.add_stimulus(circle)
	return circle

def design_unique_transition(index, n_trials):
	if index == n_trials -1:
		msg_waiting = stimuli.TextLine("The first part of the experiment is over. Press a key to continue")
		msg_waiting.preload()
		return msg_waiting
	msg_waiting = stimuli.TextLine("Press a key when ready for trial #{}".format(index+2))
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

def display_answer(trial, key, index): # il faut peut-être que je crée le stimulus *avant* de commencer l'expérience
	location = (-200 + index*200, 0)
	character = stimuli.TextLine(key, location)
	character.preload()
	trial.add_stimulus(character)
	character.present(clear = False)

		
def constant2character(constant, dictionnaire):
	"""Given a single constant, returns the associated character"""
	for char, val in dictionnaire.items():
		if val == constant:
			return char		
"""		
def try_get_data(exp, trial, list_licit_char, nb):
	# We assume that an array of digits and letter has just been displayed 
	#We want the user to write down the digits she noticed 
	for j in range(nb):
		key, rt = exp.keyboard.wait(list_licit_char)
		if key == ENTER:
			break
		elif key in list_licit_char:
			display_answer(trial, key, j)
			exp.data.add([trial, key])
"""
""" Je ferais mieux de faire un get_data, un remember_data un display data / error """

def get_data(exp, trial, list_licit_char, nb_occurences, n_trial, n_set, partial, reporting_error, blankscreen):
	key = 'a'
	n = 0
	while key != ENTER and n < nb_occurences:
		key, rt = exp.keyboard.wait()
		if key in list_licit_char:
			char = constant2character(key, dictionnaire())
			#display_answer(trial, key, n)
			exp.data.add([n_set, partial, nb_occurences, n_trial, char, rt])
			list_licit_char.remove(key)
			n += 1
		elif key != ENTER:
			reporting_error.present()
			exp.clock.wait(500)
			blankscreen.present()
			
	
def display_transition(blankscreen, msg_waiting, exp):
	blankscreen.present()
	exp.clock.wait(200)
	msg_waiting.present()
	exp.keyboard.wait()
	blankscreen.present()

	
