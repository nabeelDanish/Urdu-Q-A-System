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
def getSentences(passage, delimiter = ['۔', '،']):
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