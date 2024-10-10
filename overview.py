import streamlit as st
import pandas as pd
from streamlit_elements import *
import numpy as np
st.set_page_config(layout="wide")


data = pd.read_csv("final.csv")

tab1, tab2 ,tab3 = st.tabs(['Demographics', 'Univariates', 'Bivariates'])

with tab1:
    st.write(data.head())
    age_density_dict = [ {
        'id' : '18-24',
        'label': '18-24',
        'value': 210,
        "color": "hsl(355, 70%, 50%)" },
        {
        'id' : '25-34',
        'label': '25-34',
        'value': 94,
        "color": "hsl(277, 70%, 50%)"  
        },
        {'id' : '35-54',
        'label': '35-54',
        'value': 32,
        "color": "hsl(151, 70%, 50%)"},
        {
        'id' : '55+',
        'label': '55+',
        'value': 12,
        "color": "hsl(127, 70%, 50%)"
        }
        
    ]

    df_gender = pd.DataFrame(data['Gender'].value_counts())
    df_gender['Gender']= df_gender.index
    gender_density_dict = df_gender.to_dict(orient='records')

    df_location = pd.DataFrame(data['Location'].value_counts())
    df_location['Location']= df_location.index
    location_density_dict = df_location.to_dict(orient='records')

    with elements(dashboard):
        layout =[
            dashboard.Item("first", 0,0,4,2.5),
            dashboard.Item("second", 5,0,5,2.5),
            dashboard.Item("third", 0,6,10,2.5),
        ]

        with dashboard.Grid(layout):

            mui.Box(nivo.Pie(
                data = age_density_dict,
                margin={ 'top': 40, 'right': 80, 'bottom': 80, 'left': 80 },
            innerRadius={0.5},
            padAngle={0.7},
            cornerRadius={3},
            activeOuterRadiusOffset={8},
            borderWidth={1},
            borderColor={
                'from': 'color',
                'modifiers': [
                    [
                        'darker',
                        0.2
                    ]
                ]
            },
            arcLinkLabelsSkipAngle={10},
            arcLinkLabelsTextColor="#333333",
            arcLinkLabelsThickness={2},
            arcLinkLabelsColor={ 'from': 'color' },
            arcLabelsSkipAngle={10},
            arcLabelsTextColor={
                'from': 'color',
                'modifiers': [
                    [
                        'darker',
                        2
                    ]
                ]
            },

            legends=[
                {
                    'anchor': 'bottom',
                    'direction': 'row',
                    'justify': False,
                    'translateX': 0,
                    'translateY': 56,
                    'itemsSpacing': 0,
                    'itemWidth': 100,
                    'itemHeight': 18,
                    'itemTextColor': '#999',
                    'itemDirection': 'left-to-right',
                    'itemOpacity': 1,
                    'symbolSize': 18,
                    'symbolShape': 'circle',
                    'effects': [
                        {
                            'on': 'hover',
                            'style': {
                                'itemTextColor': '#000'
                            }
                        }
                    ]
                }
            ]

            ), key = 'first')


            mui.Box(
                nivo.Bar(
                data=gender_density_dict,
                keys=['count'],
                indexBy="Gender",
                padding={0.3},
                margin={ "top": 20, "right": 20, "bottom": 40, "left":100},
                axisBottom={"tickSize":0, "tickPadding":2, "tickRotation":0,"legend": "Count",  "legendPosition": 'middle', "legendOffset":20},
                axisLeft={"legend":"Genders","legendPosition":"middle", "tickSize":0, "legendOffset":-80}, colors={"scheme": "category10"},
                borderWidth={2},
                borderColor={"from":"color","modifiers":[["darker",0.4]]},  
                isFocusable=True,
                layout="horizontal",
                enableGridY=False,
                enableGridX= True,
                enableLabel=False          
                ), key = 'second'
            )

            mui.Box(
                nivo.Bar(
                data=location_density_dict,
                keys=['count'],
                indexBy="Location",
                padding={0.3},
                margin={ "top": 20, "right": 20, "bottom": 40, "left":100},
                axisBottom={"tickSize":0, "tickPadding":2, "tickRotation":0,"legend": "Count",  "legendPosition": 'middle', "legendOffset":20},
                axisLeft={"legend":"Locations","legendPosition":"middle", "tickSize":0, "legendOffset":-80}, colors={"scheme": "category10"},
                borderWidth={2},
                borderColor={"from":"color","modifiers":[["darker",0.4]]},  
                isFocusable=True,

                enableGridY=True,
                enableGridX= False,
                enableLabel=False          
                ), key = 'third'
            )


