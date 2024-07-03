import dash
import plotly.graph_objects as go
from dash import dcc, html, callback, callback_context
from dash.dependencies import Output, Input, State, MATCH, ALL
import plotly.express as px 
import dash_bootstrap_components as dbc
import pandas as pd
import geopandas as gpd
import requests
from dash_bootstrap_templates import load_figure_template
import plotly.io as pio
import numpy as np
from sklearn.cluster import KMeans
from shapely import wkt


load_figure_template(["pulse", "pulse_dark"])
layout = go.Layout(template= pio.templates["pulse"])

dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"
font_family = 'Times New Roman, Times, serif'

# Work Files 
json_file_url = 'https://raw.githubusercontent.com/Salvatore-Rocha/GIS_Dataviewer/4e8c24d98c3b6b9ac5ee4cd08de263316b35a7da/Files/cdmx-alcaldias-4326.json'
response = requests.get(json_file_url)
json_data_alc = response.json()

json_file_url = 'https://raw.githubusercontent.com/Salvatore-Rocha/GIS_Dataviewer/4e8c24d98c3b6b9ac5ee4cd08de263316b35a7da/Files/georef_mex_col_tr.json'
response = requests.get(json_file_url)
json_data_col = response.json()

# CSV File in Githubt (added ?raw=true at the end of the URL or it will not parse it correctly) 
listings = pd.read_csv("https://github.com/Salvatore-Rocha/GIS_Dataviewer/blob/4c775b644374f6c5b217d7138729e154eba22261/Files/listings_n_col_alc.csv?raw=true")
listings['geometry'] = listings['geometry'].apply(wkt.loads)
listings = gpd.GeoDataFrame(listings, geometry='geometry')
listings.set_crs(epsg=4326, inplace=True)

header = html.H1(
    "Discover Mexico City's Airbnb Scene", 
    className="p-2 mb-2 text-center",
    style={'fontFamily': font_family, 'textTransform': 'uppercase'},
                )

sources = html.Div(
    [
        html.P("By Eduardo Salvador Rocha", style={'fontFamily': font_family}),
        html.Label(
            [
                "Links: ",
                html.A(
                    "Eduardo's GitHub|  ",
                    href="https://github.com/Salvatore-Rocha/GIS_Dataviewer",
                    target="_blank",
                ),
                html.A(
                    "Code (.py file) |   ",
                    href="https://github.com/Salvatore-Rocha/GIS_Dataviewer/blob/4c775b644374f6c5b217d7138729e154eba22261/src/app.py",
                    target="_blank",
                
                ),
                html.A(
                    "Code (Jupyter Notebook (Google Colab) |   ",
                    href="https://colab.research.google.com/drive/1Xnx0tj9BDDt_NgxE2d2gdFr93wkmJ-bh?usp=sharing",
                    target="_blank",
                
                ),
            ], style={'fontFamily': font_family,}
        ),
    ]
)

def alcaldias_fig():
    fig = go.Figure()

    # Define the transparency value
    transparency = 0.5

    # Interpolated palette with transparency
    palette = [
        f'rgba(255, 0, 0, {transparency})',       # Red
        f'rgba(255, 77, 0, {transparency})',      # Orange
        f'rgba(255, 153, 0, {transparency})',     # Orange
        f'rgba(255, 230, 0, {transparency})',     # Yellow
        f'rgba(171, 230, 0, {transparency})',     # Yellow
        f'rgba(85, 230, 0, {transparency})',      # Yellow
        f'rgba(0, 230, 0, {transparency})',       # Green
        f'rgba(0, 204, 42, {transparency})',      # Green
        f'rgba(0, 153, 128, {transparency})',     # Cyan
        f'rgba(0, 102, 213, {transparency})',     # Cyan
        f'rgba(0, 77, 255, {transparency})',      # Blue
        f'rgba(85, 26, 255, {transparency})',     # Blue
        f'rgba(170, 0, 213, {transparency})',     # Purple
        f'rgba(213, 0, 170, {transparency})',     # Purple
        f'rgba(255, 0, 85, {transparency})',      # Pink
        f'rgba(255, 0, 0, {transparency})'        # Red
    ]

    # Adding polygons to the plot
    for i, feature in enumerate(json_data_alc['features']):
        lon, lat = zip(*feature['geometry']['coordinates'][0])
        fig.add_trace(go.Scattermapbox(
            mode="lines", 
            lon=lon + (lon[0],),
            lat=lat + (lat[0],),
            hoverinfo="text",
            text=feature['properties']['NOMBRE'],
            name=feature['properties']['NOMBRE'],  
            fill='toself', 
            line=dict(width=1, color=palette[i % len(palette)]), 
            fillcolor=palette[i % len(palette)] 
        ))

    fig.update_layout(
        width=1000, 
        height=800, 
        title=("Alcaldias CDMX"),
        mapbox_style="carto-positron",
        mapbox_zoom=9.8,
        mapbox_center={"lat": 19.3215, "lon": -99.18235},
        margin={"r":0,"t":0,"l":0,"b":0}
    )

    return fig

