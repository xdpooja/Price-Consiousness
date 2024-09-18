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


# For Increase
if select_metric != 'Feeling Towards Price Of Items (Increase in Price)' and select_metric != 'Feeling Towards Price Of Items (Decrease in Price)':
    filtered_df_increase = data[selected_increase + [select_metric]]
    melted_increase_df = filtered_df_increase.melt(id_vars=[select_metric], var_name='Category', value_name='Sensitivity')

# For Decrease
    filtered_df_decrease = data[selected_decrease + [select_metric]]
    melted_decrease_df = filtered_df_decrease.melt(id_vars=[select_metric], var_name='Category', value_name='Sensitivity')


line_charts = ['Age', 'Income', 'time category','willingness for additional charges']
bar_charts = ['Gender', 'Location', 'Decision maker', 'payment preference','shopping preference','planned or preplanned', 'transaction frequency']
special_charts = ['Feeling Towards Price Of Items (Increase in Price)', 'Feeling Towards Price Of Items (Decrease in Price)']

#for special charts 
if select_metric in special_charts:
    def process_category_fair(feeling_col, response_col):
        # Filter for 'fairly charged'
        fairly_charged_df = data[data[feeling_col] == 'Fairly Charged']
        
        # Count 'yes' responses
        response_counts = fairly_charged_df[response_col].value_counts()
        
        return response_counts.get('Yes', 0), response_counts.get('No', 0)
    
    # List of categories and their respective columns
    categories = {
        'Leisure and Travel': ('Leisure; entertainment and travel', 'Leisure; entertainment and travel.1'),
        'Food and Dishes': ('Food and dishes', 'Food and dishes.1'),
        'Commodities and Groceries': ('Commodities and groceries', 'Commodities and groceries.1'),
        'Productivity and Technology': ('Productivity; gadgets and technology', 'Productivity; gadgets and technology.1'),
        'Lifestyle and Clothing': ('Lifestyle; beauty and clothing', 'Lifestyle; beauty and clothing.1')
    }

    special_charts_price_increase_fair = {'Category': [], 'Yes Count': [], 'No Count': []}

    for category, (feeling_col, response_col) in categories.items():
        yes_count_fair, no_count_fair = process_category_fair(feeling_col, response_col)
        special_charts_price_increase_fair['Category'].append(category)
        special_charts_price_increase_fair['Yes Count'].append(yes_count_fair)
        special_charts_price_increase_fair['No Count'].append(no_count_fair)
        
    fair_df = pd.DataFrame(special_charts_price_increase_fair).to_dict(orient='records')
    
    def process_category_over(feeling_col, response_col):
        # Filter for 'fairly charged'
        over_charged_df = data[data[feeling_col] == 'Overcharged']
        
        # Count 'yes' responses
        response_counts = over_charged_df[response_col].value_counts()
        
        return response_counts.get('Yes', 0), response_counts.get('No', 0)
    
    special_charts_price_increase_over = {'Category': [], 'Yes Count': [], 'No Count': []}

    for category, (feeling_col, response_col) in categories.items():
        yes_count_over, no_count_over = process_category_over(feeling_col, response_col)
        special_charts_price_increase_over['Category'].append(category)
        special_charts_price_increase_over['Yes Count'].append(yes_count_over)
        special_charts_price_increase_over['No Count'].append(no_count_over)
        
    over_df = pd.DataFrame(special_charts_price_increase_over).to_dict(orient='records')

    def process_category_under(feeling_col, response_col):
        # Filter for 'fairly charged'
        under_charged_df = data[data[feeling_col] == 'Undercharged']
        
        # Count 'yes' responses
        response_counts = under_charged_df[response_col].value_counts()
        
        return response_counts.get('Yes', 0), response_counts.get('No', 0)
    
    special_charts_price_increase_under = {'Category': [], 'Yes Count': [], 'No Count': []}

    for category, (feeling_col, response_col) in categories.items():
        yes_count_under, no_count_under = process_category_under(feeling_col, response_col)
        special_charts_price_increase_under['Category'].append(category)
        special_charts_price_increase_under['Yes Count'].append(yes_count_under)
        special_charts_price_increase_under['No Count'].append(no_count_under)
        
    under_df = pd.DataFrame(special_charts_price_increase_under).to_dict(orient='records')
   
    def process_category_fair_decrease(feeling_col, response_col):
        # Filter for 'fairly charged'
        fairly_charged_df = data[data[feeling_col] == 'Fairly Charged']
        
        # Count 'yes' responses
        response_counts = fairly_charged_df[response_col].value_counts()
        
        return response_counts.get('Yes', 0), response_counts.get('No', 0)
    
    # List of categories and their respective columns
    categories2 = {
        'Leisure and Travel': ('Leisure; entertainment and travel', 'decrease Leisure; entertainment and travel'),
        'Food and Dishes': ('Food and dishes', 'decrease Food and dishes'),
        'Commodities and Groceries': ('Commodities and groceries', 'decrease Commodities and groceries'),
        'Productivity and Technology': ('Productivity; gadgets and technology', 'decrease Productivity; gadgets and technology'),
        'Lifestyle and Clothing': ('Lifestyle; beauty and clothing', 'decerase Lifestyle; beauty and clothing')
    }
    special_charts_price_decrease_fair = {'Category': [], 'Yes Count': [], 'No Count': []}

    for category, (feeling_col, response_col) in categories2.items():
        yes_count_fair, no_count_fair = process_category_fair_decrease(feeling_col, response_col)
        special_charts_price_decrease_fair['Category'].append(category)
        special_charts_price_decrease_fair['Yes Count'].append(yes_count_fair)
        special_charts_price_decrease_fair['No Count'].append(no_count_fair)
        
    fair_decrease_df = pd.DataFrame(special_charts_price_decrease_fair).to_dict(orient='records')
   
    def process_category_over_decrease(feeling_col, response_col):
        # Filter for 'fairly charged'
        over_charged_df = data[data[feeling_col] == 'Fairly Charged']
        
        # Count 'yes' responses
        response_counts = over_charged_df[response_col].value_counts()
        
        return response_counts.get('Yes', 0), response_counts.get('No', 0)

    special_charts_price_decrease_over = {'Category': [], 'Yes Count': [], 'No Count': []}

    for category, (feeling_col, response_col) in categories2.items():
        yes_count_fair, no_count_fair = process_category_over_decrease(feeling_col, response_col)
        special_charts_price_decrease_over['Category'].append(category)
        special_charts_price_decrease_over['Yes Count'].append(yes_count_fair)
        special_charts_price_decrease_over['No Count'].append(no_count_fair)
        
    over_decrease_df = pd.DataFrame(special_charts_price_decrease_over).to_dict(orient='records')   
    
    def process_category_under_decrease(feeling_col, response_col):
        # Filter for 'fairly charged'
        over_charged_df = data[data[feeling_col] == 'Fairly Charged']
        
        # Count 'yes' responses
        response_counts = over_charged_df[response_col].value_counts()
        
        return response_counts.get('Yes', 0), response_counts.get('No', 0)

    special_charts_price_decrease_under = {'Category': [], 'Yes Count': [], 'No Count': []}

    for category, (feeling_col, response_col) in categories2.items():
        yes_count_fair, no_count_fair = process_category_over_decrease(feeling_col, response_col)
        special_charts_price_decrease_under['Category'].append(category)
        special_charts_price_decrease_under['Yes Count'].append(yes_count_fair)
        special_charts_price_decrease_under['No Count'].append(no_count_fair)
        
    under_decrease_df = pd.DataFrame(special_charts_price_decrease_under).to_dict(orient='records')
   
    

