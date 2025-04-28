# i plan on connecting this to my wordle graphics soon
# it chooses "soare" first, so i hard-coded that so it doesn't have to think every time
# the lookup table for the second guess is faster than thinking
# salet doesn't use greedy alg for first word, i didn't come up with that though

from collections import defaultdict
from copy import copy
from math import log
import numpy as np
from random import choice, shuffle

with open('wordle_words1.txt', 'r') as file:
    wordlist=[line.strip() for line in file.readlines()]
with open('wordle_words2.txt', 'r') as file:
	big_wordlist=set([line.strip() for line in file.readlines()])
	big_wordlist.update(wordlist)
alphabet = [chr(i) for i in range(ord('a'), ord('z')+1)]

lookup = {'cbccc': 'brond', 'bbcbc': 'crash', 'cbcbb': 'grate', 'cbcac': 'unrid', 'cbcca': 'courd', 'cbcbc': 'beard', 'cbaac': 'abled', 'bbccc': 'crags', 'cbccb': 'tonic', 'cbcba': 'grece', 'cbbca': 'flong', 'cbbcc': 'corni', 'cbcab': 'after', 'cbbbc': 'glare', 'cbacc': 'noway', 'bbbbc': 'leash', 'cbbba': 'repla', 'cbbac': 'alien', 'cbaca': 'allot', 'cbbcb': 'rotis', 'cbbab': 'alter', 'bbcca': 'trace', 'bbccb': 'trash', 'bbcac': 'ashen', 'bbcaa': 'asset', 'caccc': 'corny', 'cacbc': 'crumb', 'cabcc': 'bingy', 'cabac': 'lingy', 'cacac': 'gormy', 'caaac': 'baler', 'caacc': 'rally', 'babcc': 'basil', 'baccc': 'ricin', 'bacbb': 'chimp', 'caccb': 'corby', 'cacbb': 'haute', 'bbcba': 'fusty', 'cccbc': 'drone', 'cccba': 'runic', 'cccaa': 'crumb', 'ccabc': 'himbo', 'cccbb': 'trice', 'bccaa': 'pudor', 'ccbab': 'hotel', 'ccbac': 'livor', 'ccbbc': 'guile', 'cccac': 'nidor', 'ccccc': 'cornu', 'cccca': 'groin', 'ccacc': 'doily', 'ccccb': 'north', 'bcccc': 'micro', 'bbbca': 'blast', 'bcbbc': 'fouth', 'ccbcc': 'courd', 'bcbcc': 'boffs', 'ccbcb': 'troll', 'ccbca': 'bling', 'bccca': 'moria', 'bccac': 'rumor', 'cabbc': 'cadgy', 'cacaa': 'cadet', 'cacca': 'thing', 'cacab': 'thrum', 'bacbc': 'sumph', 'bccbc': 'rhone', 'bccba': 'quich', 'bbbcc': 'pucks', 'ccbba': 'fiend', 'cbabc': 'relay', 'cbabb': 'delta', 'cccab': 'mohur', 'bcccb': 'gurdy', 'babac': 'easel', 'cbaba': 'eclat', 'cbbbb': 'tramp', 'ccbbb': 'title', 'bccab': 'ester', 'bccbb': 'troth', 'baabc': 'false', 'cabcb': 'fatal', 'cabca': 'fault', 'ccaac': 'geoid', 'ccaaa': 'filet', 'ccacb': 'filth', 'ccbaa': 'fleet', 'caabc': 'halve', 'baccb': 'pasha', 'bcaaa': 'islet', 'babbc': 'lapse', 'cabab': 'later', 'cabbb': 'lathe', 'bbbba': 'least', 'bcbac': 'loser', 'bcbcb': 'lusty', 'baacc': 'palsy', 'ccaca': 'pilot', 'bcabc': 'pulse', 'aabcc': 'sadly', 'aacac': 'safer', 'aacca': 'saint', 'aaacc': 'noway', 'aaacb': 'salty', 'aaabc': 'salve', 'aaccc': 'yupon', 'aaccb': 'satin', 'aacbc': 'sauce', 'aacbb': 'saute', 'abbcc': 'chill', 'abbbc': 'scale', 'abccc': 'cramp', 'abcca': 'roman', 'abcbc': 'pharm', 'accbc': 'prink', 'accba': 'swept', 'acccc': 'unrip', 'acbcc': 'plouk', 'accca': 'churn', 'accac': 'thrip', 'accbb': 'novum', 'abbca': 'shalt', 'accaa': 'sheet', 'acbbc': 'chimp', 'acacc': 'silky', 'acccb': 'yoick', 'abcbb': 'grike', 'abbbb': 'stale', 'acbac': 'spiel', 'acbaa': 'sleet', 'acbba': 'smelt', 'acbcb': 'stool', 'abacc': 'solar', 'acabc': 'solve', 'acbca': 'spilt', 'abaca': 'splat', 'acaca': 'split', 'abccb': 'prink', 'abbcb': 'stalk', 'accab': 'puked', 'acbab': 'steel', 'acbbb': 'stole', 'abcba': 'sweat', 'caacb': 'talon', 'bbcbb': 'tease', 'ccabb': 'tilde', 'caaaa': 'valet', 'bacca': 'waist'} 

