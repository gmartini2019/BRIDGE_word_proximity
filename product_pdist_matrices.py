import numpy as np
import pandas as pd
from scipy.spatial import distance_matrix
import glob
import sys


def compute_distance_matrices(base_name: str, folder_path: str, dimensions: int):
    checkpoints = []
    csv_files = glob.glob(folder_path + '/' + base_name)
    print(folder_path + '/' + base_name)
    dataframes = [pd.read_csv(file) for file in csv_files]

    pairwise_distances = []

    for index, dataframe in enumerate(dataframes):
        print(f'DATAFRAME #{str(index)}')
        split_columns = dataframe['global_encoding'].str.split(':', expand=True)
        split_columns.columns = [f'dim_{i+1}' for i in range(split_columns.shape[1])]
        new_df = pd.concat([dataframe['word_raw'], split_columns], axis=1)
        embedding_columns = [f'dim_{i+1}' for i in range(dimensions)]
        new_df[embedding_columns] = new_df[embedding_columns].apply(pd.to_numeric, errors='coerce')
        embeddings = new_df[embedding_columns].values
        dist_matrix = distance_matrix(embeddings, embeddings)
        dist_df = pd.DataFrame(dist_matrix, index=new_df['word_raw'], columns=new_df['word_raw'])
        epoch_dict = {
            'epoch': index,
            'distance_matrix': dist_df
        }
        pairwise_distances.append(epoch_dict)
    return pairwise_distances


def main():

    base_name = sys.argv[1]
    folder_path = sys.argv[2]
    dimensions = int(sys.argv[3]) 

    pdist_matrices = compute_distance_matrices(base_name, folder_path, dimensions)

    for matrix in pdist_matrices:
        epoch = matrix['epoch']
        print(f'Converting to csv the epoch: {epoch}')
        matrix['distance_matrix'].to_csv(f'distance_matrices/{epoch}_pdist.csv')

if __name__ == "__main__":
    main()
    

