# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from tkinter.ttk import Style
from plotly import graph_objects as go
from turtle import width
from dash import Dash, html, dcc, dash_table, Input, Output, State, callback_context
import plotly.express as px
import pandas as pd
import numpy
import datetime
from werkzeug.debug.tbtools import DebugTraceback
import mongodb
import mysql_own
import neo4j_own
from plotly import graph_objects as go

faculty_name = "Agouris,Peggy"

app = Dash(__name__)
mysqlclient = mysql_own.MySQLClient()
profnames = mysqlclient.find_all_faculty_names()
mysqlclient.close()
mysqlclient = mysql_own.MySQLClient()
pubcount_df = mysqlclient.get_faculty_pub_citation_count(faculty_name)
pub_trend_bar_graph = px.bar(pubcount_df, x="Year", y="Publication Count",
                             barmode="group", title="Publication Trend")
neo4jclient = neo4j_own.MyNeo4jClient(
    "bolt://localhost:7687", "neo4j", "marino1228")
pubcount_df = neo4jclient.get_top_pub_list(faculty_name)
cite_trend_scatterplot = px.scatter(pubcount_df, x="Year", y="Citations",
                                    size="Citations", color="Citations", hover_name="Title",
                                    log_x=False, size_max=60, title="Citation Trend")
data = mysqlclient.get_top_venue_list(faculty_name)
num_pubs = [x["Number of Publications"] for x in data]
citations = [x["Number of Citations"] for x in data]
venues = [x["Venue"] for x in data]
data = {"Number of Publications": num_pubs,
        "Venue": venues, "Citations": citations}
fig3 = px.funnel(data, y='Venue', x='Number of Publications', color='Venue', labels={
}, hover_data=["Number of Publications", "Citations"])
fig3.update_yaxes(visible=False, showticklabels=False)
fig3.update_layout(showlegend=False)
app.layout = html.Div(children=[
    html.Div(
        className="header-title",
        children=[
            html.H2(
                id="title",
                children="Faculty Match",
            ),
            html.Div(
                id="learn_more",
                children=[
                    html.Img(className="logo",
                             src=app.get_asset_url("profpic.png"))
                ],
            ),
        ],
    ),
    html.Div(
        id="grid",
        children=[
            html.Center(
                html.H4('Who is the best professor to collaborate with?')),
            html.Div([html.Div([html.Center(html.P("Select professor name you may be interested in:")), ], className='one-third column'),
                      html.Div([dcc.Dropdown(
                          id="dropdown",
                          options=profnames,
                          value="Agouris,Peggy",
                          clearable=False,
                      )], className='two-thirds column')], className='row'),
        ],
        className="pretty_container"
    ),
    html.Div(children=[
        html.Div(children=[
            html.Div([html.Center(html.H4('Citation Trend'),), dcc.Graph(
                id='cite_trend_scatter',
                figure=pub_trend_bar_graph,
            ), ],
                className="pretty_container one-half column"),
            html.Div([
                html.Center(html.H4('Top Publications'),),
                dash_table.DataTable(
                    id='top_pub_table',
                    style_cell=dict(textAlign='center'),
                    style_header=dict(backgroundColor="darkslategray",
                                      color='white', fontWeight='bold'),
                    style_data={
                        'whiteSpace': 'normal',
                        'height': 'auto',
                    },
                ),
            ],
                className="pretty_container one-half column"),
        ],
            className="row"),
    ], ),
    html.Div(children=[
        html.Div(children=[html.Center(html.H4('Publication Trend'),), dcc.Graph(
            id='pub_trend_bar',
            figure=pub_trend_bar_graph,
        ),
        ], className="pretty_container one-half column"),
        html.Div(children=[html.Center(html.H4('Top Venues'),),
                           dcc.Graph(
            id='top_venue_funnel',
            figure=fig3,
        ),
        ], className="pretty_container one-half column"),

    ], className="row"),
    html.Div([
        html.Div(id="grid2",
             children=[
                 html.Center(html.H4('Add Notes and Favorites')),
                 html.Div([
                     html.Div([html.Center(html.P('Select a professor you want to write about:')), ],
                          className='one-third column'),
                     html.Div([dcc.Dropdown(profnames, value="Agouris,Peggy",
                                            id='demo-dropdown', clearable=False, ), ],
                              className='two-third column'),
                 ],
                     className='row'),
                 html.H5(' '),
                 html.Div([html.Div([dcc.Textarea(
                     id='textarea-example',
                     value='Place to write your notes about the faculty member selected above',
                     style={'height': 100, 'width': 600},
                 ), html.Button('Save/Update Note', id='save-update', n_clicks=0),
                     html.Button('Delete Note', id='delete', n_clicks=0),
                 ], className='one-half column'),
                     html.Div([dcc.Textarea(
                         id='textarea-example2',
                         value='Place to write why the selected faculty member is your favorite',
                         style={'height': 100, 'width': 600},
                     ), html.Button('Save/Update Favorite', id='save-update-fav', n_clicks=0),
                         html.Button('Delete Favorite',
                                     id='delete-fav', n_clicks=0),
                     ], className='one-half column'),
                 ], className='row'),
             ],
        ),
    ], className="pretty_container"),

    html.Div(children=[
        html.Div(children=[html.Center(html.H4('Notes'),),
                           dash_table.DataTable(
            id='table3',
            style_cell=dict(textAlign='center'),
            style_header=dict(backgroundColor="darkslategray",
                              color='white', fontWeight='bold'),
            style_data={
                'whiteSpace': 'normal',
                'height': 'auto',
            },
        ),
        ], className="pretty_container one-half column"),
        html.Div([html.Center(html.H4('Favorites')), dash_table.DataTable(
            id='table4',
            style_cell=dict(textAlign='center'),
            style_header=dict(backgroundColor="darkslategray",
                              color='white', fontWeight='bold'),
            style_data={
                'whiteSpace': 'normal',
                'height': 'auto',
            },
        ), ], className="pretty_container one-half column"),

    ], className="row"),
])


