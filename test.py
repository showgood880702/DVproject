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
import dash_bootstrap_components as dbc
import dash_daq as daq
import plotly.express as px

# https://htmlcheatsheet.com/css/

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

# ==========================================Interactive Components==========================================#
# levels = df_salary.levelbyexperience.unique().tolist()
states = sorted(df_salary.State.dropna().unique().tolist())
sectors = ['Max', 'Min', 'Average', 'Median']
years = list(range(2017, 2021))
companys = sorted(df_salary.company.dropna().unique().tolist())

# level_options = [dict(label=level, value=level) for level in levels]
state_options = [dict(label=state, value=state) for state in states]
sector_options = [dict(label=sector, value=sector) for sector in sectors]
company_options = [dict(label=company, value=company) for company in companys]

# ===================Experience Level===================#
# dropdown_level = dcc.Dropdown(
#     id='level_drop',
#     options=level_options,
#     value=levels[0],
#     multi=False
# )

# ===================Mean Max Min Median===================#
dropdown_sector = dcc.Dropdown(
    id='sector_option',
    options=sector_options,
    value=sectors[0],
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
    value=2017,
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
    value=['Amazon'],
    multi=True
)

# ===================Pie===================#
dropdown_pie = dcc.Dropdown(
    id='pie_option',
    options=["Gender", "Race", "Education", "Level of Experience"],
    value="Gender",
    multi=False
)

# ===================Hist===================#
dropdown_hist = dcc.Dropdown(
    id='hist_option',
    options=["Mean", "Median", "Max", "Min", "Standard Deviation"],
    value="Mean",
    multi=False
)
radio_hist = daq.ToggleSwitch(
    id='monthly-toggle-switch',
    value=False,
    label='Yearly / Monthly',
    labelPosition='bottom'
)
##################################################APP###################################################################

app = dash.Dash(__name__)

server = app.server

