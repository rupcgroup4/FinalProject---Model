import numpy as np
import plotly.graph_objects as go

# eval = np.load('./envs/model/Logs/PPO/SpyEnv/spy_200k_vs_agents_50k.npz')
eval = np.load('./envs/model/Logs/PPO/AgentsEnv/agents_50k_vs_spy_50k.npz')

print(eval['results'])
print(eval['timesteps'])
print(eval['ep_lengths'])


avg = [np.average(x) for x in eval['results']]
steps = eval['timesteps']
f = go.FigureWidget()

f.add_scatter(y=avg, x=steps )

f.update_layout(
    width=800, 
    height=400,
    xaxis_title="Steps", 
    yaxis_title="Reward average", 
    title="spy_50k_vs_agents_50k",
    font=dict(
        family="Courier New, monospace",
        size=18,  # Set the font size here
        color="RebeccaPurple"
    ),
)

f.show()


