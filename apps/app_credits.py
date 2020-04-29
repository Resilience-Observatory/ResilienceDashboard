import dash_core_components as dcc
import dash_html_components as html

from app import app

#MEMBERS INFO
members = [
    'David Pastor-Escuredo',
    'Pedro J. Zufiria Zatarain',
    'Carlota Tarazona Lizarraga',
    'Roger Quispe Rondan',
    'Juan Sebastian Ochoa Zambrano',
    'Carlos García-Mauriño',
    'Alejandro Jarabo Peñas'
]

members_info = {
    members[0]: {
        'desc' : 'Ph.D. from Technical University Madrid. Founder and CEO of the LifeD Lab and the platform Humcoin.',
        'linkedin': 'https://www.linkedin.com/in/david-pastor-escuredo-59543320/'
    },
    members[1]: {
        'desc' : 'Professor at Universidad Politécnica de Madrid.',
        'linkedin': 'https://www.linkedin.com/in/pedro-j-zufiria-31488774/'
    },
    members[2]: {
        'desc' : 'Telecommunications engineer with focus on Data for Social Good.',
        'linkedin': 'https://www.linkedin.com/in/carlota-tarazona-lizarraga-7638b514a/?originalSubdomain=es'
    },
    members[3]: {
        'desc' : 'Software Engineer.',
        'linkedin': 'https://www.linkedin.com/in/roger-quispe-rondan-a86b7b110/'
    },
    members[4]: {
        'desc' : 'Second-year Ph.D. student in Computing Sciences for SmartCities at the Technical School of Engineers and Computer Systems of the Universidad Politécnica de Madrid.',
        'linkedin': 'https://www.linkedin.com/in/juan-sebastian-ochoa-zambrano-485a0013b/'
    },
    members[5]: {
        'desc' : 'Student of Telecommunications Engineering at UPM. GNU/Linux and free (libre) open source software enthusiast.',
        'linkedin': 'https://www.linkedin.com/in/carlos-g-m/'
    },
    members[6]: {
        'desc' : 'Student of Telecommunications Engineering at UPM.',
        'linkedin': 'https://www.linkedin.com/in/alejandro-jarabo-pe%C3%B1as-aa990a166/'
    }
}

members_boxes = [
    html.Div(className = 'column is-one-third', children = [
        html.Div(className='box',children = [
            html.Div(className = 'columns', children = [
                html.Div(className = 'column', children = [
                    html.H1(member,className = 'subtitle is-4'),
                ]), 
                html.Div(className = 'column is-narrow', children = [
                    html.A('LinkedIn',href=members_info[member]['linkedin'],target='_blank')
                ]) 
            ]),
            html.H1(members_info[member]['desc'],className = 'subtitle is-6')
        ])
    ]) for member in members
]

#LAYOUT
layout = html.Div(className = '', children = [
    html.Div(className = 'box', children = [
        html.H1('Description of the project',className = 'title is-4'),
        html.Div(className = 'box', children = [
            html.H1('Resilience in communities and cities affected by the COVID-19 can be effectively built upon AI-powered Collective Intelligence. Understanding social narratives is key to design actions and policies for accelerating a human centered recovery. We propose a dashboard to measure the social impact of the COVID-19, the social response and the changes produced based on analytics of social media and surveys making use of networks, machine learning, natural language processing and dynamics systems tools integrated with epidemiological data sources. This dashboard will help make a real-time monitoring of the pandemic evolution, interconnect stakeholders and design projects. This system will be useful both for short-term decision making and long-term policies definition, and will definitely help Europe to recover from the current pandemics, and to be better prepared for future crises or pandemics.',className = 'subtitle is-6'),
        ]),
        html.H1('Members',className = 'title is-4'),
        html.Div(className = 'columns', children = members_boxes[0:3]),
        html.Div(className = 'columns', children = members_boxes[3:6]),
        html.Div(className = 'columns', children = members_boxes[6:])
    ])
])