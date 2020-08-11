# ================================================================================================================
# -------------------------------------[ RULE-BASED URDU Q/A SYSTEM ]---------------------------------------------
# ================================================================================================================

# A Rule Based Question and Answering model for Urdu Documents and questions
# By Nabeel Danish

from stemmer import *
from utility import *
import time

# -----------------------------------------
#       Loading Global Dictionaries
# -----------------------------------------

# Named Entity Recognition
jobs = loadFile('source/jobs.txt')
persons = loadFile('source/persons.txt')
numbers = loadFile('source/numbers.txt')
dates = loadFile('source/dates.txt')
countries = loadFile('source/countries.txt')
cities = loadFile('source/cities.txt')
prepositions = loadFile('source/prepositions.txt')
locations = loadFile('source/locations.txt')
called = loadFile('source/called.txt')
reasons = loadFile('source/reasons.txt')

# Part of Speech
stopwords = loadFile('source/stop_words.txt')
alphabets = loadFile('source/alphabets.txt')
numbers = loadFile('source/numbers.txt')
amount = loadFile('source/amount.txt')

# Question Keywords
whoKeywords = loadFile('source/whoKeywords.txt')
howManyKeywords = loadFile('source/howManyKeywords.txt')
whenKeywords = loadFile('source/whenKeywords.txt')
whereKeywords = loadFile('source/whereKeywords.txt')
whatKeywords = loadFile('source/whatKeywords.txt')
whyKeywords = loadFile('source/whyKeywords.txt')

kis = loadFile('source/kis.txt')
kis_who = loadFile('source/kis_who.txt')
kon_what = loadFile('source/kon_what.txt')

# Score Numbers
clue = 3
good_clue = 4
confident = 6
slam_dunk = 20

# =======================================================================
# ----------------------------[ FUNCTIONS ]------------------------------
# =======================================================================

# wordMatch Function
def wordMatch(score, sentence_keywords, question_keywords):

	for i in range(len(sentence_keywords)):
		if sentence_keywords[i] in question_keywords:
			score = score + clue

	return score

# Get Who Score
def getWhoScore(scores, passage_keywords, question_keywords):

	for i in range(len(passage_keywords)):
		# Get WordMatch
		scores[i] = wordMatch(scores[i], passage_keywords[i], question_keywords[0])

		# Other Rules
		for j in range(len(passage_keywords[i])):
			if passage_keywords[i][j] in persons:
				scores[i] = scores[i] + confident

			if passage_keywords[i][j] in jobs:
				scores[i] = scores[i] + good_clue

	return scores

# Get Numeral Score
def getHowManyScore(scores, passage_keywords, question_keywords, specificWord):

	for i in range(len(passage_keywords)):

		# Get WordMatch
		scores[i] = wordMatch(scores[i], passage_keywords[i], question_keywords[0])

		# Other Rules
		for j in range(len(passage_keywords[i])):

			if (((passage_keywords[i][j] in numbers) | (passage_keywords[i][j].isnumeric())) & (specificWord in passage_keywords[i])):
				scores[i] = scores[i] + good_clue

	return scores

