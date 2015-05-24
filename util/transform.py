import pandas as pd
import os, pdb

sensors = {
    'Urban Launchpad' : 'ci4yfbbdb000d03zzoq8kjdl0',
    'GlenParklifeLogger': 'ci4yhy9yy000f03zznho5nm7c',
    'ClimateNinja9000': 'ci4yyrdqi000j03zz8ylornqd',
    'Exploratorium': 'ci4vy1tfy000m02s7v29jkkx4',
    'Datavore': 'ci4lnqzte000002xpokc9d25v',
    'Grand Theater': 'ci4usvy81000302s7whpk8qlp',
    'mapsense' : 'ci4usvryz000202s7llxjafaf',
    'GehlData' : 'ci4xcxxgc000n02tci92gpvi6',
    'a-streetcar-named-data-sensor' : 'ci4usss1t000102s7hkg0rpqg',
    'AlleyCat' : 'ci4tmxpz8000002w7au38un50',
    'DataDonut' : 'ci4yf50s5000c03zzt4h2tnsq',
    'grapealope' : 'ci4ut5zu5000402s7g6nihdn0'
}

sensor_map = {y:x for x,y in sensors.iteritems()}

def create_features(df):
    df['timestamp'] = pd.to_datetime(df.timestamp)
    df['db'] = df.sound.apply(lambda x: 0.0158 * x + 49.184)

    # account for UTC
    df['hour'] = df.timestamp.map(lambda t: (t.hour - 7) % 24)
    return df

def map_names(df, map):
    df['name'] = df.source.map(map)
    return df

if __name__ == '__main__':
    df = pd.read_csv('data/data.csv')
    df = df[pd.notnull(df.sound)]
    df['sound'] = df.sound.astype(int)
    df = create_features(df)
    df = map_names(df, sensor_map)
    df.to_csv('data/transform.csv', index=False)

    df = df.set_index('timestamp')

    for name in df.name.unique():
        sub = df[df['name'] == name]
        sub.to_csv('data/csv/' + name + '.csv')
        agg = sub.resample('30S', how='mean')
        agg['hour'] = agg.index.map(lambda t: t.hour)
        agg['name'] = name
        agg = agg[pd.notnull(agg.db)]
        agg.to_csv('data/csv/30sec_agg_' + name + '.csv')
