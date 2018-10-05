import collections
from collections import Counter
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import math
import string
import operator
import pandas as pd
import pickle
# Read Csv file
"""
my_file = pd.read_csv('table.csv', delimiter='\t')

# Initialize counter and words to ignore
counter = Counter('')
counterF = Counter('')
sr = stopwords.words('english')
punctuation = string.punctuation

# For every entry in the csv file, count important words
for entry in my_file.get_values():
    is_male= True if entry[1] == 'M' else False
    current_entry = str(entry[0])
    current_entry = current_entry.lower()
    for token in word_tokenize(current_entry):
        if token in sr or token in punctuation:
            continue 
        elif is_male:
            counter[token] += 1
        else:
            counterF[token] += 1

# Count difference between the Male results and Female results
counter.subtract(counterF)

# Create a new 'weight' object which is a logarithmic mapping of the original values
# This is an object where positive values imply that a gender is more likely male
log_distributed_results = {}
for key in counter.keys():
    value = float(counter[key])
    if value >= 0:
        log_distributed_results[key] = math.log1p(value)
    else:
        log_distributed_results[key] = -math.log1p(-value)

# Save the distribution as a pickled object
with open('genderClassifier.pyobj', 'wb') as output:
    pickle.dump(log_distributed_results, output, pickle.HIGHEST_PROTOCOL)    
"""
# Function to load the pickled object
def getGenderClassifierObject():
    with open('bestClassifier.pyobj', 'rb') as f:
        try:
            return pickle.load(f)
        except EOFError:
            print('Hit end of file')

# Load the file
my_obj = getGenderClassifierObject()
#print(my_obj)


my_file = pd.read_csv('./twitter_gender.csv', index_col=False, usecols=[0,1], skiprows=0000, nrows=1000)

def scoreText(classifierObject, text):
    score = 0.0
    for token in word_tokenize(text):
        if token in classifierObject:
            score += classifierObject[token]
    return score

incorrect_entries = ['']
all_scores = 0
len_all_scores = 0
all_scoresF = 0
len_all_scoresF = 0
def calculateEffectiveness(set_threshold=0, best_threshold = 0, best_score = 0):
    global all_scores, len_all_scores, all_scoresF, len_all_scoresF
    num_of_entries = 0
    num_of_correct_guesses = 0
    for entry in my_file.get_values():
        # Average of all values with a 64:36 split which favours twitter's 64% male basis
        threshold = (all_scores/(len_all_scores or 1) + all_scoresF/(len_all_scoresF or 1))/2 
        current_score = scoreText(dict(my_obj), str(entry[1]))
        if entry[0] == 0:
            all_scores += current_score
            len_all_scores += 1 
        else:
            all_scoresF += current_score
            len_all_scoresF += 1
        if current_score >= threshold and entry[0] == 0:
            incorrect_entries.append([entry[1], entry[0]])
            num_of_correct_guesses += 1
        elif current_score < threshold and entry[0] == 1:
            incorrect_entries.append([entry[1], entry[0]])
            num_of_correct_guesses += 1
        else:
            incorrect_entries.append([entry[1], 1.5*entry[0]])
        num_of_entries += 1

    current_percentage = num_of_correct_guesses/num_of_entries
    print("Current entry " + str(threshold) + " with an effectiveness from 0->1 of " + str(current_percentage))
    if current_percentage > best_score:
        best_score = current_percentage
        best_threshold = threshold

current_best_threshold = 0
current_best_score = 0.00
calculateEffectiveness(5.0, current_best_threshold, current_best_score)
print(all_scores/len_all_scores)
print(all_scoresF/len_all_scoresF)
#for i in range(-30, 0, 5):
#    calculateEffectiveness(1.4 + i/10, current_best_threshold, current_best_score)
#    print("" + str(current_best_score) +  str(current_best_threshold))

# Save the distribution as a pickled object
with open('incorrectlyClassifiedEntries.pyobj', 'wb') as output:
    pickle.dump(incorrect_entries, output, pickle.HIGHEST_PROTOCOL) 