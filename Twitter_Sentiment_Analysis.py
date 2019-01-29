# Twitter Sentiment Analysis 
" Created on Fri Jan 25 12:32:51 2019 @author: Ranjan Kaul "

from tweepy import API,Cursor
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import Tw_Credentials

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure

from textblob import TextBlob

import re 


"#################################### TW-CLIENT ################################################################"
class TwClient():
    def __init__(self,tw_usr=None):
        self.auth = TwAuth.twauth(self)
        self.twclient = API(self.auth)                    

        self.tw_usr = tw_usr                                  ## ID from which to get tweets from

    def gt_usr_tm_tw(self,num_tw):                            ## gets tweets from own user profile 
                                                              ## untill id defined == None
        tw = []
        for tweet in Cursor(self.twclient.user_timeline ,id = self.tw_usr ).items(num_tw):
            tw.append(tweet)
        return(tw)
    def gt_usr_fr(self,num_fr):                               ## gets friends from own user profile 
                                                              ## untill id defined == None
        fr_list = []
        for fr in Cursor(self.twclient.twclient,id = self.tw_usr ).items(num_fr):
            fr.append(fr_list)
        return(fr_list)
        
        
    def gt_hm_tm_tw(self, num_tw):
        tweets = []
        for tweet in Cursor(self.twclient.home_timeline,id=self.tw_user).items(num_tw):
            tweets.append(tweet)
        return tweets
"!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!TW-Authentication!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
class TwAuth():
    
    def twauth(self):
        auth = OAuthHandler(Tw_Credentials.CONSUMER_KEY,Tw_Credentials.CONSUMER_SECRET)        ## inheriting from OAUTH               
        auth.set_access_token(Tw_Credentials.ACCESS_TOKEN,Tw_Credentials.ACCESS_TOKEN_SECRET)  ## Passing Credentials    
        return auth


"#################################### TW-CREATE_DATA_STREAM #######################################################"
class Twitter_Stream():                                      ##  Class to get the Tweets from twitter

    def __init__(self):
        pass
###################################################################################################################################    
    def stream_tweets(self,fetched_tweets_filename,taggs):   ## Function passing the authentication details
        listen = TwListener(fetched_tweets_filename)         ## creating a instance of the 
        auth =TwAuth.twauth(self)
        stream = Stream(auth, listen)
        stream.filter(track=[taggs])                         ## Keyword that want to stream 
        
"##################################### TW-PROCESS_DATA_STREAM #####################################################################"
class TwListener(StreamListener):                            ## inheriting from StreamListener
    
        def __init__(self,fetched_tweets_file):
            self.fetched_tweets_file = fetched_tweets_file
###################################################################################################################################
        def on_data(self,data):
            try :
                print(data)                                  ## print out the data that we capture
                with open(self.fetched_tweets_file,'a') as tf :
                    tf.write(data)
                return True
            except BaseException as e:
                print("Error on Data : %s " %str(e))
            return True
#####################################################################################################################################        
        def error(self,status):                              ##  print out any error that occurs  
            if status == 402: 
                print(status)                                ## if you accidentaly pull too much 
                return False                                 ## >> data from twitter and are on verge of getting banned
            else:                                            
                print(status)
"###################################################################################################################################"                
class TwAnalyser():
    
    def tw_analyse(self,tweets):
        df = pd.DataFrame(data=[tweet.text for tweet in tweets],columns=['Tweets'])
        df['Retweet'] = pd.DataFrame(data=[tweet.retweet_count for tweet in tweets])
        df['Likes'] = pd.DataFrame(data=[tweet.favorite_count for tweet in tweets])
        df['date'] = pd.DataFrame(data=[tweet.created_at for tweet in tweets])
        a = (str (input("Do You want to analyse sentiment Y or N : "))).upper()
        if a == "Y":
            a_list = []
            for tweet in df['Tweets']:
                tweet =' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())
                b = TextBlob((tweet))
                b = b.sentiment.polarity
                a_list.append(b)
            df['sentiment'] = pd.Series(a_list).values 
        print(df)
        return df 
    
    def tw_plot(self,tweets):
        
        fig = figure(num="None",figsize=(10,10))
        
        plt.subplot(211)
        analyse = TwAnalyser()
        a= (analyse.tw_analyse(tweets))
    
        plt.plot(a['date'].values,a['Retweet'].values , color='green',label = 'Retweets')
        plt.plot(a['date'].values,a['Likes'].values , color='red',label = 'Likes')
        
        plt.grid(True)
                
        likes_max = a['Likes'].idxmax()
        re_max = (a['Retweet'].values).tolist()
        re_maxx = re_max.index(max(re_max))
        
        
        plt.annotate('Highest Likes',xy=(a.date[likes_max],a.Likes[likes_max]))
        plt.annotate('Highest Retweet',xy=(a.date[re_maxx],a.Retweet[re_maxx]))
        
        plt.scatter(a.date[re_maxx],a.Retweet[re_maxx],marker = "o",label ="highest retweet",color = 'k')
        plt.scatter(a.date[likes_max],a.Likes[likes_max],marker = "*",label ="highest likes",color = 'k')
        
        plt.xticks(rotation = 90)
        
        plt.xlabel("Dates")
        plt.ylabel("People")
        plt.legend()
        
        plt.subplot(212)
        plt.plot(a['date'].values,a['sentiment'].values , color='green',label = 'sentiment')
        plt.grid(True)
        plt.xticks(rotation = 90)
        plt.xlabel("Dates")
        plt.ylabel("sentiment")
        plt.legend()
        
        
        plt.show()
   
    def plot_sentiment(self, tweet):
        pass
    
    def keyword_search(self):
        auth = TwAuth.twauth(self)
        api = API(auth)
        tweets = api.search('republic day', count=10)
        #print(tweets)
        return tweets


"######################################## TW-MAIN ####################################################################################"     
if __name__ == "__main__":
   
    client = TwClient("pycon")                    # when we have a specific user
    tweets = client.gt_usr_tm_tw(100)             # profile for sentiment analysis
                                                  #
    analyse = TwAnalyser()                        #
    analyse.tw_plot(tweets)                       #
                                                   #
####################################################  
#    taggs = "republicday"                         # when we have a specific key word
#    fetched_tweets_file =taggs+".json"            # for sentiment analysis,saved in 
#    ts = Twitter_Stream()                         # file.
#    ts.stream_tweets(fetched_tweets_file,taggs)   #
                                                   #
####################################################
       
   
    
 
#    analyse = TwAnalyser()                        
#    tweets = analyse.keyword_search()
#    analyse.tw_plot(tweets)
    
    
    


    