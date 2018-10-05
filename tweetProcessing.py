import csv
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from functools import reduce
import nltk
import matplotlib.pylab as plb
import string


# Opens and processes up to 100000 tweets where the csv has tweets in the 3rd row.
# My dataset has row 1 as indeces, row 2 as positive or negative sentiment and the 3rd as the tweet
with open('train.csv', 'r') as csvFile:
    myReader = csv.reader(csvFile, delimiter=',')
    #allRows = list(myReader)
    sr = stopwords.words('english')
    print(type(sr))
    clean_tokens = [] 
    iterationCount = 0
    
    # Reads every value up to the size of 100000 and counts the occurences of all words (A.k.a. no punctuation, no I, you, he, etc...)
    for row in myReader:
        if iterationCount >= 100000:
            break
        tokens = word_tokenize(row[2].lower())
        for token in tokens:
            if token not in sr and token not in string.punctuation:
                clean_tokens.append(token)
        iterationCount += 1
    freq = nltk.FreqDist(clean_tokens)
    
    # Gets iterations with 20, 40, 60, 80 most common words and plot each separately
    for i in range(1, 5):
        plb.subplot(5,1,i)
        itemPairs = freq.most_common(i * 20)
        xItems = []
        yItems = []
        for item in itemPairs:
            xItems.append(item[0])
            yItems.append(item[1])
        #Useful to visualize what the data looks like
        #print(str(xItems))
        #print(str(yItems))
        plb.plot(xItems, yItems)
    plb.show()