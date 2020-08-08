from prototype import *
# Debugging Part Starts
for i in range(1, 6):
	getAnswer(
		"input/1973_oil_crisis/passages/0010.txt", 
		"input/1973_oil_crisis/questions/question_10_" + str(i) + ".txt", 
		'output/answer_' + str(i) + '.txt', debugging = True)
# Debugging Part Ends