if select_metric in line_charts:
    def create_price_increase_yes_dict(melted_df, selected_people_column, selected_price_columns):
        price_increase_yes_dict = []

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
                    (melted_df['Category'] == product) &
                    (melted_df['Sensitivity'] == 'Yes')
                ].shape[0]
                
                product_data["data"].append({"x": value, "y": overcharged_count})
            
            price_increase_yes_dict.append(product_data)
        
        return price_increase_yes_dict

    price_increase_yes_dict = create_price_increase_yes_dict(melted_increase_df, select_metric, select_product)
    #st.write(overestimate_dict)

    def create_price_increase_no_dict(melted_df, selected_people_column, selected_price_columns):
        price_increase_no_dict = []

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
                fairlycharged_count = melted_df[
                    (melted_df[selected_people_column] == value) &
                    (melted_df['Category'] == product) &
                    (melted_df['Sensitivity'] == 'No')
                ].shape[0]
                
                product_data["data"].append({"x": value, "y": fairlycharged_count})
            
            price_increase_no_dict.append(product_data)
        
        return price_increase_no_dict
    
    price_increase_no_dict = create_price_increase_no_dict(melted_increase_df, select_metric, select_product)
    

    def create_price_decrease_yes_dict(melted_df, selected_people_column, selected_price_columns):
        price_decrease_yes_dict = []

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
                fairlycharged_count = melted_df[
                    (melted_df[selected_people_column] == value) &
                    (melted_df['Category'] == product) &
                    (melted_df['Sensitivity'] == 'Yes')
                ].shape[0]
                
                product_data["data"].append({"x": value, "y": fairlycharged_count})
            
            price_decrease_yes_dict.append(product_data)
        
        return price_decrease_yes_dict
    
    price_decrease_yes_dict = create_price_decrease_yes_dict(melted_decrease_df, select_metric, selected_decrease)
 
    def create_price_decrease_no_dict(melted_df, selected_people_column, selected_price_columns):
        price_decrease_no_dict = []

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
                fairlycharged_count = melted_df[
                    (melted_df[selected_people_column] == value) &
                    (melted_df['Category'] == product) &
                    (melted_df['Sensitivity'] == 'No')
                ].shape[0]
                
                product_data["data"].append({"x": value, "y": fairlycharged_count})
            
            price_decrease_no_dict.append(product_data)
        
        return price_decrease_no_dict
    
    price_decrease_no_dict = create_price_decrease_no_dict(melted_decrease_df, select_metric, selected_decrease)
    

