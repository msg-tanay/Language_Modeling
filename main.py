"""
15-110 Hw6 - Language Modeling Project
Name: M.S.G.Tanay
AndrewID:
"""

import main_tests as test

project = "Language" # don't edit this

### WEEK 1 ###

'''
loadBook(filename)
#1 [Check6-1]
Parameters: str
Returns: 2D list of strs
'''
def loadBook(filename):   # defining a function to read a file
    fileObj=open(filename,'r')
    Corpus=fileObj.read()
    Corpus=str(Corpus)    # cleaning the text as per our requirements
    Corpus=Corpus.split("\n")
    corpus=[]
    for each in Corpus:
        each=each.split(" ")
        if each!=[""]:
            corpus.append(each)
    del Corpus
    return corpus         # a corpus is created


'''
getCorpusLength(corpus)
#2 [Check6-1]
Parameters: 2D list of strs
Returns: int
'''
def getCorpusLength(corpus): # defining a function to get the total number of words in the given corpus
    totalCount=0
    for each in corpus:
        totalCount=totalCount+len(each)
    return totalCount


'''
buildVocabulary(corpus)
#3 [Check6-1]
Parameters: 2D list of strs
Returns: list of strs
'''
def buildVocabulary(corpus): # a function to get all the unique words in the corpus which are called unigrams
    unigrams=[]
    for subList in corpus:
        for each in subList:
            if each not in unigrams:
                unigrams.append(each)
    return unigrams


'''
countUnigrams(corpus)
#4 [Check6-1]
Parameters: 2D list of strs
Returns: dict mapping strs to ints
'''
def countUnigrams(corpus):   # a function to get unigrams in the corpus and the number of times they have occured in the text
    unigramCounts={}
    for subList in corpus:
        for each in subList:
            if each not in unigramCounts:
                unigramCounts[each]=1
            else:unigramCounts[each]+=1
    return unigramCounts


'''
getStartWords(corpus)
#5 [Check6-1]
Parameters: 2D list of strs
Returns: list of strs
'''
def getStartWords(corpus): # a function to get the words which are used to start a sentence in the given corpus
    uniqueStartWords=[]
    for each in corpus:
        if each[0] not in uniqueStartWords:
            uniqueStartWords.append(each[0])
    return uniqueStartWords


'''
countStartWords(corpus)
#5 [Check6-1]
Parameters: 2D list of strs
Returns: dict mapping strs to ints
'''
def countStartWords(corpus):  # a function to get the frequency of the starting words in the corpus
    startWordfreq={}
    for each in corpus:
        if each[0] not in startWordfreq:
            startWordfreq[each[0]]=1
        else:startWordfreq[each[0]]+=1
    return startWordfreq


'''
countBigrams(corpus)
#6 [Check6-1]
Parameters: 2D list of strs
Returns: dict mapping strs to (dicts mapping strs to ints)
'''
def countBigrams(corpus):  # a function to get the bigrams
    bigramfreq={}
    for sentence in corpus:
        for ind in range(len(sentence)-1):
            if sentence[ind] not in bigramfreq: # checking if a word doesn't exist in bigram frequency variable
                bigramfreq[sentence[ind]]={}    # if it doesn't exist, creating a dictionary to pair the next words and their frequencies
            if sentence[ind+1] in bigramfreq[sentence[ind]]:
                bigramfreq[sentence[ind]][sentence[ind+1]]+=1
            else:bigramfreq[sentence[ind]][sentence[ind+1]]=1
    return bigramfreq


### WEEK 2 ###

'''
buildUniformProbs(unigrams)
#1 [Check6-2]
Parameters: list of strs
Returns: list of floats
'''
def buildUniformProbs(unigrams): # a function to get the uniform probabilities i.e. all words have the same probability irrespective of any factors
    uniProb=[]
    for i in range(len(unigrams)):
        uniProb.append(1/len(unigrams))
    return uniProb
    


'''
buildUnigramProbs(unigrams, unigramCounts, totalCount)
#2 [Check6-2]
Parameters: list of strs ; dict mapping strs to ints ; int
Returns: list of floats
'''
def buildUnigramProbs(unigrams, unigramCounts, totalCount): # a function to get the probability of a unigram occuring in the corpus
    uniProbList=[]
    for i in range(len(unigrams)):
        uniProbList.append(unigramCounts[unigrams[i]]/totalCount)
    return uniProbList


'''
buildBigramProbs(unigramCounts, bigramCounts)
#3 [Check6-2]
Parameters: dict mapping strs to ints ; dict mapping strs to (dicts mapping strs to ints)
Returns: dict mapping strs to (dicts mapping strs to (lists of values))
'''
def buildBigramProbs(unigramCounts, bigramCounts): # a function to get the pairs of bigrams and the probabilities with which they occur
    d={}
    for prevWord in bigramCounts:
        wordList=[]
        probList=[]
        for each in bigramCounts[prevWord]:
            probList.append(bigramCounts[prevWord][each]/unigramCounts[prevWord])
            wordList.append(each)
        d[prevWord]={}
        d[prevWord]["words"]=wordList
        d[prevWord]["probs"]=probList
    return d


