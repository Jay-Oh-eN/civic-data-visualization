# all:
# #download:
# update:
# upload:
# parse:
# transform:
# generate:


# download historical files from S3

# scrape any additional data needed since last archive

# upload new data to S3

# concatenate all of the data files into one for each sensor

data/json: util/download.py
	python util/download.py
	touch data/json

# parse all of the json files into CSV
data/csv: data/json
	python util/parse.py
	touch data/csv

# concatenate CSV
data/data.csv: data/csv
	cat data/csv/* > data/data.csv

# generate more features to visualize by creating a dB and hour column
# also parse the timestamps and create a column of the sensor names.
data/transform.csv: util/transform.py data/data.csv
	python util/transform.py

# create violin plots, calculate summary statistics, and line plot of means
figures: util/generate.py data/transform.csv
	python util/generate.py

clean:
	rm data/json*
	rm data/csv/*
	rm data/data.csv
	rm data/transform.csv
	rm data/trees.csv
	rm figures/*
