import pandas as pd
import numpy as np
import matplotlib as plt

import seaborn as sns
sns.set_theme()

def plot_path(csv_path):
    """
        input: A path to a csv file containing coordinates
        output: The csv file cleaned, a png plotting the path followed, a png plotting the position heatmap

        returns: nothing
    """

    positions = pd.read_csv(csv_path, index_col="Unnamed: 0", converters={'0': pd.eval})

    positions["x"] = positions["0"].apply(lambda coords: coords[0])
    positions["y"] = positions["0"].apply(lambda coords: 480-coords[1])
    positions.drop("0", axis=1, inplace=True)

    positions.to_csv(f"{csv_path[:-4]}_clean.csv")

    ax = sns.scatterplot(data=positions, x="x", y="y", color="gold")
    ax.set(title='Tracked positions')
    ax.set(xlabel="X", ylabel="Y", xlim=(0, 640), ylim=(0, 480))
    ax.set()
    fig = ax.get_figure()
    fig.savefig(f'./images/{csv_path[7:17]}_tracked_positions_plot.png',bbox_inches='tight')

    ax2 = sns.histplot(data=positions, x="x", y="y", color="gold")
    ax2.set(title='Position Heatmap')
    ax2.set(xlabel="X", ylabel="Y", xlim=(0, 640), ylim=(0, 480))
    fig = ax.get_figure()
    fig.savefig(f'./images/{csv_path[7:17]}_heatmap_positions_plot.png',bbox_inches='tight')

    return None