@ app.callback(
    Output('cite_trend_scatter', 'figure'),
    Input('dropdown', 'value'))
def update_figure(faculty_name):
    # REPLACE WITH YOUR NEO4J PASSWORD HERE
    neo4jclient = neo4j_own.MyNeo4jClient(
        "bolt://localhost:7687", "neo4j", "marino1228")
    pubcount_df = neo4jclient.get_top_pub_list(faculty_name)
    cite_trend_scatterplot = px.scatter(pubcount_df, x="Year", y="Citations",
                                        size="Citations", color="Citations", hover_name="Title",
                                        log_x=False, size_max=60)
    return cite_trend_scatterplot


@ app.callback(
    Output('pub_trend_bar', 'figure'),
    Input('dropdown', 'value'))
def update_figure(faculty_name):
    mysqlclient = mysql_own.MySQLClient()
    pubcount_df = mysqlclient.get_faculty_pub_citation_count(faculty_name)
    pub_trend_bar_graph = px.bar(pubcount_df, x="Year", y="Publication Count",
                                 barmode="group")
    return pub_trend_bar_graph


@ app.callback(
    Output('top_pub_table', 'data'),
    Input('dropdown', 'value'))
def update_table(faculty_name):
    # REPLACE WITH YOUR NEO4J PASSWORD HERE
    neo4jclient = neo4j_own.MyNeo4jClient(
        "bolt://localhost:7687", "neo4j", "marino1228")
    return neo4jclient.get_top_pub_list(faculty_name)[:8]


@ app.callback(
    Output('top_venue_funnel', 'figure'),
    Input('dropdown', 'value'))
def update_top_venue_table(faculty_name):
    data = mysqlclient.get_top_venue_list(faculty_name)
    num_pubs = [x["Number of Publications"] for x in data]
    citations = [x["Number of Citations"] for x in data]
    venues = [x["Venue"] for x in data]
    data = {"Number of Publications": num_pubs,
            "Venue": venues, "Citations": citations}
    fig3 = px.funnel(data, y='Venue', x='Number of Publications', color='Venue', labels={
    }, hover_data=["Number of Publications", "Citations"])
    fig3.update_yaxes(visible=False, showticklabels=False)
    fig3.update_layout(showlegend=False)
    return fig3


@ app.callback(
    Output('table3', 'data'),
    Input('save-update', 'n_clicks'),
    Input('delete', 'n_clicks'),
    State('demo-dropdown', 'value'),
    State('textarea-example', 'value'),
)
def update_output(btn1, btn2, dropdown, note):
    mongoclient = mongodb.MyMongoClient()
    changed_id = [p['prop_id'] for p in callback_context.triggered][0]
    if 'save-update' in changed_id:
        mongoclient.insert_note(dropdown, note)
    else:
        mongoclient.delete_note(dropdown)
    return mongoclient.get_notes()


@ app.callback(
    Output('table4', 'data'),
    Input('save-update-fav', 'n_clicks'),
    Input('delete-fav', 'n_clicks'),
    State('demo-dropdown', 'value'),
    State('textarea-example2', 'value'),
)
def update_output2(btn1, btn2, dropdown, note):
    mongoclient = mongodb.MyMongoClient()
    changed_id = [p['prop_id'] for p in callback_context.triggered][0]
    if 'save-update' in changed_id:
        mongoclient.insert_fav(dropdown, note)
    else:
        mongoclient.delete_fav(dropdown)
    return mongoclient.get_favs()


if __name__ == '__main__':
    app.run_server(debug=True)
