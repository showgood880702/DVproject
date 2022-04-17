import dash
import plotly
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
from plotly.subplots import make_subplots
import numpy as np
import pandas as pd
import plotly.graph_objs as go
import os
import dash_daq as daq
import plotly.express as px
import random

# ==========================================Data==========================================#

path = 'https://raw.githubusercontent.com/nalpalhao/DV_Practival/master/datasets/'

df_salary = pd.read_csv(os.getcwd() + '/df_salary.csv')
df_company = pd.read_csv(os.getcwd() + '/df_company.csv')
# ==========================================PreProcess==========================================#

mean_salary = df_salary.groupby(['State'])[['totalyearlycompensation', 'costIndex', 'averageIncome']].mean()
max_salary = df_salary.groupby(['State'])['totalyearlycompensation'].max()
min_salary = df_salary.groupby(['State'])['totalyearlycompensation'].min()
median_salary = df_salary.groupby(['State'])['totalyearlycompensation'].median()
df_bar = pd.concat([mean_salary, max_salary, min_salary, median_salary], axis=1).reset_index()
df_bar.columns = ['State', 'Average', 'costIndex', 'averageIncome', 'Max', 'Min', 'Median']

df_company = df_company.set_index('company')
b = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 100]
l = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
df_salary["Years of Experience"] = pd.cut(df_salary['yearsofexperience'], bins=b, labels=l, include_lowest=True)

statename = df_salary[['State', 'StateName']].drop_duplicates().set_index('State')

df_salary["quartils"] = pd.qcut(df_salary.totalyearlycompensation, 4)


# Preprocess Function for inequliaty chart

def preprocess(col):
    gender_dict = dict()
    iterable = df_salary[col].value_counts()
    for quartil in df_salary["quartils"].drop_duplicates():
        to_add = list()
        for idx, point in enumerate(iterable.index):
            add = df_salary[(df_salary["quartils"] == quartil) & (df_salary[col] == point)].shape[0] / iterable[
                idx] * 100
            to_add.append(add)
        gender_dict[quartil] = to_add
    df_ = pd.DataFrame(gender_dict.values(), columns=iterable.index)
    return df_


gender = preprocess("gender")
race = preprocess("Race")
education_df = preprocess("Education")
experience_df = preprocess("ExperienceLevel")

# ==========================================Interactive Components==========================================#
states = sorted(df_salary.State.dropna().unique().tolist())
sectors = ['Max', 'Min', 'Average', 'Median']
years = list(range(2017, 2021))
companys = sorted(df_salary.company.dropna().unique().tolist())

state_options = [dict(label=state, value=state) for state in states]
sector_options = [dict(label=sector, value=sector) for sector in sectors]
company_options = [dict(label=company, value=company) for company in companys]

# ===================Mean Max Min Median===================#
dropdown_sector = dcc.Dropdown(
    id='sector_option',
    options=sector_options,
    value=sectors[-1],
    multi=False
)

# ===================States===================#
dropdown_state = dcc.Dropdown(
    id='state_option',
    options=state_options,
    value=states[0],
    multi=True
)

# ===================Year Slider===================#
slider_year = dcc.Slider(
    id='year_slider',
    min=2017,
    max=2020,
    marks={str(i): '{}'.format(str(i)) for i in years},
    value=2020,
    step=1
)

# ===================Show costIndex===================#
radio_costIndex = daq.ToggleSwitch(
    id='costIndex',
    value=False,
    label='Show / Hide',
    labelPosition='bottom'
)

# ===================Show avgIncome===================#
radio_avgIncome = daq.ToggleSwitch(
    id='avgIncome',
    value=False,
    label='Show / Hide',
    labelPosition='bottom'
)

# ===================Company===================#
dropdown_company = dcc.Dropdown(
    id='company_option',
    options=company_options,
    value=['Amazon', 'eBay'],
    multi=True
)

# ===================Pie===================#
dropdown_pie = dcc.Dropdown(
    id='pie_option',
    options=["Gender", "Race", "Education", "Level of Experience"],
    value="Gender",
    multi=False
)

# ===================Box Vio===================#

radio_box = daq.ToggleSwitch(
    id='box-vio-switch',
    value=False,
    label='Violinplot / Boxplot',
    labelPosition='bottom'
)

# ===================Hist===================#
radio_note = daq.BooleanSwitch(
    id='my-toggle-switch',
    on=True,
    label="Show Annotation",
    labelPosition='bottom'
),
##################################################APP###################################################################

app = dash.Dash(__name__)

server = app.server

