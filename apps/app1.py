
import dash_core_components as dcc
import dash_html_components as html
import dash_table

from dash.dependencies import Input, Output

import pandas as pd
import geopandas as gpd
import json
import os

import plotly.graph_objects as go
import plotly.express as px
import plotly.io as pio


from data.iso_country_codes import CC
from urllib.request import urlretrieve

import math
import random

import pickle

import networkx as nx

from app import app

#Load data
keywords = pd.read_csv('data/CoronaMadrid_keywords_ordered_currentflowbetweenness_7_nonfiltered.csv')
kw_params = ['freq','cfbetweenness','eigenvalue']
inform_covid = pd.read_csv('data/inform-covid-analysis-v01_page3-unix.csv', sep=';')

data = [dict(
    type='choropleth',
    autocolorscale = True,
    locations = inform_covid['Country'],
    z = inform_covid['INFORM COVID-19 RISK'].apply(lambda x: float(x.replace(',','.'))),
    locationmode = 'country names',
    marker = dict(
        line = dict (
            color = 'rgb(255,255,255)',
            width = 2
        ) ),
    colorbar = dict(
        title = "COVID-19 RISK",
        thickness=10),
)]

layout = dict(
        title = '',
        height = 350,
        geo = dict(
            scope='europe',
            showlakes = True,
            lakecolor = 'rgb(255, 255, 255)'
        ),
        hovermode='closest',
        margin=dict(r=0, l=0, t=0, b=0)
)
    
fig_eu = go.FigureWidget(data=data, layout=layout)


#Preload graph
with open('data/PostsCorMadNet7_viz.cnf', 'rb') as f:
    Gu2 = pickle.load(f)
N = Gu2.number_of_nodes()
V = Gu2.number_of_edges()

labels=[]
for node in Gu2.nodes.data():
    #Generamos la etiqueta
    label = node[0]+' #freq:'+str(node[1]['freq']/20)
    #Añadir al array
    labels.append(label)

pos=nx.spring_layout(Gu2)

Xv=[pos[k][0] for k in Gu2.nodes()]
Yv=[pos[k][1] for k in Gu2.nodes()]
Xed,Yed=[],[]
for edge in Gu2.edges():
    Xed+=[pos[edge[0]][0],pos[edge[1]][0], None]
    Yed+=[pos[edge[0]][1],pos[edge[1]][1], None]

freqs = []
for freq in Gu2.nodes.data('freq'):
    freqs.append(freq[1]/20) #Necesario normalizar de alguna forma

#Available colors
colors = [
    '#1f77b4',  # muted blue
    '#ff7f0e',  # safety orange
    '#2ca02c',  # cooked asparagus green
    '#d62728',  # brick red
    '#9467bd',  # muted purple
    '#8c564b',  # chestnut brown
    '#e377c2',  # raspberry yogurt pink
    '#7f7f7f',  # middle gray
    '#bcbd22',  # curry yellow-green
    '#17becf'   # blue-teal
]

#Plotly style
pio.templates.default = 'plotly_white'

