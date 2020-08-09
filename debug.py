from prototype import *
# Debugging Part Starts
for i in range(1, 6):
	getAnswer(
		"input/French_and_Indian_War/passages/0003.txt", 
		"input/French_and_Indian_War/questions/question_3_" + str(i) + ".txt", 
		'output/answer_' + str(i) + '.txt', debugging = True)
# Debugging Part Ends