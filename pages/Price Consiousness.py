import streamlit as st
import pandas as pd
from streamlit_elements import *
st.set_page_config(layout="wide")


data_ = pd.read_csv("final.csv")

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

price_columns = [ 'movie ticket price','medium pizza price', 'coca cola price', 'oven price', 'shampoo price']

price_columns2 = [ 'movie ticket','medium pizza',  'shampoo']
price_columns3 = ['coca cola', 'oven']
col1, col2, col3= st.columns([0.6, 0.2,0.2])
with col1:
    select_product = st.multiselect("Price Awareness of", price_columns2, default= [ 'movie ticket','medium pizza',   'shampoo'])
with col2 :
    select_product2 = st.multiselect("Other Products", options=[ 'oven'], default='oven')
with col3:
    select_product3 =st.multiselect("", options=['coca cola', ], default='coca cola')
select_metric = st.selectbox("Choose Group", ['Age',  'Income', 'Decision maker', 'time category','payment preference', 'transaction frequency'])
filtered_df = data[select_product + [select_metric]]

melted_df = filtered_df.melt(id_vars=[select_metric], var_name='Product', value_name='Awareness')

filtered_df2 = data[select_product2 + [select_metric]]

melted_df2 = filtered_df2.melt(id_vars=[select_metric], var_name='Product', value_name='Awareness')

filtered_df3 = data[select_product3 + [select_metric]]

melted_df3 = filtered_df3.melt(id_vars=[select_metric], var_name='Product', value_name='Awareness')

line_charts = ['Age', 'Income', 'time category', 'willingness for additional charges','planned or preplanned']
bar_charts = ['Gender', 'Location', 'Decision maker', 'payment preference','shopping preference', 'transaction frequency']


if select_metric in line_charts:

    def create_price_awareness_dict(melted_df, selected_people_column, selected_price_columns):
        awareness_dict = []
        order_dict = {
        'Age': ['18-24', '25-34', '35-54', '55+'],
        'Income': ['Below Rs. 50,000', 'Rs. 50,000- 2,00,000', 'Rs. 2,00,000- 5,00,000', 'Above Rs. 5,00,000'],
        'time category': ['No Time', 'Very Little Time', 'Moderate Time', 'Considerable Time', 'Excessive Time'],
        'willingness for additional charges': ['0', '0.05', '0.1', '0.2', 'More than 20%'],
        'planned or preplanned': ['Pre Planned', 'Spontaneous'],
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
                overestimate_count = melted_df[
                    (melted_df[selected_people_column] == value) &
                    (melted_df['Product'] == product)
                ]['Awareness'].mean()
                
                overestimate_count = 0 if pd.isna(overestimate_count) else round(overestimate_count, 2)

                product_data["data"].append({"x": value, "y": overestimate_count})
            
            awareness_dict.append(product_data)
        
        return awareness_dict
    
    awareness_dict = create_price_awareness_dict(melted_df, select_metric, select_product)

    def create_price_awareness_dict2(melted_df, selected_people_column, selected_price_columns):
        awareness_dict = []
        order_dict = {
        'Age': ['18-24', '25-34', '35-54', '55+'],
        'Income': ['Below Rs. 50,000', 'Rs. 50,000- 2,00,000', 'Rs. 2,00,000- 5,00,000', 'Above Rs. 5,00,000'],
        'time category': ['No Time', 'Very Little Time', 'Moderate Time', 'Considerable Time', 'Excessive Time'],
        'willingness for additional charges': ['0', '0.05', '0.1', '0.2', 'More than 20%'],
        'planned or preplanned': ['Pre Planned', 'Spontaneous'],
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
                overestimate_count = melted_df[
                    (melted_df[selected_people_column] == value) &
                    (melted_df['Product'] == product)
                ]['Awareness'].mean()
                overestimate_count = 0 if pd.isna(overestimate_count) else round(overestimate_count, 2)
                product_data["data"].append({"x": value, "y": overestimate_count})
            
            awareness_dict.append(product_data)
        
        return awareness_dict
    
    awareness_dict2 = create_price_awareness_dict2(melted_df2, select_metric, select_product2)

    def create_price_awareness_dict3(melted_df, selected_people_column, selected_price_columns):
        awareness_dict = []
        order_dict = {
        'Age': ['18-24', '25-34', '35-54', '55+'],
        'Income': ['Below Rs. 50,000', 'Rs. 50,000- 2,00,000', 'Rs. 2,00,000- 5,00,000', 'Above Rs. 5,00,000'],
        'time category': ['No Time', 'Very Little Time', 'Moderate Time', 'Considerable Time', 'Excessive Time'],
        'willingness for additional charges': ['0', '0.05', '0.1', '0.2', 'More than 20%'],
        'planned or preplanned': ['Pre Planned', 'Spontaneous'],
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
                overestimate_count = melted_df[
                    (melted_df[selected_people_column] == value) &
                    (melted_df['Product'] == product)
                ]['Awareness'].mean()
                overestimate_count = 0 if pd.isna(overestimate_count) else round(overestimate_count, 2)
                product_data["data"].append({"x": value, "y": overestimate_count})
            
            awareness_dict.append(product_data)
        
        return awareness_dict
    
    awareness_dict3 = create_price_awareness_dict3(melted_df3, select_metric, select_product3)

if select_metric in bar_charts:

    def create_overestimated_bar_dict(melted_df, selected_people_column, selected_price_columns):
        custom_dict = []
        order_dict = {'Decision maker': ['No', 'Yes, but only for myself', 'Yes, for the whole household'],  'transaction frequency':['Less Frequent',  'More Frequent'],
                      'payment preference': ['Cash', 'Digital']}
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
                    (melted_df['Product'] == product)
                ]['Awareness'].mean()
                overestimate_count = 0 if pd.isna(overestimate_count) else round(overestimate_count, 2)
                # Add the product value and corresponding color
                entity_key = product  # Remove spaces from the product name
                entry[entity_key] = overestimate_count
                entry[f"{entity_key}Color"] = colors[j % len(colors)]
            
            custom_dict.append(entry)
        
        return custom_dict
    
    overestimate_bar_dict = create_overestimated_bar_dict(melted_df, select_metric, select_product)

    def create_overestimated_bar_dict2(melted_df, selected_people_column, selected_price_columns):
        custom_dict = []
        order_dict = {'Decision maker': ['No', 'Yes, but only for myself', 'Yes, for the whole household'],  'transaction frequency':['Less Frequent',  'More Frequent'],
                      'payment preference': ['Cash', 'Digital']}
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
                    (melted_df['Product'] == product)
                ]['Awareness'].mean()
                overestimate_count = 0 if pd.isna(overestimate_count) else round(overestimate_count, 2)
                # Add the product value and corresponding color
                entity_key = product  # Remove spaces from the product name
                entry[entity_key] = overestimate_count
                entry[f"{entity_key}Color"] = colors[j % len(colors)]
            
            custom_dict.append(entry)
        
        return custom_dict
    
    overestimate_bar_dict2 = create_overestimated_bar_dict2(melted_df2, select_metric, select_product2)

    def create_overestimated_bar_dict3(melted_df, selected_people_column, selected_price_columns):
        custom_dict = []
        order_dict = {'Decision maker': ['No', 'Yes, but only for myself', 'Yes, for the whole household'],  'transaction frequency':['Less Frequent',  'More Frequent'],
                      'payment preference': ['Cash', 'Digital']}
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
                    (melted_df['Product'] == product)
                ]['Awareness'].mean()
                overestimate_count = 0 if pd.isna(overestimate_count) else round(overestimate_count, 2)
                # Add the product value and corresponding color
                entity_key = product  # Remove spaces from the product name
                entry[entity_key] = overestimate_count
                entry[f"{entity_key}Color"] = colors[j % len(colors)]
            
            custom_dict.append(entry)
        
        return custom_dict
    
    overestimate_bar_dict3 = create_overestimated_bar_dict3(melted_df3, select_metric, select_product3)

 
with elements(dashboard):
    if select_metric in line_charts:
        layout1 = [
            dashboard.Item("first", 0,0,5,3),
            dashboard.Item("second", 5,0,5,3),
            dashboard.Item("third", 0,5,5,3),
            dashboard.Item("extra", 6,5,5,3)
        ]

        with dashboard.Grid(layout1):
