from jupyter_dash import JupyterDash 
import dash_table
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input,Output 
import plotly.express as px
import pandas as pd
import requests

app = JupyterDash(__name__)

df=pd.read_csv('zomato.csv')

#Data Engineering
df.loc[df['Currency'] == 'Botswana Pula(P)', 'Currency'] = 'Philippine Peso'
df.loc[df['Currency'] == 'Indian Rupees(Rs.)', 'Currency'] = 'Indian Rupee'
df.loc[df['Currency'] == 'Dollar($)', 'Currency'] = 'Australian Dollar'
df.loc[df['Currency'] == 'Brazilian Real(R$)', 'Currency'] = 'Brazilian Real'
df.loc[df['City'] == 'Bras韄lia', 'City'] = 'Brasilia'
df.loc[df['City'] == 'S恚o Paulo', 'City'] = 'Sao Paulo'
df.loc[df['City'] == 'Vineland Station', 'Currency'] = 'Canadian Dollar'
df.loc[df['City'] == 'Chatham-Kent', 'Currency'] = 'Canadian Dollar'
df.loc[df['City'] == 'Consort', 'Currency'] = 'Canadian Dollar'
df.loc[df['City'] == 'Yorkton', 'Currency'] = 'Canadian Dollar'
df.loc[df['Currency'] == 'Indonesian Rupiah(IDR)', 'Currency'] = 'Rupiah'
df.loc[df['Currency'] == 'NewZealand($)', 'Currency'] = 'New Zealand Dollar'
df.loc[df['Currency'] == 'Qatari Rial(QR)', 'Currency'] = 'Qatari Rial'
df.loc[df['City'] == 'Singapore', 'Currency'] = 'Singapore Dollar'
df.loc[df['Currency'] == 'Rand(R)', 'Currency'] = 'Rand'
df.loc[df['Currency'] == 'Sri Lankan Rupee(LKR)', 'Currency'] = '	Sri Lanka Rupee'
df.loc[df['Currency'] == 'Turkish Lira(TL)', 'Currency'] = 'Turkish Lira'
df.loc[df['City'] == '哿stanbul', 'City'] = 'Istanbul'
df.loc[df['Currency'] == 'Emirati Diram(AED)', 'Currency'] = 'UAE Dirham'
df.loc[df['Currency'] == 'Pounds(專)', 'Currency'] = 'Pound Sterling'
df.loc[df['Country Code'] == 216, 'Currency'] = 'US Dollar'


df1=['Restaurant Name','City','Cuisines','Average Cost for two','Price in INR','Aggregate rating','Rating text','Votes']
country=[]
c=['India','Australia','Brazil','Canada','Indonesia','New Zealand','Phillipines','Qatar','Singapore','South Africa',
   'Sri Lanka','Turkey','UAE','United Kingdom','United States	']
v=[1,14,30,37,94,148,162,166,184,189,191,208,214,215,216]

countries=[{"label":'India',"value":1},{"label":'Australia',"value":14},{"label":'Brazil',"value":30},{"label":'Canada',"value":37},
                              {"label":'Indonesia',"value":94},{"label":'New Zealand',"value":148},{"label":'Phillipines',"value":162},
                              {"label":'Qatar',"value":166},{"label":'Singapore',"value":184},{"label":'South Africa',"value":189},
                              {"label":'Sri Lanka',"value":191},{"label":'Turkey',"value":208},{"label":'UAE',"value":214},
                                            {"label":'United Kingdom',"value":215},{"label":'United States',"value":216}]
countries1={14:"AUD",30:'BRL',37:"CAD",
            94:'IDR',148:"NZD",162:'PHP',184:'SGD',189:'ZAR',215:'GBP',216:'USD'}
                              
for j in range(len(v)):
  country.append({'label':c[j],'value':v[j]})
colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}
def fig_outline(x,y,z):
    x(font_family="Courier New",font_color="blue",legend_title_font_color="green")
    y(title_font_family="Arial")
    z( type="rect",xref="paper",yref="paper",x0=0,y0=0, x1=1.0,y1=1.0,
                  line=dict(
                color="black",
                width=1,
            )
        )