class Game():
	def __init__(s, word = choice(wordlist)):
		s.live = True
		s.word = word
		s.grays = []
		s.yellow_list = []
		s.yellow_dict={x:[] for x in range(5)}
		s.greens=[None for _ in range(5)]
		s.tries = 0

	def submit_guess(s, guess):
		s.tries += 1
		if s.word == guess:
			s.live = False
			return True
		for i, letter in enumerate(list(guess)):
			if letter == s.word[i]:
				s.greens[i]=letter
			elif letter in s.word:
				s.yellow_list.append(letter)
				s.yellow_dict[i].append(letter)
			else:
				s.grays.append(letter)

class AI:
	def __init__(s, word=choice(wordlist)):
		s.game = Game(word)
		s.possible_words = copy(wordlist)

	def get_possibleness(s, guess):
		letters=list(guess)
		for i, letter in enumerate(letters):
			if letter in s.game.grays:
				return False
			if letter in s.game.yellow_dict[i]:
				return False
			if s.game.greens[i] and not letter==s.game.greens[i]:
				return False
		for letter in s.game.yellow_list:
			if not letter in letters:
				return False
		return True
	
	def get_result(s,word,guess):
		result = ''
		for i, letter in enumerate(list(guess)):
			if letter == word[i]:
				result += 'a'
			elif letter in word:
				result += 'b'
			else:
				result += 'c'
		return result
	
	def get_guess_score(s, spread):
		result = 0
		for n in spread.values():
			result += log(len(s.possible_words)/n,2)*n  #/len(s.possible_words) not necessary (expeirmentally determiend), adding n**2 works nearly as well (scores 3.5513816925734023) and the only difference might just be in the best score comparisons when things are equal
		return result
	def choose_second_guess(s):
		'''result = s.get_result(s.game.word,'salet')
		if not result in lookup:
			lookup[result] = s.choose_guess()'''
		return lookup[s.get_result(s.game.word,'salet')]

	def choose_guess(s):
		s.possible_words = [word for word in s.possible_words if s.get_possibleness(word)]
		if len(s.possible_words) < 3:
			return s.possible_words[0]
		best_score = 0
		choice = None
		for guess in big_wordlist:
			spread = copy(defaultdict(int))
			for word in s.possible_words:
				spread[s.get_result(word,guess)] += 1
			score = s.get_guess_score(spread)
			if score > best_score or (score==best_score and guess in s.possible_words):
				best_score = score
				choice = guess
		
		return choice


'''word = 'twist'
assert word in wordlist'''

ai = AI('joint')
print('salet')
ai.game.submit_guess('salet')
guess = ai.choose_second_guess()
print(guess)
ai.game.submit_guess(ai.choose_second_guess())
while ai.game.live:
    guess = ai.choose_guess()
    print(guess)
    ai.game.submit_guess(guess)
print(f'Win in {ai.game.tries} tries!')
'''

total = 0
for word in wordlist:
    ai = AI(word)
    print('salet')
    ai.game.submit_guess('salet')
    guess = ai.choose_second_guess()
    print(guess)
    ai.game.submit_guess(ai.choose_second_guess())
    while ai.game.live:
        guess = ai.choose_guess()
        print(guess)
        ai.game.submit_guess(guess)
    print(f'Win in {ai.game.tries} tries!')
    total += ai.game.tries

print(lookup)
print(total/len(wordlist))
# 3.437823834196891'''
