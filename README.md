# Discover Mexico City's Airbnb Scene
### 🌎 Project Overview
This project is designed to visualize the Airbnb scene in Mexico City and is made using the Python libraries of Plotly and Dash. This web-app aims to allow users to delve into various aspects of Mexico City's Airbnb market data set using an interactive and user-friendly interface, examining different administrative divisions (alcaldías) and neighborhoods (colonias).

### 🔎 Visual aspects of the project:

![GIS Viewer Tab1](https://github.com/Salvatore-Rocha/GIS_Dataviewer/blob/main/Files/GIS_viewer_Tab_1ov.png?raw=true)
![GIS Viewer Tab2](https://github.com/Salvatore-Rocha/GIS_Dataviewer/blob/main/Files/GIS_viewer_Tab_2ov.jpg?raw=true)
![GIS Viewer Tab3](https://github.com/Salvatore-Rocha/GIS_Dataviewer/blob/main/Files/GIS_viewer_Tab_3ov.png?raw=true)
![GIS Viewer Tab4](https://github.com/Salvatore-Rocha/GIS_Dataviewer/blob/main/Files/GIS_viewer_Tab_4ov.png?raw=true)

### 🔑 Key components:

- Visualization of Administrative Divisions: Users can explore the geographical layout and boundaries of Mexico City's 16 alcaldías. Each alcaldía can be visualized in detail, showing how Airbnb listings are distributed across these larger administrative regions.

- Neighborhood Insights: The project also provides a detailed view of the smaller neighborhoods (colonias), allowing for a more granular analysis of the Airbnb listings. This helps in understanding the dynamics within individual neighborhoods and comparing them across the city.
- 
- Airbnb Listings Analysis: The core of the project involves analyzing Airbnb listings based on various factors:
  - Price: Visualize how the prices of Airbnb listings vary across different regions, helping to identify more expensive and more affordable areas.
  - Number of Reviews: By examining the number of reviews, users can gauge the popularity and activity level of listings in different areas. This can highlight tourist hotspots and areas with high engagement.
  - Density: Analyzing the density of listings helps in understanding the concentration of Airbnb properties, which can indicate areas with high competition or high demand.
  - Clustering Analysis: The project includes functionality to perform clustering analysis on the Airbnb listings. This helps in identifying natural groupings of listings based on various attributes, providing insights into market segmentation and spatial patterns.
- Interactive Features: The interactive maps and visualizations are a major feature of the project. Users can switch between different views, update graphs dynamically, and interact with the data in real-time. This interactivity enhances the user experience and allows for a deeper exploration of the data.


### 📄 Data Sources
- Airbnb data set: [Insideairbnb.com/mexico-city](https://insideairbnb.com/mexico-city/)
- CDMX Alcaldias JSON file: [Cdmx-alcaldias-4326.json](https://github.com/Salvatore-Rocha/GIS_Dataviewer/blob/main/Files/cdmx-alcaldias-4326.json)
  - The original file was downloaded from [Idegeo.centrogeo.org.mx](https://idegeo.centrogeo.org.mx/layers/geonode%3Aalcaldias)
- [Georef-mexico-colonia.geojson](https://github.com/Salvatore-Rocha/GIS_Dataviewer/blob/main/Files/georef-mexico-colonia.geojson)
  - Original GeoJSON file was downloaded from [Public.opendatasoft](https://public.opendatasoft.com/explore/dataset/georef-mexico-colonia/export/?disjunctive.sta_code&disjunctive.sta_name&disjunctive.mun_code&disjunctive.mun_name&disjunctive.col_code&disjunctive.col_name&sort=year&location=15,19.38479,-99.23717&basemap=jawg.light)
 

### 🔗 External links

To better understand parts of the code, the logic behind certain structures, and the transformations applied, please refer to the following Google Colab notebook.

[Google Colab Notebook](https://colab.research.google.com/drive/1Xnx0tj9BDDt_NgxE2d2gdFr93wkmJ-bh?usp=sharing)