#layout of app
app.layout = html.Div([
    html.Div([html.H1(children='ZOMATO DATA ANALYSIS',style={"color": "red", "font-weight": "bold"})]),
              
        html.Div([html.H2('Analysis of Costliest Restaurants ',style={"color": "#7D3C98", "font-weight": "bold"})]),
            html.Div([html.H3('Select Country :'),
            dcc.Dropdown(id='nadu',options=country,value=1,optionHeight=50)],
                    style={'width': '25%','display': 'inline-block'}),
            dcc.Graph(id='nadu-nagar'),html.Div(id='f'),
            dash_table.DataTable(id='frame_table',
                    columns=[{'id': c, 'name': c} for c in df1],page_size=15,

                    style_cell_conditional=[
                        {
                            'if': {'column_id': c},
                            'textAlign': 'left'
                        } for c in ['Restaurant Name','City','Cuisines','Average Cost for two',
                                    'Rating text','Votes'
]
                    ],
                    style_data={
                        'color': 'black',
                        'backgroundColor': 'white'
                    },
                    style_data_conditional=[
                        {
                            'if': {'row_index': 'odd'},
                            'backgroundColor': 'rgb(220, 220, 220)',
                        }
                    ],
                    style_header={
                        'backgroundColor': 'rgb(210, 210, 210)',
                        'color': 'black',
                        'fontWeight': 'bold'
                    }
                ),
            
         html.Div([
                html.Div([html.H2('Restaurant location analysis',style={"color": "#7D3C98", "font-weight": "bold"})]),
                  html.Div([html.P("Select a country:"),
                  dcc.RadioItems(
                      id='candidate', 
                      options=countries,
                      value=1,
                      inline=False)],style={'width': '25%','float': 'left','display': 'inline-block'}),
                  html.Div([dcc.Graph(id="map")],style={'width': '75%','display': 'inline-block'})]),
                  
                
          html.Div([html.H2('Rating analysis',style={"color": "#7D3C98", "font-weight": "bold"})]),
                html.Div([html.H3('Select Country :'),
                dcc.Dropdown(id='nad',options=country,value=1)],
                         style={'width': '25%','float': 'left','display': 'inline-block'}),
                html.Div([html.H3('Select City :'),
                dcc.Dropdown(id='nag')],style={'width': '25%','display': 'inline-block'}),
                dcc.Graph(id='nagar-cuisine'),
                html.Div(id='f1'),
                dash_table.DataTable(id='frame_table1',
                   columns=[{'id': c, 'name': c} for c in df1],page_size=15,

                    style_cell_conditional=[
                        {
                            'if': {'column_id': c},
                            'textAlign': 'left'
                        } for c in ['Restaurant Name','City','Cuisines','Average Cost for two',
                                    'Rating text','Votes'
]
                    ],
                    style_data={
                        'color': 'black',
                        'backgroundColor': 'white'
                    },
                    style_data_conditional=[
                        {
                            'if': {'row_index': 'odd'},
                            'backgroundColor': 'rgb(220, 220, 220)',
                        }
                    ],
                    style_header={
                        'backgroundColor': 'rgb(210, 210, 210)',
                        'color': 'black',
                        'fontWeight': 'bold'
                    }
                ),html.Div([dcc.Graph(id="map1")])
                ])
             
            
    

    
#callback to update the cities of selected country
@app.callback(
    Output('nag', 'options'),
    Input('nad', 'value'))
def set_cities_options(selected_country):
  filtered_city=df[df['Country Code'] == selected_country]
  b=filtered_city['City'].unique()
  return [{'label': i, 'value': i} for i in b]




#callback to update the scatter plot graph cities vs average cost of selected country
@app.callback(
    Output('nadu-nagar', 'figure'),
    Input('nadu', 'value'))
    
def update_graph(nadu_name):
    filtered_df = df[df['Country Code'] == nadu_name]
    a=[(country[i]["label"]) for i in range(len(country)) for key,value in country[i].items() if value==nadu_name]
    fig = px.scatter(filtered_df, x="City", y='Average Cost for two',
                     color='Average Cost for two',size='Average Cost for two',
                     hover_data=['Restaurant Name','Cuisines','Currency','Has Table booking'],
                     title=f'Analysis of price range in {str(a[0])}',
                     height=400)
   
    fig_outline(fig.update_layout,fig.update_xaxes,fig.add_shape)
    return fig

#callback to update the datatable title of a selected country's restaurants
@app.callback(
    Output('f', 'children'),
    [Input('nadu', 'value')])
def display_tabletitle(nadu_name):
    o=[(country[i]["label"]) for i in range(len(country)) for key,value in country[i].items() if value==nadu_name]
    return html.H3(f'Take a look at the Restaurants ranked from the costliest to cheapest in {str(o[0])}')

#callback to update the currency  of selected country to INR
@app.callback(
    Output('frame_table', 'data'),
    Input('nadu', 'value'))
