import streamlit as st
import pandas as pd
import plotly.express as px

data = pd.read_csv('dummmmy.csv')

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