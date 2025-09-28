import plotly.express as px
import pandas as pd

# visualize demographic as grouped bar chart

def survival_demographics():
    # Load Titanic dataset
    df = pd.read_csv('https://raw.githubusercontent.com/leontoddjohnson/datasets/main/data/titanic.csv')
    df.columns = df.columns.str.lower()

    # Create a new column in the Titanic dataset that classifies passengers into age categories (i.e., a pandas `category` series). The categories should be:
    #     - Child (up to 12) - Teen (13–19) - Adult (20–59) - Senior (60+)  
    df = df.dropna(subset=['age']).copy()  # Drop rows where age is NaN
    bin_size = [0, 12, 19, 59, float('inf')]
    labels = ['Child', 'Teen', 'Adult', 'Senior']

    df['age_group'] = pd.cut(df['age'], bins=bin_size, labels=labels, right=True, include_lowest=True)

    # 2. Group the passengers by class, sex, and age group. 
    # 3. For each group, calculate:  

    #     - The number of survivors, `n_survivors`
    #     - The survival rate, `survival_rate`
    # 4. Return a table that includes the results for *all* combinations of class, sex, and age group. 
    # 5. Order the results so they are easy to interpret.  
    grouped = (df
        .groupby(['pclass', 'sex', 'age_group'])
        .agg(
            count=('survived', 'size'),
            n_survivors=('survived', 'sum')
            )
        .reset_index()
    )

    classes = [1, 2, 3]
    sexes = ['female', 'male']
    ages = ['Child', 'Teen', 'Adult', 'Senior']

    combos = pd.DataFrame(
        [            (c, s, a) for c in classes for s in sexes for a in ages],
        columns=['pclass', 'sex', 'age_group']
    )

    combos['pclass'] = combos['pclass'].astype(int)
    grouped['pclass'] = grouped['pclass'].astype(int)

    grouped = combos.merge(grouped, on=['pclass', 'sex', 'age_group'], how='left')
    grouped[['count', 'n_survivors' ]] = grouped[['count', 'n_survivors']].fillna(0).astype(int)
    
    grouped['survival_rate'] = grouped['n_survivors'] / grouped['count']
    grouped['survival_rate'] = grouped['survival_rate'].fillna(0.0)

    grouped['age_group'] = pd.Categorical(grouped['age_group'], categories=labels, ordered=True)
    grouped = grouped.sort_values(by=['pclass','sex','age_group'])

    return grouped.sort_values(by=['pclass', 'sex', 'age_group'])

#exercise 2

def family_groups():
    # Load Titanic dataset
    df = pd.read_csv('https://raw.githubusercontent.com/leontoddjohnson/datasets/main/data/titanic.csv')
    df.columns = df.columns.str.lower()


    # to explore the relationship between family size, passenger class, and ticket fare. 
# 1. Create a new column in the Titanic dataset that represents the total family size for each passenger, `family_size`. 
# Family size is defined as the number of siblings/spouses aboard plus the number of parents/children aboard, plus the passenger themselves.
# 2. Group the passengers by family size and passenger class. For each group, calculate:  
#    - The total number of passengers, `n_passengers`
#    - The average ticket fare, `avg_fare`
#    - The minimum and maximum ticket fares (to capture variation in wealth), `min_fare` and `max_fare`

    
    df['family_size'] = df['sibsp'] + df['parch'] + 1  # +1 for the passenger themselves
    out = (
         df.groupby(['family_size','pclass'])
        .agg(
            n_passengers=('survived', 'size'),
            avg_fare=('fare', 'mean'),
            min_fare=('fare', 'min'),
            max_fare=('fare', 'max')
        )
        .reset_index()  
    )
    # 3. Return a table with these results, sorted so that the values are clear and easy to interpret (for example, by class and then family size).
    return out.sort_values(by=['pclass', 'family_size'])

# 4. Write a function called `last_names()` that extracts the last name of each passenger from the `Name` column, and returns the count for each last name (i.e., a pandas series with last name as index, and count as value). Does this result agree with that of the data table above? Share your findings in your app using `st.write`.

def last_names():
    # Load Titanic dataset
    df = pd.read_csv('https://raw.githubusercontent.com/leontoddjohnson/datasets/main/data/titanic.csv')
    df.columns = df.columns.str.lower()
    last = df['name'].str.split(',').str[0].str.strip()
    return last.value_counts()


# 5. Just like you did in Exercise 1, come up with a clear question that your results makes you curious about. Write this question in your app.py file above the call to your visualization function. Then, create a Plotly visualization in a function named `visualize_families()` that directly addresses your question. As in Exercise 1 you are free to choose the chart type that you think best communicates the findings.
