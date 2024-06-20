import sys
import pandas as pd
from visualize_network import visualize_network
from nearest_neighbors import nearest_neighbors
from scipy.spatial import distance_matrix

def main():
    """
    Main function to process input arguments and visualize the network of a given word.
    """
    if len(sys.argv) != 4:
        print("Usage: python main.py <word> <n> <filename>")
        sys.exit(1)

    # Extract arguments
    word = sys.argv[1]
    n = int(sys.argv[2])
    filename = sys.argv[3]

    # Create the file path
    file_path = f'Data/{filename}'

    try:
        # Load the distance matrix from the specified file
        print("Getting the df")
        df = pd.read_excel(file_path)

        split_columns = df['global_encoding'].str.split(':', expand=True)
        split_columns.columns = [f'dim_{i+1}' for i in range(split_columns.shape[1])]
        new_df = pd.concat([df['word_raw'], split_columns], axis=1)

        embedding_columns = [f'dim_{i+1}' for i in range(128)]
        new_df[embedding_columns] = new_df[embedding_columns].apply(pd.to_numeric, errors='coerce')
        embeddings = new_df[embedding_columns].values
        dist_matrix = distance_matrix(embeddings, embeddings)
        dist_df = pd.DataFrame(dist_matrix, index=new_df['word_raw'], columns=new_df['word_raw'])

        # Retrieve the nearest neighbors
        neighbors = nearest_neighbors(word, n, dist_df)
        print(f'The {n} nearest neighbors, for the word {word}, are the following:')
        print(neighbors)
        # Visualize the network
        visualize_network(word, n, dist_df) 

        print(f"Network graph saved in 'Graphs/{word}_{n}_network.png'")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()