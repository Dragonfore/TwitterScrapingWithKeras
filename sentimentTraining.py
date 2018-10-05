from bs4 import BeautifulSoup
import urllib.request
import nltk
from nltk.corpus import stopwords
import matplotlib.pyplot as plt
from nltk.tokenize import sent_tokenize
response = urllib.request.urlopen('http://php.net/') 
html = response.read() 
soup = BeautifulSoup(html,"html5lib") 
text = soup.get_text(strip=True) 
tokens = [t for t in text.split()]
clean_tokens = tokens[:]
sr = stopwords.words('english')
for token in tokens:
    if token in stopwords.words('english'):
        clean_tokens.remove(token) 
freq = nltk.FreqDist(clean_tokens) 
for key,val in freq.items(): 
    print (str(key) + ':' + str(val))

freq.plot(20, cumulative=False)
"""
# Data to plot
labels = 'Positive', 'Slightly Positive', 'Neutral', 'Slightly Negative', 'Negative'
sizes = [215, 130, 245, 210, 180]
colors = ['blue', 'lightskyblue', 'grey', 'r','firebrick']
explode = (0.1, 0, 0, 0, 0)  # explode 1st slice
 
# Plot
plt.pie(sizes, explode=explode, labels=labels, colors=colors,
        autopct='%1.1f%%', shadow=True, startangle=140)
 
plt.axis('equal')
plt.show()
"""

