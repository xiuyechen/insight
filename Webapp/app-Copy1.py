import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pprint
from googleapiclient.discovery import build
import pandas as pd
import pickle, os
import emoji
import collections 

#################
# load files

# load google query results
fullfile = os.path.expanduser("~/Dropbox/insight/Google/"+'Song99Qs.p')
with open(fullfile, 'rb') as fp:
    Q = pickle.load(fp)
song_names = list(Q.keys())

# load model trained from twitter data
from sklearn.feature_extraction.text import TfidfVectorizer
vectorizer = TfidfVectorizer(ngram_range=(1, 3), analyzer='char',
                             use_idf=False)

from sklearn.linear_model import Perceptron
from sklearn.pipeline import Pipeline
clf = Pipeline([
    ('vec', vectorizer),
    ('clf', Perceptron(tol=1e-3)),
])
fullfile = os.path.expanduser("~/Dropbox/insight_side/"+'clf_0927.p') # perceptron
with open(fullfile, 'rb') as fp:
    clf = pickle.load(fp)

# load my emoji list
fullfile = os.path.expanduser("~/Dropbox/insight/Emoji/"+'mySmileys.p')
with open(fullfile, 'rb') as fp:
    emoji_list = pickle.load(fp)
len(emoji_list)
#################
# custom functions
def google_search(input_value):

    #from dotenv import load_dotenv
    #import os
    #load_dotenv()
    #my_developerKey = os.getenv('GOOGLE_DEVELOPER_KEY')
    #customsearch_cx = os.getenv('GOOGLE_CUSTOM_SEARCH_ENGINE_CX')
    my_developerKey = 'AIzaSyBUCKZDkUQTQWSjpqspjDqheeqWITRvNPA'
    customsearch_cx = '005602575294155670075:voquhyomtdq'

    service = build("customsearch", "v1",
            developerKey=my_developerKey)

    res = service.cse().list(
        q=str(input_value),
        cx=customsearch_cx,
        ).execute()

    df = parse_return(res)
    return df

def parse_content(res):
    
    # res.keys() = ['kind', 'items', 'queries', 'searchInformation', 'context', 'url']  
    items = res['items']
    strList = [];
    for ii in range(10):
        item = items[ii]
        # dict_keys(['kind', 'title', 'htmlTitle', 'link', 'displayLink', 'snippet', 'htmlSnippet', 'cacheId', 'formattedUrl', 'htmlFormattedUrl', 'pagemap'])
        string = item['title'] + item['snippet']
        strList.append(string)
    # df = pd.DataFrame(strList)
    return strList

def parse_return_annotated(res,labels):
    # import pandas as pd
    # res.keys() = ['kind', 'items', 'queries', 'searchInformation', 'context', 'url']  
    items = res['items']
    strList = [];
    for ii in range(10):
        item = items[ii]
        # dict_keys(['kind', 'title', 'htmlTitle', 'link', 'displayLink', 'snippet', 'htmlSnippet', 'cacheId', 'formattedUrl', 'htmlFormattedUrl', 'pagemap'])
        header = str(ii+1) + " " + str(labels[ii])
        strList.append(header)
        strList.append(item['title'])
        strList.append(item['snippet'])
        strList.append(item['formattedUrl'])
        strList.append('~~~~~~~~~~~~~~~~~~~~~')
        
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

# def parse_return(res):
    
#     # res.keys() = ['kind', 'items', 'queries', 'searchInformation', 'context', 'url']  
#     items = res['items']
#     strList = [];
#     for ii in range(10):
#         item = items[ii]
#         # dict_keys(['kind', 'title', 'htmlTitle', 'link', 'displayLink', 'snippet', 'htmlSnippet', 'cacheId', 'formattedUrl', 'htmlFormattedUrl', 'pagemap'])
#         strList.append(item['title'])
#         strList.append(item['snippet'])
#         strList.append(item['formattedUrl'])
#         strList.append('~~~~~~~~~~~~~~~~~~~~~')
        
#     df = pd.DataFrame(strList)
#     return df

def generate_table(dataframe, max_rows=30):
    return html.Table( 
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )

app = dash.Dash()

colors = {
    'background': '#FFFAFA',#'#FFFFE0',
    'text': '0B0A0A'
}

list_of_images = [1,2,3]

app.layout = html.Div(children=[ # style={'backgroundColor': colors['background']}, 
    html.H1(
        children='Google it...',
        style={
            #'textAlign': 'center',
            'color': colors['text']
        }
    ),

    dcc.Input(
        id='input_text', value='chicken farm', type='search', style={
            'textAlign': 'left',
            'width' : 600,
            'fontSize': 18,
            'marginBottom': 20, 
              }),
    
    dcc.RadioItems(
        id='radio_emoji',
        options=[
            {'label': '(all)  ', 'value': 'emoji0'},
            {'label': '😃  ', 'value': 'emoji1'},
            {'label': '😓  ', 'value': 'emoji2'},
            {'label': '😡  ', 'value': 'emoji3'}
        ],
        value='emoji0',
        labelStyle={'display': 'inline-block'}, style={
            'fontSize': 18}
    ),
    
    #html.Img(id='image'),
    
    html.Div(id='table-container')

])

@app.callback(
    Output('radio_emoji', 'options'),
    [Input('input_text', 'value')])
def update_radioItems(input_text):
    #df = google_search(input_value)
    # if input_text == 'Despacito':
    Res = Q.get('Despacito')
        
    # get 10 pages, combine emojis 
    # not all data have 100 results 
    Labels = []
    for i in range(len(Res)):
        res = Res[i]
        if 'items' in res.keys():
            strList = parse_content(res)
            predicted = clf.predict(strList)
            labels = get_labels_from_predicted(predicted,emoji_list)
            Labels = Labels + labels

    # SORT EMOJIS        
    freq = collections.Counter(Labels) 

    X = [] # emoji
    Y = [] # count occurrence
    for key, value in freq.items(): 
        X.append(key)
        Y.append(value)
        # print(key + " -> " + str(value))

    keydict = dict(zip(X, Y))
    X.sort(key=keydict.get,reverse=True)
    top3 = X[0:3]
    
    return [{'label': '(all)  ', 'value': 'emoji0'},
            {'label': top3[0]+'  ', 'value': 'emoji1'},
            {'label': top3[1]+'  ', 'value': 'emoji2'},
            {'label': top3[2]+'  ', 'value': 'emoji3'}]

#####    
@app.callback(
    Output('table-container', 'children'),[ 
    Input('input_text', 'value'),
    Input('radio_emoji','value')])
def update_table(input_text,radio_emoji,Q,clf):
    Res = Q.get('Despacito')
    strList = parse_content(Res[0])
    predicted = clf.predict(strList)
    df = parse_return_annotated(Res[0],labels)
    
    # update RadioItems (emojis options)
    if radio_emoji=='emoji1':
        # print('emoji1') #?
        strList = parse_content(Res[0])
        predicted = clf.predict(strList)
        labels = get_labels_from_predicted(predicted,emoji_list)
        df = parse_return_annotated(Res[0],labels)

        # make df with annotation!
        #df = google_search(input_text)
    elif radio_emoji=='emoji2':
        fakedata = [{'select':2}]
        df = pd.DataFrame(fakedata)
    return generate_table(df)

# @app.callback(
#     Output('table-container', 'children'), 
#     [Input('input_text', 'value')]
# )
# def update_table(input_value):
#     # df = google_search(input_value)
#     df = pd.DataFrame(["TESTING"])
#     return generate_table(df)

if __name__ == '__main__':
    app.run_server(debug=True)
