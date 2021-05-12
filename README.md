# pcbs_perceptual_selection_based_on_alphanumeric_class
PCBS Final project : Perceptual selection based on alphanumeric class

## Description of Duncan's experiment
The purpose of the project is to simulate the experiments described in the article "Perceptual selection based on alphanumeric class" (Duncan 1983).

In this article, participants are shown biref displays of digits and letters. There are two different reports. In the partial report, participants are asked to report as many digits as possible, while ignoring the letters (or vice versa). In the whole report, they are asked to report both digits and letters. Participants take part to both reports, in a random order.

## Experimental findings
There are three main findings.
1. Participants would report more digits (resp letters) in the partial report than in the whole report
2. When letters can be ignored, the probability of reporting a given digit increases as the total number of digits decreases (and vice versa for letters)

Regardless of it, participants report more characters in the whole report, because they can report every character they spot. Contrarywise, in the partial report, the participant may spot a character s/he is not supposed to report: hence "wasting" attention for irrelevant characters.

## What I do
In this work, I shall therefore program the experiment (displaying characters). I also verify every response of the participant with the digits/letters/characters that are to be reported. I then store all the results in a .xpd  file.

I make a couple of simplifications compared to Duncan's experiment. 
1. I do not use the same sets of characters. Indeed, I want to ensure the maximal portability of the program. Yet, the characters A, Z, Q, W, M, Y are not located at the same place in French and Anglo-saxon keyboards. I therefore rule out these characters, even though Duncan makes use of it.
This is a loss, as Duncan chooses the three possible sets of characters in order to ensure a low/medium/high proximity between letters and digits (therefore making the partial report from quite simple to quite hard). Yet, portability is considered more important.

2. I shorten the experiment a lot. In Duncan's experiment, it takes around two hours to finish all the tasks. This is obviously too long for ou purpose. Hence, I decided to design only 4 trials for the partial report and 4 trials for the whole report. It should not take longer than 2 minutes for a participant to finish the experiment I design.

## To do
Had I had more time, I would have tried to make people run my experiment and do some data analysis upon the saved data (in the xpd files) to try to replicate Duncan's results.


