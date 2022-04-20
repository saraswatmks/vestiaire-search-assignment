### How to run ?

1. Unzip the data
2. Go to the project root
3. Create a conda env using `make create_environment`
4. Activate the env using `conda activate search`
5. Code can be executed using command line but the keywords indexing needs to be done everytime. So is better to use ipython in terminal.

Run the following code from the project root to run search:

```python
>>> ipython
>>> from src.query import QueryToCategory
>>> q = QueryToCategory()
>>> q.search("black trouser")
>>> q.search("prada")
```

### Approach Taken

TLDR; My approach is build on the hypothesis that page views following a search query would share same category. For ex. if a user searches for 'shoes', chances are less immediate clicks will happen on bags. So there exists a signal in this sequential data.

#### Data set

- The data set contains session level interaction of a user with search & product pages.
- The immediate click sequence can leveraged to learn the similarity between a query and what category it belongs.
- We drop the sessions with no clicks since it provides no signal.
- We group search and immediate page views per session in one group. So, if one session has two search queries, it results in two groups.
- Finally, we create a grouped list of keywords for each category. The list of keywords is a combination of search queries and product titles.

#### Model

- We use sqlite FTS (Full text search) module to mock an in memory search engine.

### Other possible options

This problem can be solved in other ways too, such as:

- Using embeddings: We can generate embedding at word level or character level, then map the new query to the category of existing queries in our search logs using a similarity score.
- Using neural network: Using search queries -> category as training data set, we build a network using softmax at the final layer which predicts the probability of a query belonging to a particular category. This approach provides us the flexibility of either learning the representations of the queries or using them from a pretrained model.