if select_metric in bar_charts:

    def create_price_increase_yes_bar_dict(melted_df, selected_people_column, selected_price_columns):
        custom_dict = []
        order_dict = {'Decision maker': ['No', 'Yes, but only for myself', 'Yes, for the whole household']}
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
                    (melted_df['Category'] == product) &
                    (melted_df['Sensitivity'] == 'Yes')
                ].shape[0]
                
                # Add the product value and corresponding color
                entity_key = product  # Remove spaces from the product name
                entry[entity_key] = overestimate_count
                entry[f"{entity_key}Color"] = colors[j % len(colors)]
            
            custom_dict.append(entry)
        
        return custom_dict
    
    price_increase_yes_bar_dict = create_price_increase_yes_bar_dict(melted_increase_df, select_metric, select_product)

    def create_price_increase_no_bar_dict(melted_df, selected_people_column, selected_price_columns):
        price_increase_no_bar_dict = []
        
        colors = ['hsl(314, 70%, 50%)', 'hsl(173, 70%, 50%)', 'hsl(252, 70%, 50%)', 
                'hsl(125, 70%, 50%)', 'hsl(48, 70%, 50%)']  # Add more colors as needed
        
        order_dict = {'Decision maker': ['No', 'Yes, but only for myself', 'Yes, for the whole household']}
        if selected_people_column in order_dict:
            ordered_values = order_dict[selected_people_column]
        else:
            ordered_values = melted_df[selected_people_column].unique()

        
        for i, value in enumerate(ordered_values):
            entry = {selected_people_column: value}
            
            for j, product in enumerate(selected_price_columns):
                # Count the number of "overestimated" entries for this product and selected group
                awareness_count = melted_df[
                    (melted_df[selected_people_column] == value) &
                    (melted_df['Category'] == product) &
                    (melted_df['Sensitivity'] == 'No')
                ].shape[0]
                
                # Add the product value and corresponding color
                entity_key = product  # Remove spaces from the product name
                entry[entity_key] = awareness_count
                entry[f"{entity_key}Color"] = colors[j % len(colors)]
            
            price_increase_no_bar_dict.append(entry)
        
        return price_increase_no_bar_dict
    
    price_increase_no_bar_dict = create_price_increase_no_bar_dict(melted_increase_df, select_metric, select_product)
    
    def create_price_decrease_yes_bar_dict(melted_df, selected_people_column, selected_price_columns):
        price_decrease_yes_bar_dict = []
        
        colors = ['hsl(314, 70%, 50%)', 'hsl(173, 70%, 50%)', 'hsl(252, 70%, 50%)', 
                'hsl(125, 70%, 50%)', 'hsl(48, 70%, 50%)']  # Add more colors as needed
        
        order_dict = {'Decision maker': ['No', 'Yes, but only for myself', 'Yes, for the whole household']}
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
                    (melted_df['Category'] == product) &
                    (melted_df['Sensitivity'] == 'Yes')
                ].shape[0]
                
                # Add the product value and corresponding color
                entity_key = product  # Remove spaces from the product name
                entry[entity_key] = underestimation_count
                entry[f"{entity_key}Color"] = colors[j % len(colors)]
            
            price_decrease_yes_bar_dict.append(entry)
        
        return price_decrease_yes_bar_dict
    
    price_decrease_yes_bar_dict = create_price_decrease_yes_bar_dict(melted_decrease_df, select_metric, selected_decrease)

    def create_price_decrease_no_bar_dict(melted_df, selected_people_column, selected_price_columns):
        price_decrease_no_bar_dict = []
        
        colors = ['hsl(314, 70%, 50%)', 'hsl(173, 70%, 50%)', 'hsl(252, 70%, 50%)', 
                'hsl(125, 70%, 50%)', 'hsl(48, 70%, 50%)']  # Add more colors as needed
        
        order_dict = {'Decision maker': ['No', 'Yes, but only for myself', 'Yes, for the whole household']}
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
                    (melted_df['Category'] == product) &
                    (melted_df['Sensitivity'] == 'No')
                ].shape[0]
                
                # Add the product value and corresponding color
                entity_key = product  # Remove spaces from the product name
                entry[entity_key] = underestimation_count
                entry[f"{entity_key}Color"] = colors[j % len(colors)]
            
            price_decrease_no_bar_dict.append(entry)
        
        return price_decrease_no_bar_dict
    
    price_decrease_no_bar_dict = create_price_decrease_no_bar_dict(melted_decrease_df, select_metric, selected_decrease)


