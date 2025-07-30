
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import ast

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

# Parse fence coordinates
x = ast.literal_eval(stadium["Wall_X"])
y = ast.literal_eval(stadium["Wall_Y"])
z = ast.literal_eval(stadium["Wall_Height"])

# 3D Plot
fig = go.Figure(data=[go.Scatter3d(
    x=x, y=y, z=z,
    mode='lines+markers',
    marker=dict(size=4, color=z, colorscale='Viridis'),
    line=dict(color='blue', width=5)
)])

fig.update_layout(
    title="3D Outfield Fence",
    scene=dict(
        xaxis_title='X (ft)',
        yaxis_title='Y (ft)',
        zaxis_title='Height (ft)',
        aspectratio=dict(x=1, y=1, z=0.4)
    ),
    margin=dict(l=0, r=0, b=0, t=30)
)

st.plotly_chart(fig, use_container_width=True)