def display_table(nadu_name):
        if nadu_name==1:
            m_curr=[]
            
            filtered_df_data = df[df['Country Code'] == nadu_name]
            for b in range(len(filtered_df_data)):
                m_curr.append('-')
            x1=filtered_df_data.sort_values(by='Average Cost for two', ascending=False)
            #d=list(x1['Average Cost for two'])
            z1=x1[['Restaurant Name','City','Cuisines']]
            z11=x1[['Aggregate rating','Rating text','Votes']]
            z2=pd.DataFrame({'Average Cost for two':x1['Average Cost for two'].astype(str)+' '+x1['Currency'],
                             'Price in INR':m_curr})
            #z4=pd.DataFrame(m_curr, columns=[])
            z3=pd.concat([z1,z2,z11], axis=1)
            
            return z3.to_dict(orient='records')
        
        elif nadu_name==166:
            filtered_df_data = df[df['Country Code'] == nadu_name]
            x1=filtered_df_data.sort_values(by='Average Cost for two', ascending=False)
            m_curr=list(round((x1['Average Cost for two']*22.53),2))
            #d=list(x1['Average Cost for two'])
            z1=x1[['Restaurant Name','City','Cuisines']]
            z11=x1[['Aggregate rating','Rating text','Votes']]
            z2=pd.DataFrame({'Average Cost for two':x1['Average Cost for two'].astype(str)+' '+x1['Currency'],
                             'Price in INR':m_curr})
            #z4=pd.DataFrame(m_curr, columns=[])
            z3=pd.concat([z1,z2,z11], axis=1)
            
            return z3.to_dict(orient='records')
        elif nadu_name==191:
            filtered_df_data = df[df['Country Code'] == nadu_name]
            x1=filtered_df_data.sort_values(by='Average Cost for two', ascending=False)
            m_curr=list(round((x1['Average Cost for two']*0.26),2))
            #d=list(x1['Average Cost for two'])
            z1=x1[['Restaurant Name','City','Cuisines']]
            z11=x1[['Aggregate rating','Rating text','Votes']]
            z2=pd.DataFrame({'Average Cost for two':x1['Average Cost for two'].astype(str)+' '+x1['Currency'],
                             'Price in INR':m_curr})
            #z4=pd.DataFrame(m_curr, columns=[])
            z3=pd.concat([z1,z2,z11], axis=1)
            
        elif nadu_name==208:
            filtered_df_data = df[df['Country Code'] == nadu_name]
            x1=filtered_df_data.sort_values(by='Average Cost for two', ascending=False)
            m_curr=list(round((x1['Average Cost for two']*4.20),2))
            #d=list(x1['Average Cost for two'])
            z1=x1[['Restaurant Name','City','Cuisines']]
            z11=x1[['Aggregate rating','Rating text','Votes']]
            z2=pd.DataFrame({'Average Cost for two':x1['Average Cost for two'].astype(str)+' '+x1['Currency'],
                             'Price in INR':m_curr})
            #z4=pd.DataFrame(m_curr, columns=[])
            z3=pd.concat([z1,z2,z11], axis=1)
            
            return z3.to_dict(orient='records')
        
        elif nadu_name==214:
            filtered_df_data = df[df['Country Code'] == nadu_name]
            x1=filtered_df_data.sort_values(by='Average Cost for two', ascending=False)
            m_curr=list(round((x1['Average Cost for two']*22.35),2))
            #d=list(x1['Average Cost for two'])
            z1=x1[['Restaurant Name','City','Cuisines']]
            z11=x1[['Aggregate rating','Rating text','Votes']]
            z2=pd.DataFrame({'Average Cost for two':x1['Average Cost for two'].astype(str)+' '+x1['Currency'],
                             'Price in INR':m_curr})
            #z4=pd.DataFrame(m_curr, columns=[])
            z3=pd.concat([z1,z2,z11], axis=1)
            
            return z3.to_dict(orient='records')
        else:
            filtered_df_data = df[df['Country Code'] == nadu_name]
            x1=filtered_df_data.sort_values(by='Average Cost for two', ascending=False)
            d=list(x1['Average Cost for two'])
            m_curr=[]
            y1=countries1[nadu_name]
            for i in range(len(d)):
                from_currency = y1
                to_currency = 'INR'
                amount = float(d[i])
                response = requests.get(f"https://api.frankfurter.app/latest?amount={amount}&from={from_currency}&to={to_currency}")
                #print(f"{amount} {from_currency} is {response.json()['rates'][to_currency]} {to_currency}")
                m_curr.append(str(response.json()['rates'][to_currency])+' INR')
        
            z1=x1[['Restaurant Name','City','Cuisines']]
            z11=x1[['Aggregate rating','Rating text','Votes']]
            z2=pd.DataFrame({'Average Cost for two':x1['Average Cost for two'].astype(str)+' '+x1['Currency'],
                            'Price in INR':m_curr})
            #z4=pd.DataFrame(m_curr, columns=[])
            z3=pd.concat([z1,z2,z11], axis=1)
            
            return z3.to_dict(orient='records')

