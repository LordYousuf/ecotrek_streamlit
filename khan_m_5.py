import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import streamlit as st

# Streamlit App title
st.title("Data Visualization App")

# First section: Sales vs Temperature Correlation
st.header("Sales vs Temperature Correlation")

# Load data
df_sales = pd.read_excel("IA 4_LastYearSales.xlsx")
st.write(df_sales.head())  # Display the first few rows of the dataframe

# Create scatter plot
fig_sales = px.scatter(df_sales, x="Temperature (°F)", y="GreenTote",
                       trendline="ols",
                       title="Correlation Between Sales and Temperature",
                       labels={"Temperature": "Temperature (°F)", "GreenTote": "GreenTote Sales Performance"},
                       opacity=0.6)

# Display the figure in the Streamlit app
st.plotly_chart(fig_sales)

# Second section: Customer Sentiment Distribution
st.header("Customer Sentiment Polarity Distribution")

# Load sentiment data
df_sentiment = pd.read_csv("Khan_Muhammad_sentiment.csv")
expected_categories = ["Positive", "Neutral", "Negative"]

# Process sentiment counts
sentiment_counts = df_sentiment["Sentiment_Label"].value_counts().reindex(expected_categories, fill_value=0)

# Create bar chart
categories = sentiment_counts.index.tolist()
values = sentiment_counts.values.tolist()

color_map = {"Positive": "green", "Neutral": "gray", "Negative": "red"}
bar_colors = [color_map.get(sentiment, "blue") for sentiment in categories]

fig_sentiment = go.Figure(data=[go.Bar(x=categories, y=values, marker=dict(color=bar_colors))])
fig_sentiment.update_layout(title='Customer Sentiment Polarity Distribution',
                            xaxis_title='Sentiment Category',
                            yaxis_title='Number of Reviews',
                            template='plotly_white')

# Display the figure in the Streamlit app
st.plotly_chart(fig_sentiment)

# Third section: Word Cloud for Reviews
st.header("Word Cloud for Reviews")

# Create and display word clouds for each sentiment category
df_sentiment['Sentiment_Label'] = df_sentiment['Sentiment_Label'].str.lower()

positive_reviews = " ".join(df_sentiment[df_sentiment['Sentiment_Label'] == 'positive']['Review'].dropna())
neutral_reviews = " ".join(df_sentiment[df_sentiment['Sentiment_Label'] == 'neutral']['Review'].dropna())
negative_reviews = " ".join(df_sentiment[df_sentiment['Sentiment_Label'] == 'negative']['Review'].dropna())

def generate_wordcloud(text, color, title):
    wordcloud = WordCloud(width=800, height=400, background_color=color, colormap="coolwarm").generate(text)
    plt.figure(figsize=(8, 4))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.title(title, fontsize=14)
    st.pyplot(plt)

# Generate and display word clouds
generate_wordcloud(positive_reviews, "white", "Positive Reviews Word Cloud")
generate_wordcloud(neutral_reviews, "lightgray", "Neutral Reviews Word Cloud")
generate_wordcloud(negative_reviews, "black", "Negative Reviews Word Cloud")