app.layout = html.Div(
    [
        html.Div(
            [
                html.P('Job Situation of Software Engineers in the US',
                       style={"font-weight": "bold",
                              "font-size": 24,
                              "text-align": "center",
                              "margin-bottom": "10px"}
                       ),
                html.P(
                    "Analysis of a salary dataset scraped from Glassdoor covering the years 2017-2020",
                    style={"margin-top": "0px",
                           "font-size": 20,
                           "text-align": "center", }
                ),
            ],
            id='headtitle',
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.Div(
                            [
                                html.P(
                                    'Are you looking for a job in Software Engineering? In this graph you can see the '
                                    'df_salary split up by US-State. You have the option to select the maximum, '
                                    'minimum, average or  median salary and put it into comparison to the Cost of '
                                    'Living Index or State Average Income. Feel free to play with the different '
                                    'options!',
                                    style={"text-align": "justify",
                                           'margin-left': '20px',
                                           'margin-right': '20px',
                                           "font-size": 14},
                                ),
                                html.Div(
                                    [
                                        html.Div(
                                            [
                                                html.Label(
                                                    'Salary',
                                                    style={"font-weight": "bold",
                                                           "font-size": 14}
                                                ),
                                                html.Br(),
                                                dropdown_sector,
                                            ],
                                            id='dropdown',
                                            style={"text-align": "justify",
                                                   'margin': '5px',
                                                   'width': '30%'},
                                            # className='box'
                                        ),
                                        html.Div(
                                            [
                                                html.Div(
                                                    [
                                                        html.Label('Cost of Living Index',
                                                                   style={"font-weight": "bold",
                                                                          "font-size": 14}
                                                                   ),
                                                        radio_costIndex
                                                    ],
                                                    id='cost',
                                                    style={"text-align": "center",
                                                           'width': '50%'},
                                                ),

                                                html.Div(
                                                    [
                                                        html.Label('State Average Income',
                                                                   style={"font-weight": "bold",
                                                                          "font-size": 14}
                                                                   ),
                                                        radio_avgIncome
                                                    ],
                                                    id='income',
                                                    style={"text-align": "center",
                                                           'width': '50%'},
                                                ),
                                            ],
                                            id='choose',
                                            style={'display': 'flex',
                                                   'margin': '5px',
                                                   'width': '70%'},
                                            # className='box'
                                        )
                                    ], id='drop and choose',
                                    style={'display': 'flex',
                                           'margin-left': '10px',
                                           'margin-right': '10px'},
                                    # className='box'
                                ),
                            ],
                            id='subtitle1', className='box'),
                        html.Div(
                            [
                                dcc.Graph(id='bar_graph'),
                            ],
                            id='barplot',
                            # style={'height': '10%'},
                            className='box'
                        ),
                    ],
                    id='1st col',
                    style={'width': '50%'}
                ),

                html.Div(
                    [
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.P(
                                            'On the map you can see the salary by state in the US. Again you can use '
                                            'the filter options on the left to select you desired configuration. '
                                            'Additionally you can select the range of years on the slider below.',
                                            style={"text-align": "justify",
                                                   'margin-left': '20px',
                                                   'margin-right': '20px',
                                                   "font-size": 14}
                                        ),
                                    ], id='subtitle2'
                                ),
                                html.Div(
                                    [
                                        html.P('Year',
                                               style={"font-weight": "bold",
                                                      "text-align": "center"}),
                                        slider_year
                                    ],
                                    id='year slider',
                                    style={"margin-left": "10px",
                                           "margin-right": "10px"},
                                ), ]
                        ),

                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.H3(
                                            "Maximum",
                                            style={"text-align": "center",
                                                   "font-weight": "bold"}
                                        ),
                                        html.P(
                                            id="max_state",
                                            style={"text-align": "center"}
                                        ),
                                        html.P(
                                            id="max_value",
                                            style={"text-align": "center"}
                                        ),
                                    ],
                                    className="box",
                                    style={"text-align": "center",
                                           'border-radius': '10px',
                                           'background-color': '#FAEBD7',
                                           'margin': '10px',
                                           'padding': '10px',
                                           'box-shadow': '2px 2px 2px lightgrey',
                                           'width': '50%'},
                                    id="Highest",
                                ),
                                html.Div(
                                    [
                                        html.H3(
                                            "Minimum",
                                            style={"text-align": "center",
                                                   "font-weight": "bold"}
                                        ),
                                        html.P(
                                            id="min_state",
                                            style={"text-align": "center"}
                                        ),
                                        html.P(
                                            id="min_value",
                                            style={"text-align": "center"}
                                        ),
                                    ],
                                    style={"text-align": "center",
                                           'border-radius': '10px',
                                           'background-color': '#FAEBD7',
                                           'margin': '10px',
                                           'padding': '10px',
                                           'box-shadow': '2px 2px 2px lightgrey',
                                           'width': '50%'},
                                    id="Lowest",
                                ),
                            ],
                            id="info-container",
                            style={"display": "flex"},
                            # className="box"
                        ),

                        html.Div(
                            [
                                dcc.Graph(id='map_figure'),
                            ],
                            id='Mapplot',
                            # style={'width': '60%'},
                            # className='box'
                        ),
                    ],
                    id='2nd col',
                    style={'width': '50%'},
                    className='box'
                ), ],
            id='2nd row',
            style={'display': 'flex'},
            # className='box'
        ),
        html.Div(
            [
                html.P('Salary based on work experience by US region',
                       style={"font-weight": "bold",
                              "font-size": 24,
                              "text-align": "center",
                              'margin': '10px'}
                       ),
                html.Div(
                    [
                        html.Div(
                            [
                                dcc.Graph(id='line_plot1')
                            ], style={'width': '50%'}
                        ),
                        html.Div(
                            [
                                dcc.Graph(id='line_plot2')
                            ], style={'width': '50%'}
                        ),
                    ],
                    id='line plots',
                    style={'display': 'flex',
                           'margin-left': '20px'}
                )
            ],
            id='3rd row',
            # style={'display': 'flex'},
            className='box'
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.P('Employee\'s satisfaction in different companies',
                               style={"font-weight": "bold",
                                      "font-size": 24,
                                      "text-align": "center",
                                      "margin-bottom": "10px"}
                               ),
                        html.Div(
                            [
                                html.P('Select companies',
                                       style={"margin-bottom": "10px",
                                              "margin-left": "10px"}),
                                dropdown_company
                            ],
                            id='select company',
                            style={"margin-right": "20px",
                                   "margin-left": "20px"}
                        ),
                        html.Div(
                            [
                                html.Div(
                                    [
                                        dcc.Graph(id='radar_graph1')
                                    ],
                                    id='radarplot1',
                                    style={'width': '50%'}
                                    # className='box'
                                ),
                                html.Div(
                                    [
                                        dcc.Graph(id='radar_graph2')
                                    ],
                                    id='radarplot2',
                                    style={'width': '50%'}
                                    # className='box'
                                )
                            ],
                            id='radartplot',
                            style={'display': 'flex',
                                   "margin-right": "20px",
                                   # "margin-left": "20px"
                                   }
                        )

                    ],
                    id='3rd row 1st row',
                    # style={'width': '80%'},
                    # className='box'
                ),
                html.Div(
                    [
                        html.P('Information about the selected Top Rated Company',
                               style={"font-weight": "bold",
                                      "font-size": 24,
                                      "text-align": "center",
                                      "margin-bottom": "10px"}
                               ),
                        html.Br(),
                        html.Div(
                            [
                                html.Div(
                                    [
                                        dcc.Graph(id='indicator')
                                    ],
                                    id='indicator plot',
                                    style={'width': '25%'}
                                ),
                                html.Div(
                                    [
                                        html.Div(
                                            [
                                                html.Div(
                                                    [
                                                        html.H3('Top Rated Company in Chosen'),
                                                        html.P(id='Chosen companies'),
                                                    ],
                                                    id='company title',
                                                    style={'width': '33%'},
                                                    className='box_comment'
                                                ),
                                                html.Div(
                                                    [
                                                        html.H3('Interview Duration'),
                                                        html.P(id='Interview Duration'),
                                                    ], style={'width': '33%'},
                                                    className='box_comment'
                                                ),
                                                html.Div(
                                                    [
                                                        html.H3('Interview Difficulty'),
                                                        html.P(id='Interview Difficulty'),
                                                    ], style={'width': '33%'},
                                                    className='box_comment'
                                                )
                                            ],
                                            id='431row',
                                            style={'display': 'flex'},
                                        ),
                                        html.Div(
                                            [

                                                html.Div(
                                                    [
                                                        html.H3('Company Size'),
                                                        html.P(id='Company Size'),
                                                    ], style={'width': '33%'},
                                                    className='box_comment'
                                                ),
                                                html.Div(
                                                    [
                                                        html.H3('Industry'),
                                                        html.P(id='Industry'),
                                                    ], style={'width': '33%'},
                                                    className='box_comment'
                                                ),
                                                html.Div(
                                                    [
                                                        html.H3('Revenue Size'),
                                                        html.P(id='Revenue Size'),
                                                    ], style={'width': '33%'},
                                                    className='box_comment'
                                                )
                                            ],
                                            id='432row',
                                            style={'display': 'flex'},
                                        )
                                    ],
                                    id='box comments',
                                    style={'width': '75%'},
                                ),
                            ], id='company indicator',
                            style={'display': 'flex',
                                   'margin-left': '50px',
                                   'margin-right': '50px'},
                        )
                    ],
                    id='3rd row 2nd row',
                    # style={'display': 'flex'}
                ),
                dcc.Graph(id='Corr_plot',
                          style={"margin-right": "40px",
                                 "margin-left": "40px"})
            ], id='4th row',
            # style={'display': 'flex'},
            className='box'
        ),
        html.Div(
            [
                html.P('Salary based on sociodemographic factors',
                       style={"font-weight": "bold",
                              "font-size": 24,
                              "text-align": "center",
                              "margin-bottom": "10px",
                              }
                       ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.Div(
                                    [
                                        dropdown_pie,
                                        dcc.Graph(id='Graph_Pie1'),
                                        html.Div(
                                            [
                                                html.Div(
                                                    radio_note,
                                                    id='note switch',
                                                    style={'width': '50%'}
                                                ),
                                                html.Div(
                                                    [
                                                        radio_box
                                                    ],
                                                    id='box switch',
                                                    style={'width': '50%'}
                                                ),
                                            ], id='switches',
                                            style={'display': 'flex'}
                                        ),
                                    ],
                                    style={'width': '30%',
                                           'margin': '20px',
                                           "margin-left": "40px"
                                           },
                                    id='pie charts'
                                ),
                                html.Div(
                                    [
                                        dcc.Graph(id='Graph_hist1',
                                                  style={"margin-right": "40px",
                                                         "margin-left": "40px"}
                                                  )
                                    ],
                                    style={'width': '70%'},
                                    id='boxplot'
                                ),
                            ],
                            id='5th row 1st row',
                            style={'height': '40%',
                                   'display': 'flex'}
                        ),
                        html.Div(
                            [dcc.Graph(id='Gender_Graph')],
                            id='noteplot',
                            style={'height': '60%'}, ),

                    ],
                    id='5th row fig',
                    style={'height': '50%'}
                )
            ],
            id='5th row',
            # style={'display': 'flex'},
            className='box'
        ),
        html.Div(
            [
                html.P('Gender-Salary Analysis',
                       style={"font-weight": "bold",
                              "font-size": 24,
                              "text-align": "center",
                              "margin-bottom": "10px",
                              }
                       ),
                html.Br(),

                html.Div([
                    dcc.Tabs(id='tabs-example-1', value='Industry', children=[
                        dcc.Tab(label='Industry', value='Industry'),
                        dcc.Tab(label='State', value='State'),
                        dcc.Tab(label='Company Size', value='Company Size')
                    ]
                             ),
                    html.Div(id='tabs-example-content-1')
                ],
                    style={"margin-right": "40px",
                           "margin-left": "40px"}
                ),
            ], id='6th row',
            className='box'
        ),
        html.Div(
            [
                html.P('Authors',
                       style={"font-weight": "bold",
                              "font-size": 24,
                              "text-align": "center",
                              "margin-bottom": "10px",
                              }
                       ),
                html.Div(
                    [
                        html.P('Renan Stoffel (m20210594)',
                               style={'width': '25%',
                                      "text-align": "center",
                                      "font-size": 14}, ),
                        html.P('Marcel Geller (m20210606)',
                               style={'width': '25%',
                                      "text-align": "center",
                                      "font-size": 14}, ),
                        html.P('Robin Schmidt (m20210602)',
                               style={'width': '25%',
                                      "text-align": "center",
                                      "font-size": 14}, ),
                        html.P('Qi Shi (m20210981)',
                               style={'width': '25%',
                                      "text-align": "center",
                                      "font-size": 14}, ),
                    ],
                    style={'display': 'flex'},
                    className='box'
                ),
                html.Div(
                    [
                        html.P('If you want to make some further analysis, feel free to download the datasets here:',
                               style={'font-size': 14}),
                        html.Button("Download CSV", id="btn_csv"),
                        dcc.Download(id="download-dataframe-csv1"),
                        dcc.Download(id="download-dataframe-csv2"),
                    ],
                    className='box',
                    style={'margin-top': '0px'}
                )
            ],
        )
    ],
    style={'background-color': '#f3f3f1',
           "display": "flex",
           "flex-direction": "column",
           'padding': '50px'},
)


