import numpy as np
import pandas as pd
from sklearn.preprocessing import normalize, LabelEncoder

def split_data(df, look_back=12, ratio=0.8, predict_n=5, Y_column=0):
    """
    Split the data into training and test sets
    Keras expects the input tensor to have a shape of (nb_samples, timesteps, features).
    :param df: Pandas dataframe with the data.
    :param look_back: Number of weeks to look back before predicting
    :param ratio: fraction of total samples to use for training
    :param predict_n: number of weeks to predict
    :param Y_column: Column to predict
    :return:
    """
    df = np.nan_to_num(df.values).astype("float32")
    # n_ts is the number of training samples also number of training sets
    # since windows have an overlap of n-1
    n_ts = df.shape[0] - look_back - predict_n
    data = np.empty((n_ts, look_back + predict_n, df.shape[1]))
    for i in range(n_ts - predict_n):
        #         print(i, df[i: look_back+i+predict_n,0])
        data[i, :, :] = df[i: look_back + i + predict_n, :]
    train_size = int(n_ts * ratio)
    print(train_size)
    train = data[:train_size, :, :]
    test = data[train_size:, :, :]
    #     np.random.shuffle(train)
    # We are predicting only column 0
    X_train = train[:-look_back, :look_back, :]
    Y_train = train[look_back:, -predict_n:, Y_column]
    X_test = test[:-look_back, :look_back, :]
    Y_test = test[look_back:, -predict_n:, Y_column]

    return X_train, Y_train, X_test, Y_test


def normalize_data(df):
    """
    Normalize features in the example table
    :param df:
    :return:
    """
    if 'municipio_geocodigo' in df.columns:
        df.pop('municipio_geocodigo')

    for col in df.columns:
        if col.startswith('nivel'):
            # print(col)
            le = LabelEncoder()
            le.fit(df[col])
            df[col] = le.transform(df[col])

    norm = normalize(df, norm='l2', axis=0)
    df_norm = pd.DataFrame(norm, columns=df.columns)

    return df_norm
