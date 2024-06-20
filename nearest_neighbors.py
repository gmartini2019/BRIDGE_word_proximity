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

    # Check if the word is in the index of the DataFrame
    if word not in dist_df.index:
        return "Word not found in dataset."

    # Retrieve the row corresponding to 'word', which contains distances to all other words
    distances = dist_df.loc[word]

    # Sort the distances while excluding the first element (distance to itself, which is zero)
    nearest = distances.sort_values().iloc[1:n+1]

    # Create a list of dictionaries for each neighboring word and its distance
    neighbors = [{'word': idx, 'distance': dist} for idx, dist in nearest.items()]

    # Check if 'the' is in the nearest neighbors but not included in the final list (due to an edge case or a bug)
    if 'the' in nearest and 'the' not in [neighbor['word'] for neighbor in neighbors]:
        # Extract the distance to 'the' from the DataFrame
        the_distance = distances['the']
        
        # Append the missing 'the' to the list of neighbors
        neighbors.append({'word': 'the', 'distance': the_distance})
    
    # Return the list of nearest neighbors
    return neighbors
