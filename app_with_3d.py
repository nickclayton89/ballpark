
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import ast
import numpy as np

st.set_page_config(page_title="MLB Stadium Dashboard", layout="wide")

# Load the data
@st.cache_data
def load_data():
    return pd.read_csv("mlb_stadiums_with_fence.csv")

df = load_data()

# Sidebar for stadium selection
stadium_names = df["Stadium"].tolist()
selected_stadium = st.sidebar.selectbox("Select a Stadium", stadium_names)

# Filter the selected stadium
stadium = df[df["Stadium"] == selected_stadium].iloc[0]

# Display stadium info
st.title(f"{stadium['Stadium']} ({stadium['Team']})")
st.markdown(f"**Location**: {stadium['City']}, {stadium['State']}")
st.markdown(f"**Year Built**: {stadium['Year_Built']}")
st.markdown(f"**Capacity**: {stadium['Capacity']:,}")
st.markdown(f"**Surface**: {stadium['Surface']}")
st.markdown(f"**Roof Type**: {stadium['Roof_Type']}")
st.markdown(f"**Altitude**: {stadium['Altitude_ft']} ft")

# Parse outfield wall coordinates
x = ast.literal_eval(stadium["Wall_X"])
y = ast.literal_eval(stadium["Wall_Y"])
z = ast.literal_eval(stadium["Wall_Height"])

# Additional geometry: infield, mound, seating
field_radius = 400
mound_radius = 9
mound_height = 1
infield_side = 90
seating_rings = 4
seating_step = 10

theta = np.linspace(np.pi, 0, 100)
mound_theta = np.linspace(0, 2 * np.pi, 50)
mound_x = mound_radius * np.cos(mound_theta)
mound_y = mound_radius * np.sin(mound_theta)
mound_z = np.ones_like(mound_x) * mound_height

infield_x = [0, 0, infield_side, infield_side, 0]
infield_y = [0, infield_side, infield_side, 0, 0]
infield_z = [0] * 5

seating_traces = []
for i in range(seating_rings):
    ring_r = field_radius + 20 + i * 20
    ring_h = (i + 1) * seating_step
    ring_x = ring_r * np.cos(theta)
    ring_y = ring_r * np.sin(theta)
    ring_z = np.ones_like(ring_x) * ring_h
    seating_traces.append(go.Scatter3d(
        x=ring_x, y=ring_y, z=ring_z,
        mode='lines',
        line=dict(color='gray', width=2),
        name=f"Seating Ring {i+1}"
    ))

# Plotly 3D rendering
fig = go.Figure()

# Outfield wall
fig.add_trace(go.Scatter3d(x=x, y=y, z=z,
                           mode='lines', line=dict(color='blue', width=5),
                           name='Outfield Wall'))

# Mound
fig.add_trace(go.Scatter3d(x=mound_x, y=mound_y, z=mound_z,
                           mode='lines', line=dict(color='orange', width=3),
                           name='Pitcher Mound'))

# Infield
fig.add_trace(go.Scatter3d(x=infield_x, y=infield_y, z=infield_z,
                           mode='lines', line=dict(color='green', width=4),
                           name='Infield'))

# Seating
for trace in seating_traces:
    fig.add_trace(trace)

fig.update_layout(
    title=f"3D Rendering of {stadium['Stadium']}",
    scene=dict(
        xaxis_title='X (ft)',
        yaxis_title='Y (ft)',
        zaxis_title='Height (ft)',
        aspectratio=dict(x=1, y=1, z=0.5)
    ),
    showlegend=True,
    margin=dict(l=0, r=0, t=30, b=0)
)

st.plotly_chart(fig, use_container_width=True)
