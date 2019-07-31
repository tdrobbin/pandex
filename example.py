from pandex import *
import pandas as pd
import numpy as np
import plotly_express as px


def rand_df(rows=5, cols=3, cumsum=False):
    if cumsum == 'False':
        return pd.DataFrame(np.random.randn(rows, cols))

    df = pd.DataFrame(np.random.randn(rows, cols)).cumsum()
    # return df
    return make_px_tidy_df(df)


dbaord = SimpleDashboard(
    title='Pandex Dashboard',
    # dark_theme=True,
    charts=[
        [
            section('PXChart Interface')
        ],
        [
            PXChart(title='gapminder', chart_type='area', pd_obj=px.data.gapminder, x="year", y="pop", color="continent", line_group="country"),
            PXChart(title='Iris Heatmap', chart_type='density_heatmap', pd_obj=px.data.iris, x="sepal_width", y="sepal_length")
        ],
        [
            PXChart(title='Scatter', chart_type='scatter', pd_obj=px.data.iris, x="sepal_width", y="sepal_length", color="species", layout=dict(legend_orientation='h')),
            PXChart(title='Scatter No Color', chart_type='scatter', pd_obj=px.data.iris, x="sepal_width", y="sepal_length"),
            PXChart(title='Scatter Marginal', chart_type='scatter', pd_obj=px.data.iris, x="sepal_width", y="sepal_length", color="species", marginal_y="rug", marginal_x="histogram"),
        ],
        [
            PXChart(title='Cumulative Return', chart_type='line', pd_obj=rand_df, pd_obj_kwargs=dict(rows=300, cumsum=True), x='index', y='value', color='variable')
        ],
        [
            section('SimpleChart Interface')
        ],
        [
            PXChart(title='Cumulative Return 2', chart_type='line', pd_obj=rand_df, pd_obj_kwargs=dict(rows=300, cumsum=True), x='index', y='value', color='variable'),
            PXTable(title='Table', chart_type=None, pd_obj=px.data.iris)
        ],
    ]
)

dbaord.run(debug=True)