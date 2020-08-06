# Function to remove Postfix
def removePostfix(word):
	# Rules
	if len(word) <= 3:
		return word
	
	elif (word[-1] == 'ں'):
		if (word[-2] == 'و'):
			if (word[-3] == 'ی'):
				word = word[:-3]
				word = word + 'ی'
			else:
				word = word[:-2]

		elif (word[-2] == 'ا') & (word[-3] == 'ی'):
			word = word[:-3]
			word = word + 'ی'
		elif (word[-2] == 'ء') & (word[-3] == 'و'):
			word = word[:-3]
		elif (word[-2] == 'ی'):
			if (word[-3] == 'ء'):
				word = word[:-3]
			else:	
				word = word[:-2]

	elif (word[-1] == 'ے'):
		word = word[:-1]
		word = word + 'ا'

	return word