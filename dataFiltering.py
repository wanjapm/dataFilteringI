#!/usr/bin/env python
# coding: utf-8

# In[322]:


path = "/mnt/c/Users/user/Downloads/amazon_reviews_us_Gift_Card_v1_00.tsv.gz"


# In[323]:


import gzip
import csv
f = gzip.open(path,'rt', encoding='utf8')


# In[324]:


reader = csv.reader(f,delimiter='\t')


# In[325]:


header = next(reader)


# In[326]:


dataset = []
for line in reader:
    d = dict(zip(header,line))
    # convert fields to numbers or boolean where possible    
    for field in ['star_rating', 'helpful_votes', 'total_votes']:
        d[field] = int(d[field])
    for field in ['vine', 'verified_purchase']:
        if d[field] == 'Y':
            d[field] =  True
        else:
            d[field] =  False

    dataset.append(d)

len(dataset)


# In[327]:


print("Sample dataset:")
print(dataset[0])


# In[328]:


# filter reviews according to year (remove old reviews before the year 2010)
# some records do not have the key 'review_date', check for it otherwise key error
dataset = [d for d in dataset if 'review_date' in d]
len(dataset)


# In[329]:


for d in dataset:
    d['yearInt'] = int(d['review_date'][:4])


# In[330]:


dataset = [d for d in dataset if d['yearInt'] > 2009]
print(f"Number of reviews made before the year 2010: {len(dataset)}")


# In[331]:


# keep reviews that haven't recieved many votes yet or where more than half of review votes considered review helpful
# helpful reviews
dataset = [d  for d in dataset if d['total_votes'] < 3 or d['helpful_votes'] / d['total_votes'] >=0.5]
print(f"Number of 'helpful' reviews: {len(dataset)}")


# In[332]:


from collections import defaultdict
nReviewsPerUser = defaultdict(int)
# how many reviews per user
for d in dataset:
    nReviewsPerUser[d['customer_id']] +=1


# In[333]:


# filter users who have written 2 or more reviews
dataset = [d for d in dataset if nReviewsPerUser[d['customer_id']]>1]
print(f"Number of reviews made by users who have made 2 or more reviews: {len(dataset)}")


# In[334]:


# filter out reviews which have less than 10 words as uninformative
dataset = [d for d in dataset if len(d['review_body'].split()) > 9]
print(f"Number of reviews which have more than 10 words (informative): {len(dataset)}")


# In[335]:


# filter products that have few reviews
nReviewsPerProduct = defaultdict(int)
for d in dataset:
    nReviewsPerProduct[d['product_id']] +=1


# In[336]:


dataset = [d for d in dataset if nReviewsPerProduct[d['product_id']] > 10 ]
print(f"Number of reviews for products with more than 10 reviews: {len(dataset)}")


# In[337]:


# filter out users who have only given 5 star ratings
userReviews = defaultdict(list)
for d in dataset:
    userReviews[d['customer_id']].append(d['star_rating'])
    


# In[338]:


dataset =  [d for d in dataset if userReviews[d['customer_id']].count(5) != len(userReviews[d['customer_id']])]
print(f"Number of reviews without reviews by users who have only given 5 star ratings: {len(dataset)}")


# In[339]:


# filter out users who have not written a review in the past year
from datetime import datetime
from datetime import timedelta

today = datetime.today()
oneyearago = today - timedelta(days=365)


# In[340]:


userReviewYears = defaultdict(list)
for d in dataset:
    userReviewYears[d['customer_id']].append(datetime.strptime(d['review_date'],'%Y-%m-%d'))


# In[341]:


dataset = [d for d in dataset if max(userReviewYears[d['customer_id']]) >= oneyearago ]
len(dataset)
print(f"Number of reviews made in the past year {len(dataset)}")


# In[342]:


# filter reviews that are not part of the vine program
dataset = [d for d in dataset if d['vine']]
print(f"Number of reviews made by members of the vine program: {len(dataset)}")


# In[ ]:




