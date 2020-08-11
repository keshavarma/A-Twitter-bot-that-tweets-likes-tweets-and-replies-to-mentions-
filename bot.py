import json
import random
import time
import sys
import tweepy
from os import environ

consumer_key =environ['consumer_key']
consumer_secret_key =environ['consumer_secret_key']
access_token =environ['access_token']
access_token_secret =environ['access_token_secret']

FILE_NAME = 'last_seen_id.txt'

def retrieve_last_seen_id(file_name):
    f_read = open(file_name, 'r')
    last_seen_id = int(f_read.read().strip()) 
    f_read.close()
    return last_seen_id

def store_last_seen_id(last_seen_id, file_name):
    f_write = open(file_name, 'w')
    f_write.write(str(last_seen_id))
    f_write.close()
    return

def get_quotes():
    with open('quotes.json',encoding='utf-8') as f:
        quotes_json = json.load(f)
    return quotes_json['quotes']

def get_random_quote():
    quotes = get_quotes()
    random_quote = random.choice(quotes)
    return random_quote

def create_tweet():
    quote = get_random_quote()
    tweet = """
            {}
            
            """.format(quote['quote'])
    return tweet


def tweet_quote():
    

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret_key)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True,wait_on_rate_limit_notify=True)


    
    print('getting a random quote...')        
    tweet = create_tweet()
    try:
        api.update_status(tweet)
    except tweepy.TweepError as e:
        print(e.reason)
   

def like_tweets():

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret_key)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True,wait_on_rate_limit_notify=True)


    search=['swamivivekananda','dharma','ramakrishna mission', 'upanishads','gita','vedanta','indian wisdom','srikrishna','shiva','om']
    ntweets=150

    for s in search:
        for tweet in tweepy.Cursor(api.search,s).items(ntweets):
            try:
                tweet.favorite()
                print("Tweet liked")
            except tweepy.TweepError as e:
                print(e.reason)
            except StopIteration:
                break    
                    

def reply_mentions():
    
    
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret_key)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True,wait_on_rate_limit_notify=True)

    
    print("retrieving and replying...",flush=True)
    last_seen_id=retrieve_last_seen_id(FILE_NAME)
    mentions = api.mentions_timeline(last_seen_id,tweet_mode='extended')
    for mention in reversed(mentions):
        try:
            print(str(mention.id) + '--' + mention.full_text,flush=True)
            last_seen_id=mention.id
            store_last_seen_id(last_seen_id,FILE_NAME)
            api.update_status('@' + mention.user.screen_name + ' I am a bot. So if you have any queries you can contact @keshavarmah')
            print("responded back...")
        except Exception:
            print("no mention ):")
            
if __name__ == "__main__":
    interval=60*60*24

    while True:
        tweet_quote()
        like_tweets()
        print("done for today..")
        time.sleep(interval)
         
        
              
    

    





        
