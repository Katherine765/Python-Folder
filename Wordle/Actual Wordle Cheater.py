wordlist = []
with open('wordle_words1.txt', 'r') as file:
    wordlist=[line.strip() for line in file.readlines()]

def main(wordlist):
	process = input('Enter green letters in the following format: 1s 5e \n')
	process = process.split()
	green = {x:None for x in range(5)}
	for group in process:
		green[int(group[0])-1] = group[1]
	process = input('Enter yellow letters in the following format: 3t 3a \n')
	process = process.split()
	yellow = {x:[] for x in range(5)}
	somewhere=[]
	for group in process:
		yellow[int(group[0])-1].append(group[1])
		somewhere.append(group[1])
	grey = input('Enter grey letters in the following format: r p \n')
	grey = grey.split()

	game=Game(green, yellow, somewhere, grey)

	possible=[]
	for potential_guess in wordlist:
		if game.checkValidity(potential_guess):
			possible.append(potential_guess)

	game.generateData(possible)
	game.rank(possible)


class Game():
	def __init__(self, green, yellow, somewhere, grey):
		self.frequency, self.placement = {}, {}

		self.green = green
		self.yellow = yellow
		self.somewhere = somewhere
		self.grey = grey

		self.check=None
		self.scores={}

	def checkValidity(self, potential_guess):
		guess_list=list(potential_guess)

		for x, letter in enumerate(guess_list):
			#No grays in word
			if letter in self.grey:
				return False
				
			#No unmoved yellow
			if letter in self.yellow[x]:
				return False

		for x, letter in enumerate(self.somewhere):
        	#All yellows in word
			if not letter in guess_list:
				return False

		for x, key in enumerate(self.green.keys()):
			if not self.green[key] == guess_list[x]:
				if not self.green[key] is None:
					return False

		return True

	def generateData(self, possible):
		self.frequency=[0 for x in range(26)]
		self.placement=[[0 for x in range(5)] for x in range(26)]
		for possible_guess in possible:
			guess_list=list(possible_guess)
			for x in range(5):
				letterNum=ord(possible_guess[x])-97
				#frequency counted once per word
				if x == possible_guess.find(guess_list[x]):
					self.frequency[letterNum] += 1
				(self.placement[letterNum])[x] += 1


	def rank(self, possible):
		
		for possible_guess in possible:
			guess_list=list(possible_guess)

			score=0
			for x, letter in enumerate(guess_list):
				letterToNumber=ord(letter)-97
                #limits frequency points to 1 time per word
				if x == possible_guess.find(letter):
					score += self.frequency[letterToNumber]

				score += .55*(self.placement[letterToNumber])[x]

			self.scores[possible_guess] = round(score, 1)

		#turns it into a list
		#list
		self.scores = sorted(self.scores.items(), key=lambda x:x[1])
		#chooses last 5 items then reverses the order
		#dunno what happens if there are less than 5 options
		self.scores = self.scores[-5:]
		self.scores.reverse()
		print(self.scores)

main(wordlist)
