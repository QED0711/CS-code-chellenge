import pandas as pd
import plotly
import plotly.graph_objects as go


def map_feature(
    df, 
    state_count_df, 
    feature_ranges, 
    feature, 
    colorscale="YlGn", 
    reversescale=False, 
    save=False
    ):
    """
    Given a set of dfs, features ranges, and a specified feature, plots a heatmap of the US for the given feature.
    """
    for company in df.building_name.unique():

        current_df = df[df.building_name == company]
        current_df = current_df.groupby(['state']).mean().reset_index()
        
        current_state_count = state_count_df[state_count_df.building_name == company][['state', 'total_in_state']]
        current_df = current_df.merge(current_state_count, on=['state'])

        current_df['text'] = f"({feature_ranges[feature]['title']})"

        fig = go.Figure(data=go.Choropleth(
            locations=current_df['state'],
            z=current_df[feature],
            zmin=feature_ranges[feature]['crange'][0],
            zmax=feature_ranges[feature]['crange'][1],
            locationmode='USA-states',  
            text=current_df.text,
            colorscale=colorscale,
            marker_line_color='white',
            reversescale=reversescale,  
            colorbar=dict(
                tickmode='array',
                tickvals=list(range(*feature_ranges[feature]['crange'])),
                ticks='outside',
                thickness=5,
                len=0.75,
                x=0,
                xpad=0,
            ),
        ))

        fig.update_layout(
            # title_text=f"{company.title()}: {feature_ranges[feature]['title']}",
            geo_scope='usa'
        )
        
        if save:
            # fig.show(renderer='iframe')
            plotly.io.write_html(fig, f"../visuals/{company.replace(' ', '_')}-{feature}-map.html", include_plotlyjs='cdn')
        else:
            fig.show()