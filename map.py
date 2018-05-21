import json
import numpy as np
import folium
import os
import data_view2 as dv

def plot_map(station_data, filename = '', plot_data = None, model = False):
    
    base_name = 'Map'
    coordinates = station_data[list(station_data.keys())[0]][1]['Coordinates']

    Map = folium.Map(coordinates, zoom_start = 8 )

    for station in station_data.keys():
        
        station_coordinates = [station_data[station][1]['Coordinates'][0], station_data[station][1]['Coordinates'][1]]
        
        plot_data = plot_data_info(station_data,station,filename,model)

        html_info = """
        <h5> <b>Dados do Posto</b></h5>
        <p> <big><b>Nome: </b>{}<\p>
        <p> <b>Código: </b>{}<\p>
        <p> <b>Área de drenagem: </b> {} km<sup>2<\sup> <\p>
        <p> <b>Latitude: </b>{} <sup>o<\sup><\p>
        <p> <b>Longitude: </b> {} <sup>o<\sup><\p>
        <a href="{}", target = blank > Data View </a>
        </big>
        """.format(
        station_data[station][1]['Name'].upper(),
        station_data[station][1]['Code'],
        station_data[station][1]['DrainArea'], 
        station_data[station][1]['Coordinates'][0],
        station_data[station][1]['Coordinates'][1],
        plot_data
        )

        folium.Marker(station_coordinates, popup = html_info).add_to(Map)

    dv.out_view_name(filename, base_name = base_name)
    Map.save(filename)