import pickle
import json

def getGenderClassifierObject():
    with open('bestClassifier.pyobj', 'rb') as f:
        try:
            return pickle.load(f)
        except EOFError:
            print('Hit end of file')

my_classifier = getGenderClassifierObject()
my_json = json.dumps(my_classifier)
my_json_file = open('bestClassifier.json', 'w')
my_json_file.write(my_json)
my_json_file.close()