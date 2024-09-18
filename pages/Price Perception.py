import streamlit as st
import pandas as pd
import numpy as np
from streamlit_elements import *
st.set_page_config(layout="wide")


data = pd.read_csv("final.csv")
perceprtion_columns = [ 'Leisure; entertainment and travel', 'Food and dishes',
       'Commodities and groceries', 'Productivity; gadgets and technology',
       'Lifestyle; beauty and clothing',]

select_product = st.multiselect("Price Perception of", perceprtion_columns, default=perceprtion_columns)
select_metric = st.selectbox("Choose Group", ['Age', 'Location', 'Income', 'Decision maker', 'time category','payment preference','shopping preference'])
filtered_df = data[select_product + [select_metric]]

melted_df = filtered_df.melt(id_vars=[select_metric], var_name='Category', value_name='Perception')
line_charts = ['Age', 'Income', 'time category', 'willingness for additional charges']
bar_charts = ['Gender', 'Location', 'Decision maker', 'payment preference','shopping preference','planned or preplanned', 'transaction frequency']

dummmydf = pd.read_csv('dummmmy.csv')
filtered_df2 = dummmydf[select_product + [select_metric]]
melted_df2 = filtered_df2.melt(id_vars=[select_metric], var_name='Category', value_name='Perception')

col1, col2 = st.columns([0.7,0.3])


if select_metric in line_charts:
    def create_price_overcharged_dict(melted_df, selected_people_column, selected_price_columns):
        overcharged_dict = []

        order_dict = {
        'Age': ['18-24', '25-34', '35-54', '55+'],
        'Income': ['Below Rs. 50,000', 'Rs. 50,000- 2,00,000', 'Rs. 2,00,000- 5,00,000', 'Above Rs. 5,00,000'],
        'time category': ['No Time', 'Very Little Time', 'Moderate Time', 'Considerable Time', 'Excessive Time'],
        'willingness for additional charges': ['0', '0.05', '0.1', '0.2', 'More than 20%']
        }
    
        if selected_people_column in order_dict:
            ordered_values = order_dict[selected_people_column]
        
        else:
            ordered_values = melted_df[selected_people_column].unique()

        colors = ['hsl(314, 70%, 50%)', 'hsl(173, 70%, 50%)', 'hsl(252, 70%, 50%)', 
                'hsl(125, 70%, 50%)', 'hsl(48, 70%, 50%)']  # Add more colors as needed
        
        for i, product in enumerate(selected_price_columns):
            product_data = {"id": product, "color": colors[i % len(colors)], "data": []}
            
            
            for value in ordered_values:
                # Count the number of "overestimated" entries for this product and selected people group value
                overcharged_count = melted_df[
                    (melted_df[selected_people_column] == value) &
                    (melted_df['Category'] == product) 
                ]['Perception'].mean()
                
                product_data["data"].append({"x": value, "y": overcharged_count})
            
            overcharged_dict.append(product_data)
        
        return overcharged_dict
   

    overcharged_dict = create_price_overcharged_dict(melted_df2, select_metric, select_product)
 
if select_metric in bar_charts:

    def create_overcharged_bar_dict(melted_df, selected_people_column, selected_price_columns):
        custom_dict = []
        order_dict = {'Decision maker': ['No', 'Yes, but only for myself', 'Yes, for the whole household'],
                      'shopping preference':['Online', 'Indifferent', 'Offline']}
        if selected_people_column in order_dict:
            ordered_values = order_dict[selected_people_column]
        else:
            ordered_values = melted_df[selected_people_column].unique()

        colors = ['hsl(314, 70%, 50%)', 'hsl(173, 70%, 50%)', 'hsl(252, 70%, 50%)', 
                'hsl(125, 70%, 50%)', 'hsl(48, 70%, 50%)']  # Add more colors as needed
        
        for i, value in enumerate(ordered_values):
            entry = {selected_people_column: value}
            
            for j, product in enumerate(selected_price_columns):
                # Count the number of "overestimated" entries for this product and selected group
                overestimate_count = melted_df[
                    (melted_df[selected_people_column] == value) &
                    (melted_df['Category'] == product)
                ]['Perception'].mean().round(2)
                
                # Add the product value and corresponding color
                entity_key = product  # Remove spaces from the product name
                entry[entity_key] = overestimate_count
                entry[f"{entity_key}Color"] = colors[j % len(colors)]
            
            custom_dict.append(entry)
        
        return custom_dict
    
    overecharged_bar_dict = create_overcharged_bar_dict(melted_df2, select_metric, select_product)



