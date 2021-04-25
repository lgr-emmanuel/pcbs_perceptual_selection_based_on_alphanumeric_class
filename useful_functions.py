import numpy as np
import random
from expyriment import design, control, stimuli, io

MAX_DELAY_RESPONSE = 3000
ENTER = 13

def choose_three_digits(liste):
	indexes = [k for k in range(6)]
	chosen_indexes = np.random.choice(indexes, 3, replace = False)
	chosen_digits =  [liste[0][k] for k in chosen_indexes]
	chosen_indexes = np.random.choice(indexes, 3, replace = False)
	chosen_letters = [liste[1][k] for k in chosen_indexes]
	
	chosen_characters = chosen_digits + chosen_letters
	random.shuffle(chosen_characters)
	return chosen_characters


def choose_one_digit(liste):
	indexes = [k for k in range(6)]
	chosen_indexes = np.random.choice(indexes, 5, replace = False)
	chosen_letters =  [liste[1][k] for k in chosen_indexes]
	chosen_indexes = np.random.choice(indexes, 1)
	chosen_digit = [liste[0][k] for k in chosen_indexes]
	
	chosen_characters = chosen_digit + chosen_letters
	random.shuffle(chosen_characters)
	return chosen_characters
	
		
def which_set_of_characters(liste_1, liste_2, liste_3):
	""" The set of characters is set for the entire duration of the experiment """
	n = random.randint(1, 3)
	if n == 1:
		return 1, liste_1
	elif n == 2:
		return 2, liste_2
	else:
		return 3, liste_3

def dictionnaire():
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


def make_list(set_exp):
	index = random.randint(0, 1)
	if index == 0:
		index = 3
		liste = choose_three_digits(set_exp)
	else:
		liste = choose_one_digit(set_exp)
		index = 1
	return index, liste
			
def circle():
	trial_circle = design.Trial()
	circle = stimuli.Circle(3)
	circle.preload()
	trial_circle.add_stimulus(circle)
	return circle

def draw_characters(liste, distance_to_origin):
	if len(liste) != 6:
		return "The length of the list does not match the experimental design"
	
	trial = design.Trial()
	for k, char in enumerate(liste):
		location = (np.cos(k*np.pi/3)*distance_to_origin, np.sin(k*np.pi/3)*distance_to_origin)
		stim = stimuli.TextLine(char, location)
		stim.preload()
		trial.add_stimulus(stim)
	return trial

def message_reporting_mistake(trial):
	message = stimuli.TextLine('This digit was not presented on the screen')
	message.preload()
	trial.add_stimulus(message)
	message.present()

def display_answer(trial, key, index): # il faut peut-être que j'aie créé le stimulus *avant* de commencer l'expérience
	location = (-200 + index*200, 0)
	character = stimuli.TextLine(key, location)
	character.preload()
	trial.add_stimulus(character)
	character.present(clear = False)

def characters2constants(liste, dictionnaire):
	liste_constantes = []
	for element in liste:
		value = dictionnaire[str(element)]
		liste_constantes.append(value)
	return liste_constantes
		
def constant2character(constant, dictionnaire):
	for k, val in dictionnaire.items():
		if val == constant:
			return k		
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


def get_data(exp, trial, list_licit_char, nb_occurences, n_trial, n_set, partial = True):
	key = 'a'
	n = 0
	while key != ENTER and n < nb_occurences:
		key, rt = exp.keyboard.wait(keys = list_licit_char, duration = MAX_DELAY_RESPONSE)
		if key in list_licit_char:
			char = constant2character(key, dictionnaire())
			#display_answer(trial, key, n)
			exp.data.add([n_set, partial, nb_occurences == 3, n_trial, char, rt])
			list_licit_char.remove(key)
			n += 1
	
	
def design_unique_transition(index):
	msg_waiting = stimuli.TextLine("Press a key when ready for trial #{}".format(index+2))
	msg_waiting.preload()
	return msg_waiting

def design_all_transitions(n_trials):
	list_stimuli = []
	for k in range(n_trials):
		stim = design_unique_transition(k)
		list_stimuli.append(stim)
	return list_stimuli
	
	
def display_transition(blankscreen, msg_waiting, exp):
	blankscreen.present()
	exp.clock.wait(200)
	msg_waiting.present()
	exp.keyboard.wait()
	blankscreen.present()

	
