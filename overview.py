import streamlit as st
import pandas as pd
from streamlit_elements import *
st.set_page_config(layout="wide")


data = pd.read_csv("final.csv")

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
