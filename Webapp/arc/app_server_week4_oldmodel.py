# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import glob

# import dash
# import dash_core_components as dcc
# import dash_html_components as html
# from dash.dependencies import Input, State, Output, Event
import pprint
from googleapiclient.discovery import build
import pandas as pd
import pickle, os
import emoji
import collections 
import datetime
from dotenv import load_dotenv

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

################# load files ###########

load_dotenv()
insight_datadir = os.getenv('INSIGHT_DATADIR')
    
# load google query results
fullfile = os.path.expanduser(insight_datadir + 'Song10Qs.p')
with open(fullfile, 'rb') as fp:
    Q = pickle.load(fp)
song_names = list(Q.keys())

# load model trained from twitter data
from sklearn.feature_extraction.text import TfidfVectorizer
vectorizer = TfidfVectorizer(ngram_range=(1, 3), analyzer='char',
                             use_idf=False)

from sklearn.linear_model import Perceptron
from sklearn.pipeline import Pipeline
# clf = Pipeline([
#     ('vec', vectorizer),
#     ('clf', Perceptron(tol=1e-3)),
# ])
fullfile = os.path.expanduser(insight_datadir + 'clf_0927.p') # perceptron
with open(fullfile, 'rb') as fp:
    clf = pickle.load(fp)

# load my emoji list
fullfile = os.path.expanduser(insight_datadir + 'mySmileys.p')
with open(fullfile, 'rb') as fp:
    emoji_list = pickle.load(fp)
len(emoji_list)

################# custom functions #############
def google_search_json(query,page_ix):
    # Build a service object for interacting with the API. Visit
    # the Google APIs Console <http://code.google.com/apis/console>
    # to get an API key for your own application.
    #if not page_ix:
     #   page_ix = 1
    start_ix = 10*(page_ix-1)+1

    load_dotenv()
    my_developerKey = os.getenv('GOOGLE_DEVELOPER_KEY')
    customsearch_cx = os.getenv('GOOGLE_CUSTOM_SEARCH_ENGINE_CX')
#     my_developerKey = 'AIzaSyBUCKZDkUQTQWSjpqspjDqheeqWITRvNPA'
#     customsearch_cx = '005602575294155670075:voquhyomtdq'


    service = build("customsearch", "v1",
            developerKey=my_developerKey)

    res = service.cse().list(
        q=query,
        cx=customsearch_cx,
        start=start_ix,
      ).execute()
    
    return res 

def parse_content(res):
    
    # res.keys() = ['kind', 'items', 'queries', 'searchInformation', 'context', 'url']  
    items = res['items']
    strList = [];
    for ii in range(len(items)):
        item = items[ii]
        string = item['title'] + item['snippet']
        strList.append(string)
    # df = pd.DataFrame(strList)
    return strList

def parse_return_annotated(res,labels):
    items = res['items']
    strList = [];
    for ii in range(len(items)):
        item = items[ii]
        header = str(ii+1) + " " + str(labels[ii])
        strList.append(header)
        strList.append(item['title'])
        strList.append(item['snippet'])
        strList.append(item['formattedUrl'])
        strList.append('... ... ... ...')
        
    df = pd.DataFrame(strList)
    return df

def get_labels_from_predicted(predicted,emoji_list):
    labels = []
    labels_text = []
    for ix in list(predicted):
        e = emoji_list[ix]
        labels.append(e)
        labels_text.append(emoji.UNICODE_EMOJI[e])
    return labels

def generate_table(dataframe, max_rows=50):
    return html.Table( 
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )

def generate_radio(top_labels):
    return dcc.RadioItems(
        id='radio_emoji',
        options=[
            {'label': '(all)  ', 'value': -1},
            {'label': top_labels[0]+'  ', 'value': 0},
            {'label': top_labels[1]+'  ', 'value': 1},
            {'label': top_labels[2]+'  ', 'value': 2}
        ],
        value = -1,
        labelStyle={'display': 'inline-block'}, style={
            'fontSize': 24}
    )
def parse_return_filtered(Res,Label_pages,label):
    strList = [];
    # go through 10 pages
    for ii in range(len(Label_pages)):
        label_p = Label_pages[ii]
        res = Res[ii]
        
        if 'items' in res.keys():
            items = res['items']
            for jj in range(len(label_p)): # same len as items?
                e = label_p[jj]
                if e == label:
                    item = items[jj]
                    header = str(ii*10 + jj + 1) + " " + label
                    strList.append(header)
                    strList.append(item['title'])
                    strList.append(item['snippet'])
                    strList.append(item['formattedUrl'])
                    strList.append('... ... ... ...')
    
    df = pd.DataFrame(strList)
    return df

def google_search_10pages(query):
    # make a dict, keys = query terms # this dict only has one key pair
    Q = {}

