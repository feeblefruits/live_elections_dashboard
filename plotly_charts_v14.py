
# coding: utf-8

# Daemon params
DaemonIterations = 24    # make this something big for production (50000000) and small while testing (5)
DaemonInterval = 600    # run the daemon every 15 x 60 = 900 seconds
DaemonLoops = 0         # init count - so keep this zero

import time
import requests
from requests.auth import HTTPBasicAuth
import pandas as pd
import json

import plotly.plotly as py
import plotly.graph_objs as go

import numpy as np

import plotly 
plotly.tools.set_credentials_file(username='{insert your own Plotly username here}', api_key='{insert your own Plotly API key here}')

username = '{insert your own Plotly username here}'
password = '{insert your own Plotly password here}'

access_token = '{insert your own Plotly access token here}'

URL = "https://api.elections.org.za/"

headers = {'Authorization': 'bearer ' + access_token}

r = requests.get(URL, headers=headers)
r.status_code

national_election_code = '699'
provincial_election_code = '827'

# dry-run national ID: 848
# dry-run provincial ID: 849

# 2019 National event ID: 699
# 2019 Provincial event ID: 827

# 2014 National event ID: 291
# 2014 Provincial event ID: 292

# 2016 Local event ID: 402

def get_vd_stats(election_id):
    r = requests.get(URL + 'api/v1/ResultsProgress?ElectoralEventID=' + str(election_id),
        headers = headers)
    return r.json()

def give_random_colour():

    colour = list(np.random.choice(range(256), size=3))
    colour = 'rgb' + str(colour).replace('[', '(').replace(']', ')')
    
    return colour

def round_value(value):
    return round(value, 2)

def get_colours(name):
        
    if name == 'ACDP':
        party_colour = 'rgb(0, 51, 153)'
        
    elif name == 'ACM':
        party_colour = 'rgb(153, 0, 204)'
                
    elif name == 'ANC':
        party_colour = 'rgb(0, 153, 0)'
        
    elif name == 'ATM':
        party_colour = 'rgb(204, 255, 255)'
        
    elif name == 'BLF':
        party_colour = 'rgb(255, 80, 80)'
        
    elif name == 'CPSA':
        party_colour = 'rgb(204, 0, 204)'
        
    elif name == 'COPE':
        party_colour = 'rgb(255, 255, 0)'
        
    elif name == 'DA':
        party_colour = 'rgb(51, 153, 255)'
        
    elif name == 'EFF':
        party_colour = 'rgb(255, 0, 0)'
        
    elif name == 'GOOD':
        party_colour = 'rgb(255, 153, 0)'
        
    elif name == 'ICOSA':
        party_colour = 'rgb(255, 112, 77)'
        
    elif name == 'IFP':
        party_colour = 'rgb(255, 204, 0)'
        
    elif name == 'NFP':
        party_colour = 'rgb(255, 153, 51)'
    
    elif name == 'PAC':
        party_colour = 'rgb(0, 51, 0)'

    elif name == 'UDM':
        party_colour = 'rgb(255, 255, 0)'
        
    elif name == 'VF PLUS':
        party_colour = 'rgb(0, 153, 51)'
                                
    else:
        party_colour = give_random_colour()

    return party_colour

def get_vd_stats(election_id):
    
    r = requests.get(URL + 'api/v1/ResultsProgress?ElectoralEventID=' + str(election_id),
                    headers = headers)
    return r.json()

def get_contesting_parties(election_id):

    r = requests.get(URL + 'api/v1/ContestingParties?ElectoralEventID=' + str(election_id),
                     headers=headers)
    return r.json()

def get_national_results(election_id):

    r = requests.get(URL + 'api/v1/NPEBallotResults?ElectoralEventID=' + str(election_id),
                     headers=headers)
    return r.json()

