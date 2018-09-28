# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State


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

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

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

def generate_table(dataframe, max_rows=30):
    return html.Table( 
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )

def generate_radio(labels):
    return dcc.RadioItems(
        id='radio_emoji',
        options=[
            {'label': '(all)  ', 'value': 'emoji0'},
            {'label': labels[0]+'  ', 'value': 'emoji1'},
            {'label': labels[1]+'  ', 'value': 'emoji2'},
            {'label': labels[2]+'  ', 'value': 'emoji3'}
        ],
        value='emoji0',
        labelStyle={'display': 'inline-block'}, style={
            'fontSize': 24}
    )

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.config['suppress_callback_exceptions']=True

########## LAYOUT #############
app.layout = html.Div([

    html.H3(children='😀😁😂🤣😃😄😅😆😉😊😋😎😍😘😙😚🙂🤗🤔😐😑😶🙄😏😣😥😮🤐😯😪😫😴😌😛😜😝',style={'textAlign': 'center',}),

    html.H3(children='The Sentimental Search Bar',style={'textAlign': 'center',}),
    html.H3(children='🤤😒😓😔😕🙃🤑😲☹️🙁😖😞😟😤😢😭😦😨😩😬😰😱😳😵😡😠😷🤒🤕🤢🤧😇🤠🤡🤥🤓',style={'textAlign': 'center',}),
    
    dcc.Input(id='input-text', type='search', value='climate change is...',
             style={'width' : 600}),
    
    html.Button(id='submit-text', n_clicks=0, children='Submit'),
    html.Div(id='radio-container'),
    
    html.Div(id='table-container')
])

######### CALLBACKS ############
@app.callback(Output('radio-container', 'children'),
              [Input('submit-text', 'n_clicks')],
              [State('input-text', 'value')])
def update_radio(n_clicks, input1):
    a = datetime.datetime.now()
    fakedata = [{'hour':a.hour},{'second':a.second}]
    df = pd.DataFrame(fakedata)
    labels = [str(a.second),'😳','😵']
    return generate_radio(labels)


@app.callback(Output('table-container', 'children'),
              [Input('radio_emoji', 'value')])
def update_output(input1):
    a = datetime.datetime.now()
    fakedata = [{'hour':input1},{'second':a.second}]
    df = pd.DataFrame(fakedata)
    
    return generate_table(df)

if __name__ == '__main__':
    app.run_server(debug=True)