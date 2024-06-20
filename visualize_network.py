#Import necessary libraries
import os
import networkx as nx
import matplotlib.pyplot as plt

#Internal dependencies
from nearest_neighbors import nearest_neighbors

def visualize_network(word, n,  dist_df):
    """
    Visualizes a network graph of a word and its nearest neighbors, and saves the image.
    
    Args:
    word (str): The central word of the network graph.
    n (int): Number of neighbors to include in the graph.
    dist_df (pd.DataFrame): DataFrame containing pairwise distances between words.
    """
    G = nx.Graph()
    
    # Get nearest neighbors for the central word
    neighbors = nearest_neighbors(word, n, dist_df)
    
    # Add the central node with specific styling
    G.add_node(word, size=20, color='red')
    
    # Add nodes and edges for each neighbor
    for neighbor in neighbors:
        G.add_node(neighbor['word'], size=10, color='blue')
        G.add_edge(word, neighbor['word'], weight=1 / neighbor['distance'])
    
    # Position nodes using a spring layout
    pos = nx.spring_layout(G)
    
    # Extract node colors and sizes for visualization
    colors = [G.nodes[n]['color'] for n in G]
    sizes = [G.nodes[n]['size'] for n in G]
    
    # Draw the network graph
    nx.draw_networkx_nodes(G, pos, node_color=colors, node_size=sizes)
    nx.draw_networkx_edges(G, pos, width=1.0, alpha=0.5)
    nx.draw_networkx_labels(G, pos, font_size=16, font_family='sans-serif')
    
    # Ensure the 'Graphs' directory exists
    if not os.path.exists('Graphs'):
        os.makedirs('Graphs')
    
    # Save the plot to the 'Graphs' folder
    plt.axis('off')  # Hide axes
    plt.savefig(f'Graphs/{word}_{n}_network.png', format='png')
    plt.close()  # Close the plot to free memory
