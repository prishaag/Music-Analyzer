#calculations, and create visuals
# we need to output calculation into a txt file
import os
import sqlite3
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import linregress



def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

# returns lists of yt data
def meanYtData(cur):
    cur.execute("SELECT ytprimary.id, views, likes, comments FROM ytprimary JOIN ytsecondary WHERE ytprimary.id = ytsecondary.id ORDER BY ytprimary.id")
    songs = cur.fetchall()
    viewTotals = 0
    likeTotals = 0
    commentTotals = 0
    viewMeans = []
    likeMeans = []
    commentMeans = []
    for view in songs:
        viewTotals += view[1]
        likeTotals += view[2]
        commentTotals += view[3]
        if view[0] % 10 == 0:
            viewMeans.append(((viewTotals / 10), (view[0])))
            likeMeans.append(((likeTotals / 10), (view[0])))
            commentMeans.append(((commentTotals / 10), (view[0])))
    return viewMeans, likeMeans, commentMeans           
        
# returns list of spotify data as tuples
def meanSpotifyData(cur):
    cur.execute("SELECT spotify.id, popularity, danceability, tempo, master.title, master.artist FROM spotify JOIN master WHERE spotify.id = master.id ORDER BY spotify.id")
    songs = cur.fetchall()
    return songs
    
# returns audio features for visualizations
def getAudioFeatures(cur):
    cur.execute("SELECT popularity, danceability, tempo FROM spotify")
    audio_features = cur.fetchall()
    return audio_features

# creates line plot and takes in plot parameters
def createLinePlot(ax, data, xLabel, yLabel, plotTitle):
    xValues = [item[1] for item in data]
    yValues = [item[0] for item in data]
    ax.plot(xValues, yValues, marker='o')
    ax.set_xlabel(xLabel)
    ax.set_ylabel(yLabel)
    ax.set_title(plotTitle)

# creates histogram and takes in plot parameters
def createHistogram(ax, featureData, featureName):
    ax.hist(featureData, bins=20, color='skyblue', edgecolor='black')
    ax.set_xlabel(featureName)
    ax.set_ylabel('Frequency')
    ax.set_title(f'Histogram of {featureName}')
    ax.grid(axis='y', linestyle='--', alpha=0.7)

# creates scatter plot with given parameters
def createScatterPlot(ax, xValues, yValues, xLabel, yLabel, plotTitle):
    ax.scatter(xValues, yValues, marker='o', label='Data')

    # regression line
    slope, intercept, r_value, p_value, std_err = linregress(xValues, yValues)
    line = slope * np.array(xValues) + intercept
    ax.plot(xValues, line, color='red', label=f'Correlation: {r_value:.2f}')

    ax.set_xlabel(xLabel)
    ax.set_ylabel(yLabel)
    ax.set_title(plotTitle)
    ax.legend()

def main():
    cur, conn = setUpDatabase('database.db')
    views, likes, comments = meanYtData(cur)
    f = open('calculation.txt', 'w')
    f.write("Mean Views by Ranking\n")
    for view in views:
        f.write(f'songs ranked {view[1]-10}-{view[1]} mean views: ')
        f.write(str(view[0]) + '\n')
    f.write("\nMean Likes by Ranking\n")
    for like in likes:
        f.write(f'songs ranked {like[1]-10}-{like[1]} mean likes: ')
        f.write(str(like[0]) + '\n')
    f.write("\nMean Comments by Ranking\n")
    for cm in comments:
        f.write(f'songs ranked {cm[1]-10}-{cm[1]} mean comments: ')
        f.write(str(cm[0]) + '\n')
    spotifyData = meanSpotifyData(cur)
    f.write("\nSong stats by rank\n")
    for d in spotifyData:
        f.write(f'{d[0]}. "{d[4]}" by {d[5]}:\n') 
        f.write(f'Popularity: {d[1]},    Danceablity: {d[2]},    Tempo {d[3]}\n\n')
        
    audioFeatures = getAudioFeatures(cur)

    # individual audio features
    popularity = [feature[0] for feature in audioFeatures]
    danceability = [feature[1] for feature in audioFeatures]
    tempo = [feature[2] for feature in audioFeatures]

    # setting up subplots
    fig, axs = plt.subplots(3, 3, figsize=(15, 12))

    # creating scatter plots for yt data
    createLinePlot(axs[0, 0], views, 'Ranking Intervals (higher is lower rank)', 'Mean Views by Ranking Intervals', 'Mean Views by Ranking Intervals')
    createLinePlot(axs[0, 1], likes, 'Ranking Intervals (higher is lower rank)', 'Mean Likes by Ranking Intervals', 'Mean Likes by Ranking Intervals')
    createLinePlot(axs[0, 2], comments, 'Ranking Intervals (higher is lower rank)', 'Mean Comments by Ranking Intervals', 'Mean Comments by Ranking Intervals')

    # creating scatter plots for spotify data
    createScatterPlot(axs[1, 1], popularity, tempo, 'Popularity', 'Tempo', 'Tempo by Popularity')
    createScatterPlot(axs[1, 0], popularity, danceability, 'Popularity', 'Danceability', 'Danceability by Popularity')

    # creating histograms for spotify audio features
    createHistogram(axs[2, 0], danceability, 'Danceability')
    createHistogram(axs[2, 1], tempo, 'Tempo')
    plt.tight_layout()
    plt.show()
    
    print(audioFeatures)

main()