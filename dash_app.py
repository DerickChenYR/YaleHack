# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
#import plotly.plotly as py
import plotly.graph_objs as go
import plotly.express as px


from db_classes import meme_processed
from db_query import sqlalchemy_to_df, prepare_entities_freq, prepare_gallery_memes
import base64


#DF holding processed meme data
df = sqlalchemy_to_df(meme_processed)

df_positive = df[df['capt_sentiment'] + df['text_sentiment'] > 0]
df_positive_comp = df.sort_values(by=['comp_score'], ascending=False)

df_negative = df[df['capt_sentiment'] + df['text_sentiment'] < 0]
df_negative_comp = df.sort_values(by=['comp_score'], ascending=True)

entities_positive = prepare_entities_freq(df_positive, top = 20)
entities_negative = prepare_entities_freq(df_negative, top = 20)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

encoded_logo = base64.b64encode(open("jetblue_logo.jpg", 'rb').read())


header = html.Div(children=[
    html.Img(src='data:image/png;base64,{}'.format(encoded_logo.decode()), style={"width":"30%", "padding":5, "max-width":200}),
    html.H1('Meme Sentiment Classifier Analysis', style={"font-weight":"bold"}),
    html.P("A YaleHack Project by Anand Chitale and Derick Chen"),
    html.P("We evaluated meme sentiments based on three metrics, the polarity of the image template, the natural language sentiments of the image text and that of the caption. After scraping and storing the images as local jpegs, Google Cloud APIs were utilised to analyse the sentiments of the individaul sentiment components. Cloud Vision was used to extract the image text with OCR API, and Natural Language API was used to extract entities and to perform text based sentiment analysis. Image format sentiment was derived with a supervised ML training model. We extract text-based sentiments from a training set of memes and instructed the ML model to learn the correlation between the images and the labels.", style={"padding-left":"15%", "padding-right":"15%"})
    ], style={"text-align":"center"})


#Favourable Gallery
display_count = 5
encoded_imgs = prepare_gallery_memes(df_positive_comp, top = display_count)
decoded_imgs = []
for img in encoded_imgs:
    decoded_imgs.append(html.Img(src='data:image/png;base64,{}'.format(img.decode()), style={"width":"{}%".format(90/display_count), "padding":5}))

gallery_positive = html.Div(children=decoded_imgs, style={"text-align":"center", "background-color":"#e5ecf6", "margin-left":"5%", "margin-right":"5%"});


#Negative Gallery
display_count = 5
encoded_imgs = prepare_gallery_memes(df_negative_comp, top = display_count)
decoded_imgs = []
for img in encoded_imgs:
    decoded_imgs.append(html.Img(src='data:image/png;base64,{}'.format(img.decode()), style={"width":"{}%".format(90/display_count), "padding":5}))

gallery_negative = html.Div(children=decoded_imgs, style={"text-align":"center", "background-color":"#e5ecf6", "margin-left":"5%", "margin-right":"5%"});



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
        title='What JetBlue could improve on',
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




#Sentiment Distribution Histogram

layout = go.Layout(
    #width='80%',
    title='Meme Composite Sentiment Distribution',
    legend=dict(orientation="h"),
    yaxis=dict(
        title='Sentiment % Distribution'
    ),
    margin={'l': 50, 'b': 50, 't': 40, 'r': 50},
)

fig = go.Figure(data=[
        go.Histogram(x=df["comp_score"], histnorm="percent")
    ], layout=layout)

sentiment_distribution_histogram = dcc.Graph(
            id='sentiment_distribution_histogram',
            figure=fig,
            config={'modeBarButtonsToRemove': ['sendDataToCloud']}
        )



#Define app layout
app.layout = html.Div(children=[
    
    header,
    
    #First Section, two columns
    html.Div([
        html.H3("Entity Mentions in Most and Least Favourable Memes", style ={"text-align":"center","margin-top":40}),
        html.Div(
            className = "row",
            children=[
                html.Div(children=[bar_positive_entities], className="six columns"),
                html.Div(children=[bar_negative_entities], className="six columns"),
            ],
            style={}
        )
    ]),

    #Gallery Section
    html.Div([
        html.H3("Memes with Most Favourable Sentiments", style ={"text-align":"center","margin-top":40}),
        gallery_positive,
        html.H3("Memes with Least Favourable Sentiments", style ={"text-align":"center","margin-top":40}),
        gallery_negative,

    ]),

    #Historical Section
    html.Div([
        html.H3("Historical Sentiment Trend", style ={"text-align":"center","margin-top":40}),
        html.Div(
            className = "row",
            children=[
                #html.P("Content for section 2.", style ={"text-align":"center"}),
                historical_meme_sentiment
            ],
            style={}
        )
    ]),

    html.Div([
        html.H3("Sentiment Distribution", style ={"text-align":"center","margin-top":40}),
        sentiment_distribution_histogram

    ])

    
])

if __name__ == '__main__':
    app.run_server(debug=True)