#     for q in qL:
    Res = []
    for page in range(10):
        page_ix = page + 1
        res = google_search_json(query,page_ix)
        Res.append(res)
    Q[query] = Res

    # save history # crude
    fullfile = os.path.expanduser(insight_datadir + "history/" + query + '.p')
    with open(fullfile, 'wb') as fp:
        pickle.dump(Q, fp)
    
    return Res

def get_past_queries():
    mydir = os.path.expanduser(insight_datadir + "history/")
    past_Q = []
    for file in os.listdir(mydir):
        if file.endswith(".p"):
            past_Q.append(file[:-2])
    return past_Q

def get_search_Res(query):
    # first check if this search has been done (and is already stored)
    past_Q = get_past_queries()

    if query in past_Q:
        # load 
        fullfile = os.path.expanduser(insight_datadir + "history/" + query + '.p')
        with open(fullfile, 'rb') as fp:
            Q = pickle.load(fp)
            Res = Q.get(query)
    else:
        try:
            Res = google_search_10pages(query)
        except:
            import datetime
            a = datetime.datetime.now()
            ix = a.second % 10
            key = list(Q)[ix] # load a random query out of the 10 samples loaded
            Res = Q.get(key)
            print(key)
    
    # combine emojis from 10 pages (but not all data have 100 results)
    Labels = [] # this is a flat list
    Label_pages = [] # this is a list of lists, matching Res structure
    for i in range(len(Res)):
        res = Res[i]
        if 'items' in res.keys():
            strList = parse_content(res)
            predicted = clf.predict(strList)
            labels = get_labels_from_predicted(predicted,emoji_list)
            Labels = Labels + labels
            Label_pages.append(labels)
    # text = " ".join(Labels) # this should be visualized as WordCloud!

    return Res,Labels,Label_pages

def get_top_labels(Labels):
#     top_labels = ['😀','😁','😂']
    freq = collections.Counter(Labels) 

    X = [] # emoji
    Y = [] # count occurrence
    for key, value in freq.items(): 
        X.append(key)
        Y.append(value)
        print(key + " -> " + str(value))
    keydict = dict(zip(X, Y))
    X.sort(key=keydict.get,reverse=True)
    top_labels = X[0:3]
    
    return top_labels


########## MAIN ################
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.config['suppress_callback_exceptions']=True

########## LAYOUT #############
app.layout = html.Div([

    html.H3(children='😀😁😂🤣😃😄😅😆😉😊😋😎😍😘😙😚🙂🤗🤔😐😑😶🙄😏😣😥😮🤐😯😪😫😴😌😛😜😝',style={'textAlign': 'center',}),

    html.H3(children='The Sentimental Search Bar',style={'textAlign': 'center',}),
    html.H3(children='🤤😒😓😔😕🙃🤑😲☹️🙁😖😞😟😤😢😭😦😨😩😬😰😱😳😵😡😠😷🤒🤕🤢🤧😇🤠🤡🤥🤓',style={'textAlign': 'center',}),
    
    dcc.Input(id='input-text', type='search', value='how to raise pigeons on the balcony',
             style={'width' : 600}),
    
    html.Button(id='submit-text', n_clicks=0, children='Submit'),
    
    html.Button(id='submit-random', n_clicks=0, children='Try a random example'),
    
    html.Div(id='radio-container'),
    
    html.Div(id='table-container')
    
    # actual Google bar: https://cse.google.com/cse?cx=005602575294155670075:voquhyomtdq
])

######### CALLBACKS ############
# STEP 1: search and update emojis
@app.callback(Output('radio-container', 'children'),
              [Input('submit-text', 'n_clicks')],
              [State('input-text', 'value')])
def update_radio(n_clicks, query):
    Res,Labels,Label_pages = get_search_Res(query)
    
    # save
    fullfile = os.path.expanduser(insight_datadir + 'this_query.p')
    with open(fullfile, 'wb') as fp:
        pickle.dump([Res,Labels,Label_pages], fp)

    # sort labels, find top_emojis, and make new display
    top_labels = get_top_labels(Labels)
    return generate_radio(top_labels)#,generate_table(df)


# STEP 2: update table
@app.callback(Output('table-container', 'children'),
              [Input('radio_emoji', 'value')])
def update_output(value):
    #Res,Labels,Label_pages = get_search_Res()
    # This should just share with update_radio
    # load
    fullfile = os.path.expanduser(insight_datadir +'this_query.p')
    with open(fullfile, 'rb') as fp:
        Res,Labels,Label_pages = pickle.load(fp)
        
    if int(value) == -1:
        res = Res[0]
        labels = Label_pages[0]
        df = parse_return_annotated(res,labels)
    else:
        top_labels = get_top_labels(Labels)
        label = top_labels[int(value)]
        df = parse_return_filtered(Res,Label_pages,label)
    return generate_table(df)

if __name__ == '__main__':
    app.run_server(debug=True,port=5000,host='0.0.0.0')