#LAYOUT
layout = html.Div(className = '', children = [
    html.Div(className = 'box', children = [
        html.Div(className = 'columns', children = [
            html.Div(id = 'selected-country', className = 'column is-one-third'),
            html.Div(className = 'column is-one-third', children = [
                dcc.Graph(
                    id = 'graph-eu',
                    figure = fig_eu,
                    hoverData={'points': [{'location': 'Select a country on the map'}]}
                )
            ]),
            html.A(className = 'column is-one-third', children = [
                    html.Img(id = 'logo', src='/assets/logo.png'),
                ], 
                href='https://readymag.com/u1187351608/1830554/', 
                target='_blank'
            )
            
        ]),
        html.Div(className = 'column is-narrow', children = [
            html.H1('Twitter posts analysis',className = 'title is-2'),
        ]),
        html.Div(className = 'columns', children = [
            html.Div(className = 'column', children = [
                html.Div(className = 'columns', children = [
                    html.Div(className = 'column', children = [
                        html.H1('Posts network graph',className = 'title is-5'),
                        html.Div(id='posts-net-graph', className='box')
                    ])
                ])
            ]),
            html.Div(className = 'column is-one-third', children = [
                html.Div(className = 'columns', children = [
                    html.Div(className = 'column is-narrow', children = [
                        html.H1('Hot topics',className = 'title is-5')
                    ]),
                    html.Div(className = 'column is-narrow', children = [
                        html.Label(
                            [
                                "Order parameter",
                                dcc.Dropdown(
                                    id="param-selector-1",
                                    options=[{"label": i, "value": i} for i in kw_params],
                                    placeholder='Select hot topics order param',
                                    value=kw_params[1],
                                    searchable=True,
                                    multi=False,
                                    style=dict(
                                        width = 300
                                    )
                                )
                            ]
                        )
                    ]),
                    html.Div(className = 'column is-narrow', children = [
                        html.Label(
                            [
                                "Axis type",
                                dcc.Dropdown(
                                    id="axis-type-1",
                                    options=[{"label": i, "value": i} for i in ['linear','log']],
                                    placeholder='Select axis type',
                                    value='log',
                                    searchable=True,
                                    multi=False
                                )
                            ]
                        )
                    ])
                ]),
                html.Div(id='hot-topics', className='box')
            ])
        ]),
        html.Div(className = 'column is-narrow', children = [
            html.H1('Twitter users analysis',className = 'title is-2'),
        ]),
        html.Div(className = 'columns', children = [
            html.Div(className = 'column', children = [
                html.Div(className = 'columns', children = [
                    html.Div(className = 'column', children = [
                        html.H1('Users network graph',className = 'title is-5'),
                        html.Div(id='users-net-graph', className='box')
                    ])
                ])
            ]),
            html.Div(className = 'column is-one-third', children = [
                html.Div(className = 'columns', children = [
                    html.Div(className = 'column is-narrow', children = [
                        html.H1('Relevant users',className = 'title is-5')
                    ]),
                    html.Div(className = 'column is-narrow', children = [
                        html.Label(
                            [
                                "Order parameter",
                                dcc.Dropdown(
                                    id="param-selector-2",
                                    options=[{"label": i, "value": i} for i in kw_params],
                                    placeholder='Select relevant users order param',
                                    value=kw_params[1],
                                    searchable=True,
                                    multi=False,
                                    style=dict(
                                        width = 300
                                    )
                                )
                            ]
                        )
                    ]),
                    html.Div(className = 'column is-narrow', children = [
                        html.Label(
                            [
                                "Axis type",
                                dcc.Dropdown(
                                    id="axis-type-2",
                                    options=[{"label": i, "value": i} for i in ['linear','log']],
                                    placeholder='Select axis type',
                                    value='log',
                                    searchable=True,
                                    multi=False
                                )
                            ]
                        )
                    ])
                ]),
                html.Div(id='relevant-users', className='box')
            ])
        ])

    ])
])

# FUNCTIONS


# CALLBACKS

# CALLBACK 0 - Country selector
@app.callback(Output(component_id = 'selected-country',component_property = 'children'),
              [Input('graph-eu', 'hoverData')])
def gen_selected_country(hoverData) :

    try :
        selected_country = hoverData['points'][0]['location']
        covid_risk = hoverData['points'][0]['z']
        return [
            html.H1(selected_country,className='title is-1'),
            html.H1('COVID-19 RISK : {}'.format(covid_risk),className='title is-2'),
            html.H1('',className='title is-2'),
            html.H1('Data analysis for selected country below...',className='title is-3'),
        ]
    except :
        return [
            html.H1('No country selected',className='title is-1')
        ]
    

# CALLBACK 1 - Posts Network Graph Generation
@app.callback(Output(component_id = 'posts-net-graph',component_property = 'children'),
              [Input(component_id = 'param-selector-1',component_property = 'value'),
              Input(component_id = 'axis-type-1',component_property = 'value')])
def gen_posts_net_graph(selected_param,axis_type) :
    trace3=go.Scatter(x=Xed,
        y=Yed,
        mode='lines',
        line=dict(
            color=colors[2],
            width=1
        ),
        opacity=0.5,
        hoverinfo='none'
    )
    trace4=go.Scatter(x=Xv,
        y=Yv,
        mode='markers',
        name='net',
        marker=dict(
            symbol='circle-dot',
            size=freqs,
            color=colors[0],
            line=dict(
                color='black',
                width=0.5
            ),
            opacity=0.9
        ),
        text=labels,
        hoverinfo='text'
    )
    layout2d = go.Layout(
        title="",
        height=500,
        showlegend=False,
        margin=dict(r=0, l=0, t=0, b=0),
        xaxis = {
            'showgrid':False,
            'visible':False
        },
        yaxis = {
            'showgrid':False,
            'showline':False,
            'zeroline':False,
            'autorange':'reversed',
            'visible':False
        }
    )


    data1=[trace3, trace4]
    fig1=go.Figure(data=data1, layout=layout2d)

    return [
        dcc.Graph(
            id = 'graph-1',
            figure = fig1
        )
    ]


# CALLBACK 2 - Hot topics barchart
@app.callback(Output(component_id = 'hot-topics',component_property = 'children'),
              [Input(component_id = 'param-selector-1',component_property = 'value'),
              Input(component_id = 'axis-type-1',component_property = 'value')])
def gen_hot_topics(selected_param,axis_type) :

    #Sort values
    kws_df = keywords.sort_values(selected_param,ascending=False).iloc[0:15]

    unique_kws = kws_df.word.unique().tolist()

    fig = go.Figure()
    for unique_kw in unique_kws :
        kw_df = kws_df[kws_df.word == unique_kw]
        fig.add_trace(go.Bar(x=[unique_kw],
            y=[kw_df[selected_param].iloc[0]],
            name=unique_kw
        ))



    fig.update_layout(
        height=450,
        margin=dict(r=0, l=0, t=0, b=0),
        yaxis=dict(
            title=selected_param,
            type=axis_type
        )
    )

    return [
        dcc.Graph(
            id = 'graph-2',
            figure = fig
        )
    ]


# CALLBACK 3 - Users Network Graph Generation
@app.callback(Output(component_id = 'users-net-graph',component_property = 'children'),
              [Input(component_id = 'param-selector-2',component_property = 'value'),
              Input(component_id = 'axis-type-2',component_property = 'value')])
def gen_users_net_graph(selected_param,axis_type) :
    trace3=go.Scatter(x=Xed,
        y=Yed,
        mode='lines',
        line=dict(
            color=colors[2],
            width=1
        ),
        opacity=0.5,
        hoverinfo='none'
    )
    trace4=go.Scatter(x=Xv,
        y=Yv,
        mode='markers',
        name='net',
        marker=dict(
            symbol='circle-dot',
            size=freqs,
            color=colors[0],
            line=dict(
                color='black',
                width=0.5
            ),
            opacity=0.9
        ),
        text=labels,
        hoverinfo='text'
    )
    layout2d = go.Layout(
        title="",
        height=500,
        showlegend=False,
        margin=dict(r=0, l=0, t=0, b=0),
        xaxis = {
            'showgrid':False,
            'visible':False
        },
        yaxis = {
            'showgrid':False,
            'showline':False,
            'zeroline':False,
            'autorange':'reversed',
            'visible':False
        }
    )


    data1=[trace3, trace4]
    fig1=go.Figure(data=data1, layout=layout2d)

    return [
        dcc.Graph(
            id = 'graph-3',
            figure = fig1
        )
    ]


# CALLBACK 4 - Most relevant users
@app.callback(Output(component_id = 'relevant-users',component_property = 'children'),
              [Input(component_id = 'param-selector-2',component_property = 'value'),
              Input(component_id = 'axis-type-2',component_property = 'value')])
def gen_relevant_users(selected_param,axis_type) :

    #Sort values
    kws_df = keywords.sort_values(selected_param,ascending=False).iloc[0:15]

    unique_kws = kws_df.word.unique().tolist()

    fig = go.Figure()
    for unique_kw in unique_kws :
        kw_df = kws_df[kws_df.word == unique_kw]
        fig.add_trace(go.Bar(x=[unique_kw],
            y=[kw_df[selected_param].iloc[0]],
            name=unique_kw
        ))



    fig.update_layout(
        height=450,
        margin=dict(r=0, l=0, t=0, b=0),
        yaxis=dict(
            title=selected_param,
            type=axis_type
        )
    )

    return [
        dcc.Graph(
            id = 'graph-4',
            figure = fig
        )
    ]
