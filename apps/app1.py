
import dash_core_components as dcc
import dash_html_components as html
import dash_table

from dash.dependencies import Input, Output

import pandas as pd
import json

import plotly.graph_objects as go
import plotly.io as pio

import math

import networkx as nx

from app import app

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
            html.Div(className = 'column is-narrow', children = [
                html.H1('Random generated graph visualization',className = 'title is-4'),
            ]),
            html.Div(className = 'column is-narrow', children = [
                html.Button('New graph',className='button', id='update-button')
            ])
        ]),
        html.Div(id='random-graph', className='box')
    ])
])

# CALLBACKS

# CALLBACK 1 - Random Graph Generation
@app.callback(Output(component_id = 'random-graph',component_property = 'children'),
              [Input(component_id = 'update-button',component_property = 'n_clicks')])
def gen_random_graph(n_clicks) :
    #Randomw graph gen
    G = nx.random_geometric_graph(200, 0.125)

    #Edges creation
    edge_x = []
    edge_y = []
    for edge in G.edges():
        x0, y0 = G.nodes[edge[0]]['pos']
        x1, y1 = G.nodes[edge[1]]['pos']
        edge_x.append(x0)
        edge_x.append(x1)
        edge_x.append(None)
        edge_y.append(y0)
        edge_y.append(y1)
        edge_y.append(None)

    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=0.5, color='#888'),
        hoverinfo='none',
        mode='lines')

    node_x = []
    node_y = []
    for node in G.nodes():
        x, y = G.nodes[node]['pos']
        node_x.append(x)
        node_y.append(y)

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers',
        hoverinfo='text',
        marker=dict(
            showscale=True,
            # colorscale options
            #'Greys' | 'YlGnBu' | 'Greens' | 'YlOrRd' | 'Bluered' | 'RdBu' |
            #'Reds' | 'Blues' | 'Picnic' | 'Rainbow' | 'Portland' | 'Jet' |
            #'Hot' | 'Blackbody' | 'Earth' | 'Electric' | 'Viridis' |
            colorscale='YlGnBu',
            reversescale=True,
            color=[],
            size=10,
            colorbar=dict(
                thickness=15,
                title='Node Connections',
                xanchor='left',
                titleside='right'
            ),
        line_width=2
    ))

    #Color node points
    node_adjacencies = []
    node_text = []
    for node, adjacencies in enumerate(G.adjacency()):
        node_adjacencies.append(len(adjacencies[1]))
        node_text.append('# of connections: '+str(len(adjacencies[1])))

    node_trace.marker.color = node_adjacencies
    node_trace.text = node_text
    
    #Create nodes graph
    fig = go.Figure(
            data=[edge_trace, node_trace],
            layout=go.Layout(
                title='<b>Network graph',
                height=600,
                titlefont_size=16,
                showlegend=False,
                hovermode='closest',
                margin=dict(b=20,l=5,r=5,t=40),
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
    )


    return [
        dcc.Graph(
            id = 'graph',
            figure = fig
        )
    ]