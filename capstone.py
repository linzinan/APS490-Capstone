# -*- coding: utf-8 -*-
"""capstone.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1vKH9KOxgYazmQQTqzMC9nUrXDy0l9tgx
"""

import pandas as pd
import numpy as np

path = "/Users/anton/Desktop/APS490/APS490-Capstone/Data/TEST/"
header = ["tag", "rssi", "avrg_rssi", "dist", "time"]

df_1m = pd.read_csv(path+"1m", names=header)
df_2m = pd.read_csv(path+"2m", names=header)
df_3m = pd.read_csv(path+"3m", names=header)
df_4m = pd.read_csv(path+"4m", names=header)
df_5m = pd.read_csv(path+"5m", names=header)
df_d1 = pd.read_csv(path+"Device1.csv", names=header)
df_d2 = pd.read_csv(path+"Device2.csv", names=header)
df_d3 = pd.read_csv(path+"Device3.csv", names=header)
df = [df_1m, df_2m, df_3m, df_4m, df_5m]
df_d = [df_d1, df_d2, df_d3]

# drop field
def drop(field, data):
  for i in range(len(data)):
    data[i].drop(columns=field, inplace=True)

# convert time to seconds
def to_elasped(data):
  for i in range(len(data)):
    data[i]['elapsed_seconds'] = (pd.to_datetime(data[i]['time']) - pd.to_datetime(data[i]['time'][0])).dt.total_seconds().round(1)
    data[i] = data[i].assign(elapsed_seconds = data[i]['elapsed_seconds'].round(1))

to_elasped(df)
drop(['tag', 'time'], df)
df_2m.head()

from scipy.signal import butter,filtfilt
from plotly.subplots import make_subplots
import plotly.graph_objects as go

# Filter requirements.
T = 120         # Sample Period
fs = 3.0       # sample rate, Hz
cutoff = 0.03    # desired cutoff frequency of the filter, Hz
nyq = 0.5 * fs  # Nyquist Frequency
order = 4     # parameter for filter
n = int(T * fs) # total number of samples

data = df_1m['rssi'].append(df_4m['rssi'])

def butter_lowpass_filter(data, cutoff, fs, order):
    normal_cutoff = cutoff / nyq
    # Get the filter coefficients
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    y = filtfilt(b, a, data)
    return y

# Filter the data, and plot both the original and filtered signals.
y = butter_lowpass_filter(data, cutoff, fs, order)
fig = go.Figure()
fig.add_trace(go.Scatter(
            y = df_1m['rssi'],
            #x = df_1m['elapsed_seconds'],
            mode='markers',
            name = 'Raw RSSI Signal (1 meter away)',
            #marker_color= 'grey'
            ))
fig.add_trace(go.Scatter(
            y = df_4m['rssi'],
            x = np.linspace(len(df_1m),len(df_1m)+len(df_4m)-1,len(df_4m)),
            mode='markers',
            name = 'Raw RSSI Signal (4 meters away)',
            marker_color = 'rgba(77, 63, 196, .8)'
            ))
# fig.add_trace(go.Scatter(
#             y = df_1m['avrg_rssi'].append(df_4m['avrg_rssi']),
#             line =  dict(shape =  'spline' ),
#             name = 'Rolling-Avrg Filtered RSSI'
#             ))

fig.add_trace(go.Scatter(
            y = df_1m['avrg_rssi'].append(df_4m['avrg_rssi']),
            line =  dict(shape =  'spline' ),
            name = 'Rolling-Avrg Filtered RSSI'
            ))

# fig.add_trace(go.Scatter(
#             y = df_4m['avrg_rssi'],
#             x = np.linspace(len(df_1m),len(df_1m)+len(df_4m)-1,len(df_4m)),
#             line =  dict(shape =  'spline' ),
#             name = 'Rolling-Avrg Filtered RSSI'
#             ))
fig.add_trace(go.Scatter(
            y = y,
            line =  dict(shape =  'spline' ),
            name = 'Butterworth Filtered RSSI',
            marker_color = 'red'
            ))

fig.update_layout(
    title={
        'text': "Comparison between Butterworth and Rolling Average Filter",
        'y':0.9,
        'x':0.5,
        # 'xanchor': 'center',
        # 'yanchor': 'top'
    },
    xaxis_title="Time (s)",
    yaxis_title="RSSI (Signal Strength)",
    font=dict(
        family="Courier New",
        size=14,
        color="#7f7f7f"
    ),
    legend=dict(x=.65, y=1.03, font=dict(size = 10))
)
fig.show()

