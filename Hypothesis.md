# Hypotheses and Dataset Analysis

## Hypotheses



   - H1: Restaurants with more awards tend to have higher average rating.

   - H2: Restaurants that offer more options for vegan, gluten-free, and other dietary preferences tend to have higher average rating.

   - H3: Restaurants with higher average price tend to have higher average rating.

   - H4: As the number of cuisine types offered increase, the average rating tends to decrease.

   - H5: As the number of features offered increase, the average rating tends to increase.
   
   - H6: The longer the restaurant's opening hours per week, the average rating tends to decrease.

   - H7: Restaurants in city with high population tends to have higher average rating than restaurants located in low population cities.


## Metrics
To prove/disprove our hypotheses, we can propose the following metrics:

- num_award. The number of awards. This metrics is linked to H1.
- vegetarian_friendly, vegan_options, gluten_free. They are defined as binary value that tells if the restaurant offers the related option or not. This metrics is linked to H2.
- Avg_price. The average price set by the restaurant. It is defined as medium between the minimum value and the maximum value in price_range. This metrics is linked to H3.
- Num_cuisines. The number of cuisines offered by the restaurant. It is defined by counting the distinct types of value in cuisines. This metrics is linked to H4.
- Num_features. The number of features offered by the restaurant. It is defined by counting the distinct types of value in features. This metrics is linked to H5.
- Open_hours_per_week. The number of hours for week the restaurant is open. This metrics is linked to H6.
- Population. The number of inhabitants for city in which the restaurant is located. This metrics is linked to H7.


## Bonus Task
   - Use the hypotheses and relevant features to predict the final price range of restaurants.

7. **Bias Analysis**:
   - After preparing the dataset, select 200 rows and evaluate them.
   - Compare the predictions from our model with the actual ratings to identify potential bias in the reviews.