def colonias_fig():
    # Convert JSON to GeoDataFrame
    geojson_data_colonias = gpd.GeoDataFrame.from_features(json_data_col['features'])
    fig = px.choropleth_mapbox(geojson_data_colonias, 
                                        geojson=geojson_data_colonias.geometry, 
                                        locations=geojson_data_colonias.index, 
                                        mapbox_style="carto-positron",
                                        zoom=5,
                                        opacity=0.25,
                                        color_discrete_sequence=["green"],
                                        custom_data=['col_name', 'mun_name'],
                                        )
    
    fig.update_traces(
        hovertemplate="<b>Colonia</b>: %{customdata[0]}<br><b>Delegacion</b>: %{customdata[1]}"
    )

    fig.update_layout(
        width=1000, 
        height=800, 
        mapbox_zoom=10,
        mapbox_center={"lat": 19.3415, "lon": -99.18235},
        margin={"r":0,"t":0,"l":0,"b":0})
    return fig

text_alcaldias = "In Mexico City, alcaldías are administrative divisions similar to boroughs or districts. They serve as local government \
    units responsible for managing various aspects of urban life within their boundaries, including public services, infrastructure, and \
    community development. Each alcaldía is headed by a mayor (alcaldesa or alcalde) who is elected by the residents of the area. These \
    officials work to address the unique needs and challenges of their communities while collaborating with city-wide authorities to ensure \
    coordinated governance across Mexico's vibrant capital."

tit_alc = "Alcaldías in Focus"

text_colonia = "Mexico City's alcaldías encompass numerous neighborhoods, known as colonias, each with its own distinct character and \
    history. With a total of 16 alcaldías and over 300 colonias, the city is a tapestry of diverse cultures and lifestyles. From the \
    historic charm of Coyoacán to the bustling energy of Condesa, every colonia offers a unique experience for residents and visitors \
    alike. In Mexico City, the distinction of being the first registered colonia goes to Santa María la Ribera, established in the late\
    19th century during the Porfirio Díaz era. It's known for its picturesque kiosk in the middle of a pond. On the other hand, the latest \
    registered colonia is Ciudad Olímpica, situated in the Venustiano Carranza alcaldía. It was developed as part of the city's \
    infrastructure for the 1968 Olympics, with residential areas constructed to accommodate athletes and officials."

tit_col = "City's Vibrant Colonias"

def airbnb_by(type):
    if type == "number_of_reviews":
        fig = px.scatter_mapbox(listings, 
                            lat="latitude", 
                            lon="longitude", 
                            color=type, 
                            size=type,
                            color_continuous_scale='Jet',
                            range_color=[0, 200], 
                            zoom=10, 
                            size_max=30,
                            mapbox_style= "carto-darkmatter") 
        
    else:
        df = listings[listings['price'].notna()].copy()
        df["price_log"] = np.log(df["price"])
        
        fig = px.scatter_mapbox(df, 
                    lat="latitude", 
                    lon="longitude", 
                    color=type, 
                    size="price_log",
                    color_continuous_scale='Jet',
                    range_color=[0, 2000], 
                    zoom=10, 
                    size_max=10,
                    mapbox_style= "carto-positron") 
        
    fig.update_layout(
        width=1000, 
        height=800, 
        mapbox_zoom=10,
        mapbox_center={"lat": 19.3715, "lon": -99.18235},
        margin={"r":0,"t":0,"l":0,"b":0}
        )
    return fig

def airbnb_density():
    
    fig = px.density_mapbox(listings, 
                            lat="latitude", 
                            lon="longitude", 
                            radius=10,  
                            color_continuous_scale='Jet',
                            zoom=10, 
                            mapbox_style="open-street-map")


    fig.update_layout(
        width=1000, 
        height=800, 
        mapbox_zoom=10,
        mapbox_center={"lat": 19.3715, "lon": -99.18235},
        margin={"r":0,"t":0,"l":0,"b":0}
        )

    return fig

