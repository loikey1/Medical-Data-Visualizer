import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Import data
df = pd.read_csv('medical_examination.csv')

# Add 'overweight' column
bmi = df['weight'] / np.square(df['height']/100)
df['overweight'] = (bmi > 25).astype('uint8')

# Normalize data by making 0 always good and 1 always bad. If the value of 'cholesterol' or 'gluc' is 1, make the value 0. If the value is more than 1, make the value 1.
df['gluc'] = (df['gluc'] != 1).astype('uint8')
df['cholesterol'] = (df['cholesterol'] != 1).astype('uint8')


#-----------------------------------------------------------
# Draw Categorical Plot
def draw_cat_plot():
    # Create DataFrame for cat plot using `pd.melt` using just the values from 'cholesterol', 'gluc', 'smoke', 'alco', 'active', and 'overweight'.
    columns = [
      'active',
      'alco',
      'cholesterol',
      'gluc',
      'overweight',
      'smoke'
    ]
    df_cat = pd.melt(df, id_vars=["cardio"], value_vars=columns)

    # Group and reformat the data to split it by 'cardio'. Show the counts of each feature. You will have to rename one of the collumns for the catplot to work correctly.
    df_cat = df_cat.reset_index() \
                .groupby(['variable', 'cardio', 'value']) \
                .agg('count') \
                .rename(columns={'index': 'total'}) \
                .reset_index()

    # Draw the catplot with 'sns.catplot()'
    fig = sns.catplot(
        x="variable",
        y="total",
        col="cardio",
        hue="value",
        data=df_cat,
        kind="bar").fig

    # Do not modify the next two lines
    fig.savefig('catplot.png')
    return fig

#-----------------------------------------------------------
# Draw Heat Map
def draw_heat_map():
    # Read data
    df = pd.read_csv('medical_examination.csv')

    # Thêm cột overweight
    df['overweight'] = (df['weight'] / (df['height'] / 100) ** 2).apply(lambda x: 1 if x > 25 else 0)

    # Chuẩn hóa cholesterol và gluc
    df['cholesterol'] = df['cholesterol'].apply(lambda x: 1 if x > 1 else 0)
    df['gluc'] = df['gluc'].apply(lambda x: 1 if x > 1 else 0)

    # Filter data
    df_heat = df[
        (df['ap_lo'] <= df['ap_hi']) &
        (df['height'] >= df['height'].quantile(0.025)) &
        (df['height'] <= df['height'].quantile(0.975)) &
        (df['weight'] >= df['weight'].quantile(0.025)) &
        (df['weight'] <= df['weight'].quantile(0.975))
    ]

    # Create correlation matrix
    corr = df_heat.corr()

    # Mask for upper triangle
    mask = np.triu(np.ones_like(corr, dtype=bool))

    # Draw heatmap
    fig, ax = plt.subplots(figsize=(12, 12))
    sns.heatmap(
        corr,
        mask=mask,
        annot=True,
        fmt='.1f',
        center=0,
        square=True,
        linewidths=0.5,
        cbar_kws={'shrink': 0.5},
        ax=ax
    )
    return fig