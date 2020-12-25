Using dataset: amazon_reviews_us_Gift_Card_v1_00.tsv.gz from https://s3.amazonaws.com/amazon-reviews-pds/tsv/index.txt 

Perfom some simple data filtering

* Filter reviews according to year (remove old reviews before the year 2010)
* Keep reviews that haven't recieved many votes yet or where more than half of review votes considered review helpful
* Keep users who have written 2 or more reviews
* Filter out reviews which have less than 10 words as uninformative
* Filter products that have few reviews (less than 10)
* Filter out users who have only given 5 star ratings
* Filter out users who have not written a review in the past year
* Filter reviews that are not part of the vine program

