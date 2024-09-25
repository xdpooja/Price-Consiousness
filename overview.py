import streamlit as st
import pandas as pd
from streamlit_elements import *
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
            counts = df[select_entity].value_counts()
            
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
            
            result_dict2 = build_entity_count_dict2(data, select_product)
            
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
        
        if select_entity =='Reasonability of prices':
            col1, col2 = st.columns(2)
            with col1 : 
                select_metric = st.selectbox('Select Reasonability', ['Overcharged', 'Undercharged', 'Fairly Charged'])
            with col2:
                select_product = st.multiselect('Select Categories', options= [ 'Leisure; entertainment and travel', 'Food and dishes', 'Commodities and groceries', 'Productivity; gadgets and technology','Lifestyle; beauty and clothing'], default=['Leisure; entertainment and travel', 'Food and dishes', 'Commodities and groceries', 'Productivity; gadgets and technology','Lifestyle; beauty and clothing'])
                    
            def build_entity_count_dict2(df,select_product, select_entity):
                # Get value counts for the selected column
                counts = df[select_product][df[select_product]==select_entity].count()
                
                # Convert the counts into the desired dictionary format
                entity_count_dict = [{'category': category, 'count': count} for category, count in counts.items()]
                
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
            col1, col2 = st.columns(2)
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

            with col1: 
                select_change = st.selectbox('Choose Price Change', ['Increase in Prices', 'Decrease in Prices'])
            with col2: 

                if select_change == 'Increase in Prices':
                
                    select_product = st.multiselect(
                        "Product Category", 
                        increase_columns , 
                        default=increase_columns , 
                        format_func=lambda x: option_map_increase.get(x, option_map_decrease.get(x))
                    )
                
                if select_change == 'Decrease in Prices':

                    select_product = st.multiselect(
                        "Product Category", 
                        decrease_columns , 
                        default=decrease_columns , 
                        format_func=lambda x: option_map_decrease.get(x, option_map_decrease.get(x))
                    )
                    
            def build_entity_count_dict2(df, select_entity):
                # Get value counts for the selected column
                dummy = [ ]
                for i in select_entity:
                    counts_yes = df[i].value_counts()
                    dummy.append(counts_yes)

                entity_count_dict = []
                for x in range(len(dummy)):
                    entity_count_dict.append({'category': category, 'count': count} for category, count in dummy[x].items())
                    bleh =[ count for category, count in dummy[x].items()]
                    st.write(dummy[x])
                counts_no = df[select_entity][df[select_entity]=='No'].value_counts()
                # Convert the counts into the desired dictionary format
                
                
                return entity_count_dict
            
            result_dict2 = build_entity_count_dict2(data, select_product)
            
            st.write(result_dict2)