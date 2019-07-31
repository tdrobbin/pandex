# pandex
Simple Dashboarding using pandas, dash, and plotly express.

## Usage
Pass a function that returns a dataframe/series, and optional keyoword arguments, to a chart. Put these tpgether in a list of lists (row x column order) to create the dashboard layout.

Two main chart interfaces

Can use a simple chart, which takes a function that returns regular pandas dataframe/series: 
```python
 BarChart(title='Data', pd_obj=some_func, pd_obj_kwargs=some_func_kwargs)
 ``` 

Or can use a px chart which takes a function that returns a 'tidy'/normalized dataframe and has the same interface as plotly epress charts (https://www.plotly.express/plotly_express/). Pass title, chart type, func, func_kwargs, then any kwargs the plotly express function takes:
```python
PXChart(title='Global Population', chart_type='area', pd_obj=px.data.gapminder, x="year", y="pop", color="continent", line_group="country")
```


Pass a function that returns a 'tidy' (normalized) dataframe (same format that plotly express accepts) to a PXChart, along with the chart type and other keyword arguments for that plotly express chart type ().



Can use ```make_px_tidy_df``` to turn an 'untidy' (un-normalized) dataframe into a tidy one. Can also used ```make_return_tidy_df``` as a decorator to make a function return a tidy dataframe.

Optional dark theme.

## Example

```python
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
```

<!-- blank line -->
<figure class="video_container">
  <video controls="true" allowfullscreen="true">
    <source src="https://github.com/tdrobbin/pandex/blob/master/example_vid.mov" type="video/mmov">
  </video>
</figure>
<!-- blank line -->
