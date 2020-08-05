# Load Stopwords
def loadFile(file):
	f = open(file, encoding='utf-8')
	stopwords = f.read().splitlines()
	return stopwords

# Match Stopwords
def checkInDict(word, dictionary):
	inDict = False
	for wrd in dictionary:
		if word == wrd:
			inDict = True
			break
	return inDict

# Get Sentences Functions
def getSentences(passage, delimiter = '۔'):
	sentence = ['']
	numSentences = 0
	for char in passage:
		if char == delimiter:
			numSentences = numSentences + 1
			sentence.append('')
		else:
			sentence[numSentences] = sentence[numSentences] + char
	return sentence

# Get Keywords
def removeStopWords(tokens, stopwords):
	keywords = [['']]
	u = 0
	v = 0
	for i in range(len(tokens)):

		for j in range(len(tokens[i])):

			if not(checkInDict(tokens[i][j], stopwords)):
				keywords[u][v] = tokens[i][j]
				keywords[u].append('')
				v = v + 1
		u = u + 1
		v = 0
		keywords.append([''])
	keywords.pop()
	return keywords

# Get Tokens
def tokenize(sentences, alphabets):
	tokens = [['']]
	for i in range(len(sentences)):
		numWords = 0
		for char in sentences[i]:
			if not (char == ' ' or char == '،'):
				tokens[i][numWords] = tokens[i][numWords] + char
			else:
				numWords = numWords + 1	
				tokens[i].append('')
		tokens.append([''])

	tokens.pop()
	return tokens

# Get Sentence Scores
def getSentenceScores(scores, active, passage_keywords, question_keywords):

	for i in range(len(passage_keywords)):
		for j in range(len(question_keywords)):
			found = False
			for k in range(len(passage_keywords[i])):
				if question_keywords[0][j] == passage_keywords[i][k]:
					found = True
					active[i] = True
					break
			if found:
				scores[i] = scores[i] + 1
	return scores, active

# Get Numeral Score
def getNumeralScore(scores, active, passage_keywords, numbers):

	new_active = [False] * len(passage_keywords)
	for i in range(len(passage_keywords)):
		for j in range(len(passage_keywords[i])):
			for k in range(len(numbers)):

				if passage_keywords[i][j] == numbers[k] and active[i]:
					scores[i] = scores[i] + 1
					new_active[i] = True

	return scores, new_active

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

	# Reading and Processing the Question File
	f = open(question_file, encoding = 'utf-8')
	question = f.read()
	question_sentence = getSentences(question, '؟')
	question_tokens = tokenize(question_sentence, alphabets)
	question_keywords = removeStopWords(question_tokens, stopwords)

	# Getting the Scores
	scores = [0] * len(sentence)
	active = [False] * len(sentence)

	scores, active = getSentenceScores(scores, active, keywords, question_keywords)
	# scores, active = getNumeralScore(scores, active, keywords, numbers)

	maxScore = max(scores)
	index = 0
	for i in range(len(scores)):
		if scores[i] == maxScore:
			index = i
			break

	# Retrieving the Answer
	answer = sentence[index]
	f = open('output/answer.txt', 'w', encoding = 'utf-8')
	f.write(answer)

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
	# Debugging Part Starts