'''
getTopWords(count, words, probs, ignoreList)
#4 [Check6-2]
Parameters: int ; list of strs ; list of floats ; list of strs
Returns: dict mapping strs to floats
'''
def getTopWords(count, words, probs, ignoreList): # a function to get the required number of words with descending order of probabilities
    d={}
    c=0
    while c<count:
        m=max(probs)
        i=probs.index(m)
        if words[i] not in ignoreList and words[i] not in d:
            d[words[i]]=probs[i]
            c+=1
        probs.remove(probs[i])
        words.remove(words[i])
    return d

'''
generateTextFromUnigrams(count, words, probs)
#5 [Check6-2]
Parameters: int ; list of strs ; list of floats
Returns: str
'''
from random import choices
def generateTextFromUnigrams(count, words, probs): # a function to generate text from unigrams and their probabilities
    txt=""
    for i in range(count):
        txt=txt+str(choices(words,weights=probs))[2:-2]  # removing the square brackets and quotes and adding to the text
        if i!=count-1: # not adding space after the last word
            txt=txt+" "
    return txt


'''
generateTextFromBigrams(count, startWords, startWordProbs, bigramProbs)
#6 [Check6-2]
Parameters: int ; list of strs ; list of floats ; dict mapping strs to (dicts mapping strs to (lists of values))
Returns: str
'''
def generateTextFromBigrams(count, startWords, startWordProbs, bigramProbs):
    txt=""        # a function to generate text based on bigrams and their probabilities
    flag=False    # makes much more sense than text generated from unigrams but still gibberish
    for i in range(count):
        if i==0 or flag==True: # using flag to check whether a dot is selected
            prev=str(choices(startWords,weights=startWordProbs))[2:-2]
            txt=txt+prev
            if flag==True:flag=False
        else:
            prev=str(choices(bigramProbs[prev]["words"],weights=bigramProbs[prev]["probs"]))[2:-2]
            txt=txt+prev
        if prev==".":flag=True
        if i!=count-1:       # not adding space after the last word
            txt=txt+" "
    return txt


### WEEK 3 ###

ignore = [ ",", ".", "?", "'", '"', "-", "!", ":", ";", "by", "around", "over",
           "a", "on", "be", "in", "the", "is", "on", "and", "to", "of", "it",
           "as", "an", "but", "at", "if", "so", "was", "were", "for", "this",
           "that", "onto", "from", "not", "into" ]

'''
graphTop50Words(corpus)
#3 [Hw6]
Parameters: 2D list of strs
Returns: None
'''
def graphTop50Words(corpus): # function to generate bar graph with top 50 words based on their probabilities
    d={}
    totalCount=getCorpusLength(corpus)
    unig=buildVocabulary(corpus)
    unigc=countUnigrams(corpus)
    unigProb=buildUnigramProbs(unig,unigc,totalCount)
    d=getTopWords(50,unig,unigProb,ignore)
    barPlot(d,"Top 50 words")
    return


'''
graphTopStartWords(corpus)
#4 [Hw6]
Parameters: 2D list of strs
Returns: None
'''
def graphTopStartWords(corpus):   # function to generate bar graph with top 50 starting words based on their probabilities
    uniqStart=getStartWords(corpus)
    uniqStartc=countStartWords(corpus)
    totalC=sum(list(uniqStartc.values()))
    uniqStartProbs=[]
    for each in uniqStartc:
        uniqStartProbs.append(uniqStartc[each]/totalC)
    d=getTopWords(50,uniqStart,uniqStartProbs,ignore)
    barPlot(d,"Top 50 starting words")
    return


'''
graphTopNextWords(corpus, word)
#5 [Hw6]
Parameters: 2D list of strs ; str
Returns: None
'''
def graphTopNextWords(corpus, word):  # function to generate top 10 words which occur second in bigram pairs
    unigc=countUnigrams(corpus)
    bigc=countBigrams(corpus)
    bigProb=buildBigramProbs(unigc,bigc)
    d=getTopWords(10,bigProb[word]["words"],bigProb[word]["probs"],ignore)
    barPlot(d,"Top next words")
    return


