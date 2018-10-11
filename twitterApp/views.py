from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic as gen
from django.http import HttpResponse
from .models import evaluation, Choice, Question
import logging

logger = logging.getLogger(__name__)

# The midpoint value of the classifier which has the highest success rate
CLASSIFIER_MEDIAN_VALUE = 11.76

class IndexView(gen.ListView):
    template_name = 'twitterApp/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]


class DetailView(gen.DetailView):
    model = Question
    template_name = 'twitterApp/detail.html'

class GraphView(gen.DetailView):
    template_name='twitterApp/graph.html'
    model = Question

class ResultsView(gen.DetailView):
    model = Question
    template_name = 'twitterApp/results.html'
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'twitterApp/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('twitterApp:results', args=(question.id,)))

def index(request):
    #SELECT
    qry = evaluation.objects.order_by('-date')[0:].values('name', 'date','male_entries','female_entries','positive_entries','negative_entries')
    return render(request, 'twitterApp/graph.html', {'rs': qry, 'cs':qry[0].keys()})

def send_classifier_data(request):
    import json
    json_data = open('static/bestClassifier.json')
    json_dump = json.dumps(json_data.read())
    json_data.close()
    # request.META.get("HTTP_QUERYDATA")
    # request.META.get("HTTP_QUERYDATATYPE")
    currentQueryData = request.META.get("HTTP_QUERYDATA")
    currentQueryType = request.META.get("HTTP_QUERYDATATYPE")
    return HttpResponse(json.dumps(analyze_twitter_query(request)))
    if currentQueryData == 'realdonaldtrump' and currentQueryType == 'username':
        processed_data = {'male': 164, 'positive': 45, 'female': 180, 'negative': 119}
    else:
        processed_data = {'male': 0, 'positive': 0, 'female': 0, 'negative': 0 }
    return HttpResponse(json.dumps(processed_data)) 

def determine_gender(text_list):
    from nltk.tokenize import word_tokenize
    import json

    def scoreText(classifierObject, text):
        score = 0.0
        for token in word_tokenize(text):
            if token in classifierObject:
                score += classifierObject[token]
        return score - CLASSIFIER_MEDIAN_VALUE
    with open('static/bestClassifier.json') as file:
        try:
            text_classifications = []
            g_classifier = json.load(file)
            for text in text_list:
                text_classifications.append({'compound': scoreText(g_classifier, text['text'])})
            return text_classifications
        except Exception as ex:
            raise FileNotFoundError('Unable to load Classifier' + str(ex)) 

def determine_sentiment(text_list):
    from nltk.sentiment.vader import SentimentIntensityAnalyzer
    sentiment_list = []
    SIA = SentimentIntensityAnalyzer()
    for text in text_list:
        sentiment_list.append(SIA.polarity_scores(text['text']))
    return sentiment_list

def pull_twitter_data(queryData, queryDataType):
    import json
    test_twiter_json = open('static/exampleTweet.json')
    test_json_object = json.load(test_twiter_json)
    test_twiter_json.close()
    return test_json_object

def analyze_twitter_query(request):
    # Pull Twitter Data
    currentQueryData = request.META.get("HTTP_QUERYDATA")
    currentQueryType = request.META.get("HTTP_QUERYDATATYPE")
    tw_data = pull_twitter_data(currentQueryData, currentQueryType)

    # Parse for tweets or other necessary information into an object (or lists in the case of sentiment and gender)
    tweets = []
    for tweet in tw_data:
        # Do something
        if currentQueryData == 'realdonaldtrump':
            if len(tweets) >= 10:
                break
        tweets.append(tweet)

    # Run the two above processing information using these lists
    sentiment_list = determine_sentiment(tweets)
    gender_list = determine_gender(tweets)

    # Return the data for visualization as an object
    positive_entries = 0
    negative_entries = 0
    male_entries = 0
    female_entries = 0
    for item in sentiment_list:
        if item['compound'] >= 0:
            positive_entries += 1
        else:
            negative_entries += 1
    for item in gender_list:
        if item['compound'] >= 0:
            male_entries += 1
        else:
            female_entries += 1
    return {'male': 10* male_entries, 'positive': 10* positive_entries, 'female': 10* female_entries, 'negative': 10* negative_entries}