def getdistance(rssi,txpower):
    txpower = int(txpower)   #one meter away RSSI
    if rssi == 0:
        return -1
    else:
        ratio = rssi*1.0 / txpower
        if ratio < 1:
            return ratio ** 10
        else:
            return 0.89976 * ratio**7.7095 + 0.111

getdistance(-83.5, -69)

print([len(i) for i in df_d])

# process devices data
to_elasped(df_d)

df_d2.head()

df_d1_1 = df_d1[df_d1['tag'] == 1]
df_d1_2 = df_d1[df_d1['tag'] == 2]
df_d1_3 = df_d1[df_d1['tag'] == 3]
df_d2_1 = df_d2[df_d2['tag'] == 1]
df_d2_2 = df_d2[df_d2['tag'] == 2]
df_d2_3 = df_d2[df_d2['tag'] == 3]
df_d3_1 = df_d3[df_d3['tag'] == 1]
df_d3_2 = df_d3[df_d3['tag'] == 2]
df_d3_3 = df_d3[df_d3['tag'] == 3]
df_dd = [df_d1_1, df_d1_2, df_d1_3, df_d2_1, df_d2_2, df_d2_3, df_d3_1, df_d3_2, df_d3_3]

df_d1_2.tail(1)

minv = 1000.0
for i in df_dd:
  last = i['elapsed_seconds'].tail(1)
  if last.values[0] < minv:
    minv = last.values[0]
  print(last)

print("shortest: ", minv)

for i in range(len(df_dd)):
  df_dd[i] = df_dd[i][df_dd[i]['elapsed_seconds'] <= 841.1]

maxv = 0
for i in df_dd:
  last = i['elapsed_seconds'].tail(1)
  if last.values[0] > maxv:
    maxv = last.values[0]
  print(last)

print("longest: ", maxv)

df_d1_1.head()

from plotly.subplots import make_subplots
fig = go.Figure()
# fig.add_trace(go.Scatter(
#             y = df_d1_1['rssi'],
#             x = df_d1_1['elapsed_seconds'],
#             mode='markers',
#             name = 'Raw RSSI Signal (1 meter away)',
#             #marker_color= 'grey'
#             ))
# fig.add_trace(go.Scatter(
#             y = df_d1_2['rssi'],
#             x = df_d1_2['elapsed_seconds'],
#             mode='markers',
#             name = 'Raw RSSI Signal (1 meter away)',
#             #marker_color= 'grey'
#             ))
# fig.add_trace(go.Scatter(
#             y = df_d1_3['rssi'],
#             x = df_d1_3['elapsed_seconds'],
#             mode='markers',
#             name = 'Raw RSSI Signal (1 meter away)',
#             #marker_color= 'grey'
#             ))
fig = make_subplots(rows=1, cols=3, shared_yaxes=True, subplot_titles=("Device 1", "Device 2", "Device 3"))
fig.append_trace(go.Scatter(
            y = butter_lowpass_filter(df_d1_1['rssi'], cutoff, fs, order),
            x = df_d1_1['elapsed_seconds'],
            line =  dict(shape =  'spline' ),
            #mode='markers',
            name = 'Tag 1',
            marker_color = 'yellow'),
            row = 1, col = 1
            )
fig.add_trace(go.Scatter(
            y = butter_lowpass_filter(df_d1_2['rssi'], cutoff, fs, order),
            x = df_d1_2['elapsed_seconds'],
            #line =  dict(shape =  'spline' ),
            #mode='markers',
            name = 'Tag 2',
            marker_color = 'red'),
            row=1, col=1
            )
fig.add_trace(go.Scatter(
            y = butter_lowpass_filter(df_d1_3['rssi'], cutoff, fs, order),
            x = df_d1_3['elapsed_seconds'],
            #line =  dict(shape =  'spline' ),
            #mode='markers',
            name = 'Tag 3',
            marker_color = 'blue'),
            row=1, col=1
            )
fig.append_trace(go.Scatter(
            y = butter_lowpass_filter(df_d2_1['rssi'], cutoff, fs, order),
            x = df_d2_1['elapsed_seconds'],
            line =  dict(shape =  'spline' ),
            #mode='markers',
            name = 'Tag 1',
            showlegend=False,
            marker_color = 'yellow'),
            row = 1, col = 2
            )
