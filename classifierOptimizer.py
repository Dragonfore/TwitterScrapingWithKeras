import pickle
import math
import string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import Counter
# Function to load the pickled object
def getGenderClassifierObject():
    with open('genderClassifier.pyobj', 'rb') as f:
        try:
            return pickle.load(f)
        except EOFError:
            print('Hit end of file')

def getMisclassifiedEntries():
    with open('incorrectlyClassifiedEntries.pyobj', 'rb') as f:
        try:
            return pickle.load(f)
        except EOFError:
            print('Hit end of file')

# Load the file
my_obj = getGenderClassifierObject()
misclassifieds = getMisclassifiedEntries()
misclassifieds = misclassifieds[1:]


# Initialize counter and words to ignore
counter = Counter('')
counterF = Counter('')
sr = stopwords.words('english')
punctuation = string.punctuation

# For every entry in the csv file, count important words
for entry in misclassifieds:
    is_male= False if entry[1] else True
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

new_counter = Counter(log_distributed_results)
new_counter2 = Counter(my_obj)
new_counter += new_counter2
adjusted_values = {}
for key in new_counter.keys():
    adjusted_values[key] = float(new_counter[key] / 1.36) 

with open('genderClassifierCache.pyobj', 'wb') as output:
    pickle.dump(my_obj, output, pickle.HIGHEST_PROTOCOL)
# Save the distribution as a pickled object
with open('genderClassifier.pyobj', 'wb') as output:
    pickle.dump(adjusted_values, output, pickle.HIGHEST_PROTOCOL)   