def choropleth_col(type):
    if type == "Price":
        col_by_prices = listings.groupby(['col_code', 'col_name',"mun_name"])["price"].mean().round(2).reset_index()
        
        fig = px.choropleth_mapbox(
            col_by_prices, 
            geojson=json_data_col, 
            locations='col_code', 
            featureidkey="properties.col_code", 
            color='price',
            color_continuous_scale="Jet",
            range_color=[0,2000],
            opacity=0.8,
            mapbox_style="carto-darkmatter",
            custom_data=['col_name', 'mun_name',"price"]
        )
        
        fig.update_traces(
            hovertemplate="<b>Colonia</b>: %{customdata[0]}<br><b>Delegacion</b>: %{customdata[1]}<br><b>Precio Prom</b>: %{customdata[2]}")
        
    else:
        col_by_reviews = listings.groupby(['col_code', 'col_name',"mun_name"])["number_of_reviews"].mean().round(2).reset_index()
        
        fig = px.choropleth_mapbox(
            col_by_reviews, 
            geojson=json_data_col, 
            locations='col_code', 
            featureidkey="properties.col_code", 
            color='number_of_reviews',
            color_continuous_scale="Jet",
            hover_data={'col_name': True, 'mun_name': True},
            range_color=[0,80],
            opacity=0.8,
            custom_data=['col_name', 'mun_name',"number_of_reviews"],
            mapbox_style="carto-darkmatter",
        )
        
        fig.update_traces(
            hovertemplate="<b>Colonia</b>: %{customdata[0]}<br><b>Delegacion</b>: %{customdata[1]}<br><b>Num de Reseñas Prom</b>: %{customdata[2]}")

    fig.update_layout(
        width=1000, 
        height=800, 
        mapbox_zoom=10,
        mapbox_center={"lat": 19.3415, "lon": -99.18235},
        margin={"r":0,"t":0,"l":0,"b":0})

    return fig

def choropleth_del(type):
    if type == "Price":
        alc_by_prices =  listings.groupby('mun_name')['price'].mean().round(2).reset_index()
        fig = px.choropleth_mapbox(
            alc_by_prices, 
            geojson=json_data_alc, 
            locations='mun_name', 
            featureidkey="properties.NOMBRE", 
            color='price',
            color_continuous_scale="Jet",
            mapbox_style="carto-darkmatter",
            custom_data=['mun_name',"price"],
            opacity=0.8,
                )
        
        fig.update_traces(
            hovertemplate="<b>Delegacion</b>: %{customdata[0]}<br><b>Precio Prom</b>: %{customdata[1]}")
    else:
        alc_by_review =  listings.groupby('mun_name')['number_of_reviews'].mean().round(2).reset_index()
        fig = px.choropleth_mapbox(
            alc_by_review, 
            geojson=json_data_alc, 
            locations='mun_name', 
            featureidkey="properties.NOMBRE", 
            color='number_of_reviews',
            color_continuous_scale="Jet",
            mapbox_style="carto-darkmatter",
            custom_data=['mun_name',"number_of_reviews"],
            opacity=0.8,
                )
        
        fig.update_traces(
            hovertemplate="<b>Delegacion</b>: %{customdata[0]}<br><b>Num de Reseñas Prom</b>: %{customdata[1]}")
        
    fig.update_layout(
            width=1000, 
            height=800, 
            mapbox_zoom=9.8,
            mapbox_center={"lat": 19.3215, "lon": -99.18235},
            margin={"r":0,"t":0,"l":0,"b":0})
    return fig

def cluster_map(clusters):
    # Spatial Clustering using KMeans
    X = listings[['longitude', 'latitude']]  
    kmeans = KMeans(n_clusters=clusters)
    listings['cluster'] = kmeans.fit_predict(X)

    # Computing convex hulls of each cluster 
    # This ONLY WORKS on GEODATAFRAMES not normal Pandas dataframes; make sure to use geoframes or otherwise it will fail!!
    convex_hulls = listings.groupby('cluster')['geometry'].apply(lambda x: x.unary_union.convex_hull)
    color_scale = px.colors.cyclical.Phase

    # Cluster map
    fig = px.scatter_mapbox(listings, 
                            lat="latitude", 
                            lon="longitude", 
                            color="cluster",
                            color_continuous_scale=color_scale, 
                            size_max=15,
                            zoom=10, 
                            mapbox_style="carto-positron")


    # Add convex hulls to the plot
    for cluster, hull in zip(convex_hulls.index, convex_hulls):
        lon, lat = hull.exterior.xy
        lon = list(lon)
        lat = list(lat)
        fig.add_trace(go.Scattermapbox(
            lon=lon,
            lat=lat,
            mode='lines',
            marker=dict(size=0),
            hoverinfo='none',
            fill='toself',
            showlegend=False 
        ))

    fig.update_layout(
        width=1000, 
        height=800, 
        mapbox_zoom=10.1,
        mapbox_center={"lat": 19.3415, "lon": -99.18235},
        margin={"r":0,"t":0,"l":0,"b":0},
        coloraxis_showscale=False)

    return fig