def make_trace(votes, name):
        
    if name == 'ACDP':
        party_colour = 'rgb(0, 51, 153)'
        
    elif name == 'ACM':
        party_colour = 'rgb(153, 0, 204)'
                
    elif name == 'ANC':
        party_colour = 'rgb(0, 153, 0)'
        
    elif name == 'ATM':
        party_colour = 'rgb(204, 255, 255)'
        
    elif name == 'BLF':
        party_colour = 'rgb(255, 80, 80)'
        
    elif name == 'CPSA':
        party_colour = 'rgb(204, 0, 204)'
        
    elif name == 'COPE':
        party_colour = 'rgb(255, 255, 0)'
        
    elif name == 'DA':
        party_colour = 'rgb(51, 153, 255)'
        
    elif name == 'EFF':
        party_colour = 'rgb(255, 0, 0)'
        
    elif name == 'GOOD':
        party_colour = 'rgb(255, 153, 0)'
        
    elif name == 'ICOSA':
        party_colour = 'rgb(255, 112, 77)'
        
    elif name == 'IFP':
        party_colour = 'rgb(255, 204, 0)'
        
    elif name == 'NFP':
        party_colour = 'rgb(255, 153, 51)'
    
    elif name == 'PAC':
        party_colour = 'rgb(0, 51, 0)'

    elif name == 'UDM':
        party_colour = 'rgb(255, 255, 0)'
        
    elif name == 'VF PLUS':
        party_colour = 'rgb(0, 153, 51)'
                
    else:
        party_colour = 'rgb(229, 231, 173)'

    trace = go.Bar(
        y=['2019'],
        x=[votes],
        name=str(name),
        orientation = 'h',
        hoverinfo='none',
        text=[str(votes) + ' - ' + str(name)],
        textposition = 'inside',
        textfont=dict(
        family='Arial',
        size=14,
        ),
        marker = dict(
        color = party_colour,
        )
    )
    
    return trace

    trace = go.Bar(
        y=['2019'],
        x=[votes],
        name=str(name),
        orientation = 'h',
        hoverinfo='none',
        text=[str(votes) + ' - ' + "".join(word[0] for word in name.split())],
        textposition = 'inside',
        textfont=dict(
        family='Arial',
        size=14,
        ),
        marker = dict(
        color = party_colour,
        )
    )
    
    return trace

def get_provincial_results(election_id, province_id):
    
    r = requests.get(URL + 'api/v1/NPEBallotResults?ElectoralEventID=' + str(election_id) + '&ProvinceID=' + str(province_id),
                     headers=headers)
    return r.json()

def get_results_progress(event_id):
    
    event_id = str(event_id)
    
    r = requests.get(URL + 'api/v1/ResultsProgress?ElectoralEventID=' + event_id,
                     headers=headers)
    return r.json()

def get_province_parties(province_id):

    try:
        for party in get_provincial_results(provincial_election_code, province_id)['PartyBallotResults']:
            party_name.append(party['PartyAbbr'])
    except json.decoder.JSONDecodeError:
        pass
        
def get_province_votes(province_id):

    try:    
        for party in get_provincial_results(provincial_election_code, province_id)['PartyBallotResults']:
            vote_perc.append(party['PercOfVotes'])
    except json.decoder.JSONDecodeError:
        pass

def get_province_name(province_id):
    
    try:
        for party in get_provincial_results(provincial_election_code, province_id)['PartyBallotResults']:    
            province_name.append(get_provincial_results(provincial_election_code, province_id)['Province'])
    except json.decoder.JSONDecodeError:
        pass
    except KeyError:
        pass

def create_party_trace(int_value):
    
    name = list(province_df[['province_name', 'vote_perc']].groupby(province_df['party_name']))[int_value][0]
    
    if name == 'ACDP':
        party_colour = 'rgb(0, 51, 153)'
        
    elif name == 'ACM':
        party_colour = 'rgb(153, 0, 204)'
                
    elif name == 'ANC':
        party_colour = 'rgb(0, 153, 0)'
        
    elif name == 'ATM':
        party_colour = 'rgb(204, 255, 255)'
        
    elif name == 'BLF':
        party_colour = 'rgb(255, 80, 80)'
        
    elif name == 'CPSA':
        party_colour = 'rgb(204, 0, 204)'
        
    elif name == 'COPE':
        party_colour = 'rgb(255, 255, 0)'
        
    elif name == 'DA':
        party_colour = 'rgb(51, 153, 255)'
        
    elif name == 'EFF':
        party_colour = 'rgb(255, 0, 0)'
        
    elif name == 'GOOD':
        party_colour = 'rgb(255, 153, 0)'
        
    elif name == 'ICOSA':
        party_colour = 'rgb(255, 112, 77)'
        
    elif name == 'IFP':
        party_colour = 'rgb(255, 204, 0)'
        
    elif name == 'NFP':
        party_colour = 'rgb(255, 153, 51)'
    
    elif name == 'PAC':
        party_colour = 'rgb(0, 51, 0)'

    elif name == 'UDM':
        party_colour = 'rgb(255, 255, 0)'
        
    elif name == 'VF PLUS':
        party_colour = 'rgb(0, 153, 51)'
                
    else:
        party_colour = give_random_colour()


    annotations = []

    grouped_df = list(province_df[['province_name', 'vote_perc']].groupby(province_df['party_name']))[int_value][1]

    grouped_df = grouped_df.sort_values('vote_perc', ascending=False)

    for item in list(grouped_df['vote_perc']):
        annotations.append(str(item) + ' - ' + str(name))
    
    party_1 = go.Bar(
        x = list(grouped_df['province_name']),
        y = list(grouped_df['vote_perc']),
        name = str(party_name),
        text = annotations,
        textposition = 'inside',
        hoverinfo='none',
        textfont=dict(
        family='Arial',
        size=14
        ),
        marker = dict(
        color = party_colour,
        )
    )
    
    return party_1



