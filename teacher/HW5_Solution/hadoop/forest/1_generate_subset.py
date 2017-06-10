# Goal: Process landsat_train.csv and extract
# a subset of 100,000 training instances
#
# Output: New files landsat_train_subset.csv and landsat_train_remaining.csv

import numpy

# Open files
landsat_train = open("landsat_train.csv", 'r')
landsat_train_subset = open("landsat_train_subset.csv", 'w')
landsat_train_remaining = open("landsat_train_remaining.csv", 'w')

# Generate sorted subset of indices. Since this
# list is relatively small, we can simply genearte
# and keep it in main memory
subset = sorted(numpy.random.choice(25667779, 100000, replace=False))

# Process training file line-by-line
counter = 0
counter_subset = 0

for line in landsat_train:

    if counter % 1000000 == 0:
        print("Processing line %i ..." % counter)

    if counter_subset < len(subset) and counter == subset[counter_subset]:
        # Append to subset file
        landsat_train_subset.write(line)
        counter_subset += 1
    else:
        # Append to remaining file
        landsat_train_remaining.write(line)

    counter += 1

# Close files
landsat_train.close()
landsat_train_subset.close()
landsat_train_remaining.close()
