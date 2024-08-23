import os 
import sys
import pandas as pd
from visualize_network import visualize_network
from nearest_neighbors import nearest_neighbors
from scipy.spatial import distance_matrix
import matplotlib.pyplot as plt
import argparse

from distance_between_words import distance_between_words



def nearest_neighbors(word, n, dist_df):
    """
    Finds the n nearest neighbors of a given word in a provided distance matrix.
    
    Args:
    word (str): The word to find the neighbors for.
    n (int): Number of neighbors to retrieve.
    dist_df (pd.DataFrame): A DataFrame where each row and column represent words,
                            and the values are the distances between them.

    Returns:
    list: A list of dictionaries where each dictionary contains a 'word' and its 'distance'
          from the input word. If the word is not found, returns a string message.
    """

    # Retrieve the row corresponding to 'word', which contains distances to all other words
    distances = dist_df.loc[word]

    # Sort the distances while excluding the first element (distance to itself, which is zero)
    nearest = distances.sort_values().iloc[1:n+1]

    # Create a list of dictionaries for each neighboring word and its distance
    neighbors = [{'word_raw': idx, 'distance': dist} for idx, dist in nearest.items()]

    # Check if 'the' is in the nearest neighbors but not included in the final list (due to an edge case or a bug)
    if 'the' in nearest and 'the' not in [neighbor['word_raw'] for neighbor in neighbors]:
        # Extract the distance to 'the' from the DataFrame
        the_distance = distances['the']
        
        # Append the missing 'the' to the list of neighbors
        neighbors.append({'word_raw': 'the', 'distance': the_distance})
    
    # Return the list of nearest neighbors
    return neighbors

from scipy.spatial import distance_matrix
import matplotlib.pyplot as plt

from distance_between_words import distance_between_words



def plot_word_distances(data, specific_word, n):
    """
    Plots the distances over epochs for different words, given a DataFrame where
    each 'word' column contains a dictionary with 'word_raw' and other details.

    Args:
    data (list of dicts): The data containing epochs, words, and distances.
    """
    # Convert list of dictionaries to a DataFrame
    df = pd.DataFrame(data)

    # Flatten the 'word' column to extract the 'word_raw' and sort by 'epoch'
    df['word'] = df['word'].apply(lambda x: x['word_raw'])
    df.sort_values(by='epoch', inplace=True)

    # Get unique words for plotting
    unique_words = df['word'].unique()
    
    plot = plt.figure(figsize=(10, 6))

    for word in unique_words:
        # Filter data for each word and plot
        word_data = df[df['word'] == word]
        plt.plot(word_data['epoch'], word_data['distance'], label=word)  # Plot each word's time series

    plt.xlabel('Epoch')
    plt.ylabel('Distance')
    plt.title('Distance of Words Over Epochs')
    plt.legend()
    plt.grid(True)
    plt.show()

    plt.savefig(f'Graphs/{specific_word}_{n}.png')


def load_csv_dataframes(directory):
    files = os.listdir(directory)
    data_list = []
    for file in files:
        if file.endswith('_pdist.csv'):
            epoch = int(file.split('_')[0])
            dataframe = pd.read_csv(os.path.join(directory, file))
            if 'word_raw' in dataframe.columns:
                dataframe.set_index('word_raw', inplace=True)
            data_list.append({'epoch': epoch, 'dataframe': dataframe})
    return data_list

def find_latest_epoch_csv(directory):
    files = os.listdir(directory)

    
    max_epoch = -1
    latest_file = None
    
    for file in files:
        if file.endswith('_pdist.csv'):
            epoch = int(file.split('_')[0])
            if epoch > max_epoch:
                max_epoch = epoch
                latest_file = file
    
    return latest_file


word_list_g = []


def load_csv_dataframes(directory):
    files = os.listdir(directory)
    data_list = []
    for file in files:
        if file.endswith('_pdist.csv'):
            epoch = int(file.split('_')[0])
            dataframe = pd.read_csv(os.path.join(directory, file))
            if 'word_raw' in dataframe.columns:
                dataframe.set_index('word_raw', inplace=True)
            data_list.append({'epoch': epoch, 'dataframe': dataframe})
    return data_list

def find_latest_epoch_csv(directory):
    files = os.listdir(directory)

    
    max_epoch = -1
    latest_file = None
    
    for file in files:
        if file.endswith('_pdist.csv'):
            epoch = int(file.split('_')[0])
            if epoch > max_epoch:
                max_epoch = epoch
                latest_file = file
    
    return latest_file

def main():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('specific_word', type=str, help='Specific word to analyze')
    parser.add_argument('n', type=int, help='Number of nearest neighbors')
    args = parser.parse_args()
    directory = 'distance_matrices/'
    max_epoch = find_latest_epoch_csv(directory)
    dataframess = pd.read_csv(directory + '/' + max_epoch)
    if 'word_raw' in dataframess.columns:
            dataframess.set_index('word_raw', inplace=True)

    words = nearest_neighbors(args.specific_word, args.n, dataframess)
    dataframes = load_csv_dataframes(directory)
    word_list = []
    for word in words:
        for dataframe in dataframes:
            if 'word_raw' in dataframe['dataframe'].columns:
                dataframe['dataframe'].set_index('word_raw', inplace=True)

            distance_dict = {
                "epoch": dataframe['epoch'],
                "word": word,
                "distance": distance_between_words('hello', word['word_raw'], dataframe['dataframe']),
            }
            word_list.append(distance_dict)
    plot_word_distances(word_list, args.specific_word, args.n)

if __name__ == "__main__":
    main()