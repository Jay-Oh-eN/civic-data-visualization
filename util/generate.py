import pandas as pd
import os, pdb
import matplotlib.pyplot as plt
import seaborn as sns
import multiprocessing as mp

def make_plot(df, column):
    print "started generating: " + column
    fig = plt.figure()
    g = sns.FacetGrid(df, col="name", col_wrap=4, size=6)
    g.map(sns.violinplot, column, 'hour', color= "BrBG")
    plt.savefig('figures/' + column + '.png')
    print "finished generating: " + column

if __name__ == '__main__':
    df = pd.read_csv('data/transform.csv')
    columns = ['db', 'airquality_raw', 'dust', 'uv', 'humidity','light', 'temperature']

    # pool = mp.Pool(processes=4)
    # results = [pool.apply(make_plot, args=(df, x)) for x in columns]

    for column in columns:
        make_plot(df, column)