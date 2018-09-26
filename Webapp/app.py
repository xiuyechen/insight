import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pprint
from googleapiclient.discovery import build
import pandas as pd

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
    
def parse_return(res):
    
    # res.keys() = ['kind', 'items', 'queries', 'searchInformation', 'context', 'url']  
    items = res['items']
    strList = [];
    for ii in range(10):
        item = items[ii]
        # dict_keys(['kind', 'title', 'htmlTitle', 'link', 'displayLink', 'snippet', 'htmlSnippet', 'cacheId', 'formattedUrl', 'htmlFormattedUrl', 'pagemap'])
        strList.append(item['title'])
        strList.append(item['snippet'])
        strList.append(item['formattedUrl'])
        strList.append('~~~~~~~~~~~~~~~~~~~~~')
        
    df = pd.DataFrame(strList)
    return df

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
            {'label': '😃  ', 'value': 'emoji1'},
            {'label': '😓  ', 'value': 'emoji2'},
            {'label': '😡  ', 'value': 'emoji3'}
        ],
        value='emoji1',
        labelStyle={'display': 'inline-block'}, style={
            'fontSize': 18}
    ),
    
    #html.Img(id='image'),
    
    html.Div(id='table-container')

])

"""
@app.callback(
    Output('radio_emoji', 'children'),[ 
    Input('input_text', 'value')])
def update_RadioItems(input_text,radio_emoji):
    #df = google_search(input_value)
    
    options=[
            {'label': '😃  ', 'value': 'emoji1'},
            {'label': '😓  ', 'value': 'emoji2'},
            {'label': '😡  ', 'value': 'emoji3'}
        ],
    
    # update RadioItems (emojis options)
    if radio_emoji=='emoji1':
        print('emoji1')
        df = google_search(input_text)
    elif radio_emoji=='emoji2':
        fakedata = [{'select':2}]
        df = pd.DataFrame(fakedata)
    return generate_table(df)
"""

@app.callback(
    Output('table-container', 'children'),[ 
    Input('input_text', 'value'),
    Input('radio_emoji','value')])
def update_table(input_text,radio_emoji):
    #df = google_search(input_value)
    
    # update RadioItems (emojis options)
    if radio_emoji=='emoji1':
        print('emoji1')
        df = google_search(input_text)
    elif radio_emoji=='emoji2':
        fakedata = [{'select':2}]
        df = pd.DataFrame(fakedata)
    return generate_table(df)


if __name__ == '__main__':
    app.run_server(debug=True)
