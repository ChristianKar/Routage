"""
This module reads the data stored in Data.npy file and diplays it on a dash interface using graphs,
maps and tables

"""

import sys
from pathlib import Path
file = Path(__file__).resolve()
package_root_directory = file.parents[1]
sys.path.append(str(package_root_directory))

import dash
from dash import dash_table
import numpy as np
from dash import dcc
import plotly.graph_objs as go
from dash import html, Input, Output
from Layers.to_png import conv
from Layers.proj import reproj
import folium
from scipy.ndimage import *
from skimage import io
import rasterio as rio
import os
from scipy import stats
from Model.model_analysis import Pol_regression, error, rem_outliers, sigmoid, Func
from Model.time_pred import predict
import pandas as pd
from scipy.optimize import curve_fit
import datetime
import tensorflow as tf



D, coordinates, Cols = np.load('./Extracted_data/Data.npy', allow_pickle='TRUE')
E = np.load('./Extracted_data/NN_reg_jose.npy', allow_pickle='TRUE')
model = tf.keras.models.load_model('Model/NN_Model.h5')
predicted_speed = model.predict(np.linspace(-7, 16, 200))
predicted_speed = [i[0] for i in predicted_speed]

def convert(input):
    path = './MNT/'
    if 'proj_'+input not in os.listdir(path):
        reproj(path, input)
    if input.split('.')[0]+'.png' not in os.listdir(path):
        conv(path, input)
    with rio.open(path+'proj_'+input) as src:
        min_lat, min_lon, max_lat, max_lon = src.bounds
    with rio.open(path+input) as src:
        img = src.read(1)
    #b = [[min_lon-13.010128, min_lat-3.457402], [max_lon-13.010128, max_lat-3.457402]]
    bounds_orig = [[min_lon, min_lat], [max_lon, max_lat]]
    return bounds_orig, img


def rgb_to_hex(red, green, blue):
    """Return color as #rrggbb for the given color values."""
    return '#%02x%02x%02x' % (red, green, blue)
       

"""bounds_fin1, img1 = convert('paris.tif')
center1 = [(3*bounds_fin1[0][0]+bounds_fin1[1][0])/4,
          (3*bounds_fin1[0][1]+bounds_fin1[1][1])/4]"""

bounds_fin2, img2 = convert('Saclay.tif')
center2 = [(3*bounds_fin2[0][0]+bounds_fin2[1][0])/4,
          (3*bounds_fin2[0][1]+bounds_fin2[1][1])/4]          


app = dash.Dash(__name__)

theme = {
    'dark': True,
    'detail': '#007439',
    'primary': '#00EA64',
    'secondary': '#6E6E6E',
}

app.layout = html.Div([
    html.H1(children='Analyses and Visualisations', style={'textAlign': 'center',
                                                           'color': '#7FDBFF', 'marginBottom': '1.5em'}),

    html.Label('Choose a trajectory : ', style={'font-family': 'Times'}),
    dcc.Dropdown(
        options=[
            {'label': 'Guichet asc orux', 'value': 'T1'},
            {'label': 'Guichet asc strava', 'value': 'T3'},
            {'label': 'Guichet asc suunto', 'value': 'T4'},
            {'label': 'Guichet asc strava slow',
             'value': 'T2'},
            {'label': 'Guichet dsc strava', 'value': 'T5'}
        ],
        value='T1', style={'marginBottom': '3.5em'}, id='dropdown'
    ),

    html.Div(id='table'),

    html.Div(children='Traject and Heat map : ', style={
             'textAlign': 'center', 'marginBottom': '1.5em'}),
    html.Div(id='map'),

    html.Div(id='time', style={
             'textAlign': 'center'}),
    html.Div(id='real_time', style={
             'textAlign': 'center'}),
    html.Div(id='N_time', style={
             'textAlign': 'center'}),         
    html.Div(id='error_time', style={
             'textAlign': 'center', 'marginBottom': '1.5em'}),
         

    html.Div(children='Calculated traject speed : ',
             style={'textAlign': 'center'}),

    html.Div(id='speed'),

    html.Div(children='X Y Z coordinates : ', style={'textAlign': 'center'}),
    html.Div(id='Coords'),

    html.Div(children='Elevation error (Tif/Mesured) : ', style={'textAlign': 'center'}),
    html.Div(id='elevation'),


    html.Div(children='Elevation gradient : ', style={'textAlign': 'center'}),
    html.Div(id='gradient'),


    html.Div(children='Velocity/gradient : ', style={'textAlign': 'center'}),
    html.Div(id='Vel_g'),

    html.Div(children='Change the polynome degree : '),
    dcc.Slider(
        1,
        10,
        step=1,
        id='degree',
        value=1,
        marks={str(i): str(i) for i in range(1, 10)}),

    html.Div(id='error_table'),

    html.Div(id='Outliers'),    

    html.Div(id='Stats')    
        ])


