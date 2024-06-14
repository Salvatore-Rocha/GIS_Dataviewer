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

# Create a Plotly layout with the desired dbc template
load_figure_template(["pulse", "pulse_dark"])
layout = go.Layout(template= pio.templates["pulse"])

dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"

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
    className="bg-primary text-white p-2 mb-2 text-center"
                )

sources = html.Div(
    [
        html.P("By Eduardo Salvador Rocha"),
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
            ]
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

    # Add polygons to the plot
    for i, feature in enumerate(json_data_alc['features']):
        lon, lat = zip(*feature['geometry']['coordinates'][0])
        fig.add_trace(go.Scattermapbox(
            mode="lines",  # Added 'markers' mode to ensure filled polygons
            lon=lon + (lon[0],),
            lat=lat + (lat[0],),
            hoverinfo="text",
            text=feature['properties']['NOMBRE'],
            name=feature['properties']['NOMBRE'],  # Set the trace name
            fill='toself',  # Fill the trace with color
            line=dict(width=1, color=palette[i % len(palette)]),  # Set the line color to the palette color
            fillcolor=palette[i % len(palette)]  # Set the fill color to the palette color
        ))

    # Set up the layout
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
                                        opacity=0.5
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
        

    # Update layout to set custom window size and title
    fig.update_layout(
        width=1000, 
        height=800, 
        mapbox_zoom=10,
        mapbox_center={"lat": 19.3715, "lon": -99.18235},
        margin={"r":0,"t":0,"l":0,"b":0}
        )
    return fig

def airbnb_density():
    # Create a density map on a map using Plotly Express
    fig = px.density_mapbox(listings, 
                            lat="latitude", 
                            lon="longitude", 
                            radius=10,  # Adjust the radius as needed
                            color_continuous_scale='Jet',
                            zoom=10, 
                            mapbox_style="open-street-map")  # Change map style here


    # Update layout to set custom window size and title
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
            hover_data={'col_name': True, 'mun_name': True},
            range_color=[0,2000],
            opacity=0.8,
            mapbox_style="carto-darkmatter",
        )
    
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
            mapbox_style="carto-darkmatter",
        )

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
            opacity=0.8,
                )
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
            opacity=0.8,
                )
        
    fig.update_layout(
            width=1000, 
            height=800, 
            #title=("Alcaldias CDMX by Price"),
            #mapbox_style="carto-positron",
            mapbox_zoom=9.8,
            mapbox_center={"lat": 19.3215, "lon": -99.18235},
            margin={"r":0,"t":0,"l":0,"b":0})
    return fig

def cluster_map(clusters):
    # Spatial Clustering (Example using KMeans)
    X = listings[['longitude', 'latitude']]  # Assuming you have columns for longitude and latitude
    kmeans = KMeans(n_clusters=clusters)
    listings['cluster'] = kmeans.fit_predict(X)

    # Computing convex hulls of each cluster (this ONLY WORKS on GEODATAFRAMES, otherwise it will fail!!)
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
            showlegend=False  # Hide legend for this trace
        ))

    fig.update_layout(
        width=1000, 
        height=800, 
        #title=("Colonies in CDMX by Price"),
        mapbox_zoom=10.1,
        mapbox_center={"lat": 19.3415, "lon": -99.18235},
        margin={"r":0,"t":0,"l":0,"b":0})

    return fig

tab1 = dbc.Tab([ 
                dbc.Row([
                    dbc.Col([
                        html.H4(children = tit_alc,
                                id="titl-tab1",
                                style={"display": "flex",
                                    "justify-content": "center",
                                    "align-items": "center",
                                    "height": "100px",}
                                ),
                        dcc.RadioItems(id="radio_it_tab1",
                                                options= ["Borough / Alcaldía", "Neighborhood / Colonia"], 
                                                value='Borough / Alcaldía', 
                                                inline=False,
                                                #className="text-success",
                                                inputStyle={"margin-left":"6px", "margin-right": "2px"},
                                                #style={'fontSize': '12px'}
                                                ),
                        html.Br(),
                        dbc.Button(children = "Update graph", 
                                id="button-tab1", 
                                n_clicks=0,
                                #style={'width': '20%'}
                                ),
                        html.Br(),
                        html.Br(),
                        html.P(children=text_alcaldias, id="text-tab1"),
                            ],width= 3,
                            style={'textAlign': 'center'}
                            ),
                    dbc.Col([
                            html.Br(),
                            dcc.Loading(id="loading-tab1",
                                            type="default",
                                            children= dcc.Graph(
                                                                id = "graph-tab1",
                                                                #The default figure is gonna be the "Alcaldias" one
                                                                figure = alcaldias_fig()                            
                                                                ),
                                        )
                            ],width= 9)
                        ])
                ], label="Title Tab 1",)

