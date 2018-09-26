
# coding: utf-8

# In[1]:


# Setup
import tweepy
from tweepy import OAuthHandler
import re
import pickle
import time
  
# load info from .env
from dotenv import load_dotenv
import os
load_dotenv()
consumer_key = os.getenv('TWITTER_CONSUMER_KEY')
consumer_secret = os.getenv('TWITTER_CONSUMER_SECRET')
access_token = os.getenv('TWITTER_ACCESS_TOKEN')
access_secret = os.getenv('TWITTER_ACCESS_SECRET')

# get api
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

api = tweepy.API(auth, retry_count=3, retry_delay=5, retry_errors=set([401, 404, 500, 503]), wait_on_rate_limit=True)


# In[2]:



#Emojis0 = "😄 😃 😀 😊 ☺ 😉 😍 😘 😚 😗 😙 😜 😝 😛 😳 😁 😔 😌 😒 😞 😣 😢 😂 😭 😪 😥 😰 😅 😓 😩 😫 😨 😱 😠 😡 😤 😖 😆 😋 😷 😎 😴 😵 😲 😟 😦 😧 😈 👿 😮 😬 😐 😕 😯 😶 😇 😏 😑"
#Emojis = Emojis0.replace(" ", "")

Emoji_list = ['😠', '😯', '😴', '😇', '😝', '😡', '🤡', '😵', '🤥', '🤢', '🙁', '🤠', '🤐', '🙃', '😬', '😜', '😳', '😓', '😒', '😟', '☺️', '😢', '☹️', '😤', '🤧', '😖', '😨', '😞', '😩', '😌', '😲', '🤒', '😔', '😰', '🤕', '😮', '😫', '😛', '🤑', '😦', '😱', '🤓', '😕', '😭', '😪', '😧', '😷', '🤤']

# In[3]:
#['😰', '🤕', '😮', '😫', '😛', '🤑', '😦', '😱', '🤓', '😕', '😭', '😪', '😧', '😷', '🤤']

#%%time
#keyword = "😍" # "😋"

numberOfTweets = 5000

i = 0
for keyword in Emoji_list[16:]:
    # track timing
    t = time.time()
    
    # Empty Array 
    itemlist=[]  

    n = 0;
    for tweet in tweepy.Cursor(api.search, keyword, lang="en").items(numberOfTweets):
        dc = tweet._json
        a_str = dc.get('text')
        #list_all = re.split('( )', str) # this is a list
        #list_a = re.findall(r'[@]\S*', str) #[2,4,7]
        #list_b = [1,2,3,4,5,6]
        #list_a = [n for n in list_a if n not in list_b]

        # remove the following
        #print(re.findall(r'[@]\S*', str)) # Twitter user names
        #print(re.findall(r'[RT]\S*', str)) # "RT"
        #print(re.findall(r'[http]\S*', str)) # "RT"

        itemlist.append(a_str) 
        n = n+1
        if n % 100 == 0:
            print(str(n)+' ', end="")

    # save file
    #with open('outfile'+keyword, 'wb') as fp:
    
    with open(os.path.expanduser("~/Dropbox/insight_datadir/5k_0924/"+"outfile"+keyword+".p"), 'wb') as fp:
        pickle.dump(itemlist, fp)
    
    # print time
    elapsed = time.time() - t
    i = i+1
    print('i='+str(i)+' '+keyword+str(elapsed))


# str = dc.get('text')
# print(str)
# 
# import re
# s2 = re.split('( )', str) # this is a list
# print(s2)
# #print(s2.startswith('@'))
# #[ t for t in s2 if t.startswith('s') ]
# print(re.findall(r'[@]\S*', str))
# print(re.findall(r'[RT]\S*', str))

# # load file
# with open ('outfile', 'rb') as fp:
#     itemlist2 = pickle.load(fp)

# #itemlist2[0:3]
# print(re.findall(r'[@]\S*', itemlist2[0]))
