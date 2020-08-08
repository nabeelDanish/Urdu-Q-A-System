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
def getSentences(passage, delimiter = ['۔']):
	sentence = ['']
	numSentences = 0
	for char in passage:
		if char in delimiter:
			numSentences = numSentences + 1
			sentence.append('')
		else:
			sentence[numSentences] = sentence[numSentences] + char
	return sentence

# Get Keywords
def removeStopWords(tokens, stopwords):
	keywords = [['']]
	u = 0
	first = True
	for i in range(len(tokens)):

		for j in range(len(tokens[i])):

			if not(checkInDict(tokens[i][j], stopwords)):
				if first:
					keywords[u][0] = tokens[i][j]
					first = False
				else:
					keywords[u].append(tokens[i][j])

		if not(first):
			# End of for j
			u = u + 1
			keywords.append([''])
			first = True
	# End of For Loop

	keywords.pop()
	clearExtraChar(keywords)
	for i in range(len(keywords)):
		keywords[i] = removeDuplicates(keywords[i])
		
	return keywords

# Get Tokens
def tokenize(sentences, alphabets):
	tokens = [['']]
	delimiters = [' ', '،', '-', '–']
	for i in range(len(sentences)):
		numWords = 0
		for char in sentences[i]:
			if not (char in delimiters):
				tokens[i][numWords] = tokens[i][numWords] + char
			else:
				numWords = numWords + 1	
				tokens[i].append('')
		tokens.append([''])
	tokens.pop()
	return tokens

# Clear Function
def clearExtraChar(keywords):

	removeList = ['']
	for i in range(len(keywords)):
		keywords[i] = [j for j in keywords[i] if j not in removeList]

	return keywords

# Removing Duplicated from the list
def removeDuplicates(x):
	return list(dict.fromkeys(x))