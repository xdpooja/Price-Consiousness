import streamlit as st
import pandas as pd
import numpy as np
from streamlit_elements import *
st.set_page_config(layout="wide")


data = pd.read_csv("final.csv")

# Define your column options and mappings
increase_columns = [
    'Leisure; entertainment and travel.1',
    'Food and dishes.1', 'Commodities and groceries.1',
    'Productivity; gadgets and technology.1',
    'Lifestyle; beauty and clothing.1',
]

decrease_columns = [
    'decrease Leisure; entertainment and travel',
    'decrease Food and dishes', 'decrease Commodities and groceries',
    'decrease Productivity; gadgets and technology',
    'decerase Lifestyle; beauty and clothing',
]

option_map_increase = {
    'Leisure; entertainment and travel.1': 'Leisure; entertainment and travel', 
    'Food and dishes.1': 'Food and dishes',
    'Commodities and groceries.1': 'Commodities and groceries', 
    'Productivity; gadgets and technology.1': 'Productivity; gadgets and technology',
    'Lifestyle; beauty and clothing.1': 'Lifestyle; beauty and clothing',
}

option_map_decrease = {
    'decrease Leisure; entertainment and travel': 'Leisure; entertainment and travel', 
    'decrease Food and dishes': 'Food and dishes',
    'decrease Commodities and groceries': 'Commodities and groceries', 
    'decrease Productivity; gadgets and technology': 'Productivity; gadgets and technology',
    'decerase Lifestyle; beauty and clothing': 'Lifestyle; beauty and clothing',
}

option_reverse = {
    'Leisure; entertainment and travel.1': 'decrease Leisure; entertainment and travel',
    'Food and dishes.1' : 'decrease Food and dishes',
    'Commodities and groceries.1' :'decrease Commodities and groceries',
    'Productivity; gadgets and technology.1' : 'decrease Productivity; gadgets and technology',
    'Lifestyle; beauty and clothing.1': 'decerase Lifestyle; beauty and clothing'
}

select_product = st.multiselect(
    "Product Category", 
    increase_columns , 
    default=increase_columns , 
    format_func=lambda x: option_map_increase.get(x, option_map_decrease.get(x))
)

select_metric = st.selectbox("Choose Group", [
    'Age', 'Income', 'Decision maker', 
    'time category', 'payment preference', 
    'planned or preplanned', 'transaction frequency', 'Feeling Towards Price Of Items (Increase in Price)', 'Feeling Towards Price Of Items (Decrease in Price)'
])


selected_increase = [col for col in select_product if col in increase_columns]
selected_decrease = []
for col2 in select_product:
    col2 =option_reverse.get(col2)
    selected_decrease.append(col2)

data2= pd.read_csv('dummmmy.csv')
# For Increase
filtered_df_increase = data2[selected_increase + [select_metric]]
melted_increase_df = filtered_df_increase.melt(id_vars=[select_metric], var_name='Category', value_name='Sensitivity')

# For Decrease
filtered_df_decrease = data2[selected_decrease + [select_metric]]
melted_decrease_df = filtered_df_decrease.melt(id_vars=[select_metric], var_name='Category', value_name='Sensitivity')


line_charts = ['Age', 'Income', 'planned or preplanned','time category']
bar_charts = [ 'Decision maker', 'payment preference', 'transaction frequency']



