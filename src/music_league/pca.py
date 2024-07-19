from sklearn.decomposition import PCA

import seaborn as sns
import matplotlib.pyplot as plt

from .data import load_from_zip

def main() -> None:
    sns.set_theme()
    sns.set_style("white")

    data = load_from_zip('export.zip')

    subs = data.submissions[['Submitter ID', 'Round ID', 'Spotify URI']]
    votes = data.votes[['Round ID', 'Spotify URI', 'Voter ID', 'Points Assigned']].set_index(
        ['Round ID', 'Spotify URI']
    )

    targeted_votes = subs.join(votes, on=['Round ID', 'Spotify URI']).drop(['Round ID', 'Spotify URI'], axis='columns')
    normed = (
        targeted_votes.groupby(['Voter ID', 'Submitter ID'])
        .sum()
        .transform(lambda x: (x - x.mean()) / x.std())
        .reset_index()
    )

    all_votes = normed

    table = all_votes.pivot(index='Voter ID', columns='Submitter ID', values='Points Assigned')

    arr = table.to_numpy(na_value=0.0)

    results = PCA(n_components=2).fit_transform(arr)

    x = [r[0] for r in results]
    y = [r[1] for r in results]
    names = [row[1] for row in data.competitors.values]

    ax = sns.scatterplot(x=x, y=y, style=names, hue=names, legend=False)

    for (x, y, n) in zip(x, y, names):
        ax.text(x, y-0.1, n, ha='center', va='top', size=4)

    ax.axhline(y=0, color='#DDDDDD', lw=1)
    ax.axvline(x=0, color='#DDDDDD', lw=1)
    plt.savefig('ml.png', dpi=300)
