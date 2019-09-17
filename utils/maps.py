import pandas as pandas

import plotly.graph_objects as go


def map_feature(df, state_count_df, feature_ranges, feature, save=False):
    for company in df.building_name.unique():

        current_df = df[df.building_name == company]
        current_df = current_df.groupby(['state']).mean().reset_index()
        
        current_state_count = state_count_df[state_count_df.building_name == company][['state', 'total_in_state']]
        current_df = current_df.merge(current_state_count, on=['state'])

        fig = go.Figure(data=go.Choropleth(
            locations=current_df['state'],
            z=current_df[feature],
            zmin=feature_ranges[feature]['crange'][0],
            zmax=feature_ranges[feature]['crange'][1],
            locationmode='USA-states',         
            colorbar=dict(
                tickmode='array',
                tickvals=list(range(*feature_ranges[feature]['crange'])),
                ticks='outside',
            ),
        ))

        fig.update_layout(
            title_text=f"{company.title()}: {feature_ranges[feature]['title']}",
            geo_scope='usa'
        )
        
        if save:
            fig.show(renderer='iframe')
        else:
            fig.show()