##################################################Callbacks Plots#####################################################

@app.callback(
    [
        Output("bar_graph", "figure"),
        Output("map_figure", "figure"),
        Output("indicator", "figure"),
        Output("radar_graph1", "figure"),
        Output("radar_graph2", "figure"),
        Output("line_plot1", "figure"),
        Output("line_plot2", "figure"),
        Output('Graph_Pie1', 'figure'),
        Output('Graph_hist1', 'figure'),
        Output('Corr_plot', 'figure')
    ],
    [
        Input("sector_option", "value"),
        Input('costIndex', 'value'),
        Input("avgIncome", "value"),
        Input("company_option", "value"),
        Input('year_slider', 'value'),
        Input('pie_option', 'value'),
        Input('box-vio-switch', 'value')
    ]
)
def plots(sector, cost, income, cpys, year, value1, switch):

    ############################################Bar Plot##########################################################
    global fig_pie
    if not cost:

        bar_figure = make_subplots(rows=1, cols=2, horizontal_spacing=.05)
        bar_figure.add_trace(go.Bar(y=df_bar.sort_values([sector]).State,
                                    x=df_bar.sort_values([sector])['costIndex'],
                                    name='costIndex',
                                    orientation='h',
                                    marker=dict(color='#27AE60'),
                                    hovertemplate='State: %{y}<br>' + 'Cost of Living Index: %{x}'
                                    ),
                             row=1, col=1
                             )
        bar_figure.add_trace(go.Bar(y=df_bar.sort_values([sector]).State,
                                    x=df_bar.sort_values([sector])[sector],
                                    name=sector,
                                    orientation='h',
                                    marker=dict(color='#EC7063'),
                                    hovertemplate='State: %{y}<br>' + 'Salary: %{x}'
                                    ),
                             row=1, col=2
                             )
        if not income:
            bar_figure.add_trace(go.Bar(y=df_bar.sort_values([sector]).State,
                                        x=df_bar.sort_values([sector])['averageIncome'],
                                        name='averageIncome',
                                        orientation='h',
                                        marker=dict(color='#3498DB'),
                                        opacity=0.6,
                                        hovertemplate='State: %{y}<br>' + 'State Average Income: %{x}'
                                        ),
                                 row=1, col=2
                                 )
            bar_figure.update_layout(barmode='overlay')
        bar_figure.update_layout(margin={"r": 20, "t": 30, "l": 0, "b": 10},
                                 legend=dict(y=.0, x=.76),
                                 title=dict(text=sector + ' Salary of Software Engineers'),
                                 yaxis=dict(title='Salary'),
                                 showlegend=True,
                                 yaxis_visible=False,
                                 )
        bar_figure.update_xaxes(autorange="reversed", row=1, col=1)
    else:
        bar_figure = go.Figure()
        bar_figure.add_trace(go.Bar(y=df_bar.sort_values([sector]).State,
                                    x=df_bar.sort_values([sector])[sector],
                                    name=sector,
                                    orientation='h',
                                    marker=dict(color='#EC7063'),
                                    hovertemplate='State: %{y}<br>' + 'Salary: %{x}'
                                    ),
                             )
        if not income:
            bar_figure.add_trace(go.Bar(y=df_bar.sort_values([sector]).State,
                                        x=df_bar.sort_values([sector])['averageIncome'],
                                        name='averageIncome',
                                        orientation='h',
                                        marker=dict(color='#3498DB'),
                                        opacity=0.6,
                                        hovertemplate='State: %{y}<br>' + 'State Average Income: %{x}'
                                        ),
                                 )
            bar_figure.update_layout(barmode='overlay')
        bar_figure.update_layout(margin={"r": 20, "t": 30, "l": 0, "b": 10},
                                 legend=dict(y=.0, x=.75),
                                 title=dict(text=sector + ' Salary of Software Engineers'),
                                 yaxis=dict(title='Salary'),
                                 showlegend=True,
                                 )
    bar_figure.update_layout(width=600, height=600)
    #############################################Choropleth Plot######################################################
    df_salary0 = df_salary[df_salary['Year'] == year].copy()
    mean_salary0 = df_salary0.groupby(['State'])['totalyearlycompensation'].mean()
    max_salary0 = df_salary0.groupby(['State'])['totalyearlycompensation'].max()
    min_salary0 = df_salary0.groupby(['State'])['totalyearlycompensation'].min()
    median_salary0 = df_salary0.groupby(['State'])['totalyearlycompensation'].median()
    df_map = pd.concat([mean_salary0, max_salary0, min_salary0, median_salary0], axis=1).reset_index()
    df_map.columns = ['State', 'Average', 'Max', 'Min', 'Median']

    data_choropleth = dict(type='choropleth',
                           locations=df_map.State,
                           locationmode='USA-states',
                           z=df_map[sector],
                           text=df_map.State,
                           colorscale='Reds',
                           hovertemplate='State: %{text} <br>' + sector + ' salary: %{z}',
                           name='',
                           marker_line_color='darkred',
                           )

    layout_choropleth = dict(geo=dict(scope='usa',
                                      showlakes=True,
                                      lakecolor='#FFFFFF'
                                      ),
                             title=dict(text='US ' + sector + ' Salary based on selected range of years', x=0.5,
                                        y=0.95),
                             )

    map_figure = go.Figure(data=data_choropleth, layout=layout_choropleth)
    map_figure.update_layout(margin={"r": 0, "t": 50, "l": 0, "b": 0},
                             # width=700, height=400
                             )

    ############################################Radar Chart######################################################
    categories1 = ['Job Security/Advancement',
                   'Work/Life Balance',
                   'Compensation/Benefits',
                   'Management',
                   'Culture',
                   'Job Security/Advancement']
    categories2 = ['Work Happiness Score', 'Flexibility', 'Compensation', 'Achievement',
                   'Learning', 'Inclusion', 'Appreciation', 'Purpose', 'Energy', 'Trust',
                   'Belonging', 'Support', 'Leadership', 'Work Happiness Score']
    r1_mean = df_salary[categories1].mean().tolist()
    r2_mean = df_salary[categories2].mean().tolist()
    cols = plotly.colors.DEFAULT_PLOTLY_COLORS

    radar_chart1 = go.Figure()
    radar_chart1.add_trace(go.Scatterpolar(r=r1_mean,
                                           theta=categories1,
                                           name='Mean',
                                           showlegend=True,
                                           line=dict(color=cols[0])
                                           ))
    r_range = []
    for n, cpy in enumerate(cpys):
        r_c = df_salary[df_salary['company'] == cpy][categories1].mean().tolist()
        r_range.append(r_c)
        radar_chart1.add_trace(go.Scatterpolar(r=r_c,
                                               theta=categories1,
                                               name=cpy,
                                               showlegend=True,
                                               line=dict(color=cols[n + 1])
                                               ))

    r_range.append(r1_mean)
    r_range = np.array(r_range)
    radar_chart1.update_layout_images(template='plotly',
                                      polar=dict(radialaxis=dict(visible=True)),
                                      )
    radar_chart1.update_polars(radialaxis_range=(r_range.min() * 0.98, r_range.max() * 1.03))

    radar_chart2 = go.Figure()
    radar_chart2.add_trace(go.Scatterpolar(r=r2_mean,
                                           theta=categories2,
                                           name='Mean',
                                           showlegend=True,
                                           line=dict(color=cols[0])
                                           ))
    r_range = []
    for n, cpy in enumerate(cpys):
        r_c = df_salary[df_salary['company'] == cpy][categories2].mean().tolist()
        r_range.append(r_c)
        radar_chart2.add_trace(go.Scatterpolar(r=r_c,
                                               theta=categories2,
                                               name=cpy,
                                               showlegend=True,
                                               line=dict(color=cols[n + 1])
                                               ))
    r_range.append(r2_mean)
    r_range = np.array(r_range)
    radar_chart2.update_layout_images(template='plotly',
                                      polar=dict(radialaxis=dict(visible=True)),
                                      )
    radar_chart2.update_polars(radialaxis_range=(r_range.min() * 0.98, r_range.max() * 1.03))
    # radar_chart.update_layout(width=400, height=200)
    ############################################indicator Chart######################################################
    best_con = df_company.loc[cpys].rating_reviews.idxmax()
    over_rating = df_company.loc[best_con, 'rating_reviews']
    indicator_chart = go.Figure(go.Indicator(mode="gauge+number",
                                             value=over_rating,
                                             title={'text': "Rating",
                                                    'font_size': 20},
                                             domain=dict(x=[0, 1], y=[0, 1])
                                             ))

    indicator_chart.update_traces(value=over_rating,
                                  gauge_bar_color='#FF7F50',
                                  gauge_axis_range=[0, 5],
                                  gauge_axis_showticklabels=True,
                                  gauge_axis_nticks=6,
                                  gauge_axis_tickfont=dict(size=16),
                                  delta={'reference': 4},
                                  selector=dict(type='indicator'),
                                  )
    indicator_chart.update_layout(width=250, height=200,
                                  margin={"r": 25, "t": 10, "l": 25, "b": 0})
    ############################################Line Chart######################################################
    df1 = df_salary.groupby(["ExperienceLevel", "Region"])["totalyearlycompensation"].median().reset_index()

    line_plot1 = px.line(df1[df1["Region"].isin(df1.Region.unique())],
                         x="ExperienceLevel", y="totalyearlycompensation",
                         color="Region",
                         title="Software Engineer df_salary by Experience and State",
                         template='ggplot2')

    df2 = df_salary.groupby(["Years of Experience", "Region"])["totalyearlycompensation"].median().reset_index()

    line_plot2 = px.line(df2[df2["Region"].isin(df2.Region.unique())],
                         x="Years of Experience", y="totalyearlycompensation",
                         color="Region",
                         title="Software Engineer df_salary by Experience and Regions",
                         template='ggplot2')

    line_plot1.update_layout(width=600, height=450)
    line_plot2.update_layout(width=600, height=450)
    ############################################Correlation######################################################
    delt = 0.04
    ratings = [el + random.uniform(-delt, delt) for el in
               df_salary.query("totalyearlycompensation < 2000000").rating_reviews]
    fig_scat = px.scatter(df_salary.query("totalyearlycompensation < 2000000"), x=ratings, y="totalyearlycompensation",
                          opacity=0.25, title="Correlation between Ratings and Salary", trendline="ols",
                          trendline_color_override="red", color="ExperienceLevel", trendline_scope="overall")
    fig_scat.update_xaxes(title="Ratings by Employees")
    fig_scat.update_yaxes(title="Yearly Compensation in USD")
    fig_scat.update_layout(height=600)
    ############################################4th row######################################################
    if value1 == "Gender":

        gender_counts = df_salary.gender.value_counts()
        fig_pie = px.pie(values=gender_counts.values, names=gender_counts.index,
                         title='Gender proportions in the dataset', hole=0.3,
                         color_discrete_sequence=cols)
        fig_pie.update_layout(title=dict(y=0.85), legend=dict(y=.0, x=1),
                              margin={"r": 0, "t": 80, "l": 0, "b": 20},
                              height=300
                              )

        if switch is True:
            fig_hist = go.Figure()
            for n, name in enumerate(df_salary.gender.unique()):
                fig_hist.add_trace(
                    go.Box(values=df_salary[
                        df_salary['gender'] == name].totalyearlycompensation,
                           names=name,
                           marker_color=cols[n - 1]))
        else:
            fig_hist = go.Figure()
            for n, name in enumerate(df_salary.gender.unique()):
                fig_hist.add_trace(
                    go.Violin(y=df_salary[
                        df_salary['gender'] == name].totalyearlycompensation,
                              name=name,
                              marker_color=cols[n - 1]))

    if value1 == "Level of Experience":

        exp_counts = df_salary.ExperienceLevel.value_counts()
        fig_pie = px.pie(values=exp_counts.values, names=exp_counts.index,
                         title='Experience proportions in the dataset', hole=0.3,
                         color_discrete_sequence=cols)
        fig_pie.update_layout(title=dict(y=0.85), legend=dict(y=.0, x=1),
                              margin={"r": 0, "t": 80, "l": 0, "b": 20},
                              height=300
                              )

        if switch is True:
            fig_hist = go.Figure()
            for n, name in enumerate(df_salary.ExperienceLevel.unique()):
                fig_hist.add_trace(
                    go.Box(y=df_salary[df_salary['ExperienceLevel'] == name].totalyearlycompensation,
                           name=name,
                           marker_color=cols[n - 1]))
        else:
            fig_hist = go.Figure()
            for n, name in enumerate(df_salary.ExperienceLevel.unique()):
                fig_hist.add_trace(
                    go.Violin(y=df_salary[df_salary['ExperienceLevel'] == name].totalyearlycompensation,
                              name=name,
                              marker_color=cols[n - 1]))

    elif value1 == "Race":

        race_counts = df_salary.Race.value_counts()
        fig_pie = px.pie(values=race_counts, names=race_counts.index, title='Race proportions in the dataset',
                         hole=0.3,
                         color_discrete_sequence=cols)
        fig_pie.update_layout(title=dict(y=0.85), legend=dict(y=.0, x=1),
                              margin={"r": 0, "t": 80, "l": 0, "b": 20},
                              height=300
                              )

        if switch is True:
            fig_hist = go.Figure()
            for n, name in enumerate(df_salary.Race.unique()):
                fig_hist.add_trace(
                    go.Box(y=df_salary[df_salary['Race'] == name].totalyearlycompensation,
                           name=name,
                           marker_color=cols[n - 1]))
        else:
            fig_hist = go.Figure()
            for n, name in enumerate(df_salary.Race.unique()):
                fig_hist.add_trace(
                    go.Violin(y=df_salary[df_salary['Race'] == name].totalyearlycompensation,
                              name=name,
                              marker_color=cols[n - 1]))

    elif value1 == "Education":
        education_counts = df_salary.Education.value_counts()
        fig_pie = px.pie(values=education_counts, names=education_counts.index,
                         title='Education proportions in the dataset', hole=0.3,
                         color_discrete_sequence=cols)
        fig_pie.update_layout(title=dict(y=0.85), legend=dict(y=.0, x=1),
                              margin={"r": 0, "t": 80, "l": 0, "b": 20},
                              height=300
                              )

        if switch is True:
            fig_hist = go.Figure()
            for n, name in enumerate(df_salary.Education.unique()):
                fig_hist.add_trace(
                    go.Box(y=df_salary[df_salary['Education'] == name].totalyearlycompensation,
                           name=name,
                           marker_color=cols[n - 1]))
        else:
            fig_hist = go.Figure()
            for n, name in enumerate(df_salary.Education.unique()):
                fig_hist.add_trace(
                    go.Violin(y=df_salary[df_salary['Education'] == name].totalyearlycompensation,
                              name=name,
                              marker_color=cols[n - 1]))

    fig_hist.layout.update(showlegend=False)
    fig_hist.update_yaxes(title=f"Boxplot Yearly Compensation in USD")
    if switch is True:
        fig_hist.update_yaxes(title=f"Violin per Month Compensation in USD")
    ############################################Return######################################################

    return bar_figure, map_figure, indicator_chart, radar_chart1, radar_chart2, \
           line_plot1, line_plot2, fig_pie, fig_hist, fig_scat


