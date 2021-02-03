import numpy as np
import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import plotly.graph_objects as go  
from plotly.subplots import make_subplots
from dash.dependencies import Input, Output
from plotly.subplots import make_subplots
import dash_bootstrap_components as dbc


#Reading in the data
url2018 = 'https://github.com/KhanyaI/coffee-dashboard/blob/main/arabica_2018.csv'
df_2018 = pd.DataFrame(pd.read_csv(url2018,sep=","))


#Prepping the dataframe
replacement = {
    "Tanzania, United Republic Of": "Tanzania",
    "Cote d?Ivoire": "Ivory Coast"}

df_2018['Country.of.Origin'] = df_2018['Country.of.Origin'].replace(replacement)

#df_2018['Country.of.Origin'] = df_2018['Country.of.Origin'].str.replace('Tanzania, United Republic Of', 'Tanzania')
#df_2018['Country.of.Origin'] = df_2018['Country.of.Origin'].str.replace('Cote d?Ivoire', 'Ivory Coast',regex=True)
df_2018 = df_2018[df_2018['Country.of.Origin'].notnull()]


countries = df_2018['Country.of.Origin'].unique()


df_2018_grouped =df_2018.groupby('Country.of.Origin',as_index=False)
df_2018_grouped_median = df_2018_grouped[['Aroma','Flavor','Aftertaste', 'Acidity','Body','Balance','Uniformity','Sweetness']].median()


# Country grades for coffee on map

country_grade = df_2020.groupby(by=df_2020.Country, as_index=False)['Grade'].median()
country_grade.Grade = country_grade.Grade.round(2)

colors = {
    'text': '#210808'
}



#Subplots per attribute
figsubplots = make_subplots(rows=2, cols=4,subplot_titles=("Aftertaste", "Aroma", "Flavor", "Acidity", "Body", "Balance", "Uniformity", "Sweetness"),
  x_title='Country', y_title='Grade')

figsubplots.append_trace(go.Scatter(x=df_2018['Country.of.Origin'], y=df_2018['Aftertaste'],mode='markers'),row=1,col=1)

figsubplots.append_trace(go.Scatter(x=df_2018['Country.of.Origin'], y=df_2018['Aroma'],mode='markers'),row=1,col=2)

figsubplots.append_trace(go.Scatter(x=df_2018['Country.of.Origin'], y=df_2018['Flavor'],mode='markers'),row=1,col=3)

figsubplots.append_trace(go.Scatter(x=df_2018['Country.of.Origin'], y=df_2018['Acidity'],mode='markers'),row=1,col=4)

figsubplots.append_trace(go.Scatter(x=df_2018['Country.of.Origin'], y=df_2018['Body'],mode='markers'),row=2,col=1)

figsubplots.append_trace(go.Scatter(x=df_2018['Country.of.Origin'], y=df_2018['Balance'],mode='markers'),row=2,col=2)

figsubplots.append_trace(go.Scatter(x=df_2018['Country.of.Origin'], y=df_2018['Uniformity'],mode='markers'),row=2,col=3)

figsubplots.append_trace(go.Scatter(x=df_2018['Country.of.Origin'], y=df_2018['Sweetness'],mode='markers'),row=2,col=4)

figsubplots.update_layout(height = 800, width= 1400,showlegend=False,title_font=dict(size=18),font_family='Helvetica Neue',font_color=colors['text'])
figsubplots.update_yaxes(range=[5.5, 10.5], autorange=False)
figsubplots.update_xaxes(nticks=35)




#Processing vs Grade 

processing = df_2018.groupby("Processing.Method",as_index=False).agg({"Total.Cup.Points":"mean"}).sort_values("Total.Cup.Points", ascending=False)
fig_typesvsgrade = px.bar(x=processing['Processing.Method'].unique(),y=processing['Total.Cup.Points'].values,range_y=(80,83), color=processing['Processing.Method'],labels={'y':'Grades out of 10', 'x':'Processing type'})
fig_typesvsgrade.update_layout(height = 600, width= 1100,showlegend=False,title_text='Total Grade vs Processing type',title_font=dict(size=14),title_font_family='Helvetica Neue',font_color=colors['text'])



#App

colors = {
    'text': '#210808'
}
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

app.layout = html.Div(style={'font-family':'Helvetica Neue'}, children=[
    html.H1(children='Which coffee is the best?',
      style={
      'textAlign': 'center',
      'color': colors['text'],
      'font-weight':'bold'
      }
    ),

    html.Div(children=[
    dcc.Dropdown(
        id='my_dropdown',
        options=[
            {'label': country, 'value': country} for country in countries
        ],
        value='Ethiopia',
        style=dict(
                    width='95%',
                    color='#210808',
                )
    ),

    dcc.Graph(id="my_graph",style = {'width': '95%','margin-left':'0', 'margin-right':'0'})]),
    
    html.Div([
    dcc.Graph(figure=figsubplots)],style={'display': 'inline-block'}),

    html.Div([
    dcc.Graph(figure=fig_typesvsgrade)],style={'display': 'inline-block'})



    ])
    




@app.callback(Output("my_graph",'figure'),
              [Input('my_dropdown', 'value')])

def update_graph(value):
  df = df_2018_grouped_median[df_2018_grouped_median['Country.of.Origin'] == value]
  print(value)
  fig = px.bar(x=df.columns[1:],y= df.loc[:, df.columns != 'Country.of.Origin'].values[0],color=['#463934','#463934','#463934','#463934','#463934','#463934','#463934','#463934'], color_discrete_map='identity',
    labels={'y':'Grades out of 10', 'x':'Attributes'})
  fig.update_layout(font_family='Helvetica Neue',template="simple_white",font_color=colors['text'])
  return fig

if __name__ == '__main__':
  app.run_server(debug=True)  




"""
#2020
url2020 = 'https://github.com/KhanyaI/coffee-dashboard/blob/main/arabica_merged.csv'

df_2020 = pd.DataFrame(pd.read_csv('gs://dash-app-csv/arabica_merged.csv'))

df_2020.drop(['0', '1', '2', '3',
       '84.50', '83.83', '83.17', '86.25', '82.67', '85.00', '82.25', '84.08',
       '82.50'], axis=1,inplace=True)

fig2020 = px.scatter_geo(country_grade, locations="Country", locationmode='country names', color="Country",
                     hover_name="Grade", size="Grade",
                     projection="equirectangular")



fig2020.update_layout(height=600,width=800,showlegend=False)
"""

