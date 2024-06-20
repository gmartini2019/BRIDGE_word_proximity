import sys
import pandas as pd
from visualize_network import visualize_network
from nearest_neighbors import nearest_neighbors

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
        dist_df = pd.read_csv(file_path)

        # Retrieve the nearest neighbors
        neighbors = nearest_neighbors(word, n, dist_df)
        print(f'The {n} nearest neighbors, for the word {word}, are the following:')
        print(neighbors)
        # Visualize the network
        visualize_network(word, n, dist_df) 

        print(f"Network graph saved in 'Graphs/{word}_network.png'")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()