import pandas as pd

def distance_between_words(word1, word2, dist_df):
    """
    Finds the distance between two given words in a provided distance matrix.

    Args:
    word1 (str): The first word.
    word2 (str): The second word to find the distance to.
    dist_df (pd.DataFrame): A DataFrame where each row and column represent words,
                            and the values are the distances between them.

    Returns:
    float or str: The distance between the two words if both are found in the DataFrame,
                  otherwise returns an error message if one or both words are missing.
    """
    # Check if both words are in the DataFrame
    if word1 not in dist_df.index or word2 not in dist_df.columns:
        return "One or both words not found in the distance matrix."

    # Retrieve the distance between word1 and word2
    distance = dist_df.loc[word1, word2]

    # Return the distance
    return distance