###############################################Callbacks Indicators#####################################################

@app.callback(
    [
        Output("max_state", "children"),
        Output("max_value", "children"),
        Output("min_state", "children"),
        Output("min_value", "children"),
        Output('Chosen companies', 'children'),
        Output("Interview Difficulty", "children"),
        Output("Interview Duration", "children"),
        Output('Company Size', 'children'),
        Output('Industry', 'children'),
        Output('Revenue Size', 'children')
    ],
    [
        Input("sector_option", "value"),
        Input("company_option", "value"),
        Input('year_slider', 'value')
    ]
)
def indicator(sector, cpys, year):
    df_salary0 = df_salary[df_salary['Year'] == year].copy()
    mean_salary0 = df_salary0.groupby(['State'])['totalyearlycompensation'].mean()
    max_salary0 = df_salary0.groupby(['State'])['totalyearlycompensation'].max()
    min_salary0 = df_salary0.groupby(['State'])['totalyearlycompensation'].min()
    median_salary0 = df_salary0.groupby(['State'])['totalyearlycompensation'].median()
    df_map = pd.concat([mean_salary0, max_salary0, min_salary0, median_salary0], axis=1).reset_index()
    df_map.columns = ['State', 'Average', 'Max', 'Min', 'Median']

    max_s = statename.loc[df_map.State[df_map[sector].idxmax()]][0].strip()
    max_v = round(df_map[sector].max() / 1000, 2)
    min_s = statename.loc[df_map.State[df_map[sector].idxmin()]][0].strip()
    min_v = round(df_map[sector].min() / 1000, 2)

    best_con = df_company.loc[cpys].rating_reviews.idxmax()
    inter_dif = df_company.loc[best_con, 'interview_difficulty_reviews']
    inter_dur = df_company.loc[best_con, 'interview_duration_reviews']
    com_size = df_company.loc[best_con, 'employees_reviews']
    com_ind = df_company.loc[best_con, 'industry_reviews']
    com_rev = df_company.loc[best_con, 'revenue_reviews']

    return 'State: ' + str(max_s), ' Salary: ' + str(max_v) + 'k USD', \
           'State: ' + str(min_s), ' Salary: ' + str(min_v) + 'k USD', \
           str(best_con), str(inter_dif), str(inter_dur), str(com_size), str(com_ind), str(com_rev)