if select_metric in line_charts:
    def create_price_increase_yes_dict(melted_df, selected_people_column, selected_price_columns):
        price_increase_yes_dict = []

        order_dict = {
        'Age': ['18-24', '25-34', '35-54', '55+'],
        'Income': ['Below Rs. 50,000', 'Rs. 50,000- 2,00,000', 'Rs. 2,00,000- 5,00,000', 'Above Rs. 5,00,000'],
        'time category': ['No Time', 'Very Little Time', 'Moderate Time', 'Considerable Time', 'Excessive Time'],
        'willingness for additional charges': ['0', '0.05', '0.1', '0.2', 'More than 20%'],
        'planned or preplanned': ['Pre Planned', 'Indifferent', 'Spontaneous'],
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
                ]['Sensitivity'].mean()
                
                product_data["data"].append({"x": value, "y": overcharged_count})
            
            price_increase_yes_dict.append(product_data)
        
        return price_increase_yes_dict

    price_increase_yes_dict = create_price_increase_yes_dict(melted_increase_df, select_metric, select_product)
    

    def create_price_decrease_yes_dict(melted_df, selected_people_column, selected_price_columns):
        price_decrease_yes_dict = []

        order_dict = {
        'Age': ['18-24', '25-34', '35-54', '55+'],
        'Income': ['Below Rs. 50,000', 'Rs. 50,000- 2,00,000', 'Rs. 2,00,000- 5,00,000', 'Above Rs. 5,00,000'],
        'time category': ['No Time', 'Very Little Time', 'Moderate Time', 'Considerable Time', 'Excessive Time'],
        'willingness for additional charges': ['0', '0.05', '0.1', '0.2', 'More than 20%'],
        'planned or preplanned': ['Pre Planned', 'Indifferent', 'Spontaneous'],
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
                fairlycharged_count = melted_df[
                    (melted_df[selected_people_column] == value) &
                    (melted_df['Category'] == product)
                ]['Sensitivity'].mean()
                
                product_data["data"].append({"x": value, "y": fairlycharged_count})
            
            price_decrease_yes_dict.append(product_data)
        
        return price_decrease_yes_dict
    
    price_decrease_yes_dict = create_price_decrease_yes_dict(melted_decrease_df, select_metric, selected_decrease)
 
  

if select_metric in bar_charts:

    def create_price_increase_yes_bar_dict(melted_df, selected_people_column, selected_price_columns):
        custom_dict = []
        order_dict = {'Decision maker': ['No', 'Yes, but only for myself', 'Yes, for the whole household'],
                      'planned or preplanned': ['Pre Planned', 'Indifferent', 'Spontaneous'],
                      'transaction frequency':['Less Frequent', 'Indifferent', 'More Frequent']}
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
                ]['Sensitivity'].mean(0).round(2)
                
                # Add the product value and corresponding color
                entity_key = product  # Remove spaces from the product name
                entry[entity_key] = overestimate_count
                entry[f"{entity_key}Color"] = colors[j % len(colors)]
            
            custom_dict.append(entry)
        
        return custom_dict
    
    price_increase_yes_bar_dict = create_price_increase_yes_bar_dict(melted_increase_df, select_metric, select_product)

    def create_price_decrease_yes_bar_dict(melted_df, selected_people_column, selected_price_columns):
        price_decrease_yes_bar_dict = []
        
        colors = ['hsl(314, 70%, 50%)', 'hsl(173, 70%, 50%)', 'hsl(252, 70%, 50%)', 
                'hsl(125, 70%, 50%)', 'hsl(48, 70%, 50%)']  # Add more colors as needed
        
        order_dict = {'Decision maker': ['No', 'Yes, but only for myself', 'Yes, for the whole household'],
                      'planned or preplanned': ['Pre Planned', 'Indifferent', 'Spontaneous'],
                      'transaction frequency':['Less Frequent', 'Indifferent', 'More Frequent']}
        if selected_people_column in order_dict:
            ordered_values = order_dict[selected_people_column]
        else:
            ordered_values = melted_df[selected_people_column].unique()

        for i, value in enumerate(ordered_values):
            entry = {selected_people_column: value}
            
            for j, product in enumerate(selected_price_columns):
                # Count the number of "overestimated" entries for this product and selected group
                underestimation_count = melted_df[
                    (melted_df[selected_people_column] == value) &
                    (melted_df['Category'] == product)
                ]['Sensitivity'].mean(0).round(2)
                
                # Add the product value and corresponding color
                entity_key = product  # Remove spaces from the product name
                entry[entity_key] = underestimation_count
                entry[f"{entity_key}Color"] = colors[j % len(colors)]
            
            price_decrease_yes_bar_dict.append(entry)
        
        return price_decrease_yes_bar_dict
    
    price_decrease_yes_bar_dict = create_price_decrease_yes_bar_dict(melted_decrease_df, select_metric, selected_decrease)


with elements(dashboard):
    if select_metric in line_charts:
        layout1 = [
            dashboard.Item("first", 0,0,5,3),
            dashboard.Item("second", 5,0,5,3),
            
        ]

        with dashboard.Grid(layout1):
# label as the product and ag ad x axis
#line charts
            mui.Paper(
                nivo.Line(
                    data =price_increase_yes_dict,
                    margin={ 'top': 50, 'right': 110, 'bottom': 50, 'left': 60 },
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
                            'translateX': 100,
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
                        'legend': 'Willingness to buy after price increase',
                        'legendOffset': -40,
                        'legendPosition': 'middle',
                        'truncateTickAt': 0
                    },
                            ), key='first'
                        )


            mui.Paper(
                nivo.Line(
                    data =price_decrease_yes_dict,
                    margin={ 'top': 50, 'right': 110, 'bottom': 50, 'left': 60 },
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
                            'translateX': 100,
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
                        'legend': 'Willingness to buy after price decrease',
                        'legendOffset': -40,
                        'legendPosition': 'middle',
                        'truncateTickAt': 0
                    },
                            ), key='second'
                        )
 
    if select_metric in bar_charts:
        layout2 = [
            dashboard.Item("third", 0,0,5,3),
            dashboard.Item("fourth", 5,0,5,3),
            
        ]

        with dashboard.Grid(layout2):
            
            mui.Box(
                nivo.Bar(
                    data=price_increase_yes_bar_dict,
                    keys=select_product,
                    indexBy=select_metric,
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
                        'legend': 'Willingness to buy after price increase',
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

                ), key = 'third'
            )

            mui.Box(
                nivo.Bar(
                    data=price_decrease_yes_bar_dict,
                    keys=selected_decrease,
                    indexBy=select_metric,
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
                        'legend': 'Willingness to buy after price decrease',
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

col1, col2 = st.columns(2)

with col1:
    expander = st.expander("See what mostly people responded as when product price increase")

with col2: 
    expander2 = st.expander("See what mostly people responded as when product price decreases")


with expander:
    st.components.v1.iframe("https://datawrapper.dwcdn.net/F4KWT/1/", height=400, scrolling=True)
    st.markdown("###### 0: No 1: Yes")

with expander2:
    st.components.v1.iframe("https://datawrapper.dwcdn.net/xEfjG/1/", height=400, scrolling=True)
    st.markdown("###### 0: No 1: Yes")