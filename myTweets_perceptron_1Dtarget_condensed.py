
# coding: utf-8

# In[1]:


import os
import pickle
import numpy as np
import re
import emoji
import regex


# ## Load dataset

# In[2]:


def extract_emojis(text):

    emoji_list = []
    data = regex.findall(r'\X', text)
    for word in data:
        if any(char in emoji.UNICODE_EMOJI for char in word):
            emoji_list.append(word)

    return emoji_list


# In[52]:


# load emoji list
fullfile = os.path.expanduser("~/Dropbox/insight/Emoji/"+'mySmileys.p')
with open(fullfile, 'rb') as fp:
    L = pickle.load(fp)
print(L)
print(len(L))
target_names = L


# In[4]:


class tweet_data:
    pass

# D = tweet_data()
# D.raw_data = rawdata
# D.data = data
# D.raw_target = elist
# D.filesnames = filenames
# D.numTweets = Len


# In[36]:


# load data

fullfile = os.path.expanduser("~/Dropbox/insight/Twitter/"+'tweets_75x5k.p')
with open(fullfile, 'rb') as fp:
    D = pickle.load(fp)

len(D.data)


# In[5]:


# select subset
target_names = ['😍','😡']


# In[9]:


len(D.raw_data)


# In[45]:


# make 1D target based only on the single search-emoji
# Len = []
# for keyword in target_names:
#     fullfile = os.path.expanduser("~/Dropbox/insight_datadir/5k/"+'outfile'+keyword+'.p')
#     with open(fullfile, 'rb') as fp:
#         itemlist = pickle.load(fp)
#         Len.append(len(itemlist))
    
# numTweets = 5000
numEmojis = len(target_names)
arr = []
for i in range(numEmojis):
    arr.extend([i] * D.numTweets[i]) 
target = np.array(arr, dtype=int)

target.shape


# ### Format Tweet dataset; split training/testing
# 

# In[61]:


# this is like a struct
class tweet_train:
    pass

T = tweet_train()
T.target_names = target_names
T.data = D.data
T.filenames = D.filesnames
T.target = target


# In[8]:


fullfile = os.path.expanduser("~/Dropbox/insight/Twitter/"+'tweet_train_2x5k.p')
with open(fullfile, 'rb') as fp:
    T = pickle.load(fp)


# In[53]:


T.target_names = target_names
print(T.target_names[T.target[0]])


# In[62]:


# Split the dataset in training and test set:
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(
    T.data, T.target, test_size=0.2)


# In[65]:


len(y_test)


# ## Training a classifier 2: Perceptron

# In[47]:


# TASK: Build a vectorizer that splits strings into sequence of 1 to 3
# characters instead of word tokens
from sklearn.feature_extraction.text import TfidfVectorizer
# vectorizer = TfidfVectorizer(ngram_range=(1, 3), analyzer='char',
#                              use_idf=False)
vectorizer = TfidfVectorizer(ngram_range=(1, 3), analyzer='word',
                             use_idf=True)


# In[48]:


from sklearn.linear_model import Perceptron
from sklearn.pipeline import Pipeline
# TASK: Build a vectorizer / classifier pipeline using the previous analyzer
# the pipeline instance should stored in a variable named clf
clf = Pipeline([
    ('vec', vectorizer),
    ('clf', Perceptron(tol=1e-3)),
])


# In[67]:


# TASK: Fit the pipeline on the training set
clf.fit(X_train, y_train)


# In[70]:


# TASK: Predict the outcome on the testing set in a variable named y_predicted
y_predicted = clf.predict(X_test)


# In[68]:


len(X_train)


# In[71]:


# Print the classification report
from sklearn import metrics
print(metrics.classification_report(y_test, y_predicted,
                                    target_names=T.target_names))


# In[27]:


# from os.path import join, dirname, abspath
# from matplotlib import pyplot
# from matplotlib.cbook import get_sample_data
# from numpy import linspace
# from numpy.core.umath import pi
# from numpy.ma import sin
# # poo-mark came from emojipedia:
# # https://emojipedia-us.s3.amazonaws.com/thumbs/120/apple/96/pile-of-poo_1f4a9.png
# poo_img = pyplot.imread(get_sample_data(join(dirname(abspath(__file__)), "poo-mark.png")))
# x = linspace(0, 2*pi, num=10)
# y = sin(x)
# fig, ax = pyplot.subplots()
# plot = ax.plot(x, y, linestyle="-")
# ax_width = ax.get_window_extent().width
# fig_width = fig.get_window_extent().width
# fig_height = fig.get_window_extent().height
# poo_size = ax_width/(fig_width*len(x))
# poo_axs = [None for i in range(len(x))]
# for i in range(len(x)):
#     loc = ax.transData.transform((x[i], y[i]))
#     poo_axs[i] = fig.add_axes([loc[0]/fig_width-poo_size/2, loc[1]/fig_height-poo_size/2,
#                                poo_size, poo_size], anchor='C')
#     poo_axs[i].imshow(poo_img)
#     poo_axs[i].axis("off")
# fig.savefig("poo_plot.png")


# In[24]:


metrics.accuracy_score(y_test, y_predicted)


# The precision is the ratio tp / (tp + fp) where tp is the number of true positives and fp the number of false positives. The precision is intuitively the ability of the classifier not to label as positive a sample that is negative.
# 
# The recall is the ratio tp / (tp + fn) where tp is the number of true positives and fn the number of false negatives. The recall is intuitively the ability of the classifier to find all the positive samples.
# 
# The F-beta score can be interpreted as a weighted harmonic mean of the precision and recall, where an F-beta score reaches its best value at 1 and worst score at 0.
# 
# The F-beta score weights recall more than precision by a factor of beta. beta == 1.0 means recall and precision are equally important.
# 
# 
# F1 = 2 * (precision * recall) / (precision + recall) 
# https://github.com/scikit-learn/scikit-learn/blob/f0ab589f/sklearn/metrics/classification.py#L1363

# In[28]:


# Plot the confusion matrix
cm = metrics.confusion_matrix(y_test, y_predicted)
print(cm)


# In[29]:


import matplotlib.pyplot as plt
plt.matshow(cm, cmap=plt.cm.jet)
plt.show()


# In[26]:


# Predict the result on some short new sentences:
sentences = [
    u'lovely definition: 1. pleasant or enjoyable: 2. beautiful:',
    u'Hate speech is a communication that carries no meaning other than the expression of hatred for some group',
    u'amazing wow love this!!!',
]
predicted = clf.predict(sentences)


# In[27]:


output = []
for ii in predicted:
    output.append(T.target_names[ii])
print(output)


# In[ ]:


# save model
fullfile = os.path.expanduser("~/Dropbox/insight_datadir/Webapp_data/"+'clf_0930.p')
with open(fullfile, 'wb') as fp:
    pickle.dump(clf, fp)


# In[ ]:


# np.argsort(classifier.predict_proba(X), axis=1)[-5:]


# ## Multi-layer perceptron (1 hidden layer)

# In[32]:


# http://scikit-learn.org/stable/modules/neural_networks_supervised.html
from sklearn.neural_network import MLPClassifier
X = [[0., 0.], [1., 1.]]
y = [0, 1]
clf = MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(5, 2), random_state=1)

clf.fit(X, y) 


# In[39]:


clf.predict([[2., 2.], [-1., -2.]])


# In[34]:


[coef.shape for coef in clf.coefs_]


# In[47]:


print(clf.coefs_[2])


# In[37]:


clf.predict_proba([[2., 2.], [-1., -2.]])  


# In[29]:


XV_test = vectorizer.transform(X_test)
XV_test.shape


# In[72]:


vectorizer.get_feature_names()


# In[ ]:


docs_new = ['God is love', 'what have you done!','Oh yeah? don''t try to trick me']
X_new_counts = count_vect.transform(docs_new)
X_new_tfidf = tfidf_transformer.transform(X_new_counts)

predicted = clf1.predict(X_new_tfidf)

for doc, category in zip(docs_new, predicted):
    print('%r => %s' % (doc, T.target_names[category]))

