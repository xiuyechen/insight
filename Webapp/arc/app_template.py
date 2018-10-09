import plotly.figure_factory as ff

figure = ff.create_table(...) # see docs https://plot.ly/python/table/
app.layout = html.Div([
    dcc.Graph(id='my-table', figure=figure)
])
or in a callback like:

app.layout = html.Div([
    [...]
    dcc.Dropdown(id='my-dropdown', [...]),
    dcc.Graph(id='my-table')
])

@app.callback(Output('my-table', 'figure'), [Input('my-dropdown', 'value')])
def update_table(value):
    dff = df[df['filter-column'] == value] # replace with your own data processing code
    new_table_figure = ff.create_table(dff)
    return new_table_figure

# https://community.plot.ly/t/display-tables-in-dash/4707/19