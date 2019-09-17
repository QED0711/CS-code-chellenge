import pandas as pd

import plotly
import plotly.graph_objects as go

def make_barplots(df, features, save=False):

    for feat in features:
        fig = go.Figure(
            data=go.Bar(
                x=[x.title() for x in df.index],
                y=df[feat],
                marker_color=['#FC3D38', '#074C70', '#1892D1', '#F2625E', '#F4D00A', '#DFA025']
            )
        )

        fig.update_layout(title_text=feat.replace('_', ' ').title())

        if save:
            plotly.io.write_html(fig, f"../visuals/{feat}-bar.html")
        else:
            fig.show()
        