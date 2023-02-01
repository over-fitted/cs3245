#!/usr/bin/python3

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import re
import nltk
import sys
import getopt

seenWords = set()

malayFreq = {}
malaySum = 0

indoFreq = {}
indoSum = 0

tamilFreq = {}
tamilSum = 0

def build_LM(in_file):
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
    
    malaySum += len(seenWords)
    indoSum += len(seenWords)
    tamilSum += len(seenWords)

    for word in seenWords:
        smoothen(word, malayFreq, malaySum)
        smoothen(word, indoFreq, indoSum)
        smoothen(word, tamilFreq, tamilSum)
            

# def processString(inputString: str, langDict: Dict[str, int], langSum: int) -> int:
def processString(inputString, langDict, langSum):
    ngram = inputString[0:3]

    for char in inputString[4:]:
        ngram.append(char)
        if ngram not in langDict.keys():
            langDict[ngram] = 0
            seenWords.add(ngram)
        langDict[ngram] += 1
        langSum += 1
        ngram.pop(0)
    
    return langSum
    
# def smoothen(word: string, langDict: Dict[str, int], langSum: int) -> None:
def smoothen(word, langDict, langSum):
    if word not in langDict.keys():
        langDict[word] = 1.0 / langSum
        return

    langDict[word] = float(langDict[word] + 1) / langSum    


def test_LM(in_file, out_file, LM):
    """
    test the language models on new strings
    each line of in_file contains a string
    you should print the most probable label for each string into out_file
    """
    print("testing language models...")
    # This is an empty method
    # Pls implement your code below

    inputStrings = []
    with open(in_file) as f:
        inputStrings = f.readlines()
    for inputString in inputStrings:
        indoProb = 1.0
        malayProb = 1.0
        tamilProb = 1.0

        ngram = inputString[0:3]
        for char in inputString[4:]:
            ngram.append(char)

            # multiply probability for each language

            ngram.pop(0)

        # decide which is the best language and add the language name to front of string

    # print results
    with open(out_file) as f:
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
# test_LM(input_file_t, output_file, LM)
