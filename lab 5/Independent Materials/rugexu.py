# Ruge Xu
# si649w22 Altair transforms 2

# imports we will use
import streamlit as st
import altair as alt
import pandas as pd

datasetURL="https://raw.githubusercontent.com/eytanadar/si649public/master/lab5/assets/hw/movie_after_1990.csv"
movies_test=pd.read_csv(datasetURL, encoding="latin-1")

# Just for you to explore the features [COMMENT OUT WHEN SUBMITTING IT] 
# st.write(movies_test) ~ to see the dataset


#Title
st.title("Lab5 by Ruge Xu")

### Making of all charts [ Add altair code chunk for each of the specific charts]

# Visualization 1 
vis1_line = alt.Chart(movies_test).transform_filter(
    alt.FieldRangePredicate(field='year', range=[1990, 1997])
).mark_line().encode(
    # define the encoding of the "mini chart"
    x='year:O',
    y='mean(budget):Q'
).properties(
    width=800
)

vis1_dot = alt.Chart(movies_test).transform_filter(
    alt.FieldRangePredicate(field='year', range=[1990, 1997])
).transform_joinaggregate(
    budgetmean='mean(budget)',
    groupby=['year']
).transform_filter(
    alt.datum.budget >= alt.datum.budgetmean * 2
).mark_point(filled=True).encode(
    x='year:O',
    y='budget:Q'
).properties(
    width=800
)

vis1_text = vis1_dot.transform_joinaggregate(
    budgetmax='max(budget)',
    groupby=['year']
).transform_filter(
    alt.datum.budget == alt.datum.budgetmax
).mark_text(
    align='center',
    baseline='middle',
    dy= -15
).encode(
    text='title:N'
)

vis1 = (vis1_dot + vis1_line + vis1_text)

# Visualization 2
vis2_heatmap = alt.Chart(movies_test).transform_filter(
    {'not': alt.FieldOneOfPredicate(field='test_result', oneOf=['dubious'])}
).mark_rect().encode(
    x=alt.X('rating:Q', bin=True),
    y='test_result:N',
    color='count():Q'
).properties(
    width=600
)

vis2_text = alt.Chart(movies_test).transform_filter(
    {'not': alt.FieldOneOfPredicate(field='test_result', oneOf=['dubious'])}
).mark_text(
    align='center',
    baseline='middle'
).encode(
    x=alt.X('rating:Q', bin=True),
    y='test_result:N',
    text='count():Q'
).properties(
    width=600
)

vis2_highlight = alt.Chart(movies_test).transform_filter(
    {'not': alt.FieldOneOfPredicate(field='test_result', oneOf=['dubious'])}
).transform_joinaggregate(
    ratingmax='max(rating)',
    groupby=['test_result']
).transform_filter(
    alt.datum.ratingmax > 9
).mark_rect(
    color='', 
    stroke='red', 
    strokeWidth=2
).encode(
    x=alt.X('rating:Q', bin=True),
    y='test_result:N'
).properties(
    width=600
)

vis2 = (vis2_heatmap + vis2_text + vis2_highlight)

# Visualization 3
vis3_bar1 = alt.Chart(movies_test).transform_filter(
    alt.datum.country_binary == 'U.S. and Canada'
).mark_bar().encode(
    x='mean(dom_gross):Q',
    y='test_result:N',
    color=alt.Color('mean(dom_gross):Q', scale=alt.Scale(scheme='blues'))
)

vis3_bar2 = alt.Chart(movies_test).transform_filter(
    alt.datum.country_binary != 'U.S. and Canada'
).mark_bar().encode(
    x='mean(int_gross):Q',
    y='test_result:N',
    color=alt.Color('mean(int_gross):Q', scale=alt.Scale(scheme='reds'))
)

vis3_text1 = vis3_bar1.transform_window(
    groupby=["test_result"],
    sort=[alt.SortField("dom_gross", order="ascending")],
    Rank='rank()'
).transform_filter(
    alt.datum.Rank == 10
).mark_text(
    align='left',
    baseline='middle'
).encode(
    x=alt.value(10),
    text='title:N',
    color=alt.value('black')
)

vis3_text2 = vis3_bar2.transform_window(
    groupby=["test_result"],
    sort=[alt.SortField("int_gross", order="ascending")],
    Rank='rank()'
).transform_filter(
    alt.datum.Rank == 10
).mark_text(
    align='left',
    baseline='middle'
).encode(
    x=alt.value(10),
    text='title:N',
    color=alt.value('white')
)

vis3 = ((vis3_bar1 + vis3_text1) & (vis3_bar2 + vis3_text2)).resolve_scale(
    x='shared',
    color='independent'
)

# Visualization 4
vis4 = alt.Chart(movies_test).transform_fold(
    ['budget','int_gross'],
    as_  = ['finance','dollars']
).mark_bar().encode(
    x = 'mean(dollars):Q',
    y = 'finance:N',
    color = 'finance:N'
)

### Display charts
### Hint: Create a sidebar 'selectbox' and use if, else statements for the correct outputs [Information is also in the handout]
vis_selectbox = st.sidebar.selectbox(
    label="Select a visualization to display",
    options=['vis1', 'vis2', 'vis3', 'vis4']
)

vis_dict = {'vis1': vis1, 'vis2': vis2, 'vis3': vis3, 'vis4': vis4}

vis_dict[vis_selectbox]