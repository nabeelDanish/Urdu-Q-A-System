# Urdu-Q-A-System
A Rule based Urdu Q/A System that inputs a document and a question file and outputs the sentence or line that contains the answer to that question

Run the prototype.py file with parameters (document_file, question_file) placed in the input folder. The output is in the answer.txt in the answer file

Version 0.1: 
  developed first prototype using maximum keyword matching
  stripping stopwords from sentence tokens to retrieve keywords

Version 0.2:
  Added More rules for Who and How Many Question type
  improved the sentence score system
  using a postfix stemmer to retrieve the root of the word
  using Person Dictionary with names and titles to perform NER 
