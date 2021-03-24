#!/usr/bin/python

import tweepy
import time

auth = tweepy.OAuthHandler('whB5QDSsoXYQDBK6Xs56jkTEN', 'Pprb9pyrfzryjJwDjSiGSLmj6n6v9dD8WcrmTxCpGjHcsZtZ0v')
auth.set_access_token('1184361280326393856-W5DWbcrf4rlEmGPYIpBKABUsqqz1aH', 'KAVBPRDIwIzvjNF0Xc8qw0jQseeVroIhEKLsXWvoIkb7T')
api = tweepy.API(auth)

#Set a directory here  FILL THIS OUT
directory = " "
filename = "Tweets.txt"

def removeUsers(tweet):
        while tweet.full_text.find("@",0,4) != -1:
                if tweet.full_text.find(" ") == -1:
                        tweet.full_text = ""
                        break
                tweet.full_text = tweet.full_text[tweet.full_text.find(" ")+1:]
        return tweet.full_text

def getReplies(username): 
        for tweet in api.search(q="from:" + username + " -filter:retweets",count=1):
                accountTweet = tweet

        print(accountTweet.text)
        print(accountTweet.id)
    
        #Will need to change for google bins
        file = open(directory + " " + filename,"w")   
        storedTweets = 0   #Amount of reply tweets gotten
        movingID = 0    #keeps track of last tweet in series to progress
        retrieveAmount = 200 #real max += 100 
        tweets = api.search(q="to:" + username + " -filter:retweets -filter:links",count=100,since_id=accountTweet.id,tweet_mode='extended')
        while True:
                writeString = ""
                #Twitter has a pull limit of tweets (450 * 100 tweets)
                #using "extended" to get full_text
                try:
                        tweets = api.search(q="to:" + username + " -filter:retweets -filter:links",count=100,since_id=accountTweet.id,max_id=movingID,tweet_mode='extended')
                        for tweet in tweets:
                                if tweet.in_reply_to_status_id == accountTweet.id:
                                        tweet.full_text = removeUsers(tweet)
                                        writeString = writeString + tweet.full_text + "\n"
                                        storedTweets +=1
                                movingID = tweet.id
                        
                        file.write(writeString) #Writes tweet block to file 
                except tweepy.error.RateLimitError as e:
                        print("taking a break")
                        time.sleep(120)
                        continue  
                if len(tweets) < 20 or storedTweets > retrieveAmount: #if no more tweets to retrieve / over set limit
                        break
        file.close()

accName = input("Account name (no @): ")
getReplies(accName)