app.layout = html.Div(
    [
        html.Div(
            [
                html.P('Is Software Engineer Happy in USA?',
                       style={"font-weight": "bold",
                              "font-size": 35,
                              "text-align": "center",
                              "margin-bottom": "25px"}
                       ),
            ],
            id='headtitle',
        ),

        # html.Img(
        #     src="https://github.com/FranzMichaelFrank/health_eu/blob/main/assets/Nova_IMS.png",
        #     id="plotly-image",
        #     style={
        #         "height": "60px",
        #         "width": "auto",
        #         "margin-bottom": "25px",
        #     },
        # )

        html.Div(
            [
                html.Div(
                    [
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.Label('Salary'),
                                        html.Br(),
                                        dropdown_sector,
                                    ],
                                    id='dropdown',
                                    style={"text-align": "justify",
                                           'margin': '10px',
                                           'width': '35%'},
                                    # className='box'
                                ),
                                html.Div(
                                    [
                                        html.Div(
                                            [
                                                html.Label('Cost of Living Index'),
                                                radio_costIndex
                                            ],
                                            id='cost',
                                            style={"text-align": "center",
                                                   'width': '50%'},
                                        ),

                                        html.Div(
                                            [
                                                html.Label('State Average Income'),
                                                radio_avgIncome
                                            ],
                                            id='income',
                                            style={"text-align": "center",
                                                   'width': '50%'},
                                        ),
                                    ],
                                    id='choose',
                                    style={'display': 'flex',
                                           'margin': '10px',
                                           'width': '65%'},
                                    # className='box'
                                )
                            ], id='drop and choose',
                            style={'display': 'flex'},
                            className='box'
                        ),
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
                                html.P('Select Year'),
                                slider_year
                            ],
                            id='year slider',
                            # style={"margin-top": "0px"},
                        ),

                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.P(
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
                                    # className="box",
                                    style={"text-align": "center",
                                           'width': '50%'},
                                    id="Highest",
                                ),
                                html.Div(
                                    [
                                        html.P(
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
                                    # className="box",
                                    style={"text-align": "center",
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
                html.Div(
                    [
                        html.Div(
                            [
                                dropdown_company
                            ],
                            id='select company',
                            # style={'width': '70%'}
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
                            id='radartplot', style={'display': 'flex'}
                        )

                    ],
                    id='3rd row 1st row',
                    # style={'width': '80%'},
                    # className='box'
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
                                    style={'width': '25%'},
                                    className='box_comment'
                                ),
                                html.Div(
                                    [
                                        html.H3('Overall Rating'),
                                        html.P(id='Overall Rating'),
                                    ], style={'width': '25%'},
                                    className='box_comment'
                                ),
                                html.Div(
                                    [
                                        html.H3('Interview Experience'),
                                        html.P(id='Interview Experience'),
                                    ], style={'width': '25%'},
                                    className='box_comment'
                                ),
                                html.Div(
                                    [
                                        html.H3('Interview Difficulty'),
                                        html.P(id='Interview Difficulty'),
                                    ], style={'width': '25%'},
                                    className='box_comment'
                                )
                            ],
                            id='331row',
                            style={'display': 'flex'},
                        ),
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.H3('Interview Duration'),
                                        html.P(id='Interview Duration'),
                                    ], style={'width': '25%'},
                                    className='box_comment'
                                ),
                                html.Div(
                                    [
                                        html.H3('Company Size'),
                                        html.P(id='Company Size'),
                                    ], style={'width': '25%'},
                                    className='box_comment'
                                ),
                                html.Div(
                                    [
                                        html.H3('Industry'),
                                        html.P(id='Industry'),
                                    ], style={'width': '25%'},
                                    className='box_comment'
                                ),
                                html.Div(
                                    [
                                        html.H3('Revenue Size'),
                                        html.P(id='Revenue Size'),
                                    ], style={'width': '25%'},
                                    className='box_comment'
                                )
                            ],
                            id='332row',
                            style={'display': 'flex'},
                        ),
                    ],
                    id='3rd row 2nd row',
                    # style={'display': 'flex'}
                )
            ], id='3rd row',
            # style={'display': 'flex'},
            className='box'
        ),
        html.Div(
            [
                html.Div(
                    [
                        dcc.Graph(id='line_plot 1')
                    ]
                ),
                html.Div(
                    [
                        dcc.Graph(id='line_plot 2')
                    ]
                ),
            ],
            id='4th row',
            style={'display': 'flex'},
            className='box'
        ),
        html.Div(
            [
                html.Div(
                    [
                        dropdown_pie,
                        html.Br(),
                        dcc.Graph(id='Graph_Pie1')
                    ], style={'width': '30%'}
                ),
                html.Div(
                    [
                        dropdown_hist,
                        radio_hist,
                        dcc.Graph(id='Graph_hist1')
                    ], style={'width': '70%'}
                ),
            ],
            id='5th row',
            style={'display': 'flex'},
            className='box'
        )
    ],
    style={'background-color': '#f3f3f1',
           "display": "flex",
           "flex-direction": "column"},
)


##################################################Callbacks Plots#####################################################


@app.callback(
    [
        Output("bar_graph", "figure"),
        Output("map_figure", "figure"),
        Output("radar_graph1", "figure"),
        Output("radar_graph2", "figure"),
        Output("line_plot 1", "figure"),
        Output("line_plot 2", "figure"),
        Output('Graph_Pie1', 'figure'),
        Output('Graph_hist1', 'figure'),
    ],
    [
        Input("sector_option", "value"),
        Input('costIndex', 'value'),
        Input("avgIncome", "value"),
        Input("company_option", "value"),
        Input('year_slider', 'value'),
        Input('pie_option', 'value'),
        Input('hist_option', 'value'),
        Input('monthly-toggle-switch', 'value')
    ]
)
def plots(sector, cost, income, cpys, year, value1, value2, switch):
    # df_sector_list = [max_salary, min_salary, mean_salary, median_salary]

    ############################################Bar Plot##########################################################
    global fig_pie
    data_bar = []
    # df_sub = df_sector_list[sectors.index(sector)]
    # for level in levels:

    # df_bar = df_sub[(df_sub.levelbyexperience == level)].replace(np.nan, 0).sort_values('totalyearlycompensation')
    if not cost:

        bar_figure = make_subplots(rows=1, cols=2, horizontal_spacing=.05)
        bar_figure.add_trace(go.Bar(y=df_bar.sort_values([sector]).State,
                                    x=df_bar.sort_values([sector])['costIndex'],
                                    name='costIndex',
                                    orientation='h',
                                    marker=dict(color='#27AE60'),
                                    ),
                             row=1, col=1
                             )
        bar_figure.add_trace(go.Bar(y=df_bar.sort_values([sector]).State,
                                    x=df_bar.sort_values([sector])[sector],
                                    name=sector,
                                    orientation='h',
                                    marker=dict(color='#EC7063'),
                                    ),
                             row=1, col=2
                             )
        if not income:
            bar_figure.add_trace(go.Bar(y=df_bar.sort_values([sector]).State,
                                        x=df_bar.sort_values([sector])['averageIncome'],
                                        name='averageIncome',
                                        orientation='h',
                                        marker=dict(color='#3498DB'),
                                        opacity=0.6
                                        ),
                                 row=1, col=2
                                 )
            bar_figure.update_layout(barmode='overlay')
        bar_figure.update_layout(margin={"r": 20, "t": 30, "l": 0, "b": 10},
                                 legend=dict(y=.0, x=.72),
                                 title=dict(text=sector + ' Salary of Soft Engineer', y=.98),
                                 yaxis=dict(title='Salary'),
                                 # paper_bgcolor='#f3f3f1',
                                 # plot_bgcolor='#f3f3f1',
                                 # template='ggplot2',
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
                                    ),
                             )
        if not income:
            bar_figure.add_trace(go.Bar(y=df_bar.sort_values([sector]).State,
                                        x=df_bar.sort_values([sector])['averageIncome'],
                                        name='averageIncome',
                                        orientation='h',
                                        marker=dict(color='#3498DB'),
                                        opacity=0.6
                                        ),
                                 )
            bar_figure.update_layout(barmode='overlay')
        bar_figure.update_layout(margin={"r": 20, "t": 30, "l": 0, "b": 10},
                                 legend=dict(y=.0, x=.68),
                                 title=dict(text=sector + ' Salary of Soft Engineer', y=.98),
                                 yaxis=dict(title='Salary'),
                                 # paper_bgcolor='#f3f3f1',
                                 # plot_bgcolor='#f3f3f1',
                                 # template='ggplot2',
                                 showlegend=True,
                                 )
    bar_figure.update_layout(width=600, height=500)
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
                             title=dict(text='USA Salary on the year ', x=0.5, y=0.95),
                             # paper_bgcolor='#f3f3f1',
                             # plot_bgcolor='#f3f3f1',

                             )

    map_figure = go.Figure(data=data_choropleth, layout=layout_choropleth)
    map_figure.update_layout(margin={"r": 0, "t": 50, "l": 0, "b": 0},
                             width=700, height=400
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

    # radar_chart = make_subplots(
    #     rows=1, cols=2,
    #     column_width=[0.4, 0.4],
    #     specs=[[
    #         # {"type": "Indicator"},
    #         {"type": "Scatterpolar"},
    #         {"type": "Scatterpolar"}
    #     ]]
    # )

    # radar_chart.add_trace(go.Indicator(
    #     mode='gauge',
    #     value=3.4,
    #     domain=dict(x=[0, 1], y=[.2, 1]),
    #     title=dict(text='Rating'),
    # ),
    #     row=1, col=1
    # )
    # radar_chart.update_traces(gauge_bar_color='#85C1E9',
    #                           gauge_axis_range=[0, 5],
    #                           selector=dict(type='indicator'))
    radar_chart1 = go.Figure()
    radar_chart1.add_trace(go.Scatterpolar(r=r1_mean,
                                           theta=categories1,
                                           # fill='toself',
                                           name='Mean',
                                           # mode='markers',
                                           showlegend=False,
                                           line=dict(color=cols[0])
                                           ))
    r_range = []
    for n, cpy in enumerate(cpys):
        r_c = df_salary[df_salary['company'] == cpy][categories1].mean().tolist()
        r_range.append(r_c)
        radar_chart1.add_trace(go.Scatterpolar(r=r_c,
                                               theta=categories1,
                                               # fill='toself',
                                               name=cpy,
                                               # line_close=True,
                                               showlegend=False,
                                               line=dict(color=cols[n + 1])
                                               ))

    r_range.append(r1_mean)
    r_range = np.array(r_range)
    radar_chart1.update_layout_images(template='plotly',
                                      polar=dict(radialaxis=dict(visible=True)),
                                      )
    radar_chart1.update_polars(radialaxis_range=(r_range.min() * 0.9, r_range.max() * 1.1))

    radar_chart2 = go.Figure()
    radar_chart2.add_trace(go.Scatterpolar(r=r2_mean,
                                           theta=categories2,
                                           # fill='toself',
                                           name='Mean',
                                           # mode='markers',
                                           showlegend=True,
                                           line=dict(color=cols[0])
                                           ))
    r_range = []
    for n, cpy in enumerate(cpys):
        r_c = df_salary[df_salary['company'] == cpy][categories2].mean().tolist()
        r_range.append(r_c)
        radar_chart2.add_trace(go.Scatterpolar(r=r_c,
                                               theta=categories2,
                                               # fill='toself',
                                               name=cpy,
                                               # line_close=True,
                                               showlegend=True,
                                               line=dict(color=cols[n + 1])
                                               ))
    r_range.append(r2_mean)
    r_range = np.array(r_range)
    radar_chart2.update_layout_images(template='plotly',
                                      polar=dict(radialaxis=dict(visible=True)),
                                      )
    radar_chart2.update_polars(radialaxis_range=(r_range.min() * 0.9, r_range.max() * 1.1))
    # radar_chart.update_layout(width=400, height=200)
    # mean_year = df_salary[df_salary['year'] == year].groupby(['month'])['totalyearlycompensation'].mean()
    # max_year = df_salary[df_salary['year'] == year].groupby(['month'])['totalyearlycompensation'].max()
    # min_year = df_salary[df_salary['year'] == year].groupby(['month'])['totalyearlycompensation'].min()
    # median_year = df_salary[df_salary['year'] == year].groupby(['month'])['totalyearlycompensation'].median()
    # df_year_list = [max_year, min_year, mean_year, median_year]
    # data_line = []
    #
    # for index, sub_year in enumerate(df_year_list):
    #     data_line.append(dict(type='scatter',
    #                           x=sub_year.index,
    #                           y=sub_year.values,
    #                           name=sectors[index],
    #                           # mode='line'
    #                           )
    #                      )
    #
    # layout_line = dict(title=dict(text='Salary Trend'),
    #                    yaxis=dict(title='US Dollar'),
    #                    xaxis=dict(title='Month'),
    #                    paper_bgcolor='rgba(0,0,0,0)',
    #                    plot_bgcolor='rgba(0,0,0,0)'
    #                    )
    ############################################Line Chart######################################################
    df1 = df_salary.groupby(["ExperienceLevel", "Region"])["totalyearlycompensation"].median().reset_index()

    line_plot1 = px.line(df1[df1["Region"].isin(df1.Region.unique())],
                         x="ExperienceLevel", y="totalyearlycompensation",
                         color="Region",
                         title="Software Engineer Salaries by Experience and State")

    df2 = df_salary.groupby(["Years of Experience", "Region"])["totalyearlycompensation"].median().reset_index()

    line_plot2 = px.line(df2[df2["Region"].isin(df2.Region.unique())],
                         x="Years of Experience", y="totalyearlycompensation",
                         color="Region",
                         title="Software Engineer Salaries by Experience and Regions")
    ############################################4th row######################################################
    if value1 == "Gender":

        gender_counts = df_salary.gender.value_counts()[:-1]
        fig_pie = px.pie(values=gender_counts.values, names=gender_counts.index,
                         title='Gender proportions in the dataset', hole=0.3)

        if value2 == "Mean":
            bar_count = df_salary.groupby("gender")["totalyearlycompensation"].mean()[:-1]

        elif value2 == "Median":
            bar_count = df_salary.groupby("gender")["totalyearlycompensation"].median()[:-1]
        elif value2 == "Min":
            bar_count = df_salary.groupby("gender")["totalyearlycompensation"].min()[:-1]
        elif value2 == "Max":
            bar_count = df_salary.groupby("gender")["totalyearlycompensation"].max()[:-1]
        elif value2 == "Standard Deviation":
            bar_count = df_salary.groupby("gender")["totalyearlycompensation"].std()[:-1]

        if switch is True:
            bar_count /= 12

        fig_hist = px.bar(bar_count)

    if value1 == "Level of Experience":

        exp_counts = df_salary.ExperienceLevel.value_counts()
        fig_pie = px.pie(values=exp_counts.values, names=exp_counts.index,
                         title='Experience proportions in the dataset', hole=0.3)

        if value2 == "Mean":
            bar_count = df_salary.groupby("ExperienceLevel")["totalyearlycompensation"].mean()

        elif value2 == "Median":
            bar_count = df_salary.groupby("ExperienceLevel")["totalyearlycompensation"].median()
        elif value2 == "Min":
            bar_count = df_salary.groupby("ExperienceLevel")["totalyearlycompensation"].min()
        elif value2 == "Max":
            bar_count = df_salary.groupby("ExperienceLevel")["totalyearlycompensation"].max()
        elif value2 == "Standard Deviation":
            bar_count = df_salary.groupby("ExperienceLevel")["totalyearlycompensation"].std()

        if switch is True:
            bar_count /= 12

        fig_hist = px.bar(bar_count)

    elif value1 == "Race":

        race_counts = df_salary.Race.value_counts()
        fig_pie = px.pie(values=race_counts, names=race_counts.index, title='Race proporations in the dataset',
                         hole=0.3)

        if value2 == "Mean":
            bar_count = df_salary.groupby("Race")["totalyearlycompensation"].mean()
        elif value2 == "Median":
            bar_count = df_salary.groupby("Race")["totalyearlycompensation"].median()
        elif value2 == "Min":
            bar_count = df_salary.groupby("Race")["totalyearlycompensation"].min()
        elif value2 == "Max":
            bar_count = df_salary.groupby("Race")["totalyearlycompensation"].max()

        elif value2 == "Standard Deviation":
            bar_count = df_salary.groupby("Race")["totalyearlycompensation"].std()

        if switch is True:
            bar_count /= 12

        fig_hist = px.bar(bar_count)


    elif value1 == "Education":
        education_counts = df_salary.Education.value_counts()
        fig_pie = px.pie(values=education_counts, names=education_counts.index,
                         title='Education proporations in the dataset', hole=0.3)

        if value2 == "Mean":
            bar_count = df_salary.groupby("Education")["totalyearlycompensation"].mean()
        elif value2 == "Median":
            bar_count = df_salary.groupby("Education")["totalyearlycompensation"].median()
        elif value2 == "Min":
            bar_count = df_salary.groupby("Education")["totalyearlycompensation"].min()
        elif value2 == "Max":
            bar_count = df_salary.groupby("Education")["totalyearlycompensation"].max()
        elif value2 == "Standard Deviation":
            bar_count = df_salary.groupby("Education")["totalyearlycompensation"].std()

        if switch is True:
            bar_count /= 12

        fig_hist = px.bar(bar_count)

    fig_hist.layout.update(showlegend=False)
    fig_hist.update_yaxes(title=f"{value2} Yearly Compensation in USD")
    if switch is True:
        fig_hist.update_yaxes(title=f"{value2} per Month Compensation in USD")
    ############################################Return######################################################

    return bar_figure, map_figure, radar_chart1, radar_chart2, line_plot1, line_plot2, fig_pie, fig_hist
    # go.Figure(data=data_line, layout=layout_line)


###############################################Callbacks Indicators#####################################################

@app.callback(
    [
        Output("max_state", "children"),
        Output("max_value", "children"),
        Output("min_state", "children"),
        Output("min_value", "children"),
        Output('Chosen companies', 'children'),
        Output("Overall Rating", "children"),
        Output("Interview Experience", "children"),
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

    statename = df_salary[['State', 'StateName']].drop_duplicates().set_index('State')

    max_s = statename.loc[df_map.State[df_map[sector].idxmax()]][0].strip()
    max_v = round(df_map[sector].max() / 1000, 2)
    min_s = statename.loc[df_map.State[df_map[sector].idxmin()]][0].strip()
    min_v = round(df_map[sector].min() / 1000, 2)

    best_con = df_company.loc[cpys].rating_reviews.idxmax()
    over_rating = df_company.loc[best_con, 'rating_reviews']
    inter_exp = df_company.loc[best_con, 'interview_experience_reviews']
    inter_dif = df_company.loc[best_con, 'interview_difficulty_reviews']
    inter_dur = df_company.loc[best_con, 'interview_duration_reviews']
    com_size = df_company.loc[best_con, 'employees_reviews']
    com_ind = df_company.loc[best_con, 'industry_reviews']
    com_rev = df_company.loc[best_con, 'revenue_reviews']

    return 'State: ' + str(max_s), ' Salary: ' + str(max_v) + 'k USD', \
           'State: ' + str(min_s), ' Salary: ' + str(min_v) + 'k USD', \
           str(best_con), str(over_rating), str(inter_exp), str(inter_dif), \
           str(inter_dur), str(com_size), str(com_ind), str(com_rev)


if __name__ == '__main__':
    app.run_server(debug=True)