tab1 = dbc.Tab([ 
                dbc.Row([
                    dbc.Col([
                        html.H4(children = tit_alc,
                                id="titl-tab1",
                                style={"display": "flex",
                                    "justify-content": "center",
                                    "align-items": "center",
                                    "height": "100px",
                                    'fontFamily': font_family,
                                    }
                                ),
                        dcc.RadioItems(id="radio_it_tab1",
                                                options= ["Borough / Alcaldía", "Neighborhood / Colonia"], 
                                                value='Borough / Alcaldía', 
                                                inline=False,
                                                #inputStyle={"margin-left":"6px", "margin-right": "2px"},
                                                style={'fontFamily': font_family}
                                                ),
                        html.Br(),
                        dbc.Button(children = "See Map", 
                                id="button-tab1", 
                                n_clicks=0,
                                style={'fontFamily': font_family,}
                                ),
                        html.Br(),
                        html.Br(),
                        html.P(children=text_alcaldias, 
                               id="text-tab1",
                               ),
                            ],width= 3,
                            style={'textAlign': 'left', "font-size": '14px','fontFamily': font_family}
                            ),
                    dbc.Col([
                            html.Br(),
                            dcc.Loading(id="loading-tab1",
                                            type="default",
                                            children= dcc.Graph(
                                                                id = "graph-tab1",
                                                                figure = alcaldias_fig()                            
                                                                ),
                                        )
                            ],width= 9)
                        ])
                ], label="Overview",)

tab3 = dbc.Tab([ 
                dbc.Row([
                    dbc.Col([
                        html.H4(children = "The power of individual data visualization",
                                id="titl-tab2",
                                style={"display": "flex",
                                    "justify-content": "center",
                                    "align-items": "center",
                                    "height": "100px",
                                    'fontFamily': font_family,}
                                ),
                        html.Br(),
                        dcc.RadioItems(id="radio_it_tab2",
                                    options= ["Airbnbs by Price", 
                                            "Airbnbs by # of Reviews",
                                            "Airbnb by Density Area"], 
                                    value="Airbnb by Density Area", 
                                    inline=False,
                                    inputStyle={"margin-left":"6px", "margin-right": "2px"},
                                    style={'fontFamily': font_family,}
                                    ),
                        html.Br(),
                        dbc.Button(children = "Show Areas", 
                                        id="button-tab2", 
                                        n_clicks=None,
                                        style={'fontFamily': font_family,}
                                        ),
                        html.Br(),
                        html.Br(),
                        html.P("Visualizing individual data points rather than jurisdictions provides a more detailed and granular view of the data. This approach helps identify specific trends, hotspots, and outliers that might be obscured when data is aggregated by larger administrative areas. For Airbnb listings, it allows users to pinpoint exact locations, understand neighborhood dynamics, and make more informed decisions based on precise information rather than generalizations.", 
                               style={'font-size': '14px'})
                            ],width=3),
                    dbc.Col([
                        html.Br(),
                        dcc.Loading(id="loading-tab2",
                                        type="default",
                                        children= dcc.Graph(
                                                            id = "graph-tab2",
                                                            figure = {}                            
                                                            ),
                                    )
                            ],style={"display": "flex",
                                "justifyContent": "center",  
                                "alignItems": "center",      
                                'fontFamily': font_family,},
                            width=9)
                        ],style={'textAlign': 'left','fontFamily': font_family,},
                        justify="center")
                ],label="By Data Points")