with elements(dashboard):
    if select_metric in line_charts:
        layout1 = [
            dashboard.Item("first", 0,0,5,3),
            dashboard.Item("second", 5,0,5,3),
            dashboard.Item("third", 0,5,5,3),
            dashboard.Item("fourth",5,5,5,3 )
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
                    data =price_increase_no_dict,
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
                        'legend': 'Reluctance to buy after price increase',
                        'legendOffset': -40,
                        'legendPosition': 'middle',
                        'truncateTickAt': 0
                    },
                            ), key='second'
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
                            ), key='third'
                        )

            mui.Paper(
                nivo.Line(
                    data =price_decrease_no_dict,
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
                        'legend': 'Reluctance to buy after price decrease',
                        'legendOffset': -40,
                        'legendPosition': 'middle',
                        'truncateTickAt': 0
                    },
                            ), key='fourth'
                        )

    if select_metric in bar_charts:
        layout2 = [
            dashboard.Item("fifth", 0,0,5,3),
            dashboard.Item("sixth", 5,0,5,3),
            dashboard.Item("seventh", 0,5,5,3),
            dashboard.Item('eighth', 5,5,5,3)
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

                ), key = 'fifth'
            )

            mui.Box(
                nivo.Bar(
                    data=price_increase_no_bar_dict,
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
                        'legend': 'Reluctance to buy after price increase',
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

                ), key = 'seventh'
            )

            mui.Box(
                nivo.Bar(
                    data=price_decrease_no_bar_dict,
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
                        'legend': 'Reluctance to buy even after price decrease',
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

                ), key = 'eighth'
            )

    if select_metric =='Feeling Towards Price Of Items (Increase in Price)':

        layout3 = [
            dashboard.Item("ninth", 0,0,5,3),
            dashboard.Item("tenth", 5,0,5,3),
            dashboard.Item("eleventh", 0,5,5,3),
            
        ]

        with dashboard.Grid(layout3):
            
            mui.Box(
                nivo.Bar(
                    data=fair_df,
                    keys=['Yes Count', 'No Count'],
                    indexBy='Category',
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
                        'legend': 'People who feel they are being fairly charged',
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

                ), key = 'ninth'
            )

            mui.Box(
                nivo.Bar(
                    data=over_df,
                    keys=['Yes Count', 'No Count'],
                    indexBy='Category',
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
                        'legend': 'People who feel they are being overcharged',
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

                ), key = 'tenth'
            )

            mui.Box(
                nivo.Bar(
                    data=under_df,
                    keys=['Yes Count', 'No Count'],
                    indexBy='Category',
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
                        'legend': 'People who feel they are being undercharged',
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

                ), key = 'eleventh'
            )

    if select_metric== 'Feeling Towards Price Of Items (Decrease in Price)':
        
        layout4 = [
            dashboard.Item("twelvth", 0,0,5,3),
            dashboard.Item("thirteenth", 5,0,5,3),
            dashboard.Item("fourteenth", 0,5,5,3),
            
        ]

        with dashboard.Grid(layout4):
            
            mui.Box(
                nivo.Bar(
                    data=fair_decrease_df,
                    keys=['Yes Count', 'No Count'],
                    indexBy='Category',
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
                        'legend': 'People who feel they are being fairly charged',
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

                ), key = 'twelvth'
            )

            mui.Box(
                nivo.Bar(
                    data=over_decrease_df,
                    keys=['Yes Count', 'No Count'],
                    indexBy='Category',
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
                        'legend': 'People who feel they are being overcharged',
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

                ), key = 'thirteenth'
            )

            mui.Box(
                nivo.Bar(
                    data=under_decrease_df,
                    keys=['Yes Count', 'No Count'],
                    indexBy='Category',
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
                        'legend': 'People who feel they are being undercharged',
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

                ), key = 'fourteenth'
            )
