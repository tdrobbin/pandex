from pandex import *
import pandas as pd
import numpy as np
import plotly_express as px


def rand_df(rows=5, cols=3, cumsum=True):
    if cumsum == 'False':
        return pd.DataFrame(np.random.randn(rows, cols))

    return pd.DataFrame(np.random.randn(rows, cols)).cumsum()


# decorator from pande to make rand_df return a tidy/normalized dataframe
rand_df_tidy = make_return_px_tidy_df(rand_df)


dbaord = SimpleDashboard(
    title='Example Pandex Dashboard',
    dark_theme=True,
    charts=[
        [
            section('SimpleChart Interface')
        ],
        [
            LineChart('Line', rand_df, {'rows': 200}), 
            BarChart('Bar', rand_df),
            ScatterChart('Scatter', rand_df, {'rows': 20, 'cumsum': False})
        ],
        [
            BarChart('4 Columns', rand_df, {'cols':1}, html_col_count=4),
            AreaChart('2 Columns', rand_df, {'rows': 200}, html_col_count=8)
        ],
        [
            section('PXChart Interface')
        ],
        [
            PXChart(title='Global Population', chart_type='area', pd_obj=px.data.gapminder, x="year", y="pop", color="continent", line_group="country"),
            PXChart(title='Iris Heatmap', chart_type='density_heatmap', pd_obj=px.data.iris, x="sepal_width", y="sepal_length")
        ],
        [
            PXChart(title='Scatter', chart_type='scatter', pd_obj=px.data.iris, x="sepal_width", y="sepal_length"),            
            PXChart(title='Scatter With Categories', chart_type='scatter', pd_obj=px.data.iris, x="sepal_width", y="sepal_length", color="species"),
            PXChart(title='Scatter Marginal', chart_type='scatter', pd_obj=px.data.iris, x="sepal_width", y="sepal_length", color="species", marginal_y="rug", marginal_x="histogram"),
        ],
        [
            PXChart(title='Horizontal Legend', chart_type='line', pd_obj=rand_df_tidy, pd_obj_kwargs=dict(rows=300, cumsum=True), x='index', y='value', color='variable',  layout=dict(legend_orientation='h')),
            PXTable(title='Table', chart_type=None, pd_obj=px.data.iris),
        ],
    ]
)

if __name__ == '__main__':
    dbaord.run(debug=True, port=8055)