fig.add_trace(go.Scatter(
            y = butter_lowpass_filter(df_d2_2['rssi'], cutoff, fs, order),
            x = df_d2_2['elapsed_seconds'],
            #line =  dict(shape =  'spline' ),
            #mode='markers',
            name = 'Tag 2',
            showlegend=False,
            marker_color = 'red'),
            row=1, col=2
            )
fig.add_trace(go.Scatter(
            y = butter_lowpass_filter(df_d2_3['rssi'], cutoff, fs, order),
            x = df_d2_3['elapsed_seconds'],
            #line =  dict(shape =  'spline' ),
            #mode='markers',
            name = 'Tag 3',
            showlegend=False,
            marker_color = 'blue'),
            row=1, col=2
            )
fig.append_trace(go.Scatter(
            y = butter_lowpass_filter(df_d3_1['rssi'], cutoff, fs, order),
            x = df_d3_1['elapsed_seconds'],
            line =  dict(shape =  'spline' ),
            #mode='markers',
            name = 'Tag 1',
            showlegend=False,
            marker_color = 'yellow'),
            row = 1, col = 3
            )
fig.add_trace(go.Scatter(
            y = butter_lowpass_filter(df_d3_2['rssi'], cutoff, fs, order),
            x = df_d3_2['elapsed_seconds'],
            #line =  dict(shape =  'spline' ),
            #mode='markers',
            name = 'Tag 2',
            showlegend=False,
            marker_color = 'red'),
            row=1, col=3
            )
fig.add_trace(go.Scatter(
            y = butter_lowpass_filter(df_d3_3['rssi'], cutoff, fs, order),
            x = df_d3_3['elapsed_seconds'],
            #line =  dict(shape =  'spline' ),
            #mode='markers',
            name = 'Tag 3',
            showlegend=False,
            marker_color = 'blue'),
            row=1, col=3
            )
fig.add_trace(go.Scatter(
            y = [-73 for _ in range(len(df_d3_2['elapsed_seconds']))],
            x = df_d3_2['elapsed_seconds'],
            #line =  dict(shape =  'spline' ),
            line =  dict(dash =  'dash' ),
            #mode='markers',
            name = 'Tag 3',
            showlegend=False,
            marker_color = 'black'),
            row=1, col=1
            )
fig.add_trace(go.Scatter(
            y = [-73 for _ in range(len(df_d3_2['elapsed_seconds']))],
            x = df_d3_2['elapsed_seconds'],
            #line =  dict(shape =  'spline' ),
            line =  dict(dash =  'dash' ),
            #mode='markers',
            name = 'Tag 3',
            showlegend=False,
            marker_color = 'black'),
            row=1, col=2
            )
fig.add_trace(go.Scatter(
            y = [-73 for _ in range(len(df_d3_2['elapsed_seconds']))],
            x = df_d3_2['elapsed_seconds'],
            line =  dict(dash =  'dash' ),
            #mode='markers',
            name = 'Threshold',
            marker_color = 'black'),
            row=1, col=3
            )
fig.update_layout(
    title={
        'text': "RSSI Record of Three Tags from Three Devices",
        'y':0.9,
        'x':0.5,
        # 'xanchor': 'center',
        # 'yanchor': 'top'
    },
    xaxis_title= "Time (s)",
    yaxis_title="RSSI (Signal Strength)",
    font=dict(
        family="Courier New",
        size=14,
        color="#7f7f7f"
    ),
    legend=dict(x=.93, y=1.1, font=dict(size = 10))
)
fig.update_xaxes(title_text="Time (s)", row=1, col=2)
fig.update_xaxes(title_text="Time (s)", row=1, col=3)
fig.show()

fig = go.Figure()
fig.add_trace(go.Scatter(
            y = butter_lowpass_filter(df_d1_1['dist'], cutoff, fs, order),
            #x = df_d1_1['elapsed_seconds'],
            #mode='markers',
            name = '1',
            #marker_color= 'grey'
            ))
fig.add_trace(go.Scatter(
            y = butter_lowpass_filter(df_d1_2['dist']+0.5, cutoff, fs, order),
            #x = df_d1_2['elapsed_seconds'],
            #mode='markers',
            name = '2',
            #marker_color= 'grey'
            ))
