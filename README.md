# Urdu-Q-A-System
A Rule based Urdu Q/A System that inputs a document and a question file and outputs the sentence or line that contains the answer to that question

Run the prototype.py file with parameters (document_file, question_file) placed in the input folder. The output is in the answer.txt in the output file.
Added a result.xlxs file that tracks the models accuracy on articles from the SQUAD Dataset (Using Google Translate for both document and question). Link to the articles below. for every passage, there are 5 questions. 
Results saved in the form of yes if the answer matched the websites answer and no if not. Accuracy computed
Link to Articles:
  1973_oil_crisis: https://rajpurkar.github.io/SQuAD-explorer/explore/v2.0/dev/1973_oil_crisis.html?model=nlnet%20(single%20model)%20(Microsoft%20Research%20Asia)&version=v2.0

Version 0.1: 

  1. developed first prototype using maximum keyword matching
  2. stripping stopwords from sentence tokens to retrieve keywords

Version 0.2:

  1. Added rules for Who and How Many Question type
  2. improved the sentence score system
  3. using a postfix stemmer to retrieve the root of the word
  4. using Person Dictionary with names and titles to perform NER 
  5. *Important*: use the keywords (kitnay/kitni) near the object you wish to retrieve the quantity for: 
      Example: Dhamakay mai kitnay afrad halak hoay?
      
Version 0.3:
 
 1. Added rules for When and Where question type
 2. using date related words for time expressions
 3. using locations and city names, along with locational pronouns to identify locations in a sentence
 4. tested against some SQUAD dataset articles
 
Version 0.4:
  1. Improved Question type detection with more variations in keywords (kis nai)(kis saal)(kon sa mulk)
  2. Added improved rules for What and Why Question types