#callback to update the cities of selected country's geo visualization
@app.callback(
    Output("map", "figure"), 
    Input("candidate", "value"))
def display_scatter(candidate):
    #df1 = pd.read_csv('zomato.csv')
    df1=df[df['Country Code'] == candidate]
    k=[(countries[i]["label"]) for i in range(len(countries)) for key,value in countries[i].items() if value==candidate]
    fig1=px.scatter_mapbox(df1,lon=df1['Longitude'],title=f'Restaurants in {str(k[0])}',
                          lat=df1['Latitude'],
                          zoom=3,
                          color=df1['Has Online delivery'],
                          size=df1['Average Cost for two'],
                          hover_data=[df1['Restaurant Name'],df1['City'],df1['Cuisines'],df1['Currency']],
                          width=700,
                          height=700)
    fig1.update_layout(
    title_x=0.5,
    title_y=0.95,
    mapbox={"style": "open-street-map","center": {"lon":list(df1['Longitude'])[0], "lat" :list(df1['Latitude'])[0]} ,"zoom": 4.8},
    margin={"l": 0, "r": 0, "b": 0, "t": 80}
     )
    return fig1  

#callback to update the restaurants of selected country's cities 
@app.callback(
    Output('nagar-cuisine', 'figure'),
    Input('nad', 'value'),
    Input('nag', 'value'))
def update_graph_1(nad,nag):
    filtered_df1 = df[df['Country Code'] == nad]
    city_filtered_df= filtered_df1[filtered_df1["City"]== nag]

    fig2 = px.scatter(city_filtered_df, x="Restaurant Name", 
    y='Average Cost for two',color='Aggregate rating',size='Aggregate rating',
    hover_data=['Address','Locality','Cuisines','Currency','Has Online delivery','Has Table booking','Votes'],
    title=f'Analysis of restaurant ratings in {nag}',height=500)
    
    fig_outline(fig2.update_layout,fig2.update_xaxes,fig2.add_shape)
    return fig2

#callback to update the datatable title  of selected city of a selected country 
@app.callback(
    Output('f1', 'children'),
    [Input('nad', 'value'),
    Input('nag', 'value')])
def display_table1(nad,nag):
    o1=nag
    return html.H3(f'Take a look at the Restaurants ranked from the costliest to cheapest in {o1}')

#callback to update the currency  of selected country's city to INR
@app.callback(
    Output('frame_table1', 'data'),
    Input('nad', 'value'),
    Input('nag', 'value'))
