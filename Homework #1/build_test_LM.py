#!/usr/bin/python3

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import re
import nltk
import sys
import getopt
import math

seenWords = set()

malayFreq = {}
malaySum = 0

indoFreq = {}
indoSum = 0

tamilFreq = {}
tamilSum = 0

def build_LM(in_file):
    global indoSum
    global malaySum
    global tamilSum
    """
    build language models for each label
    each line in in_file contains a label and a string separated by a space
    """
    print("building language models...")
    # This is an empty method
    # Pls implement your code below
    inputStrings = []
    with open(in_file) as f:
        inputStrings = f.readlines()
    for inputString in inputStrings:
        # Detect language by first 3 characters, then process string with corresponding LM
        language = inputString[0:3]
        if language == "ind":
            indoSum = processString(inputString[11:], indoFreq, indoSum)
            continue
        if language == "mal":
            malaySum = processString(inputString[10:], malayFreq, malaySum)
            continue
        if language == "tam":
            tamilSum = processString(inputString[6:], tamilFreq, tamilSum)
            continue
        print("language not found",language)
    
    # Smoothen LMs by adding one of each seen ngram
    malaySum += len(seenWords)
    indoSum += len(seenWords)
    tamilSum += len(seenWords)

    for word in seenWords:
        smoothen(word, malayFreq, malaySum)
        smoothen(word, indoFreq, indoSum)
        smoothen(word, tamilFreq, tamilSum)

    # can use for ensuring model is valid
    # check(malayFreq)
    # check(indoFreq)
    # check(tamilFreq)

# Sum of all probabilities should be ~1
def check(freq):
    sum = 0.0
    for key in freq.keys():
        sum += freq[key]

    print(sum)
            
# given a language LM and the input string, add the input string ngrams to the LM
# def processString(inputString: str, langDict: Dict[str, int], langSum: int) -> int:
def processString(inputString, langDict, langSum):
    # intialise sliding window buffer
    ngram = []
    ngram[:0] = inputString[0:3]

    for char in inputString[3:]:
        ngram.append(char)
        seenWords.add(tuple(ngram))
        if tuple(ngram) not in langDict.keys():
            langDict[tuple(ngram)] = 0
        langDict[tuple(ngram)] += 1
        langSum += 1
        ngram.pop(0)
    
    return langSum
    
# Add one to each ngram count, then divide by the total count of ngrams in the LM
# def smoothen(word: string, langDict: Dict[str, int], langSum: int) -> None:
def smoothen(word, langDict, langSum):
    if word not in langDict.keys():
        langDict[word] = 1.0 / langSum
    else:
        langDict[word] = float(langDict[word] + 1) / langSum    

    # Error
    if(langDict[word] == 0):
        print("0 found")


def test_LM(in_file, out_file, LM):
    """
    test the language models on new strings
    each line of in_file contains a string
    you should print the most probable label for each string into out_file
    """
    print("testing language models...")

    inputStrings = []
    with open(in_file) as f:
        inputStrings = f.readlines()
    for i in range(len(inputStrings)):
        inputString = inputStrings[i]

        # We use logarithms for the probabilities to avoid small decimals being falsely rounded to 0
        # The more negative, the smaller the probability
        malayProb = 0.0
        indoProb = 0.0
        tamilProb = 0.0

        # Keep track of ngrams not in training data as a proportion of total ngrams in the input string
        unseen = 0.0
        total = 0.0

        ngram = []
        ngram[:0] = inputString[0:3]
        for char in inputString[3:]:
            ngram.append(char)
            total += 1
            if tuple(ngram) not in seenWords:
                unseen+=1
                ngram.pop(0)
                continue

            # multiply probability for each language
            malayProb += math.log(malayFreq[tuple(ngram)])
            indoProb += math.log(indoFreq[tuple(ngram)])
            tamilProb += math.log(tamilFreq[tuple(ngram)])

            ngram.pop(0)

        
        # ngrams not in training data too high, majority of ngrams absent, label as other language
        if unseen / total > 0.6:
            inputString = "other " + inputString
            inputStrings[i] = inputString
            continue

        # decide which is the closest language and add the language name to front of string
        best = max(indoProb, malayProb, tamilProb)

        # debugging info
        # print(i, "unseen", unseen / total,"best", best)

        if best == malayProb:
            inputString = "malaysian " + inputString
            inputStrings[i] = inputString
            continue
        if best == indoProb:
            inputString = "indonesian " + inputString
            inputStrings[i] = inputString
            continue
        
        if best == tamilProb:
            inputString = "tamil " + inputString
            inputStrings[i] = inputString
            continue
        print("best is not a probability")
        

    # print results
    with open(out_file, "w") as f:
        f.writelines(inputStrings)
    



def usage():
    print(
        "usage: "
        + sys.argv[0]
        + " -b input-file-for-building-LM -t input-file-for-testing-LM -o output-file"
    )


input_file_b = input_file_t = output_file = None
try:
    opts, args = getopt.getopt(sys.argv[1:], "b:t:o:")
except getopt.GetoptError:
    usage()
    sys.exit(2)
for o, a in opts:
    if o == "-b":
        input_file_b = a
    elif o == "-t":
        input_file_t = a
    elif o == "-o":
        output_file = a
    else:
        assert False, "unhandled option"
if input_file_b == None or input_file_t == None or output_file == None:
    usage()
    sys.exit(2)

LM = build_LM(input_file_b)
test_LM(input_file_t, output_file, LM)
