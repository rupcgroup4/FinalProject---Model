import numpy as np
import plotly.graph_objects as go

eval = np.load('./envs/model/Logs/PPO/SpyEnv/evaluations.npz')

print(eval['results'])
print(eval['timesteps'])
print(eval['ep_lengths'])


avg = [np.average(x) for x in eval['results']]
f = go.FigureWidget()

f.add_scatter(y=avg)
f.show()