with elements(dashboard):
    if select_metric in line_charts:
        layout1 = [
            dashboard.Item("first", 0,0,10,3),
            dashboard.Item("second", 5,0,5,3),
            dashboard.Item("third", 0,5,5,3)
        ]

        with dashboard.Grid(layout1):
# label as the product and ag ad x axis
#line charts
            
            mui.Paper(
                nivo.Line(
                    data =overcharged_dict,
                    margin={ 'top': 50, 'right': 160, 'bottom': 50, 'left': 60 },
                    xScale={ 'type': 'point' },
                    yScale={
                        'type': 'linear',
                        'min': 'auto',
                        'max': 'auto',
                        'stacked': False,
                        'reverse': False
                    },
                    
                    legends=[
                        {
                            'anchor': 'bottom-right',
                            'direction': 'column',
                            'justify': False,
                            'translateX': 90,
                            'translateY': 0,
                            'itemsSpacing': 0,
                            'itemDirection': 'left-to-right',
                            'itemWidth': 80,
                            'itemHeight': 20,
                            'itemOpacity': 0.75,
                            'symbolSize': 12,
                            'symbolShape': 'circle',
                            'symbolBorderColor': 'rgba(0, 0, 0, .5)',
                            'effects': [
                                {
                                    'on': 'hover',
                                    'style': {
                                        'itemBackground': 'rgba(0, 0, 0, .03)',
                                        'itemOpacity': 1
                                    }
                                }
                            ]
                        }
                    ],
                    axisBottom={
                        'tickSize': 5,
                        'tickPadding': 5,
                        'tickRotation': 0,
                        'legend': 'Category',
                        'legendOffset': 36,
                        'legendPosition': 'middle',
                        'truncateTickAt': 0
                    },
                    axisLeft={
                        'tickSize': 5,
                        'tickPadding': 5,
                        'tickRotation': 0,
                        'legend': 'Feeling of Overcharged',
                        'legendOffset': -40,
                        'legendPosition': 'middle',
                        'truncateTickAt': 0
                    },
                            ), key='first'
                        )
        
       
    if select_metric in bar_charts:
        layout2 = [
            dashboard.Item("fourth", 0,0,10,3),
            dashboard.Item("fifth", 0,4,5,3),
            
        ]

        with dashboard.Grid(layout2):
            
            mui.Box(
                nivo.Bar(
                    data=overecharged_bar_dict,
                    keys=select_product,
                    indexBy=select_metric,
                    groupMode = 'grouped',
                    margin={ 'top': 50, 'right': 130, 'bottom': 50, 'left': 60 },
                    padding={0.3},
                    valueScale={ 'type': 'linear' },
                    indexScale={ 'type': 'band', 'round': True },
                    colors={ 'scheme': 'nivo' },
                    borderColor={
                        'from': 'color',
                        'modifiers': [
                            [
                                'darker',
                                1.6
                            ]
                        ]
                    },
                    axisTop=False,
                    axisRight=False,
                    axisBottom={
                        'tickSize': 5,
                        'tickPadding': 5,
                        'tickRotation': 0,
                        'legend': select_metric,
                        'legendPosition': 'middle',
                        'legendOffset': 32,
                        'truncateTickAt': 0
                    },
                    axisLeft={
                        'tickSize': 5,
                        'tickPadding': 5,
                        'tickRotation': 0,
                        'legend': 'Overcharged',
                        'legendPosition': 'middle',
                        'legendOffset': -40,
                        'truncateTickAt': 0
                    },
                    labelSkipWidth={12},
                    labelSkipHeight={12},
                    labelTextColor={
                        'from': 'color',
                        'modifiers': [
                            [
                                'darker',
                                1.6
                            ]
                        ]
                    },
                    legends=[ {
                            'dataFrom': 'keys',
                            'anchor': 'bottom-right',
                            'direction': 'column',
                            'justify': False,
                            'translateX': 120,
                            'translateY': 0,
                            'itemsSpacing': 2,
                            'itemWidth': 100,
                            'itemHeight': 20,
                            'itemDirection': 'left-to-right',
                            'itemOpacity': 0.85,
                            'symbolSize': 20,
                            'effects': [
                                {
                                    'on': 'hover',
                                    'style': {
                                        'itemOpacity': 1
                                    }
                                }
                            ]
                        }
                    ]

                ), key = 'fourth'
            )
st.components.v1.iframe("https://datawrapper.dwcdn.net/qfwiL/1/", height=400, scrolling=True)