# Get Question Type
def getQuestionType(question_tokens):

	specificWord = ''
	question_type = ''

	for i in range(len(question_tokens)):
		for j in range(len(question_tokens[i])):

			# Checking whether the question is of type WHO
			if (question_tokens[i][j] in whoKeywords):
				if (j != len(question_tokens[i]) - 1):
					if (question_tokens[i][j + 1] in kon_what):
						if (question_tokens[i][j + 2] in locations):
							question_type = 'WHERE'
							break
						if (question_type[i][j + 2] in dates):
							question_type = 'WHEN'
							break
						if (question_type[i][j + 2] in jobs):
							question_type = 'WHO'
							break
						else:
							question_type = 'WHAT'
							break
					else:
						question_type = 'WHO'
					break
			# End if WHO 

			# Checking whether the question is of type HOW_MANY
			if (question_tokens[i][j] in howManyKeywords):
				question_type = 'HOW_MANY'

				if (j != len(question_tokens[i]) - 1):
					specificWord = question_tokens[i][j + 1]
					if specificWord in stopwords:

						if (j != 0):
							specificWord = question_tokens[i][j - 1]
					break

			# End if

			# Checking whether the question is of type WHEN
			if (question_tokens[i][j] in whenKeywords):
				question_type = 'WHEN'
				break

			# Checking whether the question is of type WHERE
			if (question_tokens[i][j] in whereKeywords):
				question_type = 'WHERE'
				break
			# End if

			# Checking whether the question is of type WHAT
			if (question_tokens[i][j] in whatKeywords):
				if (j != 0):
					if (question_tokens[i][j - 1] in amount):
						question_type = 'HOW_MANY'
						break
					if (question_tokens[i][j - 1] in reasons):
						question_type = 'WHY'
						break

				if (j != len(question_tokens[i]) - 1):
					if (question_tokens[i][j + 1] in amount):
						question_type = 'HOW_MANY'
						break
					if (question_tokens[i][j + 1] in reasons):
						question_type = 'WHY'
						break
				else:
					question_type = 'WHAT'
					break

			# Checking whether the question is of type WHY
			if (question_tokens[i][j] in whyKeywords):
				question_type = 'WHY'

			# Handling the "Kis" Cases
			if (question_tokens[i][j] in kis):
				# Who Case
				if ((question_tokens[i][j + 1] in kis_who) | (question_tokens[i][j + 1] in jobs)):
					question_type = 'WHO'
					break
				# When Case
				if (question_tokens[i][j + 1] in dates):
					question_type = 'WHEN'
					break
				# Where Case
				if (question_tokens[i][j + 1] in locations):
					question_type = 'WHERE'
					break

			#End If

		#End For
	#End for

	return question_type, specificWord

# End of function

# Get When Score
def getWhenScore(scores, keywords, question_keywords):
	
	matchDone = [False] * len(keywords)

	for i in range(len(keywords)):
		for j in range(len(keywords[i])):

			if not (matchDone[i]):
				scores[i] = wordMatch(scores[i], keywords[i], question_keywords[0])
				matchDone[i] = True

			if ((matchDone[i]) & (scores[i] > 0)):

				if ((keywords[i][j] in dates) | (checkIfYear(keywords[i][j]))):
					scores[i] = scores[i] + good_clue

			# End if
		# End for
	# End for

	return scores
# End of Function

# Get Where Score
def getWhereScore(scores, keywords, question_keywords):
	
	for i in range(len(keywords)):
		scores[i] = wordMatch(scores[i], keywords[i], question_keywords[0])

		for j in range(len(keywords[i])):
			if (keywords[i][j] in prepositions):
				scores[i] = scores[i] + clue
			if (keywords[i][j] in locations):
				scores[i] = scores[i] + good_clue
			if ((keywords[i][j] in countries) | (keywords[i][j] in cities)):
				scores[i] = scores[i] + confident
			#Endif
		# End of for loop
	# End of for loop

	return scores
# End of Function

# Get What Score
def getWhatScore(scores, keywords, question_keywords):

	# Check for question containing date expression
	containsDate = False
	askedName = False
	checkDate = ''

	for k in range(len(question_keywords[0])):
		if (question_keywords[0][k] in dates):
			containsDate = True
			checkDate = question_keywords[0][k]
		if (question_keywords[0][k] in called):
			askedName = True
	# End for

	for i in range(len(keywords)):

		# Applying Word Match
		scores[i] = wordMatch(scores[i], keywords[i], question_keywords[0])

		# Iterating more Rules
		for j in range(len(keywords[i])):
			if (containsDate):
				if keywords[i][j] == checkDate:
					scores[i] = scores[i] + confident
				if keywords[i][j] in dates:
					scores[i] = scores[i] + clue

			if ((askedName) & (keywords[i][j] in called)):
				scores[i] = scores[i] + slam_dunk

		# End for
	# End of For

	return scores

# Get Why Score
def getWhyScore(scores, keywords, tokens, question_keywords):

	# Applying word match to get BEST
	for i in range(len(keywords)):
		scores[i] = wordMatch(scores[i], keywords[i], question_keywords[0])

	# Getting the Best Sentences
	best = [False] * len(keywords)
	maxScore = max(scores)
	for i in range(len(keywords)):
		if scores[i] == maxScore:
			best[i] = True
		scores[i] = 0

	# Iterating and applying rules
	for i in range(len(keywords)):
		if best[i]:
			scores[i] = scores[i] + confident
		if (i != len(keywords) - 1):
			if (best[i + 1]):
				scores[i] = scores[i] + clue

		if (i != 0):
			if (best[i - 1]):
				scores[i] = scores[i] + good_clue

		# Checking for reasons word
		for j in range(len(tokens[i])):
			if tokens[i][j] in reasons:
				scores[i] = scores[i] + good_clue

	return scores


