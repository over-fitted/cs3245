This is the README file for A0217487U's submission
Email: e0543523@u.nus.edu

== Python Version ==

I'm using Python Version 3.10.6 for
this assignment.

== General Notes about this assignment ==

Give an overview of your program, describe the important algorithms/steps 
in your program, and discuss your experiments in general.  A few paragraphs 
are usually sufficient.

# Preprocessing stage
LMs are stored a dictionaries with keys being the ngrams and values being the frequency counters. As lists are not hashable, I converted the ngrams into tuples before storing as key.
For each line, we identify the language by the first 3 letters of the line as these 3-letter signatures would be unique. I then use processString with the appropriate language.  
In processString, I utilised a sliding window-esque buffer where at each index, we remove the oldest character in the buffer and add the new character to the buffer. I then increment the frequency of each ngram as required, and add the ngram to global seen ngrams for the smoothing stage.

For the smoothing stage, we add one instance of each seen ngram to each LM and adjust the total wordcount of each LM accordingly. We then convert the wordcounts to probabilities.
I iterated through the global seen ngrams set and optimised by combining the increment with the probability calculation, reusing the same underlying dictionary.

# Test stage
For each line, I utilised the same sliding window principle and calculated the probability of each ngram belonging to each language by multiplying probabilities of each ngram together.
As the result probabilities are too small that python would auto-convert them to 0, I instead converted each probability to their logarithm and added the logarithms. The least negative sum is the highest probability.

To account for others label, we observe the number of ngrams in the input text that were not seen in the training data as a proportion of the total number of ngrams within the input text.
We can set an arbitrary threshold for how high this proportion should be before rejecting the text and labelling it as others. 
The test data provided works with a threshold as high as 70%, but I set the threshold to 60% to be conservative due to small training data.

== Files included with this submission ==

List the files in your submission here and provide a short 1 line
description of each file.  Make sure your submission's files are named
and formatted correctly.

build_test_LM.py - the script containing all code for this project. Builds the LMs and categorises input test files.
README.txt - this file, containing my writeup.
ESSAY.txt - my answers to the essay questions. 

== Statement of individual work ==

Please put a "x" (without the double quotes) into the bracket of the appropriate statement.

[X] I, A0217487U, certify that I have followed the CS 3245 Information
Retrieval class guidelines for homework assignments.  In particular, I
expressly vow that I have followed the Facebook rule in discussing
with others in doing the assignment and did not take notes (digital or
printed) from the discussions.  

[ ] I, A0000000X, did not follow the class rules regarding homework
assignment, because of the following reason:

<Please fill in>

I suggest that I should be graded as follows:

<Please fill in>


== References ==

<Please list any websites and/or people you consulted with for this
assignment and state their role>
stackoverflow and python docs for file opening instructions.
forum for logarithm trick