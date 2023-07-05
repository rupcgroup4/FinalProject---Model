import plotly.graph_objects as go

x1=['Win Spy']
x2 = ['Win Agents']
y1=[334]
y2 =[666]


fig = go.Figure()
fig.add_trace(go.Bar(x=x1, y=y1, marker_color='black',text=y1, textposition='outside'))
fig.add_trace(go.Bar(x=x2, y=y2, marker_color='blue',text=y2, textposition='outside'))


fig.update_layout(
    title='Spy vs Agents in 1000 games', 
    yaxis_title = 'Number of wins',
    width=800, 
    height=800,
    font=dict(
        family="Courier New, monospace",
        size=22,  # Set the font size here
    ),
    )

fig.show()