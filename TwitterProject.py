import tweepy
from tweepy import OAuthHandler
import requests
import json
import pyodbc


server = 'cs3550.westus2.cloudapp.azure.com'
database = 'saraalaskarova'
username = 'saraalaskarova'
password = 'knit.hawaii.enemy'

connectionString = 'DRIVER={ODBC Driver 13 for SQL Server};SERVER=' + server + ';DATABASE=' + database
connectionString = connectionString + ';UID=' + username + ';PWD=' + password

## Create a connection
connection = pyodbc.connect(connectionString)
openConnection = connection.cursor()

## All the important information you were asked to collect from Twitter
twitterKey = 'ZAKnleEmly0npk8rpraPejh6z'
twitterSecret = 'ahymdXXyTXaklzPcq7OnTxbgBAzRe3sN0rwmKHxpN5fI3ytpt3'
accessToken = '1191910497441828864-QQ4yU0moDh8RUxJxqMu5rQejZDCe4D'
accessSecret = 'HIhDrp4bCnLJrEmO064O2Pd1BSm4tKDZjXRG5BqRgRHqQ'

#To connect to API's
base_url = "https://westus2.api.cognitive.microsoft.com"
text_analytics_base_url = base_url + "/text/analytics/v2.0/"
subscription_key='12d731aa4f4b4506b2da9f8d333a3e30' 
headers = {"Ocp-Apim-Subscription-Key": subscription_key, "Content-Type": "application/json"}

##Authenticate your app
auth = OAuthHandler(twitterKey, twitterSecret)
auth.set_access_token(accessToken, accessSecret)

## Opens a connection to twitter - respecting rate limits (so you don't get stopped
apiAccess = tweepy.API(auth, wait_on_rate_limit=True)

sqlString = 'INSERT Tweets (userName, tweetText, tweetLocation, tweetDate, sentimentScore, keyPhrases) VALUES (?,?,?,?,?,?)'

for tweet in tweepy.Cursor(apiAccess.search, q='#fortnite -filter:retweets', tweet_mode="extended", lang='en', geocode='41.0602,-111.9711,2000mi').items(2500):
    userName = tweet.user.name
    tweetText = tweet.full_text
    tweetLocation = tweet.user.location
    tweetDate = tweet.created_at

    call_id = 1
    call_text = tweetText
    api_document = []
    api_document.append({'id':str(call_id), 'language':'en', 'text':call_text }) 
    #creates a document array
    post_data={'documents':api_document}  

    sentiment_api_url = text_analytics_base_url + "sentiment"
    response = requests.post(sentiment_api_url, headers=headers, json=post_data)
    #print(response.json())
    parsed_response = response.json()
    sentimentScore = parsed_response['documents'][0]['score']

    key_phrases_api_url=text_analytics_base_url +'keyPhrases'
    response=requests.post(key_phrases_api_url, headers=headers,json=post_data)
    key_phrases=response.json()
    keyPhrasesArg = ', '.join(key_phrases['documents'][0]['keyPhrases'])

    args = userName, tweetText, tweetLocation, tweetDate, sentimentScore, keyPhrasesArg
    openConnection.execute(sqlString, args)

    openConnection.commit()
    getData = connection.cursor()
