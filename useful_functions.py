import numpy as np
import random
from expyriment import design, control, stimuli, io




def choose_three_digits(liste):
	indexes = [k for k in range(6)]
	chosen_indexes = np.random.choice(indexes, 3, replace = False)
	chosen_digits =  [liste[0][k] for k in chosen_indexes]
	chosen_indexes = np.random.choice(indexes, 3, replace = False)
	chosen_letters = [liste[1][k] for k in chosen_indexes]
	
	chosen_characters = chosen_digits + chosen_letters
	random.shuffle(chosen_characters)
	return chosen_characters


def choose_five_digits(liste):
	indexes = [k for k in range(6)]
	chosen_indexes = np.random.choice(indexes, 5, replace = False)
	chosen_digits =  [liste[0][k] for k in chosen_indexes]
	chosen_indexes = np.random.choice(indexes, 1)
	chosen_letters = [liste[1][k] for k in chosen_indexes]
	
	chosen_characters = chosen_digits + chosen_letters
	random.shuffle(chosen_characters)
	return chosen_characters
	
		
def which_set_of_characters(liste_1, liste_2, liste_3):
	n = random.randint(1, 4)
	if n == 1:
		return liste_1
	elif n == 2:
		return liste_2
	else:
		return liste_3


def draw_characters_on_screen(liste, trial, distance_to_origin):
	if len(liste) != 6:
		return "The length of the list does not match the experimental design"
	
	for k, char in enumerate(liste):
		location = (np.cos(k*np.pi/3)*distance_to_origin, np.sin(k*np.pi/3)*400)
		stim = stimuli.TextLine(char, location)
		stim.preload()
		trial.add_stimulus(stim)
	return trial


	
def get_data(exp, trial, list_licit_char):
	""" We assume that an array of digits and letter has just been displayed 
	We want the user to write down the digits she noticed """
	key, rt = exp.keyboard.wait(duration = MAX_WAIT_DELAY)
	if key in list_licit_char:
		exp.data.add([trial, key])
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