with tab2:
  
    select_entity = st.selectbox('Choose Entity', options=['Income', 'Decision maker', 'Average Price Guess', 'Reasonability of prices', 'Sensitivity of prices', 'payment preference', 'shopping preference', 'planned or preplanned', 'transaction frequency', 'willingness for additional charges', 'feeling towards discount', 'brand charges more than another'])
    other_options = [ 'Average Price Guess', 'Reasonability of prices', 'Sensitivity of prices']


    
        
    if select_entity not in other_options:
        
        def build_entity_count_dict(df, select_entity):
            # Get value counts for the selected column
            counts = df[select_entity].value_counts(normalize=True)* 100
            
            # Convert the counts into the desired dictionary format
            entity_count_dict = [{'category': category, 'count': count} for category, count in counts.items()]
            
            return entity_count_dict
        
        result_dict1 = build_entity_count_dict(data, select_entity)
        

        with elements('dashboard'):
            layout1 = [
                dashboard.Item("extra",0,0,5,3)
            ]

            with dashboard.Grid(layout1):
                

                mui.Box(
                    nivo.Bar(
                    data=result_dict1,
                    keys=['count'],
                    indexBy='category',
                    padding={0.3},
                    margin={ "top": 20, "right": 20, "bottom": 40, "left":100},
                    axisBottom={"tickSize":0, "tickPadding":2, "tickRotation":0,"legend": "Count",  "legendPosition": 'middle', "legendOffset":20},
                    axisLeft={"legend":select_entity,"legendPosition":"middle", "tickSize":0, "legendOffset":-80}, colors={"scheme": "category10"},
                    borderWidth={2},
                    borderColor={"from":"color","modifiers":[["darker",0.4]]},  
                    isFocusable=True,
                    layout="vertical",
                    enableGridY=False,
                    enableGridX= True,
                    enableLabel=False          
                    ), key = 'extra'
                )
    
    if select_entity in other_options:
        if select_entity == 'Average Price Guess': 
            col1, col2 = st.columns(2)
            with col1:
                select_product = st.multiselect('Select Products', ['movie ticket','medium pizza', 'coca cola', 'oven', 'shampoo'], default=['movie ticket','medium pizza', 'coca cola', 'oven', 'shampoo'])

             
            def build_entity_count_dict2(df, select_entity):
                # Get value counts for the selected column
                counts = df[select_entity].mean().round(2)
                
                # Convert the counts into the desired dictionary format
                entity_count_dict = [{'category': category, 'count': count} for category, count in counts.items()]
                
                return entity_count_dict
            
            def build_entity_percent_dict(df, select_entity):
                # Get value counts for the selected column
                counts = df[select_entity].mean().round(2)
                
                # Convert the counts into the desired dictionary format
                entity_count_dict = [{'category': category, 'count': count} for category, count in counts.items()]
                
                return entity_count_dict
            result_dict2 = build_entity_count_dict2(data, select_product)
            label =  ['movie ticket_label', 'medium pizza_label',
       'coca cola_label', 'oven_label', 'shampoo_label']
            result_list = []

            for i in label:
                # Get the value counts as percentage for the column
                x = data[i].value_counts(normalize=True).round(2)* 100
                
                # Create a dictionary for each product
                product_dict = {'category': i}
                
                # Update the dictionary with the value counts
                product_dict.update(x.to_dict())
                
                # Append the dictionary to the result list
                result_list.append(product_dict)
            
            # Display the result
            
            with elements('dashboard2'):
                layout2 = [
                    dashboard.Item("extra2",0,0,5,3),
                    dashboard.Item("extra3", 0, 6, 10,3)
                ]

                with dashboard.Grid(layout2):
                    

                    mui.Box(
                        nivo.Bar(
                        data=result_dict2,
                        keys=['count'],
                        indexBy='category',
                        padding={0.3},
                        margin={ "top": 20, "right": 20, "bottom": 40, "left":100},
                        axisBottom={"tickSize":0, "tickPadding":2, "tickRotation":0,"legend": "Count",  "legendPosition": 'middle', "legendOffset":20},
                        axisLeft={"legend":select_entity,"legendPosition":"middle", "tickSize":0, "legendOffset":-80}, colors={"scheme": "category10"},
                        borderWidth={2},
                        borderColor={"from":"color","modifiers":[["darker",0.4]]},  
                        isFocusable=True,
                        enableLabel= True,
                        labelPosition='end',
                        layout="vertical",
                        enableGridY=False,
                        enableGridX= True,
                            
                        ), key = 'extra2'
                    )
        
                    mui.Box(
                        nivo.Bar(
                        data=result_list,
                        keys=["more than 20% over", "5-20% over", "accurate", "5-20% under", "more than 20% under"],
                        indexBy='category',
                        padding={0.3},
                        margin={ "top": 20, "right": 80, "bottom": 40, "left":100},
                        axisBottom={"tickSize":0, "tickPadding":2, "tickRotation":0,"legend": "Count",  "legendPosition": 'middle', "legendOffset":20},
                        axisLeft={"legend":select_entity,"legendPosition":"middle", "tickSize":0, "legendOffset":-80}, colors={"scheme": "category10"},
                        borderWidth={2},
                        borderColor={"from":"color","modifiers":[["darker",0.4]]},  
                        isFocusable=True,
                        enableLabel= True,
                        labelPosition='end',
                        layout="vertical",
                        enableGridY=False,
                        enableGridX= True,
                        legends=[ {
                            'dataFrom': 'keys',
                            'anchor': 'bottom-right',
                            'direction': 'column',
                            'justify': False,
                            'translateX': 50,
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
                        
                        ), key = 'extra3'
                    )
        
        if select_entity =='Reasonability of prices':
            col1, col2 = st.columns(2)
            with col1 : 
                select_metric = st.selectbox('Select Reasonability', ['Overcharged', 'Undercharged', 'Fairly Charged'])
            with col2:
                select_product = st.multiselect('', options= [ 'Leisure; entertainment and travel', 'Food and dishes',
        'Commodities and groceries', 'Productivity; gadgets and technology',
        'Lifestyle; beauty and clothing',], default= [ 'Leisure; entertainment and travel', 'Food and dishes',
        'Commodities and groceries', 'Productivity; gadgets and technology',
        'Lifestyle; beauty and clothing',])
            def build_entity_count_dict2(df,select_product, select_entity):
                # Get value counts for the selected column
                counts = df[select_product][df[select_product]==select_entity].count()
                percentage = counts/230
                # Convert the counts into the desired dictionary format
                entity_count_dict = [{'category': category, 'count': percentage} for category, percentage in percentage.items()]
                
                return entity_count_dict
            
            result_dict2 = build_entity_count_dict2(data,select_product, select_metric)
            
            with elements('dashboard2'):
                layout2 = [
                    dashboard.Item("extra2",0,0,5,3)
                ]

                with dashboard.Grid(layout2):
                    

                    mui.Box(
                        nivo.Bar(
                        data=result_dict2,
                        keys=['count'],
                        indexBy='category',
                        padding={0.3},
                        margin={ "top": 20, "right": 20, "bottom": 40, "left":100},
                        axisBottom={"tickSize":0, "tickPadding":2, "tickRotation":0,"legend": "Count",  "legendPosition": 'middle', "legendOffset":20},
                        axisLeft={"legend":select_metric,"legendPosition":"middle", "tickSize":0, "legendOffset":-80}, colors={"scheme": "category10"},
                        borderWidth={2},
                        borderColor={"from":"color","modifiers":[["darker",0.4]]},  
                        isFocusable=True,
                        enableLabel= True,
                        labelPosition='end',
                        layout="vertical",
                        enableGridY=False,
                        enableGridX= True,
                            
                        ), key = 'extra2'
                    )

        if select_entity == 'Sensitivity of prices':
           
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
           
            select_change = st.selectbox('Choose Price Change', ['Increase in Prices', 'Decrease in Prices'])
            def build_entity_count_dict2(df):
                entity_count_dict = []  # Final list of dictionaries
                dummy = []  # Temporary list to store value counts
                
                # Determine which set of columns to use
                if select_change == 'Increase in Prices':
                    select_entity = increase_columns
                elif select_change == 'Decrease in Prices':
                    select_entity = decrease_columns
                
                # Gather value counts for the selected columns
                for i in select_entity:
                    counts_yes = df[i].value_counts(normalize=True).round(2) * 100
                    dummy.append(counts_yes)

                # Build the dictionary
                for x in range(len(dummy)):
                    yes_value = 0  # Initialize default values for Yes and No
                    no_value = 0
                    category_name = dummy[x].index.name  # Get the category name
                    
                    # Loop through the value counts for each category
                    for yes_no, count in dummy[x].items():
                        if yes_no == 'Yes':  # Check for "Yes"
                            yes_value = count
                        elif yes_no == 'No':  # Check for "No"
                            no_value = count
                    
                    # Append the dictionary for the category with Yes and No values
                    entity_count_dict.append({'category': category_name, 'Yes': yes_value, 'No': no_value})
                
                return entity_count_dict
      
            result_dict2 = build_entity_count_dict2(data)
            
            with elements('dashboard2'):
                layout2 = [
                    dashboard.Item("extra2",0,0,10,3)
                ]

                with dashboard.Grid(layout2):
                    
        
                    mui.Box(
                        nivo.Bar(
                        data=result_dict2,
                        keys=['Yes', 'No'],
                        indexBy='category',
                        padding={0.3},
                        margin={ "top": 20, "right": 20, "bottom": 40, "left":100},
                        axisBottom={"tickSize":0, "tickPadding":2, "tickRotation":0,"legend": "Count",  "legendPosition": 'middle', "legendOffset":20},
                        axisLeft={"legend":select_entity,"legendPosition":"middle", "tickSize":0, "legendOffset":-80}, colors={"scheme": "category10"},
                        borderWidth={2},
                        borderColor={"from":"color","modifiers":[["darker",0.4]]},  
                        isFocusable=True,
                        enableLabel= True,
                        labelPosition='end',
                        layout="vertical",
                        enableGridY=False,
                        enableGridX= True,
                                                legends=[ {
                            'dataFrom': 'keys',
                            'anchor': 'bottom-right',
                            'direction': 'column',
                            'justify': False,
                            'translateX': 50,
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




with tab3:
    

    products =  [ 'Leisure; entertainment and travel', 'Food and dishes',
        'Commodities and groceries', 'Productivity; gadgets and technology',
        'Lifestyle; beauty and clothing',]
    categories = ['Leisure', 'Food', 'Commodities', 'Productivity', 'Lifestyle']
    col3 , col4, col5 = st.columns(3)
    
    
    with col3:
        option1= st.selectbox(label= '', options=['Awareness of prices'],)
    with col4:
        option2 = st.selectbox(label='', options=['Perception about prices', 'Sensitivity of Prices'])
    with col5:
        option3 = st.selectbox('Average price guess', ["more than 20% over", "5-20% over", "accurate", "5-20% under", "more than 20% under"])
    
    data2 = pd.read_csv('final2.csv')
    
    if option2 == 'Perception about prices':
        dummy = st.selectbox('Select Perception', options=['Overcharged', 'Undercharged', 'Fairly Charged'])
        filtered_data = data2.loc[(data2[products] == dummy).any(axis=1), categories]
    
        result_dictt = []

        # Loop through each category and calculate the percentage of occurrences of option3
        for i, category in enumerate(categories):
            # Calculate the percentage of rows matching the selected option3
            count = (filtered_data[category] == option3).sum()
            total_count = len(filtered_data[category])
            
            if total_count > 0:
                percentage = (count / total_count) * 100
            else:
                percentage = 0  # Avoid division by zero
            
            result_dictt.append({
                'category': products[i],
                'count': round(percentage, 2)  # Rounded percentage for better readability
            })

    
    
        with elements('dashboard3'):
            layout2 = [
                dashboard.Item("extra2",0,0,10,3)
            ]

            with dashboard.Grid(layout2):
                

                mui.Box(
                    nivo.Bar(
                    data=result_dictt,
                    keys=['count'],
                    indexBy='category',
                    padding={0.3},
                    margin={ "top": 20, "right": 20, "bottom": 40, "left":100},
                    axisBottom={"tickSize":0, "tickPadding":2, "tickRotation":0,"legend": "Product",  "legendPosition": 'middle', "legendOffset":20},
                    axisLeft={"legend":f'People who feel {dummy} vs Price guess {option3}',"legendPosition":"middle", "tickSize":0, "legendOffset":-80}, colors={"scheme": "category10"},
                    borderWidth={2},
                    borderColor={"from":"color","modifiers":[["darker",0.4]]},  
                    isFocusable=True,
                    enableLabel= True,
                    labelPosition='end',
                    layout="vertical",
                    enableGridY=False,
                    enableGridX= True,
                                            legends=[ {
                        'dataFrom': 'keys',
                        'anchor': 'bottom-right',
                        'direction': 'column',
                        'justify': False,
                        'translateX': 50,
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

    if option2 == 'Sensitivity of Prices':
        option4 = st.selectbox(label='Increase or Decrease in Prices', options=['Increase', 'Decrease'])

        if option4 == 'Increase':
            columns = [
                'Leisure; entertainment and travel.1',
                'Food and dishes.1', 'Commodities and groceries.1',
                'Productivity; gadgets and technology.1',
                'Lifestyle; beauty and clothing.1',
            ]
        if option4 == 'Decrease':
            columns =  [
                'decrease Leisure; entertainment and travel',
                'decrease Food and dishes', 'decrease Commodities and groceries',
                'decrease Productivity; gadgets and technology',
                'decerase Lifestyle; beauty and clothing',
            ]

        filtered_data2 = data2[columns + categories]
       
        result_dictt2 = []
        for i, category in enumerate(categories):
                yes_count = (filtered_data2[columns[i]] == 'Yes').sum()
                no_count = (filtered_data2[columns[i]] == 'No').sum()
                total_count = yes_count + no_count
                
                if total_count > 0:
                    yes_percentage = (yes_count / total_count) * 100
                    no_percentage = (no_count / total_count) * 100
                else:
                    yes_percentage = 0  # Avoid division by zero
                    no_percentage = 0
                
                result_dictt2.append({
                    'category': category,
                    'yes': round(yes_percentage, 2),
                    'no': round(no_percentage, 2)
                })

    
        with elements('dashboard4'):
            layout2 = [
                dashboard.Item("extra2",0,0,10,3)
            ]

            with dashboard.Grid(layout2):
                

                mui.Box(
                    nivo.Bar(
                    data=result_dictt2,
                    keys=['yes', 'no'],
                    indexBy='category',
                    padding={0.3},
                    margin={ "top": 20, "right": 20, "bottom": 40, "left":100},
                    axisBottom={"tickSize":0, "tickPadding":2, "tickRotation":0,"legend": "Product",  "legendPosition": 'middle', "legendOffset":20},
                    axisLeft={"legend":f'Price guess {option3} vs Agreebality to buy when price {option4}',"legendPosition":"middle", "tickSize":0, "legendOffset":-80}, colors={"scheme": "category10"},
                    borderWidth={2},
                    borderColor={"from":"color","modifiers":[["darker",0.4]]},  
                    isFocusable=True,
                    enableLabel= True,
                    labelPosition='end',
                    layout="vertical",
                    enableGridY=False,
                    enableGridX= True,
                                            legends=[ {
                        'dataFrom': 'keys',
                        'anchor': 'bottom-right',
                        'direction': 'column',
                        'justify': False,
                        'translateX': 50,
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