# label as the product and ag ad x axis
#line charts
            real_dict = [{'Item': 'Movie Ticket', 'Price':  250, }, {'Item':'Medium Pizza','Price':300}, {'Item':'Coca Cola', 'Price':40},{'Item':'Shampoo', 'Price':300},{'Item': 'Oven', 'Price':7000}]
            mui.Paper(
                nivo.Bar(
                    data=real_dict,
                    keys= ['Price'],
                    indexBy='Item',
                    
                    margin={ 'top': 50, 'right':40, 'bottom': 50, 'left': 80 },
                    padding=0.3,
                    layout='horizontal',
                    enableTotals = True,
                    enableLabel= True,
                    labelPosition='end',
                    labelOffset= 10,
                    
                    )
                 , key='second')
                        

            mui.Paper(
                nivo.Line(
                    data =awareness_dict,
                    margin={ 'top': 50, 'right': 110, 'bottom': 50, 'left': 60 },
                    xScale={ 'type': 'point' },
                    yScale={
                        'type': 'linear',
                        'min': 'auto',
                        'max': 'auto',
                        'stacked': False,
                        'reverse': False
                    },
                    
                    useMesh=True,
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
                        
                        'legendOffset': 36,
                        'legendPosition': 'middle',
                        'truncateTickAt': 0
                    },
                    axisLeft={
                        'tickSize': 5,
                        'tickPadding': 5,
                        'tickRotation': 0,
                        'legend': 'Average Estimation of Prices',
                        'legendOffset': -40,
                        'legendPosition': 'middle',
                        'truncateTickAt': 0
                    },
                            ), key='first'
                        )

            mui.Paper(
                nivo.Line(
                    data =awareness_dict2,
                    margin={ 'top': 50, 'right': 110, 'bottom': 50, 'left': 60 },
                    xScale={ 'type': 'point' },
                    yScale={
                        'type': 'linear',
                        'min': 'auto',
                        'max': 'auto',
                        'stacked': False,
                        'reverse': False
                    },
                    
                    useMesh=True,
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
                        
                        'legendOffset': 36,
                        'legendPosition': 'middle',
                        'truncateTickAt': 0
                    },
                    axisLeft={
                        'tickSize': 5,
                        'tickPadding': 5,
                        'tickRotation': 0,
                        'legend': 'Average Estimation of Prices',
                        'legendOffset': -40,
                        'legendPosition': 'middle',
                        'truncateTickAt': 0
                    },
                            ), key='third'
                        )

            mui.Paper(
                nivo.Line(
                    data =awareness_dict3,
                    margin={ 'top': 50, 'right': 110, 'bottom': 50, 'left': 60 },
                    xScale={ 'type': 'point' },
                    yScale={
                        'type': 'linear',
                        'min': 'auto',
                        'max': 'auto',
                        'stacked': False,
                        'reverse': False
                    },
                    
                    useMesh=True,
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
                        
                        'legendOffset': 36,
                        'legendPosition': 'middle',
                        'truncateTickAt': 0
                    },
                    axisLeft={
                        'tickSize': 5,
                        'tickPadding': 5,
                        'tickRotation': 0,
                        'legend': 'Average Estimation of Prices',
                        'legendOffset': -40,
                        'legendPosition': 'middle',
                        'truncateTickAt': 0
                    },
                            ), key='extra'
                        )

           
    if select_metric in bar_charts:
        layout2 = [
            dashboard.Item("fourth", 0,0,5,3),
            dashboard.Item("fifth", 5,0,5,3),
            dashboard.Item("sixth", 0,5,5,3),
            dashboard.Item("extra2", 5,5,5,3),
        ]

        with dashboard.Grid(layout2):
            
            mui.Box(
                nivo.Bar(
                    data=overestimate_bar_dict,
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
                        
                        'legendPosition': 'middle',
                        'legendOffset': 32,
                        'truncateTickAt': 0
                    },
                    axisLeft={
                        'tickSize': 5,
                        'tickPadding': 5,
                        'tickRotation': 0,
                        'legend': 'Average Estimation of Prices',
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
            
            real_dict = [{'Item': 'Movie Ticket', 'Price':  250, }, {'Item':'Medium Pizza','Price':300}, {'Item':'Coca Cola', 'Price':40},{'Item':'Shampoo', 'Price':300},'''{'Item': 'Oven', 'Price':10000}''' ]
            mui.Paper(
                nivo.Bar(
                    data=real_dict,
                    keys= ['Price'],
                    indexBy='Item',
                    
                    margin={ 'top': 50, 'right':40, 'bottom': 50, 'left': 80 },
                    padding=0.3,
                    layout='horizontal',
                    enableTotals = True,
                    enableLabel= True,
                    labelPosition='end',
                    labelOffset= 10,
                    
                    )
                 , key='fifth')

            mui.Box(
                nivo.Bar(
                    data=overestimate_bar_dict2,
                    keys=select_product2,
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
                        
                        'legendPosition': 'middle',
                        'legendOffset': 32,
                        'truncateTickAt': 0
                    },
                    axisLeft={
                        'tickSize': 5,
                        'tickPadding': 5,
                        'tickRotation': 0,
                        'legend': 'Average Estimation of Prices',
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

                ), key = 'sixth'
            )
                
            mui.Box(
                nivo.Bar(
                    data=overestimate_bar_dict3,
                    keys=select_product3,
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
                        
                        'legendPosition': 'middle',
                        'legendOffset': 32,
                        'truncateTickAt': 0
                    },
                    axisLeft={
                        'tickSize': 5,
                        'tickPadding': 5,
                        'tickRotation': 0,
                        'legend': 'Average Estimation of Prices',
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

                ), key = 'extra2'
            )
                