fig.add_trace(go.Scatter(
            y = butter_lowpass_filter(df_d1_3['dist'], cutoff, fs, order),
            #x = df_d1_3['elapsed_seconds'],
            #mode='markers',
            name = '3',
            #marker_color= 'grey'
            ))
fig.show()

# fig = go.Figure()
# fig.add_trace(go.Scatter(
#             y = df_d3_1['rssi'],
#             x = df_d3_1['elapsed_seconds'],
#             mode='markers',
#             name = 'Raw RSSI Signal (1 meter away)',
#             #marker_color= 'grey'
#             ))
# fig.add_trace(go.Scatter(
#             y = df_d3_2['rssi'],
#             x = df_d3_2['elapsed_seconds'],
#             mode='markers',
#             name = 'Raw RSSI Signal (1 meter away)',
#             #marker_color= 'grey'
#             ))
# fig.add_trace(go.Scatter(
#             y = df_d3_3['rssi'],
#             x = df_d3_3['elapsed_seconds'],
#             mode='markers',
#             name = 'Raw RSSI Signal (1 meter away)',
#             #marker_color= 'grey'
#             ))
# fig.add_trace(go.Scatter(
#             y = butter_lowpass_filter(df_d3_1['rssi'], cutoff, fs, order),
#             x = df_d3_1['elapsed_seconds'],
#             line =  dict(shape =  'spline' ),
#             name = 'Butterworth Filtered RSSI',
#             marker_color = 'blue'
#             ))
# fig.add_trace(go.Scatter(
#             y = butter_lowpass_filter(df_d3_2['rssi'], cutoff, fs, order),
#             x = df_d3_2['elapsed_seconds'],
#             line =  dict(shape =  'spline' ),
#             name = 'Butterworth Filtered RSSI',
#             marker_color = 'blue'
#             ))
# fig.add_trace(go.Scatter(
#             y = butter_lowpass_filter(df_d3_3['rssi'], cutoff, fs, order),
#             x = df_d3_3['elapsed_seconds'],
#             line =  dict(shape =  'spline' ),
#             name = 'Butterworth Filtered RSSI',
#             marker_color = 'blue'
#             ))
# fig.show()

import plotly.express as px
fig = go.Figure()
fig.add_trace(go.Box(
            y = df_1m['avrg_rssi'],#butter_lowpass_filter(df_1m['rssi'], cutoff, fs, order),
            x = [1 for _ in range(len(df_1m['rssi']))],
            #line =  dict(shape =  'spline' ),
            #mode = 'markers',
            name = 'Butterworth Filtered RSSI',
            marker_color = 'blue'
            ))
fig.add_trace(go.Box(
            y = df_2m['avrg_rssi'],#butter_lowpass_filter(df_2m['rssi'], cutoff, fs, order),
            x = [2 for _ in range(len(df_2m['rssi']))],
            #line =  dict(shape =  'spline' ),
            #mode = 'markers',
            name = 'Butterworth Filtered RSSI',
            marker_color = 'blue'
            ))
fig.add_trace(go.Box(
            y = df_3m['avrg_rssi'],#butter_lowpass_filter(df_3m['rssi'], cutoff, fs, order),
            x = [3 for _ in range(len(df_3m['rssi']))],
            #line =  dict(shape =  'spline' ),
            #mode = 'markers',
            name = 'Butterworth Filtered RSSI',
            marker_color = 'blue'
            ))
fig.add_trace(go.Box(
            y = df_4m['avrg_rssi'],#butter_lowpass_filter(df_4m['rssi'], cutoff, fs, order),
            x = [5 for _ in range(len(df_5m['rssi']))],
            #line =  dict(shape =  'spline' ),
            #mode = 'markers',
            name = 'Butterworth Filtered RSSI',
            marker_color = 'blue'
            ))
fig.add_trace(go.Box(
            y = df_5m['avrg_rssi'],#butter_lowpass_filter(df_5m['rssi'], cutoff, fs, order),
            x = [4 for _ in range(len(df_4m['rssi']))],
            #line =  dict(shape =  'spline' ),
            #mode = 'markers',
            #name = 'Butterworth Filtered RSSI',
            marker_color = 'blue'
            ))

fig.show()

df_1m['acc_dist'] = 1
df_2m['acc_dist'] = 2
df_3m['acc_dist'] = 3
df_4m['acc_dist'] = 5
df_5m['acc_dist'] = 4

