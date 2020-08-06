from stemmer import *
from utility import *

# wordMatch Function
def wordMatch(score, sentence_keywords, question_keywords):

	for i in range(len(sentence_keywords)):
		if sentence_keywords[i] in question_keywords:
			score = score + 3

	return score

# Get Who Score
def getWhoScore(scores, passage_keywords, question_keywords):
	jobs = loadFile('source/jobs.txt')
	persons = loadFile('source/persons.txt')

	for i in range(len(passage_keywords)):
		# Get WordMatch
		scores[i] = wordMatch(scores[i], passage_keywords[i], question_keywords[0])

		# Other Rules
		for j in range(len(passage_keywords[i])):
			if passage_keywords[i][j] in persons:
				scores[i] = scores[i] + 6

			if passage_keywords[i][j] in jobs:
				scores[i] = scores[i] + 4

	return scores

# Get Numeral Score
def getHowManyScore(scores, passage_keywords, question_keywords, specificWord):
	numbers = loadFile('source/numbers.txt')

	for i in range(len(passage_keywords)):

		# Get WordMatch
		scores[i] = wordMatch(scores[i], passage_keywords[i], question_keywords[0])

		# Other Rules
		for j in range(len(passage_keywords[i])):

			if (((passage_keywords[i][j] in numbers) | (passage_keywords[i][j].isnumeric())) & (specificWord in passage_keywords[i])):
				scores[i] = scores[i] + 3

	return scores

# Get Question Type
def getQuestionType(question_tokens, stopwords):
	whoKeywords = loadFile('source/whoKeywords.txt')
	howManyKeywords = loadFile('source/howManyKeywords.txt')
	whenKeywords = loadFile('source/whenKeywords.txt')

	specificWord = ''
	question_type = ''

	for i in range(len(question_tokens)):
		for j in range(len(question_tokens[i])):

			# Checking whether the question is of type WHO
			if (question_tokens[i][j] in whoKeywords):
				question_type = 'WHO'
				break

			# Checking whether the question is of type HOW_MANY
			if (question_tokens[i][j] in howManyKeywords):
				question_type = 'HOW_MANY'
				specificWord = question_tokens[i][j + 1]
				if specificWord in stopwords:
					specificWord = question_tokens[i][j - 1]

				break

			# Checking whether the question is of type WHEN
			if (question_tokens[i][j] in whenKeywords):
				question_type = 'WHEN'
				break

	return question_type, specificWord

# Get When Score
def getWhenScore(scores, keywords, question_keywords):
	dates = loadFile('source/dates.txt')

	for i in range(len(keywords)):
		for j in range(len(keywords[i])):
			if keywords[i][j] in dates:
				scores[i] = scores[i] + 4
				scores[i] = wordMatch(scores[i], keywords[i], question_keywords[0])

	return scores


# Running the Stemmer Function
def runStemmer(keywords):
	for i in range(len(keywords)):
		for j in range(len(keywords[i])):
			keywords[i][j] = removePostfix(keywords[i][j])

	return keywords

# Main Function
def getAnswer(document, question_file):

	stopwords = loadFile('source/stop_words.txt')
	alphabets = loadFile('source/alphabets.txt')
	numbers = loadFile('source/numbers.txt')

	# Reading and processing the Passage File
	f = open(document, encoding='utf-8')
	passage = f.read()
	sentence = getSentences(passage)
	tokens = tokenize(sentence, alphabets)
	keywords = removeStopWords(tokens, stopwords)
	keywords = runStemmer(keywords)

	# Reading and Processing the Question File
	f = open(question_file, encoding = 'utf-8')
	question = f.read()
	question_sentence = getSentences(question, ['؟'])
	question_tokens = tokenize(question_sentence, alphabets)
	question_type, specificWord = getQuestionType(question_tokens, stopwords)
	question_keywords = removeStopWords(question_tokens, stopwords)
	question_keywords = runStemmer(question_keywords)
	question_keywords.pop()

	# Getting the Scores According to Question Types
	scores = [0] * len(sentence)

	if question_type == 'WHO':
		scores = getWhoScore(scores, keywords, question_keywords)

	if question_type == 'HOW_MANY':
		scores = getHowManyScore(scores, keywords, question_keywords, specificWord)

	if question_type == 'WHEN':
		scores = getWhenScore(scores, keywords, question_keywords)

	# Getting the all the Maximum Answers
	maxScore = max(scores)
	indices = []
	for i in range(len(scores)):
		if scores[i] == maxScore:
			indices.append(i)

	f = open('output/answer.txt', 'w', encoding = 'utf-8')

	# Retrieving the Answer
	for i in range(len(indices)):
		answer = sentence[indices[i]]
		f.write(answer)
		f.write("\n\n")

	# Main Function Ends

	# Debugging Part Ends
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

	# Debugging Part Ends

# Debugging Part Starts
getAnswer("input/0002.txt", "input/question.txt")
# Debugging Part Ends