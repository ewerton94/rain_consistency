import json
import numpy as np
import folium
import os
import data_view2 as dv

def plot_map(station_data, filename = '', plot_data = None, model = False):
    
    base_name = 'Map' # Nome para o mapa
    coordinates = station_data[list(station_data.keys())[0]][1]['Coordinates'] # Dado de entrada das coordendas dos pontos

    Map = folium.Map(coordinates, zoom_start = 8 ) # Do Folium

    for station in station_data.keys(): # Loop para criar vários pontos com as informações preenchidas abaixo para cada um
        
        station_coordinates = [station_data[station][1]['Coordinates'][0], station_data[station][1]['Coordinates'][1]]
        
        plot_data = plot_data_info(station_data,station,filename,model)

#Esse html_info representa as informações que vão ser apresentadas nos pop-ups que representam os pontos
#ela é escrita em html mesmo
# Os colchetes em azul é só uma forma de indicar que espaço será preenchido pelos dados que são definidos a seguir no .format()
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
        #em plot_data é informado o hiperlink de algo a ser plotado, no meu caso eu informo um hiperlink para os modelos simulados nos postos
        #eu pego esse hiperlink de outra função externa criada por mim
        #vcs podem criar um loop também para gerar os vários links de gráficos

        folium.Marker(station_coordinates, popup = html_info).add_to(Map) #Cria o ponto a ser plotado

    dv.out_view_name(filename, base_name = base_name) # uma função exportada de outro módulo criado por mim (só serve para criar um nome pro arquivo de saída)ignorem
    Map.save(filename) #plota o mapa