'''
setupChartData(corpus1, corpus2, topWordCount)
#6 [Hw6]
Parameters: 2D list of strs ; 2D list of strs ; int
Returns: dict mapping strs to (lists of values)
'''
def setupChartData(corpus1, corpus2, topWordCount): # preliminary function to prepare data for 2D graphs
    d1={}
    d2={}
    tc1=getCorpusLength(corpus1)
    tc2=getCorpusLength(corpus2)
    unig1=buildVocabulary(corpus1)
    unig2=buildVocabulary(corpus2)
    unigc1=countUnigrams(corpus1)
    unigc2=countUnigrams(corpus2)
    unigProb1=buildUnigramProbs(unig1,unigc1,tc1)
    unigProb2=buildUnigramProbs(unig2,unigc2,tc2)
    d1=getTopWords(topWordCount,unig1,unigProb1,ignore)
    d2=getTopWords(topWordCount,unig2,unigProb2,ignore)
    for each in d2:       # setting up the dictionary as per the given requirements
        if each not in d1:
            d1[each]=0
    d3={}
    for each in d1:
        if each not in d2:
            d3[each]=0
        else:d3[each]=d2[each]
    totalUnig=list(d1.keys())
    c1p=list(d1.values())
    c2p=list(d3.values())
    finalDict={"topWords":totalUnig,"corpus1Probs":c1p,"corpus2Probs":c2p}
    return finalDict


'''
graphTopWordsSideBySide(corpus1, name1, corpus2, name2, numWords, title)
#6 [Hw6]
Parameters: 2D list of strs ; str ; 2D list of strs ; str ; int ; str
Returns: None
'''
def graphTopWordsSideBySide(corpus1, name1, corpus2, name2, numWords, title):  # function to draw the bar graph such that for each word probabilities of their occurence in both books are compared side by side
    d=setupChartData(corpus1,corpus2,numWords)
    sideBySideBarPlots(d["topWords"],d["corpus1Probs"],d["corpus2Probs"],name1,name2,title)
    return


'''
graphTopWordsInScatterplot(corpus1, corpus2, numWords, title)
#6 [Hw6]
Parameters: 2D list of strs ; 2D list of strs ; int ; str
Returns: None
'''
def graphTopWordsInScatterplot(corpus1, corpus2, numWords, title): # function to draw the scatter plot comparing the occurence of words in both books
    d=setupChartData(corpus1,corpus2,numWords)
    scatterPlot(d["corpus1Probs"],d["corpus2Probs"],d["topWords"],title)
    return


### WEEK 3 PROVIDED CODE ###

"""
Expects a dictionary of words as keys with probabilities as values, and a title
Plots the words on the x axis, probabilities as the y axis and puts a title on top.
"""
def barPlot(dict, title):
    import matplotlib.pyplot as plt

    names = []
    values = []
    for k in dict:
        names.append(k)
        values.append(dict[k])

    plt.bar(names, values)

    plt.xticks(rotation='vertical')
    plt.title(title)

    plt.show()

"""
Expects 3 lists - one of x values, and two of values such that the index of a name
corresponds to a value at the same index in both lists. Category1 and Category2
are the labels for the different colors in the graph. For example, you may use
it to graph two categories of probabilities side by side to look at the differences.
"""
def sideBySideBarPlots(xValues, values1, values2, category1, category2, title):
    import matplotlib.pyplot as plt

    w = 0.35  # the width of the bars

    plt.bar(xValues, values1, width=-w, align='edge', label=category1)
    plt.bar(xValues, values2, width= w, align='edge', label=category2)

    plt.xticks(rotation="vertical")
    plt.legend()
    plt.title(title)

    plt.show()

"""
Expects two lists of probabilities and a list of labels (words) all the same length
and plots the probabilities of x and y, labels each point, and puts a title on top.
Note that this limits the graph to go from 0x0 to 0.02 x 0.02.
"""
def scatterPlot(xs, ys, labels, title):
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots()

    plt.scatter(xs, ys)

    # make labels for the points
    for i in range(len(labels)):
        plt.annotate(labels[i], # this is the text
                    (xs[i], ys[i]), # this is the point to label
                    textcoords="offset points", # how to position the text
                    xytext=(0, 10), # distance from text to points (x,y)
                    ha='center') # horizontal alignment can be left, right or center

    plt.title(title)
    plt.xlim(0, 0.02)
    plt.ylim(0, 0.02)

    # a bit of advanced code to draw a y=x line
    ax.plot([0, 1], [0, 1], color='black', transform=ax.transAxes)

    plt.show()


### RUN CODE ###

# This code runs the test cases to check your work
if __name__ == "__main__":
    print("\n" + "#"*15 + " WEEK 1 TESTS " +  "#" * 16 + "\n")
    test.week1Tests()
    print("\n" + "#"*15 + " WEEK 1 OUTPUT " + "#" * 15 + "\n")
    test.runWeek1()
    ## Uncomment these for Week 2 ##

    print("\n" + "#"*15 + " WEEK 2 TESTS " +  "#" * 16 + "\n")
    test.week2Tests()
    print("\n" + "#"*15 + " WEEK 2 OUTPUT " + "#" * 15 + "\n")
    test.runWeek2()


    ## Uncomment these for Week 3 ##

    print("\n" + "#"*15 + " WEEK 3 OUTPUT " + "#" * 15 + "\n")
    test.runWeek3()