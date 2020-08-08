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
						question_type = 'WHAT'
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

				if (j != len(question_tokens[i]) - 1):
					if (question_tokens[i][j + 1] in amount):
						question_type = 'HOW_MANY'
						break

				if (j != 0):
					if (question_tokens[i][j - 1] in reasons):
						question_type = 'WHY'
						break

				if (j != len(question_tokens[i]) - 1):
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
				if (question_tokens[i][j + 1] in kis_who):
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
	
	for i in range(len(keywords)):
		for j in range(len(keywords[i])):
			if ((keywords[i][j] in dates) | ((len(keywords[i][j]) == 4) & (keywords[i][j].isnumeric()))):
				scores[i] = scores[i] + good_clue
				scores[i] = wordMatch(scores[i], keywords[i], question_keywords[0])
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
def getAnswer(document, question_file, answer_file, debugging = False):

	# -----------------------------------------------------------------------
	# Reading and processing Files
	f = open(document, encoding='utf-8')
	passage = f.read()
	f = open(question_file, encoding = 'utf-8')
	question = f.read()

	# Getting Sentences
	sentence = getSentences(passage)
	question_sentence = getSentences(question, ['؟'])

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
	scores = [0] * len(sentence)

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

	f = open(answer_file, 'w', encoding = 'utf-8')

	# Outputting the Answers
	for i in range(len(indices)):
		answer = sentence[indices[i]]
		answer = answer + '۔'
		f.write(answer)
		f.write("\n\n")

	# Main Function Ends

	# -----------------------------------------------------------------------
	# Debugging Part Ends
	if debugging:
		print(scores)
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

		f = open('debug/specificWord.txt', 'w', encoding='utf-8') 
		f.write(specificWord)
	# End if

	# Debugging Part Ends
	# -----------------------------------------------------------------------

# End of Function
# getAnswer(
# 	"input/Harvard_University/passages/0004.txt", 
# 	"input/Harvard_University/questions/question_4_5.txt", 
# 	'output/answer_5.txt', debugging = True)