@app.callback(
    Output('Gender_Graph', 'figure'),
    Input('pie_option', 'value'),
    Input('my-toggle-switch', 'on')

)
def update_figure_gender(value, on):
    cols = plotly.colors.DEFAULT_PLOTLY_COLORS
    x_values = [str(a) + ". Quartil" for a in range(1, 5)]

    if value == "Race":
        fig = px.line(race, x=x_values, y=race.columns, markers=True, color_discrete_sequence=cols)
        y_label1 = race.iloc[0, 4]
        y_label2 = race.iloc[3, 4]
        y_categ = "black people"
        categ = "Race"

    elif value == "Gender":
        fig = px.line(gender, x=x_values, y=gender.columns, markers=True, color_discrete_sequence=cols)
        y_label1 = gender.iloc[0, 1]
        y_label2 = gender.iloc[3, 1]
        y_categ = "women"
        categ = "Gender"

    elif value == "Education":
        fig = px.line(education_df, x=x_values, y=education_df.columns, markers=True, color_discrete_sequence=cols)
        y_label1 = education_df.iloc[0, 1]
        y_label2 = education_df.iloc[3, 1]
        y_categ = "Bachelor's Graduates"
        categ = "Education Level"

    else:
        fig = px.line(experience_df, x=x_values, y=experience_df.columns, markers=True, color_discrete_sequence=cols)
        y_label1 = experience_df.iloc[0, 0]
        y_label2 = experience_df.iloc[3, 0]
        y_categ = "Entry Level Engineers"
        categ = "Experience Level"

    fig.update_layout(title=f"{categ} (In)equality",
                      xaxis_title="Quartils of the salary distribution",
                      yaxis_title="Percentage(%)",
                      legend_title=None)

    if on:
        fig.add_annotation(x=0, y=y_label1,
                           text=f"{round(y_label1)}% of {y_categ} belong to the lowest paid quartile...",
                           showarrow=True,
                           arrowhead=5,
                           bordercolor="black",
                           bgcolor="white")
        fig.add_annotation(x=3, y=y_label2,
                           text=f"...and only {round(y_label2)}% of {y_categ} belong to the highest paid quartile",
                           showarrow=True,
                           arrowhead=5,
                           bordercolor="black",
                           bgcolor="white")
    return fig


