import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd

DF_SIMPLE = pd.read_csv(
    'https://gist.githubusercontent.com/chriddyp/'
    'c78bf172206ce24f77d6363a2d754b59/raw/'
    'c353e8ef842413cae56ae3920b8fd78468aa4cb2/'
    'usa-agricultural-exports-2011.csv')


def generate_table(dataframe, max_rows=10):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )

app = dash.Dash()

app.layout = html.Div([
    dcc.Dropdown(id='my-dropdown'), # fill this in
    html.Div(id='table-container')
])

@app.callback(Output('table-container', 'children'), [Input('my-dropdown', 'value')])
def update_table(value):
    df = pd.read_csv(
    'https://raw.githubusercontent.com/plotly/'
    'datasets/master/gapminderDataFiveYear.csv')
    return generate_table(df)



#app.layout = html.Div(children=[
#    html.H4(children='US Agriculture Exports (2011)'),
#    generate_table(df)
#])

if __name__ == '__main__':
    app.run_server(debug=True)
