# Discover Mexico City's Airbnb Scene
### 🌎 Project Overview
This project visualizes the Airbnb landscape in Mexico City using Plotly and Dash, focusing on price and user reviews across two levels: administrative divisions (16 alcaldías) and neighborhoods (1812 colonias).

### 🤖 Web app link ➡️  [Discover Mexico City's Airbnb Scene](https://discover-mexico-citys-airbnb-scene.onrender.com/)

**Note**: The app is hosted on a free instance of render that will spin down with inactivity, which can delay requests by 50 seconds _or more_. **_Please be patient_**.

### 🔎 Visual aspects of the project:
![GIS Viewer Tab1](https://github.com/Salvatore-Rocha/GIS_Dataviewer/blob/main/Files/GIS_viewer_Tab_1ov.png?raw=true)
![GIS Viewer Tab2](https://github.com/Salvatore-Rocha/GIS_Dataviewer/blob/main/Files/GIS_viewer_Tab_2ov.jpg?raw=true)
![GIS Viewer Tab3](https://github.com/Salvatore-Rocha/GIS_Dataviewer/blob/main/Files/GIS_viewer_Tab_3ov.png?raw=true)
![GIS Viewer Tab4](https://github.com/Salvatore-Rocha/GIS_Dataviewer/blob/main/Files/GIS_viewer_Tab_4ov.png?raw=true)

### 🔑 Key Insights:

- #### Visualization of Administrative Divisions:
CDMX has a high density of Airbnbs in the central zone, where the Central Business District is located, alongside the majority of cultural and historical landmarks. In contrast, the southern area is characterized by natural landscapes, including Xochimilco Lake, Desierto de los Leones National Park, and the Ajusco Mountains. The northern and eastern regions are predominantly industrial and working-class, featuring densely populated neighborhoods and areas that face significant social challenges. It is important to consider these geographical and socioeconomic factors in CDMX, as they all impact the distribution of Airbnb listings in these areas.

- #### Neighborhood Insights:
The project also provides a closer look at the distribution of Airbnb listings in smaller neighborhoods (colonias), allowing for a more granular analysis. We observe a match between high Airbnb prices and listing density in the luxury areas of the city (Condesa, Polanco, Lomas de Chapultepec, Historic Centre). This insight enables more precise targeting of investment opportunities in real estate, optimization of pricing strategies, and identification of areas to address supply and demand imbalances across the city.
  
- #### Airbnb Listings Analysis:
  The core of the project involves analyzing Airbnb listings based on various factors:
  - Price: Visualize how the prices of Airbnb listings vary across different regions, helping to identify more expensive and more affordable areas.
  - Number of Reviews: A further NLP sentiment analysis must be conducted to identify what users value most based on their reviews. The number of reviews also highlights tourist hotspots and areas with high engagement.
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
