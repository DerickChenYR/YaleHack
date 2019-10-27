# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
#import plotly.plotly as py
import plotly.graph_objs as go
import plotly.express as px


from db_classes import meme_processed
from db_query import sqlalchemy_to_df, prepare_entities_freq, prepare_gallery_memes

#DF holding processed meme data
df = sqlalchemy_to_df(meme_processed)

df_positive = df[df['capt_sentiment'] + df['text_sentiment'] > 0]
df_positive_comp = df.sort_values(by=['comp_score'])

df_negative = df[df['capt_sentiment'] + df['text_sentiment'] < 0]
df_negative_comp = df.sort_values(by=['comp_score'], ascending=False)

entities_positive = prepare_entities_freq(df_positive, top = 20)
entities_negative = prepare_entities_freq(df_negative, top = 20)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)




header = html.Div(children=[
    html.H1('Meme Classifier Analysis'),
    html.P("A YaleHack Project by Anand Chitale and Derick Chen")
    ], style={"text-align":"center"})


#Favourable Gallery
display_count = 5
encoded_imgs = prepare_gallery_memes(df_positive_comp, top = display_count)
decoded_imgs = []
for img in encoded_imgs:
    decoded_imgs.append(html.Img(src='data:image/png;base64,{}'.format(img.decode()), style={"width":"{}%".format(80/display_count)}))

gallery_positive = html.Div(children=decoded_imgs);


#Negative Gallery
display_count = 5
encoded_imgs = prepare_gallery_memes(df_negative_comp, top = display_count)
decoded_imgs = []
for img in encoded_imgs:
    decoded_imgs.append(html.Img(src='data:image/png;base64,{}'.format(img.decode()), style={"width":"{}%".format(80/display_count)}))

gallery_negative = html.Div(children=decoded_imgs);

#Favourable Components
left_wordcloud = None

data = []
for entity, freq in entities_positive.items():
    trace = go.Bar(
        x=[entity],
        y=[freq],
        marker={"color":"green"}
    )
    data.append(trace)

layout = go.Layout(
        #width='80%',
        title='What people love about JetBlue',
        showlegend=False,
        margin={'l': 100, 'b': 50, 't': 80, 'r': 50},
    )

bar_positive_entities = dcc.Graph(
    id='bar_positive_entities',
    figure={
        'data': data,
        'layout': layout
    },
    config={'modeBarButtonsToRemove': ['sendDataToCloud']},

)



#Unfavourable Components
right_worldcloud = None
right_scatter = None

data = []
for entity, freq in entities_negative.items():
    trace = go.Bar(
        x=[entity],
        y=[freq],
        marker={"color":"red"}
    )
    data.append(trace)

layout = go.Layout(
        #width='80%',
        title='What people love about JetBlue',
        showlegend=False,
        margin={'l': 100, 'b': 50, 't': 80, 'r': 50},
    )

bar_negative_entities = dcc.Graph(
    id='bar_negative_entities',
    figure={
        'data': data,
        'layout': layout
    },
    config={'modeBarButtonsToRemove': ['sendDataToCloud']},

)





#Aggregate Meme-sentiment historical line chart
data = go.Scatter(
                x=df['date'],
                y=df['text_sentiment'] + df['capt_sentiment'],
                name='Likes',
                mode='lines+markers',
                fill='tozeroy',
                line=dict(
                    #shape='spline',
                    smoothing = 1.3,
                    color = 'rgb(5, 153, 223)',
                )
            )

layout = go.Layout(
    #width='80%',
    title='Meme Composite Sentiment Trend',
    legend=dict(orientation="h"),
    yaxis=dict(
        title='Sentiment Polarity'
    ),
    margin={'l': 50, 'b': 50, 't': 40, 'r': 50},
)

fig = go.Figure(data=data, layout=layout)

historical_meme_sentiment = dcc.Graph(
            id='historical_meme_sentiment',
            figure=fig,
            config={'modeBarButtonsToRemove': ['sendDataToCloud']}
        )



#Define app layout
app.layout = html.Div(children=[
    
    header,
    
    #First Section, two columns
    html.Div([
        html.Div(
            className = "row",
            children=[
                html.Div(children=[bar_positive_entities], className="six columns"),
                html.Div(children=[bar_negative_entities], className="six columns"),
            ],
            style={}
        )
    ]),

    #Second Section
    html.Div([
        gallery_positive,
        gallery_negative,
        html.Div(
            className = "row",
            children=[
                html.P("Content for section 2.", style ={"text-align":"center"}),
                historical_meme_sentiment
            ],
            style={}
        )
    ]),

])

if __name__ == '__main__':
    app.run_server(debug=True)