tab4 = dbc.Tab([
            dbc.Row([
                dbc.Col([
                    html.Br(),
                    dcc.Loading(id="loading-tab3",
                                    type="default",
                                    children= dcc.Graph(
                                                        id = "graph-tab3",
                                                        figure = {}                            
                                                        ),
                                )
                        ],style={"display": "flex",
                            "justifyContent": "center",  
                            "alignItems": "center",        
                            'fontFamily': font_family,}
                        ,width=9),
                dbc.Col([
                    html.H4(children = "Trends by boroughs and neighborhoods",
                                id="titl-tab3",
                                style={"display": "flex",
                                    "justify-content": "center",
                                    "align-items": "center",
                                    "height": "100px",
                                    'fontFamily': font_family,}
                                ),
                        html.Br(),
                        dbc.Row([ #Radio Items
                            dbc.Col([
                                dcc.RadioItems(id="radio1_it_tab3",
                                    options= ["Borough / Alcaldia",
                                              "Neighbourhood/ Colonia"], 
                                    value="Neighbourhood/ Colonia", 
                                    inline=False,
                                    inputStyle={"margin-left":"6px", "margin-right": "2px"},
                                    style={'fontSize': '12px','fontFamily': font_family,}
                                    ),
                                ],width=6),
                            dbc.Col([
                                dcc.RadioItems(id="radio2_it_tab3",
                                    options= ["Price",
                                              "Reviews Number"], 
                                    value="Price", 
                                    inline=False,
                                    inputStyle={"margin-left":"6px", "margin-right": "2px"},
                                    style={'fontSize': '12px','fontFamily': font_family,}
                                    ),
                                ],width=6),
                            ]),
                        html.Br(),
                        dbc.Button(children = "Update graph", 
                                        id="button-tab3", 
                                        n_clicks=None,
                                        style={'fontFamily': font_family,}
                                        ),
                        html.Br(),
                        html.Br(),
                        html.P("Visualizing data by jurisdictions is useful because it provides a clear and organized overview of trends and patterns within defined administrative areas. This approach helps identify regional differences, allocate resources efficiently, and develop targeted policies. For Airbnb listings, visualizing by jurisdictions allows users to understand broader market dynamics, compare different areas easily, and make decisions based on regional insights rather than isolated data points.", 
                               style={'font-size': '14px', 'fontFamily': font_family,})
                        ],width=3),
                    ]) 
            ],label="By Jurisdictions")

tab2 = dbc.Tab([
            dbc.Row([
                dbc.Col([
                    html.H4(children = "Segmentation of Mexico City's Airbnbs Using Data Clustering",
                                id="titl-tab4",
                                style={"display": "flex",
                                    "justify-content": "center",
                                    "align-items": "center",
                                    "height": "100px",
                                    'fontFamily': font_family,}
                                ),
                    html.Br(),    
                    html.P("Number of Clusters:",style={'font-size': '12px','fontFamily': font_family,}),
                    dcc.Slider(id="slider-tab4",
                                   min=5, 
                                   max=20,
                                   step= 1,
                                   value=12,
                                   included=False
                                ),
                    html.Br(),
                    dbc.Button(children = "Show Clusters", 
                                        id="button-tab4", 
                                        n_clicks=None,
                                        style={'fontFamily': font_family,}
                                        ),
                    html.Br(),
                    html.Br(),
                    html.P("Clustering is a data analysis technique that groups similar data points together based on certain characteristics. In the context of Airbnb listings, clustering can be useful for identifying patterns and trends, such as popular neighborhoods, price ranges, and types of accommodations. By grouping similar listings, hosts and guests can gain insights into market dynamics, optimize pricing strategies, and enhance the overall user experience by highlighting the most relevant options based on specific preferences.", 
                           style={'font-size': '14px',
                                  'fontFamily': font_family,
                                  }),
                    ],width=3),
                dbc.Col([
                    html.Br(),
                    dcc.Loading(id="loading-tab4",
                                    type="default",
                                    children= dcc.Graph(
                                                        id = "graph-tab4",
                                                        figure = {}                            
                                                        ),
                                )
                        ],style={"display": "flex",
                            "justifyContent": "center",
                            "alignItems": "center",
                            'fontFamily': font_family,}
                        ,width=9),
                    ],style={'textAlign': 'center','fontFamily': font_family,},
                        justify="center") 
            ],label="Clustering")

tabs = dbc.Card(dbc.Tabs([tab1,
                          tab2,
                          tab3,
                          tab4], 
                         style={'font-style': 'italic',
                                'fontFamily': font_family, 
                                "font-size":"13px"}))