tab2 = dbc.Tab([ 
                dbc.Row([
                    dbc.Col([
                        html.H4(children = "This is a long title to be updated somehow",
                                id="titl-tab2",
                                style={"display": "flex",
                                    "justify-content": "center",
                                    "align-items": "center",
                                    "height": "100px"}
                                ),
                        html.Br(),
                        dcc.RadioItems(id="radio_it_tab2",
                                    options= ["Airbnbs by Price", 
                                            "Airbnbs by # of Reviews",
                                            "Airbnb by Density Area"], 
                                    value="Airbnb by Density Area", 
                                    inline=False,
                                    #className="text-success",
                                    inputStyle={"margin-left":"6px", "margin-right": "2px"},
                                    #style={'fontSize': '12px'}
                                    ),
                        html.Br(),
                        dbc.Button(children = "Update graph", 
                                        id="button-tab2", 
                                        n_clicks=None,
                                        #style={'width': '15%'}
                                        ),
                            ],width=3),
                    dbc.Col([
                        html.Br(),
                        dcc.Loading(id="loading-tab2",
                                        type="default",
                                        children= dcc.Graph(
                                                            id = "graph-tab2",
                                                            #The default figure is gonna be the "by Price" one
                                                            figure = {}                            
                                                            ),
                                    )
                            ],style={"display": "flex",
                                "justifyContent": "center",  # centers horizontally
                                "alignItems": "center"        # centers vertically
                                },
                            width=9)
                        ],style={'textAlign': 'center'},
                        justify="center")
                ],label="Title Tab 2")

tab3 = dbc.Tab([
            dbc.Row([
                dbc.Col([
                    html.Br(),
                    dcc.Loading(id="loading-tab3",
                                    type="default",
                                    children= dcc.Graph(
                                                        id = "graph-tab3",
                                                        #The default figure is gonna be the "by Price" one
                                                        figure = {}                            
                                                        ),
                                )
                        ],style={"display": "flex",
                            "justifyContent": "center",  # centers horizontally
                            "alignItems": "center"        # centers vertically
                            }
                        ,width=9),
                dbc.Col([
                    html.H4(children = "This is a long title to be updated somehow tab3",
                                id="titl-tab3",
                                style={"display": "flex",
                                    "justify-content": "center",
                                    "align-items": "center",
                                    "height": "100px"}
                                ),
                        html.Br(),
                        dbc.Row([ #Radio Items
                            dbc.Col([
                                dcc.RadioItems(id="radio1_it_tab3",
                                    options= ["Borough / Alcaldia",
                                              "Neighbourhood/ Colonia"], 
                                    value="Neighbourhood/ Colonia", 
                                    inline=False,
                                    #className="text-success",
                                    inputStyle={"margin-left":"6px", "margin-right": "2px"},
                                    style={'fontSize': '12px'}
                                    ),
                                ],width=6),
                            dbc.Col([
                                dcc.RadioItems(id="radio2_it_tab3",
                                    options= ["Price",
                                              "Reviews Number"], 
                                    value="Price", 
                                    inline=False,
                                    #className="text-success",
                                    inputStyle={"margin-left":"6px", "margin-right": "2px"},
                                    style={'fontSize': '12px'}
                                    ),
                                ],width=6),
                            ]),
                        html.Br(),
                        dbc.Button(children = "Update graph", 
                                        id="button-tab3", 
                                        n_clicks=None,
                                        #style={'width': '15%'}
                                        ),
                        ],width=3),
                    ]) 
            ],label="Title Tab 3")

tab4 = dbc.Tab([
            dbc.Row([
                dbc.Col([
                    html.H4(children = "This is a long title to be updated somehow tab4",
                                id="titl-tab4",
                                style={"display": "flex",
                                    "justify-content": "center",
                                    "align-items": "center",
                                    "height": "100px"}
                                ),
                        html.Br(),
                        html.P("Number of Clusters:",style={'font-size': '12px'}),
                        dcc.Slider(id="slider-tab4",
                                   min=5, 
                                   max=20,
                                   step= 1,
                                   value=12,
                                   included=False
                                ),
                        html.Br(),
                        dbc.Button(children = "Update graph", 
                                        id="button-tab4", 
                                        n_clicks=None,
                                        #style={'width': '15%'}
                                        ),
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
                            "justifyContent": "center",  # centers horizontally
                            "alignItems": "center"        # centers vertically
                            }
                        ,width=9),
                    ],style={'textAlign': 'center'},
                        justify="center") 
            ],label="Title Tab 4")

tabs = dbc.Card(dbc.Tabs([tab1,tab2,tab3,tab4], style={'font-style': 'italic'}))


app =  dash.Dash(__name__, 
                 external_stylesheets= [dbc.themes.PULSE, dbc.icons.FONT_AWESOME, dbc_css],)
#server = app.server
app.layout = dbc.Container(style={'padding': '50px'},
    children=[
            header,
            html.P(["This is a paragraph with a ",  html.U(html.I(html.B("bold, italic, and underlined")))," word in it. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nam lobortis, lectus et interdum blandit, nulla dui ornare augue, at pellentesque nunc est vel ante. Quisque ullamcorper in justo congue feugiat. Integer sit amet justo aliquet, ornare odio in, luctus eros. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Ut vulputate congue turpis, sit amet blandit sapien. Nulla accumsan eu erat non volutpat. Donec convallis blandit nisi eget consectetur. Donec sodales lobortis dictum. Fusce vehicula risus non dui lacinia, interdum feugiat urna eleifend. Donec maximus in nibh a lacinia. Cras et turpis semper, pellentesque ipsum nec, euismod ex. Integer varius viverra ullamcorper. Etiam id hendrerit nunc."]),
            dbc.Row([ # 3 tabs
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
        return cluster_map(12)
    
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
    app.run_server(debug=True, port=8050)
    #app.run_server()