df_box = df_1m.append(df_2m).append(df_3m).append(df_4m).append(df_5m)

df_box = df_box.reset_index(drop=True)

mean_rssi = [i['avrg_rssi'].mean() for i in df]
temp = mean_rssi[3]
mean_rssi[3] = mean_rssi[4]
mean_rssi[4] = temp
mean_rssi

fig = go.Figure()
fig.add_trace(go.Box(
            y = df_box['avrg_rssi'],
            x = df_box['acc_dist'],
            #line =  dict(shape =  'spline' ),
            #mode = 'markers',
            name = 'RSSI Distribution',
            marker_color = 'blue'
            ))
fig.add_trace(go.Scatter(
            y = mean_rssi,
            x = np.linspace(1 ,5, 5),
            #line =  dict(shape =  'spline' ),
            #mode = 'markers',
            name = 'RSSI Mean Trendline',
            marker_color = 'Red'
            ))

fig.update_layout(
    title={
        'text': "Boxplot of the RSSI Distibution in Fixed Distance",
        'y':0.9,
        'x':0.5,
        # 'xanchor': 'center',
        # 'yanchor': 'top'
    },
    xaxis_title="Distance from the Raspberry Pi (m)",
    yaxis_title="RSSI (Signal Strength)",
    font=dict(
        family="Courier New",
        size=14,
        color="#7f7f7f"
    ),
    legend=dict(x=0.85, y=1, font=dict(size = 10))
)
fig.show()

df_output_d1_1 = df_d1_1[df_d1_1['rssi'] > -73]

df_output_d1_1 = df_output_d1_1.assign(butter = butter_lowpass_filter(df_output_d1_1['rssi'], cutoff, fs, order))



df_door_1m = pd.read_csv(path+"1m door", names=header)
df_door_2m = pd.read_csv(path+"2m door", names=header)
df_door_3m = pd.read_csv(path+"3m door", names=header)
df_door = [df_door_1m, df_door_2m, df_door_3m]

df_door_1m['acc_dist'] = 1
df_door_2m['acc_dist'] = 2
df_door_3m['acc_dist'] = 3

df_door_box = df_door_1m.append(df_door_2m).append(df_door_3m)
df_box = df_1m.append(df_2m).append(df_3m)

mean_rssi = mean_rssi[:3]
mean_rssi

mean_door = [i['avrg_rssi'].mean() for i in df_door]
mean_door

fig = go.Figure()
fig.add_trace(go.Box(
            y = df_box['avrg_rssi'],
            x = df_box['acc_dist'],
            #line =  dict(shape =  'spline' ),
            #mode = 'markers',
            name = 'RSSI Distribution',
            marker_color = 'blue'
            ))
fig.add_trace(go.Scatter(
            y = mean_rssi,
            x = np.linspace(1 ,3, 3),
            #line =  dict(shape =  'spline' ),
            #mode = 'markers',
            name = 'RSSI Mean Trendline',
            marker_color = 'Red'
            ))
fig.add_trace(go.Box(
            y = df_door_box['avrg_rssi'],
            x = df_door_box['acc_dist'],
            #line =  dict(shape =  'spline' ),
            #mode = 'markers',
            name = 'RSSI w/ Medium Interference Distribution',
            marker_color = 'rgba(0, 0, 100, .6)'
            ))
fig.add_trace(go.Scatter(
            y = mean_door,
            x = np.linspace(1 ,3, 3),
            #line =  dict(shape =  'spline' ),
            #mode = 'markers',
            name = 'RSSI w/ Medium Interference Trendline',
            marker_color = 'purple'
            ))
fig.update_layout(
    title={
        'text': "Comparison of RSSI Distibution with/ without Interference of Medium",
        'y':0.9,
        'x':0.5,
        # 'xanchor': 'center',
        # 'yanchor': 'top'
    },
    xaxis_title="Distance from the Raspberry Pi (m)",
    yaxis_title="RSSI (Signal Strength)",
    font=dict(
        family="Courier New",
        size=14,
        color="#7f7f7f"
    ),
    legend=dict(x=0.71, y=1.05, font=dict(size = 10))
)

fig.show()

import sys

if __name__ == "__main__":
    print(f"Arguments count: {len(sys.argv)}")
    for i, arg in enumerate(sys.argv):
        print(f"Argument {i:>6}: {arg}")