@app.callback(
    [Output('table', 'children'), Output('map', 'children'), Output('speed', 'children'), 
           Output('elevation', 'children'), Output('gradient', 'children')
           , Output('Vel_g', 'children'), Output('Coords', 'children')
            , Output('Outliers', 'children'),  Output('error_table', 'children')
            ,  Output('Stats', 'children'),  Output('time', 'children')
            ,  Output('real_time', 'children'),  Output('error_time', 'children'),  Output('N_time', 'children')],

    [Input('dropdown', 'value'), Input('degree', 'value')]
)
def update_output(value, slid_value):
    d = dict({'T1':0, 'T2':1,'T3':2, 'T4':3, 'T5':4, 'T6':5})
    route_Df, _, Yp2, X, velocity, df2, Xd, Yd, Zd, _, Yg, color_map, bins_text, gradient_infodetails_df = D[d[value]]

    Yg = np.array(Yg)
    C = coordinates[d[value]]
    colors = Cols[d[value]]
    map_ = folium.Map(location=center2, zoom_start=14)
    map_.add_child(folium.LatLngPopup())

    """data1 = io.imread('./MNT/paris.png')
    map_.add_child(folium.raster_layers.ImageOverlay(data1, opacity=0.4,
                                                            bounds=bounds_fin1))"""
    data2 = io.imread('./MNT/Saclay.png')
    map_.add_child(folium.raster_layers.ImageOverlay(data2, opacity=0.4,
                                                            bounds=bounds_fin2))                                                        
    for i in range(len(C)-1):
        Hex_color = '#640000'
        if colors[i][0]:
            Hex_color = rgb_to_hex(
                colors[i][0]-20, colors[i][1]-20, colors[i][2]-20)
        folium.PolyLine(C[i:i+2], weight=5, color=Hex_color).add_to(map_)
    f = go.Figure(data=[go.Scatter(x=X[1:], y=velocity[1:], name='raw speed'),
                        go.Scatter(x=X[1:], y=[None]*12+list(Yp2[1:])+[None]*4, name='filtred speed')])

    f2 = go.Figure(data=go.Scatter3d(
    x=Xd, y=Yd, z=Zd,
    marker=dict(
        size=2,
        color='darkgreen'
    ),
    line=dict(
        color='darkblue',
        width=2
    )
    ))            
    
    f3 = go.Figure(data=[go.Scatter(x=np.arange(len(route_Df['new_gradient'])), y=route_Df['new_gradient'], name='gradient'),
                        go.Scatter(x=np.arange(len(route_Df['new_gradient'])), y=[None]*12+list(Yg)+[None]*5, name='gradient_filtred')   ])   

    Z1 = stats.zscore(Yp2)
    Z2 = stats.zscore(Yg)
    f6 = go.Figure(data=[go.Scatter(x=np.arange(len(Z1)), y=Z1, mode='markers', name='speed_zscore'), 
                            go.Scatter(x=np.arange(len(Z2)), y=Z2, mode='markers', name='slope_zscore')])

    new_Yp2, new_Yg = rem_outliers(Yp2, Yg, Z1, Z2)

    A = np.linspace(-7, 16, 200)

    xdata, ydata = np.array(D[0][-4]), np.array(D[0][2])
    popt, _ = curve_fit(sigmoid, xdata, ydata)
    Y_sig = sigmoid(A, *popt)


    beta = Pol_regression(np.array(D[0][-4]), D[0][2], int(slid_value)+1)   

    """f4 = go.Figure(data=[go.Scatter(x=new_Yg, y=new_Yp2,mode='markers', name='data points'), 
                            go.Scatter(x=A, y=[Func(beta, k) for k in A], name='Polynomial regression'),
                            go.Scatter(x=A, y=predicted_speed, name='Neural Net regression'),
                            go.Scatter(x=A, y=Y_sig, name='Sigmoid Regression')])"""
    f4 = go.Figure(data=[go.Scatter(x=new_Yg, y=new_Yp2,mode='markers', name='data points'), 
                           go.Scatter(x=A, y=Y_sig, name='Sigmoid Regression')])                        
                    
    MSE, MAPE, R2 = error(new_Yp2, [Func(beta, xj) for xj in new_Yg])      
    MSE2, MAPE2, R22 = error(new_Yp2, sigmoid(new_Yg, *popt))                    

    error_df = {'T'+str(d[value]+1):['Pol reg', 'NN reg', 'Sig reg'],
                'MSE': [round(MSE, 4), int(E[d[value]][0]*10000)/10000, round(MSE2, 4)],
                'MAPE':[round(MAPE,4), int(E[d[value]][1]*10000)/10000, round(MAPE2,4)], 
                'R2':[round(R2,4), round(E[d[value]][2],4), round(R22,4)]}
    df3 = pd.DataFrame(error_df)

    x = np.array(route_Df['x'])
    y = np.array(route_Df['y'])
    z = np.array(route_Df['elevation'])

    f5 = go.Figure(data=go.Scatter3d(
    x=x, y=y, z=z,
    marker=dict(
        size=2,
        color='darkgreen'
    ),
    line=dict(
        color='darkblue',
        width=2
    )
    ))         

    f7 = go.Figure(
        data=[go.Bar(
            x = gradient_infodetails_df['gradient_range'].astype(str),
            y = gradient_infodetails_df['total_distance'].apply(lambda x: round(x / 1000, 2)),
            marker_color = color_map,
            text = bins_text
        )],
        layout=go.Layout(
            bargap = 0,
            title = 'Gradient profile of the selected route',
            xaxis_title = 'Gradient range (%)',
            yaxis_title = 'Distance covered in km',
            autosize= False,
            width = 1480,
            height = 820,
            template='ggplot2'
        )
    )
    real_time, pred_time, naive_time = predict(d[value], model)
    real_time2 = datetime.timedelta(seconds=real_time)
    pred_time2 = datetime.timedelta(seconds=pred_time)
    naive_time2 = datetime.timedelta(seconds=naive_time)
    time_error = datetime.timedelta(seconds=abs(real_time - pred_time))


    return dash_table.DataTable(data=df2.to_dict('records'),
                                columns=[{"name": i, "id": i} for i in df2.columns]), html.Iframe(id='map1', srcDoc=map_._repr_html_(), 
                                    style={"height": "450px", "width": "100%", 'marginBottom': '3.5em', 'margintop': '3.5em'}, 
                                    title='traject and elevation heatmap : '), dcc.Graph(figure=f, 
                                    style={'marginBottom': '3.5em'}), dcc.Graph(figure=f2, style={'marginBottom': '3.5em'}), dcc.Graph(figure=f3, 
                                    style={'marginBottom': '3.5em'}), dcc.Graph(figure=f4, style={'marginBottom': '3.5em'}), dcc.Graph(figure=f5, 
                                    style={'marginBottom': '3.5em'}), dcc.Graph(figure=f6, 
                                    style={'marginBottom': '3.5em'}), dash_table.DataTable(data=df3.to_dict('records'),
                                columns=[{"name": i, "id": i} for i in df3.columns]), dcc.Graph(figure=f7,
                                 style={'marginBottom': '3.5em'}), f'Estimated Time: {pred_time2}s', f'Real mesured Time: {real_time2}s', f'Time error: {time_error}s', f'Naive time: {naive_time2}s'
                                    
                  
                                     

if __name__ == '__main__':
    app.run_server(debug=True)
