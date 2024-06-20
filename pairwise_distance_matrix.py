# Import necessary libraries
import pandas as pd
from scipy.spatial import distance_matrix

def pairwise_distance_matrix(fraction: float = 1.0):
    """
    Generates a pairwise distance matrix for word embeddings.
    
    Args:
    fraction (float): Fraction of the data to sample from the dataset. Default is 1.0 (100% of the data).

    Returns:
    pd.DataFrame: A DataFrame where rows and columns are words and cell values are distances.
    """

    # Load the dataset from an Excel file located in a Data folder
    df = pd.read_excel('./Data/model_root_2024_mohammed.xlsx')
    
    # Sample a fraction of the data to reduce computation time if needed
    df_fraction = df.sample(frac=fraction)
    
    # Update the dataframe to only include the sampled data
    df = df_fraction

    # Split the 'global_encoding' column into multiple columns at each ':'
    split_columns = df['global_encoding'].str.split(':', expand=True)
    
    # Rename the newly created columns to 'dim_1', 'dim_2', ..., 'dim_n'
    split_columns.columns = [f'dim_{i+1}' for i in range(split_columns.shape[1])]
    
    # Concatenate the new dimensions back to the original dataframe
    new_df = pd.concat([df['word_raw'], split_columns], axis=1)

    # Generate a list of new column names for embeddings to numeric conversion
    embedding_columns = [f'dim_{i+1}' for i in range(128)]  # Assumes 128 dimensions for embeddings
    
    # Convert all embedding columns to numeric, coercing errors to NaN (useful for corrupt data)
    new_df[embedding_columns] = new_df[embedding_columns].apply(pd.to_numeric, errors='coerce')
    
    # Extract the numerical embeddings into a NumPy array for distance computation
    embeddings = new_df[embedding_columns].values
    
    # Calculate the pairwise distance matrix using the embeddings
    dist_matrix = distance_matrix(embeddings, embeddings)
    
    # Create a DataFrame from the distance matrix, labeling rows and columns with the corresponding words
    dist_df = pd.DataFrame(dist_matrix, index=new_df['word_raw'], columns=new_df['word_raw'])

    # Return the DataFrame containing the pairwise distances
    return dist_df