main_text = ["This project visualizes the Airbnb scene in ", html.B("Mexico City"), " using Plotly and Dash, providing insights into administrative divisions and individual hosts. It analyzes Airbnb listings based on price and number of reviews. Many choose to visit Mexico City (CDMX) for its vibrant neighborhoods and unique experiences. Staying in Roma and Condesa offers trendy cafes and nightlife, Polanco provides luxury shopping and dining, Coyoacán boasts a bohemian vibe and historic sites, Centro Histórico features iconic landmarks, and La Roma Norte combines tranquility with lively nightlife. These options make a stay in CDMX truly memorable."]

app =  dash.Dash(__name__, 
                 external_stylesheets= [dbc.themes.PULSE, dbc.icons.FONT_AWESOME, dbc_css],)
server = app.server
app.layout = dbc.Container(style={'padding': '50px'},
    children=[
            header,
            html.P(main_text,
                   style={'fontFamily': font_family,
                          'textAlign': 'justify',
                          'paddingLeft': '10rem',
                          'paddingRight': '10rem'}),
            html.Br(),
            dbc.Row([ # 4 tabs
                    tabs
                    ]),
            dbc.Row([ #Links/ Sources
                    sources
                    ]),  
],fluid=True,
  className="dbc dbc-ag-grid")

# Updating Tab1
@callback(
    Output("graph-tab1", "figure"),
    Output("text-tab1","children"),
    Output("titl-tab1","children"),
    [Input("button-tab1", "n_clicks")],
    [State("radio_it_tab1", "value")]  
)  
def city_view(n_clicks, type):
    
    ctx = callback_context
    if not ctx.triggered:
        # No input triggered the callback, return default figure or raise Exception
        return dash.no_update
    else:
        triggered_id = ctx.triggered[0]["prop_id"].split(".")[0]
    
    if triggered_id == "button-tab1":
        # Button clicked, update the graph
    
        if type == "Neighborhood / Colonia":

            fig =  colonias_fig()
            text = text_colonia
            titl = tit_col            

        else:
            fig = alcaldias_fig()
            text = text_alcaldias
            titl = tit_alc
    else:
        # Radio item interaction, do not update the graph
        return dash.no_update

    return fig, text, titl


#Updating Tab2
@callback(
    Output("graph-tab2", "figure"),
    [Input("button-tab2", "n_clicks")],
    [State("radio_it_tab2", "value")]  
)  
def airbnb_geo(n_clicks, type):
    
    if n_clicks == None:
        return airbnb_density()
    
    ctx = callback_context
    if not ctx.triggered:
        # No input triggered the callback, return default figure or raise Exception
        return dash.no_update
    else:
        triggered_id = ctx.triggered[0]["prop_id"].split(".")[0]
    
    if triggered_id == "button-tab2":
        
        if type == "Airbnbs by Price":

            fig =  airbnb_by("price")          

        elif type == "Airbnbs by # of Reviews":
            
            fig =  airbnb_by("number_of_reviews")  
            
        else:
            fig = airbnb_density()
    else:
        # Radio item interaction, do not update the graph
        return dash.no_update

    return fig

#Updating Tab3
@callback(
    Output("graph-tab3", "figure"),
    Input("button-tab3", "n_clicks"),
    Input("radio1_it_tab3", "value"),
    Input("radio2_it_tab3", "value"),  
)  
def choro_plots(n_clicks, del_col, price_review):
    
    if n_clicks == None:
        #Colonia, Price
        return choropleth_col("Price")
    
    ctx = callback_context
    if not ctx.triggered:
        # No input triggered the callback, return default figure or raise Exception
        return dash.no_update
    else:
        triggered_id = ctx.triggered[0]["prop_id"].split(".")[0]
    
    if triggered_id == "button-tab3":
        
        if del_col == "Neighbourhood/ Colonia":

            return choropleth_col(price_review)            
            
        else:
            
            return choropleth_del(price_review)
    else:
        # Radio item interaction, do not update the graph
        return dash.no_update

#Updating Tab4
@callback(
    Output("graph-tab4", "figure"),
    Input("button-tab4", "n_clicks"),
    Input("slider-tab4", "value"),
)  
def clustering_map(n_clicks, clustersss):
    
    if n_clicks == None:
        #Colonia, Price
        return cluster_map(6)
    
    ctx = callback_context
    if not ctx.triggered:
        # No input triggered the callback, return default figure or raise Exception
        return dash.no_update
    else:
        triggered_id = ctx.triggered[0]["prop_id"].split(".")[0]
    
    if triggered_id == "button-tab4":
        
        return cluster_map(clustersss)
    
    else:
        # Radio item interaction, do not update the graph
        return dash.no_update
    
if __name__=='__main__':
    #app.run_server(debug=True, port=8050)
    app.run_server()