def display_table1(nad,nag):
    
    if nad==1:
        m_curr=[] 
        filtered_df1 = df[df['Country Code'] == nad]
        city_filtered_df= filtered_df1[filtered_df1["City"]== nag]
        for b in range(len(city_filtered_df)):
                    m_curr.append('-')
        xx1=city_filtered_df.sort_values(by='Average Cost for two', ascending=False)
        zz1=xx1[['Restaurant Name','City','Cuisines']]
        zz11=xx1[['Aggregate rating','Rating text','Votes']]
        zz2=pd.DataFrame({'Average Cost for two':xx1['Average Cost for two'].astype(str)+' '+xx1['Currency'],
                        'Price in INR':m_curr})
        zz3=pd.concat([zz1, zz2,zz11], axis=1)
        
        return zz3.to_dict(orient='records')
    
    elif nad==166:
            
            filtered_df1 = df[df['Country Code'] == nad]
            city_filtered_df= filtered_df1[filtered_df1["City"]== nag]
            xx1=city_filtered_df.sort_values(by='Average Cost for two', ascending=False)
            m_curr=list(round((xx1['Average Cost for two']*22.53),2))
            zz1=xx1[['Restaurant Name','City','Cuisines']]
            zz11=xx1[['Aggregate rating','Rating text','Votes']]
            zz2=pd.DataFrame({'Average Cost for two':xx1['Average Cost for two'].astype(str)+' '+xx1['Currency'],
                            'Price in INR':m_curr})
            zz3=pd.concat([zz1, zz2,zz11], axis=1)
            
            return zz3.to_dict(orient='records')
            
    elif nad==191:
            filtered_df1 = df[df['Country Code'] == nad]
            city_filtered_df= filtered_df1[filtered_df1["City"]== nag]
            xx1=city_filtered_df.sort_values(by='Average Cost for two', ascending=False)
            m_curr=list(round((xx1['Average Cost for two']*0.26),2))
            zz1=xx1[['Restaurant Name','City','Cuisines']]
            zz11=xx1[['Aggregate rating','Rating text','Votes']]
            zz2=pd.DataFrame({'Average Cost for two':xx1['Average Cost for two'].astype(str)+' '+xx1['Currency'],
                            'Price in INR':m_curr})
            zz3=pd.concat([zz1, zz2,zz11], axis=1)
            
            return zz3.to_dict(orient='records')
            
    elif nad==208:
            filtered_df1 = df[df['Country Code'] == nad]
            city_filtered_df= filtered_df1[filtered_df1["City"]== nag]
            xx1=city_filtered_df.sort_values(by='Average Cost for two', ascending=False)
            m_curr=list(round((xx1['Average Cost for two']*4.20),2))
            zz1=xx1[['Restaurant Name','City','Cuisines']]
            zz11=xx1[['Aggregate rating','Rating text','Votes']]
            zz2=pd.DataFrame({'Average Cost for two':xx1['Average Cost for two'].astype(str)+' '+xx1['Currency'],
                            'Price in INR':m_curr})
            zz3=pd.concat([zz1, zz2,zz11], axis=1)
            
            return zz3.to_dict(orient='records')
        
    elif nad==214:
            filtered_df1 = df[df['Country Code'] == nad]
            city_filtered_df= filtered_df1[filtered_df1["City"]== nag]
            xx1=city_filtered_df.sort_values(by='Average Cost for two', ascending=False)
            m_curr=list(round((xx1['Average Cost for two']*22.35),2))
            zz1=xx1[['Restaurant Name','City','Cuisines']]
            zz11=xx1[['Aggregate rating','Rating text','Votes']]
            zz2=pd.DataFrame({'Average Cost for two':xx1['Average Cost for two'].astype(str)+' '+xx1['Currency'],
                            'Price in INR':m_curr})
            zz3=pd.concat([zz1, zz2,zz11], axis=1)
            
            return zz3.to_dict(orient='records')
    else:
            filtered_df1 = df[df['Country Code'] == nad]
            city_filtered_df= filtered_df1[filtered_df1["City"]== nag]
            xx1=city_filtered_df.sort_values(by='Average Cost for two', ascending=False)
            d=list(xx1['Average Cost for two'])
            m_curr=[]
            y1=countries1[nad]
            for i in range(len(d)):
                from_currency = y1
                to_currency = 'INR'
                amount = float(d[i])
                response = requests.get(f"https://api.frankfurter.app/latest?amount={amount}&from={from_currency}&to={to_currency}")
                #print(f"{amount} {from_currency} is {response.json()['rates'][to_currency]} {to_currency}")
                m_curr.append(str(response.json()['rates'][to_currency])+' INR')
        
            zz1=xx1[['Restaurant Name','City','Cuisines']]
            zz11=xx1[['Aggregate rating','Rating text','Votes']]
            zz2=pd.DataFrame({'Average Cost for two':xx1['Average Cost for two'].astype(str)+' '+xx1['Currency'],
                            'Price in INR':m_curr})
            #z4=pd.DataFrame(m_curr, columns=[])
            z3=pd.concat([zz1,zz2,zz11], axis=1)
            
            return z3.to_dict(orient='records')

#callback to update the restaurant location  of selected country's geo visualization
@app.callback(
    Output("map1", "figure"), 
    Input('nad', 'value'),
    Input('nag', 'value'))
def display_scatter1(nad,nag):
    #df1 = pd.read_csv('zomato.csv')
    filtered_df1 = df[df['Country Code'] == nad]
    city_filtered_df= filtered_df1[filtered_df1["City"]== nag]
    fig3=px.scatter_mapbox(city_filtered_df,lon=city_filtered_df['Longitude'],
                          lat=city_filtered_df['Latitude'],
                          zoom=3,
                          color=city_filtered_df['Has Table booking'],
                          size=city_filtered_df['Average Cost for two'],
                          hover_data=[city_filtered_df['Restaurant Name'],city_filtered_df['City'],
                                      city_filtered_df['Cuisines'],city_filtered_df['Currency']],
                          title=f'Restaurants in {nag}',width=700,
                          height=700)
    fig3.update_layout(
    title_x=0.5,
    title_y=0.95,
    mapbox={"style": "open-street-map","center": {"lon":list(city_filtered_df['Longitude'])[0], "lat" :list(city_filtered_df['Latitude'])[0]}, "zoom": 4.8},
    margin={"l": 0, "r": 0, "b": 0, "t": 80}
     )
    return fig3 
if __name__ == '__main__':
    app.run_server(mode="external")