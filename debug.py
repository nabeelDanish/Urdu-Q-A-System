from prototype import *
# Debugging Part Starts
for i in range(1, 7):
	getAnswer(
		"input/Oxygen/passages/0002.txt", 
		"input/Oxygen/questions/question_2_" + str(i) + ".txt", 
		'output/answer_' + str(i) + '.txt', debugging = True)
# Debugging Part Ends