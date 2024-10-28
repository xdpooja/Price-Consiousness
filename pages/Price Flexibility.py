import streamlit as st
import pandas as pd
import plotly.express as px

data_ = pd.read_csv('dummmmy.csv')

toggle = st.toggle('Slider options On/Off', value=True)
if toggle:
    col11, col22 = st.columns(2)
    with col11:
        slider_preference = st.selectbox('Select slider filter', options=['Payment Preference', 'Shopping Preference', 'Spontaneous or Preplanned', 'Transaction Frequency'])
    with col22:
        slider_value = [1,2,3,4,5]
        x = []

        if slider_preference == 'Payment Preference':
            x.append('Cash')
            x.append('Moderately Indifferent')
            x.append('Indifferent')
            x.append('Moderately Digital')
            x.append('Digital')
        if slider_preference == 'Shopping Preference':
            x.append('Offline')
            x.append('Moderately Indifferent')
            x.append('Indifferent')
            x.append('Moderately Online')
            x.append('Online')
        if slider_preference == 'Spontaneous or Preplanned':
            x.append('Spontaneous')
            x.append('Moderately Indifferent')
            x.append('Indifferent')
            x.append('Moderately Pre Planned')
            x.append('Pre Planned')
        if slider_preference == 'Transaction Frequency':
            x.append('Less frequent with multiple products in one high value transaction')
            x.append('Moderately Indifferent')
            x.append('Indifferent')
            x.append('Moderately Frequent')
            x.append('Frequent with lesser products in multiple low value transactions')

        def stringify(i:int = 0) -> str:
            return x[i-1]

        slider = st.select_slider(f'Scale for {slider_preference}', options=slider_value, format_func=stringify)

    data = data_[data_[slider_preference]==slider]
if not toggle:
    data = data_

option = st.selectbox('', options=['Age', 'Gender', 'Income', 'Decision maker', 'payment preference', 'shopping preference', 'planned or preplanned', 'transaction frequency','time category'])

subset_data = data[[option, 'willingness for additional charges']].value_counts(normalize=True).reset_index(name='proportion')
pivot_data = subset_data.pivot(index=option, columns='willingness for additional charges', values='proportion').fillna(0)

st.write(pivot_data)
fig = px.bar(subset_data, 
             x=option, 
             y='proportion', 
             color='willingness for additional charges', 
             title=f'Willingness for Additional Charges by {option}', 
             labels={option: option, 'proportion': 'Proportion'},
             barmode='group')

# Customize layout
fig.update_layout(xaxis_title=option, 
                  yaxis_title='Proportion', 
                  legend_title='Willingness for Additional Charges',
                  title_x=0.5)

# Show plot in Streamlit
st.plotly_chart(fig)
