import plotly.express as px
import pandas as pd

# visualize demographic as grouped bar chart

def survival_demographics():
    # Load Titanic dataset
    df = pd.read_csv('https://raw.githubusercontent.com/leontoddjohnson/datasets/main/data/titanic.csv')

    # Create a new column in the Titanic dataset that classifies passengers into age categories (i.e., a pandas `category` series). The categories should be:
#     - Child (up to 12) - Teen (13–19) - Adult (20–59) - Senior (60+)  
    bin_size = [0, 12, 19, 59, float('inf')]
    labels = ['Child', 'Teen', 'Adult', 'Senior']

    df['age_group'] = pd.cut(df['age'], bins=bin_size, labels=labels, right=True, include_lowest=True)

# 2. Group the passengers by class, sex, and age group. 
    grouped = (df
        .groupby(['pclass', 'sex', 'age_group'])
        .agg(
            count=('survived', 'size'),
            survived=('survived', 'sum')
            )
        .reset_index()
    )
    grouped['survival_rate'] = grouped['survived'] / grouped['count']


# 3. For each group, calculate:  

#     - The number of survivors, `n_survivors`
#     - The survival rate, `survival_rate`

    grouped['n_survivors'] = df[df['survived'] == 1].groupby(['pclass', 'sex', 'age_group']).size().values
    grouped['survival_rate'] = grouped['n_survivors'] / grouped['count']

# 4. Return a table that includes the results for *all* combinations of class, sex, and age group. 
# 5. Order the results so they are easy to interpret.  
    
    grouped = grouped.sort_values(by=['pclass', 'sex', 'age_group'])
    return grouped


# 6. Come up with a clear question that your results table makes you curious about (e.g., “Did women in first class have a higher survival rate than men in other classes?”). Write this question in your `app.py` file above the call to your visualization function, using `st.write("Your Question Here")`.



#exercise 2

def family_groups():
    # Load Titanic dataset
    df = pd.read_csv('https://raw.githubusercontent.com/leontoddjohnson/datasets/main/data/titanic.csv')


    # to explore the relationship between family size, passenger class, and ticket fare. 
# 1. Create a new column in the Titanic dataset that represents the total family size for each passenger, `family_size`. 
# Family size is defined as the number of siblings/spouses aboard plus the number of parents/children aboard, plus the passenger themselves.
    df['family_size'] = df['sibsp'] + df['parch']
    df['family_size'].value_counts(sorts=False)

    
# 2. Group the passengers by family size and passenger class. For each group, calculate:  
#    - The total number of passengers, `n_passengers`
#    - The average ticket fare, `avg_fare`
#    - The minimum and maximum ticket fares (to capture variation in wealth), `min_fare` and `max_fare`

    family_groups = (
        df.groupby(['family_size', 'pclass'])
        .agg(
            n_passengers=('passenger_id', 'size'),
            avg_fare=('fare', 'mean'),
            min_fare=('fare', 'min'),
            max_fare=('fare', 'max')
        )
        .reset_index()
    )

# 3. Return a table with these results, sorted so that the values are clear and easy to interpret (for example, by class and then family size).


# 4. Write a function called `last_names()` that extracts the last name of each passenger from the `Name` column, and returns the count for each last name (i.e., a pandas series with last name as index, and count as value). Does this result agree with that of the data table above? Share your findings in your app using `st.write`.

# 5. Just like you did in Exercise 1, come up with a clear question that your results makes you curious about. Write this question in your app.py file above the call to your visualization function. Then, create a Plotly visualization in a function named `visualize_families()` that directly addresses your question. As in Exercise 1 you are free to choose the chart type that you think best communicates the findings.
