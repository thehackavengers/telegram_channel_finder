import pandas as pd


def save_csv(data):

    df = pd.DataFrame(data)

    df.to_csv("data/channels.csv", index=False)

    return df