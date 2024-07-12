# 2 Macro Hypotheses

##  First hypothesis: select most relevant features to predict avg_rating



   - H1: Restaurants with more awards tend to have higher average rating.

   - H2: Restaurants that offer more options for vegan, gluten-free, and other dietary preferences tend to have higher average rating.

   - H3: As the number of cuisine types offered increase, the average rating tends to decrease.
   
   - H4: Restaurants in city with high population tends to have higher average rating than restaurants located in low population cities.


## Metrics
To prove/disprove the first hypothesis, we can propose the following metrics:

- num_award. The number of awards. This metrics is linked to H1.
- vegetarian_friendly, vegan_options, gluten_free. They are defined as binary value that tells if the restaurant offers the related option or not. This metrics is linked to H2.
- Num_cuisines. The number of cuisines offered by the restaurant. It is defined by counting the distinct types of value in cuisines. This metrics is linked to H3.
- Population. The number of inhabitants for city in which the restaurant is located. This metrics is linked to H4.


## Second hypothesis: explain the bias of the predictions
   - Use the hypotheses and relevant features to predict the final price range of restaurants.

7. **Bias Analysis**:
   - After preparing the dataset, select 50 rows and evaluate them.
   - Compare the predictions from our model with the actual ratings to identify potential bias in the reviews.