def get_seat_calculation(election_id):

    r = requests.get(URL + 'api/v1/NPESeatCalculationResults?ElectoralEventID=' + str(election_id),
                     headers=headers)
    return r.json()

# Main Loop for the Daemon
while True:

    provinces_ids = list(range(1, 10))

    party_name = []
    vote_perc = []
    province_name = []

    for province in provinces_ids:
        get_province_parties(province)
        get_province_votes(province)
        get_province_name(province)

    province_df = pd.DataFrame()

    province_df['province_name'] = province_name
    province_df['party_name'] = party_name
    province_df['vote_perc'] = vote_perc
    province_df['vote_perc'] = province_df['vote_perc'].apply(round_value)


    party_traces = []

    for party in range(0, len(list(province_df[['province_name', 'vote_perc']].groupby(province_df['party_name'])))):
        party_traces.append(create_party_trace(party))

    party_traces = sorted(party_traces, key=lambda k: k['y'], reverse=True)

    # provincial votes graph below

    data = party_traces
    layout = go.Layout(
        barmode='stack',
        showlegend=False,

        yaxis=dict(
            autorange=True,
            showgrid=False,
            zeroline=False,
            showline=False,
            ticks='',
            showticklabels=False
            ),
        xaxis=dict(
            autorange=True,
            showgrid=False,
            zeroline=False,
            showline=False,
            ticks='',
            showticklabels=True
        ),

        margin=go.layout.Margin(
        l=10,
        r=10,
        b=30,
        t=40,
        pad=10
        )
    )

    fig = go.Figure(data=data, layout=layout)
    py.plot(fig, filename='provincial_votes_by_province_and_party_graph', auto_open=False)

    # national votes graph below

    # get results ready for dataframe table

    results_name = []
    results_valid_votes = []
    results_perc_votes = []

    for party in get_national_results(national_election_code)['PartyBallotResults']:
        results_name.append(party['PartyAbbr'])
        results_valid_votes.append(party['ValidVotes'])
        results_perc_votes.append(party['PercOfVotes'])

    results_df = pd.DataFrame()

    results_df['Party'] = results_name
    results_df['Valid Votes'] = results_valid_votes
    results_df['Percentage of Votes'] = results_perc_votes

    top_parties_df = results_df.sort_values('Percentage of Votes', ascending=False)[:3]

    bottom_parties_df = pd.DataFrame()
    bottom_parties_df['Party'] = ['OTHER']
    bottom_parties_df['Valid Votes'] = [results_df.sort_values('Valid Votes', ascending=False)[3:]['Valid Votes'].sum()]
    bottom_parties_df['Percentage of Votes'] = [results_df.sort_values('Percentage of Votes', ascending=False)[3:]['Percentage of Votes'].sum()]

    top_bar_df = pd.concat([top_parties_df, bottom_parties_df], ignore_index=True)
    top_bar_df['Percentage of Votes'] = top_bar_df['Percentage of Votes'].apply(round_value)

    data = []

    for integer in range(0, len(top_bar_df)):
    	data.append(make_trace(top_bar_df['Percentage of Votes'][integer], top_bar_df['Party'][integer]))

    data = data
    layout = go.Layout(
        barmode='stack',
        showlegend=False,
        
        yaxis = dict(
            autorange=True,
            showgrid=False,
            zeroline=False,
            showline=False,
            ticks='',
            showticklabels=False
        ),
        
        xaxis = dict(
            autorange=True,
            showgrid=False,
            zeroline=False,
            showline=False,
            ticks='',
            showticklabels=True
        ),

        margin=go.layout.Margin(
        l=10,
        r=10,
        b=30,
        t=40,
        pad=10
        )
    )
        
    fig = go.Figure(data=data, layout=layout)
    py.plot(fig, filename='national_votes_per_party_graph', auto_open=False)

    # table detailed results

    party_names = []
    party_abr = []

    for party in get_contesting_parties(national_election_code):
        party_names.append(party['Name'])
        party_abr.append(party['Abbreviation'])

    df_legend = pd.DataFrame()

    df_legend['Party'] = party_abr
    df_legend['Full Name'] = party_names
    df_legend['Colour Legend'] = df_legend['Party'].apply(get_colours)

    df_legend = pd.merge(df_legend, results_df, on='Party')
    df_legend['Full Name'] = df_legend['Full Name'].str.title()

    df_legend = df_legend.sort_values('Percentage of Votes', ascending=False)
    
    # create plotly table for detail and legend purposes

    trace0 = go.Table(
        columnwidth = [300, 100],
        header = dict(
        values = ['Party Name', 'Abbreviation', 'Valid Votes', 'Percentage'],
        line = dict(color = 'black'),
        fill = dict(color = 'white'),
        align = 'center',
        font = dict(color = 'black', size = 12)
      ),
        cells = dict(
        values = [df_legend['Full Name'],
                df_legend['Party'],
                df_legend['Valid Votes'],
                df_legend['Percentage of Votes']],

                fill = dict(color = ['white', 'white', 'white', 'white']),
                line = dict(color = ['#e0e0e0', '#e0e0e0', '#e0e0e0', '#e0e0e0']),
                align = 'left',
                font = dict(color = ['black', 'black', 'black', 'black'], size = 11)
                ))

    layout = go.Layout(margin=go.layout.Margin(
            l=10,
            r=10,
            b=30,
            t=40,
            pad=10)
                  )

    data = [trace0]

    fig = dict(data=data, layout=layout)

    py.plot(fig, filename = "cell variable color", auto_open=False)

    results_counted = round(get_vd_stats(699)['VDResultsIn'] / get_vd_stats(699)['VDTotal'] * 100)
    results_outstanding = 100 - results_counted

    trace_1 = go.Bar(
        y=['Results'],
        x=[results_counted],
        orientation = 'h',
        hoverinfo='none',
        text=str(results_counted) + ' - Results Counted',
        textposition = 'inside',
        textfont=dict(
        family='Arial',
        size=14,
            ),
        )

    trace_2 = go.Bar(
        y=['Results'],
        x=[results_outstanding],
        orientation = 'h',
        hoverinfo='none',
        text=str(results_outstanding) + ' - Results Outstanding',
        textposition = 'inside',
        textfont=dict(
        family='Arial',
        size=14,
            ),
        )

    data = [trace_1, trace_2]
    layout = go.Layout(
        barmode='stack',
        showlegend=False,
    
        yaxis = dict(
            autorange=True,
            showgrid=False,
            zeroline=False,
            showline=False,
            ticks='',
            showticklabels=False
            ),
    
        xaxis = dict(
            autorange=True,
            showgrid=False,
            zeroline=False,
            showline=False,
            ticks='',
            showticklabels=True
            ),

        margin=go.layout.Margin(
            l=10,
            r=10,
            b=30,
            t=40,
            pad=10
            )
        )
    
    fig = go.Figure(data=data, layout=layout)
    py.plot(fig, filename='district_results', auto_open=False)

    results_counted = round(get_vd_stats(699)['VDResultsIn'] / get_vd_stats(699)['VDTotal'] * 100, 2)
    results_outstanding = round(100 - results_counted, 2)

    trace_1 = go.Bar(
        y=['Results'],
        x=[results_counted],
        orientation = 'h',
        hoverinfo='none',
        text=str(results_counted) + ' - Results Counted',
        textposition = 'inside',
        textfont=dict(
        family='Arial',
        size=14,
        ),
    )
    trace_2 = go.Bar(
        y=['Results'],
        x=[results_outstanding],
        orientation = 'h',
        hoverinfo='none',
        text=str(results_outstanding) + ' - Results Outstanding',
        textposition = 'inside',
        textfont=dict(
        family='Arial',
        size=14,
        ),
    )
    data = [trace_1, trace_2]
    layout = go.Layout(
        barmode='stack',
        showlegend=False,
        yaxis = dict(
            autorange=True,
            showgrid=False,
            zeroline=False,
            showline=False,
            ticks='',
            showticklabels=False
        ),
        xaxis = dict(
            autorange=True,
            showgrid=False,
            zeroline=False,
            showline=False,
            ticks='',
            showticklabels=True
        ),
        margin=go.layout.Margin(
            l=10,
            r=10,
            b=30,
            t=40,
            pad=10
        )
    )
    fig = go.Figure(data=data, layout=layout)
    # py.plot(fig, filename='district_results', auto_open=False)

    # Stop the Daemon after X loops
    DaemonLoops += 1
    if DaemonLoops == DaemonIterations:
        break

    # Control Daemon speed
    time.sleep(DaemonInterval)


print("Our Daemon has done its Job")