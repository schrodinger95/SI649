# Your Name
# si649f20 altair transforms 2

# imports we will use
import altair as alt
import pandas as pd
import streamlit as st

#Title
st.title("Lab6 by Ruge Xu")

#Import data
df1=pd.read_csv("https://raw.githubusercontent.com/eytanadar/si649public/master/lab6/hw/data/df1.csv")
df2=pd.read_csv("https://raw.githubusercontent.com/eytanadar/si649public/master/lab6/hw/data/df2_count.csv")
df3=pd.read_csv("https://raw.githubusercontent.com/eytanadar/si649public/master/lab6/hw/data/df3.csv")
df4=pd.read_csv("https://raw.githubusercontent.com/eytanadar/si649public/master/lab6/hw/data/df4.csv")

# change the 'datetime' column to be explicitly a datetime object
df2['datetime'] = pd.to_datetime(df2['datetime'], errors = 'coerce', utc=True)
df3['datetime'] = pd.to_datetime(df3['datetime'], errors = 'coerce', utc=True)
df4['datetime'] = pd.to_datetime(df4['datetime'], errors = 'coerce', utc=True)

#Sidebar
vis_selectbox = st.sidebar.selectbox(
    label="Select a visualization to display",
    options=['Vis1', 'Vis2', 'Vis3', 'Vis4']
)

###### Making of all the charts


########Vis 1

##Interaction requirement 2, change opacity when hover over

##Interaction requirement 3 and 4, create brushing filter

##Static Component - Bars

##Static Component - Emojis

##Static Component - Text

##Put all together
vis1_selection=alt.selection_single(on="mouseover", empty="none")
vis1_selection2=alt.selection_interval()

vis1_opacityCondition=alt.condition(vis1_selection, alt.value(1), alt.value(0.6))

vis1_bar = alt.Chart(df1).mark_bar(color='orange', size=15).encode(
    x=alt.X('PERCENT:Q', axis=None),
    y=alt.Y('EMOJI:N', axis=alt.Axis(title=None, tickSize=0, domain=False, labels=False), sort=alt.EncodingSortField(field='PERCENT:Q', order='descending'))
).transform_filter(
    vis1_selection2
).encode(
    opacity=vis1_opacityCondition,
    tooltip='EMOJI:N'
).interactive()

vis1_text1 = alt.Chart(df1).mark_text(width=20).encode(
    y=alt.Y('EMOJI:N', axis=None, sort=alt.EncodingSortField(field='PERCENT:Q', order='descending')),
    text='EMOJI:N'
).encode(
    opacity=vis1_opacityCondition
).add_selection(
    vis1_selection2
)

vis1_text2 = alt.Chart(df1).mark_text(width=20).encode(
    y=alt.Y('EMOJI:N', axis=None, sort=alt.EncodingSortField(field='PERCENT:Q', order='descending')),
    text='PERCENT_TEXT:N'
).encode(
    opacity=vis1_opacityCondition
).add_selection(
    vis1_selection2
)

chart1 = alt.hconcat(vis1_text1, vis1_text2, vis1_bar
).resolve_scale(
    y='shared'
).configure_view(
    strokeWidth=0
).configure_axis(
    grid=False
).add_selection(
    vis1_selection
)


########Vis 2

#Zooming and Panning

#vertical line

#interaction dots

#Static component line chart

#Put all together
vis2_selection=alt.selection_interval(bind="scales",encodings=["x"])

vis2_selection2 = alt.selection_single(nearest=True, on='mouseover', fields=['datetime'], empty='none')

vis2_line = alt.Chart(df2).mark_line(size=2.5).encode(
    x=alt.X('datetime', title=None, scale=alt.Scale(type="utc")),
    y=alt.Y('tweet_count', title='Four-minute rolling average'),
    color='team'
)

vis2_points = alt.Chart(df2).mark_circle(color='black', size=70).encode(
    x=alt.X('datetime', title=None, scale=alt.Scale(type="utc")),
    y=alt.Y('tweet_count', title='Four-minute rolling average'),
    opacity=alt.condition(vis2_selection2, alt.value(1), alt.value(0)),
    tooltip=['tweet_count', 'datetime', 'team']
).interactive(bind_y=False)

vis2_selectors = alt.Chart(df2).mark_point().encode(
    x=alt.X('datetime', scale=alt.Scale(type="utc")),
    opacity=alt.value(0),
).add_selection(
    vis2_selection2
)

vis2_rules = alt.Chart(df2).mark_rule(color='lightgray', size=4).encode(
    x=alt.X('datetime', scale=alt.Scale(type="utc")),
).transform_filter(
    vis2_selection2
)

chart2 = (vis2_line + vis2_selectors + vis2_rules + vis2_points).add_selection(
    vis2_selection
)


########Vis3

#Altair version
emojis=list(df3['emoji'].unique())

