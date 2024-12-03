import plotly.graph_objects as go
import numpy as np



def draw_spot_simulation(spot: list[np.array], T: int):
    spot_fig = go.Figure()
    n = len(spot[0])
    t = np.linspace(0, T, n)
    for i in range(len(spot)):
        spot_fig.add_trace(
            go.Scatter(
                x=t,
                y=spot[i],
                name=f"simulation {i + 1}"
            )
        )
    spot_fig.update_layout(template="plotly_white")
    return spot_fig