@app.callback(
    Output('tabs-example-content-1', 'children'),
    Input('tabs-example-1', 'value')
)
def render_content(tab):
    if tab == 'Industry':
        return html.Div([
            dcc.Graph(figure=return_graph(label=tab))
        ])
    elif tab == 'State':
        return html.Div([
            dcc.Graph(figure=return_graph("State", label=tab))
        ])
    elif tab == 'Company Size':
        return html.Div([
            dcc.Graph(figure=return_graph("revenue_reviews", label=tab))
        ])

def return_graph(feature="industry_reviews", label="Industry"):
    ###
    # Gender Pyramide:

    import plotly.graph_objects as gp
    pyramid = df_salary.groupby([feature, "gender"])["totalyearlycompensation"].mean().unstack().iloc[:,
              :2].sort_values(by="Male")
    y_sal = pyramid.index
    x_M = pyramid['Male'] * -1
    x_F = pyramid['Female']

    # Creating instance of the figure
    fig_pyram = gp.Figure()

    # Adding Male data to the figure
    fig_pyram.add_trace(gp.Bar(y=y_sal, x=x_M,
                               name='Male',
                               orientation='h'))

    # Adding Female data to the figure
    fig_pyram.add_trace(gp.Bar(y=y_sal, x=x_F,
                               name='Female', orientation='h',
                               customdata=np.transpose([round(np.divide((-x_M - x_F), x_M) * 100)]),
                               texttemplate="%{customdata[0]}%",
                               textposition="outside",
                               textfont_color="blue"))

    # Updating the layout for our graph
    if label == "Company Size":
        heights = 400
    else:
        heights = 800
    fig_pyram.update_layout(title=f'Mean Salary - Comparison between {label} and Gender',
                            title_font_size=22, barmode='relative',
                            yaxis=dict(title=label, tickmode='linear'),
                            bargap=0.2, bargroupgap=0,
                            height=heights,
                            xaxis=dict(tickvals=[-220000, -160000, -100000, -40000,
                                                 0, 40000, 100000, 160000, 220000],

                                       ticktext=["220k", '160k', '100k', '40k', '0',
                                                 '40k', '100k', '160k', "220k"],

                                       title='Yearly mean compensation in USD',
                                       title_font_size=14)
                            )
    return fig_pyram


@app.callback(
    Output("download-dataframe-csv1", "data"),
    Output("download-dataframe-csv2", "data"),
    Input("btn_csv", "n_clicks"),
    prevent_initial_call=True,
)
def func(n_clicks):
    return dcc.send_data_frame(df_salary.to_csv, "df_salary.csv"), \
           dcc.send_data_frame(df_company.to_csv, "df_salary.csv.csv")


if __name__ == '__main__':
    app.run_server(debug=True)