# Running the Stemmer Function
def runStemmer(keywords):
	for i in range(len(keywords)):
		for j in range(len(keywords[i])):
			keywords[i][j] = removePostfix(keywords[i][j])

	return keywords

# =======================================================================
# ---------------------------[ MAIN FUNCTION ]---------------------------
# =======================================================================

# Main Function
def getAnswer(document, question, debugging = False):

	# -----------------------------------------------------------------------
	# Reading and processing Files
	f = open(document, encoding='utf-8')
	passage = f.read()

	# Getting Sentences
	sentence = getSentences(passage)
	question_sentence = ['']
	question_sentence[0] = question
	question_sentence.append('')

	# Running Tokenizer
	tokens = tokenize(sentence, alphabets)
	question_tokens = tokenize(question_sentence, alphabets)

	# Removing Stopwords and getting keywords only
	keywords = removeStopWords(tokens, stopwords)
	question_keywords = removeStopWords(question_tokens, stopwords)

	# Running Stemmer on Keywords
	keywords = runStemmer(keywords)
	question_keywords = runStemmer(question_keywords)

	# Getting Question Type
	question_type, specificWord = getQuestionType(question_tokens)
	specificWord = removePostfix(specificWord)
	question_keywords.pop()

	# -----------------------------------------------------------------------
	# Getting the Scores According to Question Types
	scores = [0] * len(keywords)

	if question_type == 'WHO':
		scores = getWhoScore(scores, keywords, question_keywords)

	elif question_type == 'HOW_MANY':
		scores = getHowManyScore(scores, keywords, question_keywords, specificWord)

	elif question_type == 'WHEN':
		scores = getWhenScore(scores, keywords, question_keywords)

	elif question_type == 'WHERE':
		scores = getWhereScore(scores, keywords, question_keywords)

	elif question_type == 'WHAT':
		scores = getWhatScore(scores, keywords, question_keywords)

	elif question_type == 'WHY':
		scores = getWhyScore(scores, keywords, tokens, question_keywords)

	else:
		for i in range(len(keywords)):
			scores[i] = wordMatch(scores[i], keywords[i], question_keywords[0])
	# -----------------------------------------------------------------------

	# Getting the all the Maximum Answers
	maxScore = max(scores)
	indices = []
	for i in range(len(scores)):
		if scores[i] == maxScore:
			indices.append(i)

	answers = ['']

	# Outputting the Answers
	for i in range(len(indices)):
		answers[i] = sentence[indices[i]]
		answers[i] = answers[i] + '۔'
		answers.append('')
	answers.pop()
	# Main Function Ends

	# -----------------------------------------------------------------------
	# Debugging Part Ends
	if debugging:
		f = open('debug/scores.txt', 'w')
		for i in range(len(scores)):
			f.write(str(scores[i]))
			f.write("\n")

		f = open('debug/keywords.txt', 'w', encoding = 'utf-8')
		for i in range(len(keywords)):
			for j in range(len(keywords[i])):
				f.write(keywords[i][j])
				f.write("\n")

		f = open('debug/tokens.txt', 'w', encoding='utf-8')
		for i in range(len(tokens)):
			for j in range(len(tokens[i])):
				f.write(tokens[i][j])
				f.write("\n")

		f = open('debug/question_keywords.txt', 'w', encoding='utf-8')
		for i in range(len(question_keywords)):
			for j in range(len(question_keywords[i])):
				f.write(question_keywords[i][j])
				f.write("\n")

		f = open('debug/question_tokens.txt', 'w', encoding='utf-8')
		for i in range(len(question_tokens)):
			for j in range(len(question_tokens[i])):
				f.write(question_tokens[i][j])
				f.write("\n")

		f = open('debug/sentences.txt', 'w', encoding='utf-8')
		for i in range(len(sentence)):
			f.write(sentence[i])
			f.write("\n")

		f = open('debug/debug.txt', 'w', encoding='utf-8') 
		f.write('Specific Word = ' + specificWord)
		f.write('Question Type = ' + question_type)

	return answers

	# End if
	# Debugging Part Ends
	# -----------------------------------------------------------------------