vis3_selectEmoji=alt.selection_single(
    fields=['emoji'],
    init={"emoji":emojis[0]},
    bind=alt.binding_radio(options=emojis,name="Select Emoji"),
    name="emoji"
)

vis3_selection2=alt.selection_interval(empty="none")

vis3_line = alt.Chart(df3).mark_line(size=2.5).encode(
    x=alt.X('datetime', title=None, scale=alt.Scale(type="utc")),
    y=alt.Y('tweet_count', title='Four-minute rolling average'),
    color='emoji'
).add_selection(
    vis3_selectEmoji, vis3_selection2
).transform_filter(
    vis3_selectEmoji
)

vis3_circles = alt.Chart(df3).mark_circle(color='black').encode(
    x=alt.X('datetime', title=None, scale=alt.Scale(type="utc")),
    y=alt.Y('tweet_count', title='Four-minute rolling average'),
    opacity=alt.condition(vis3_selection2, alt.value(0.7), alt.value(0))
).transform_filter(
    vis3_selectEmoji
)

chart3 = vis3_line + vis3_circles

#Streamlit widget version

vis3_line_2 = alt.Chart(df3).mark_line(size=2.5).encode(
    x=alt.X('datetime', title=None, scale=alt.Scale(type="utc")),
    y=alt.Y('tweet_count', title='Four-minute rolling average'),
    color='emoji'
).add_selection(
    vis3_selection2
)

vis3_circles_2 = alt.Chart(df3).mark_circle(color='black').encode(
    x=alt.X('datetime', title=None, scale=alt.Scale(type="utc")),
    y=alt.Y('tweet_count', title='Four-minute rolling average'),
    opacity=alt.condition(vis3_selection2, alt.value(0.7), alt.value(0))
)

chart3_2 = vis3_line_2 + vis3_circles_2

########Vis4 BONUS OPTIONAL

#Altair version
emojis2 = list(df4['emoji'].unique())
emojis2.sort(reverse=True)

vis4_selection=alt.selection_single(fields=['emoji'], init={'emoji': emojis2[0]})

vis4_opacityCondition=alt.condition(vis4_selection, alt.value(1), alt.value(0.01))

vis4_opacityCondition2=alt.condition(vis4_selection, alt.value(1), alt.value(0))

vis4_line = alt.Chart(df4).mark_line(size=2.5).encode(
    x=alt.X('datetime', axis=alt.Axis(title=None, tickCount=5), scale=alt.Scale(type="utc")),
    y=alt.Y('tweet_count', axis=alt.Axis(title='Four-minute rolling average', tickCount=5)),
    color=alt.Color('emoji', legend=None),
    opacity=vis4_opacityCondition2
).properties(
    title='Tears were shed-of joy and sorrow'
)

vis4_legend = alt.Chart(df4).mark_text(
    align='center',
    baseline='middle',
    size=25
).add_selection(
    vis4_selection
).encode(
    text='emoji',
    y=alt.Y('emoji', sort='-y', axis=None),
    opacity=vis4_opacityCondition
).properties(
    height=70, width=60, title='Legend'
)

chart4 = (vis4_line | vis4_legend).configure_view(
    strokeWidth=0
)

#Streamlit widget version
vis4_line_2 = alt.Chart(df4).mark_line(size=2.5).encode(
    x=alt.X('datetime', axis=alt.Axis(title=None, tickCount=5), scale=alt.Scale(type="utc")),
    y=alt.Y('tweet_count', axis=alt.Axis(title='Four-minute rolling average', tickCount=5)),
    color=alt.Color('emoji', legend=None)
).properties(
    title='Tears were shed-of joy and sorrow'
)

chart4_2 = vis4_line_2


##### Display graphs

vis_dict = {'Vis1': chart1, 'Vis2': chart2, 'Vis3': chart3, 'Vis4': chart4}

if vis_selectbox == 'Vis1':
    st.header('Visualization 1')
elif vis_selectbox == 'Vis2':
    st.header('Visualization 2')
elif vis_selectbox == 'Vis3':
    st.header('Visualization 3')
elif vis_selectbox == 'Vis4':
    st.header('Visualization 4')

if vis_selectbox == 'Vis1' or vis_selectbox == 'Vis2':
    vis_dict[vis_selectbox]
elif vis_selectbox == 'Vis3':
    st.subheader('Altair version')
    vis_dict[vis_selectbox]
    st.subheader('Streamlit version')
    selected_emoji = st.radio(label='Select Emoji',options=emojis)
    chart3_2 = chart3_2.transform_filter(
        alt.datum.emoji == selected_emoji
    )
    chart3_2
else:
    st.subheader('Altair version')
    vis_dict[vis_selectbox]
    st.subheader('Streamlit version')
    selected_emoji = st.radio(label='Select Emoji',options=emojis2)
    chart4_2 = chart4_2.encode(
        opacity=alt.condition(alt.datum.emoji == selected_emoji, alt.value(1), alt.value(0))
    )
    chart4_2
    