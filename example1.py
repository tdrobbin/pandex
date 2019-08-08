from pandex import *
import pandas as pd
import numpy as np
import plotly_express as px
import dash_core_components as dcc


def rand_df(rows=5, cols=3, cumsum=True):
    if cumsum == 'False':
        return pd.DataFrame(np.random.randn(rows, cols))

    return pd.DataFrame(np.random.randn(rows, cols)).cumsum()


dbaord = SimpleDashboard(
    title='Example Pandex Dashboard',
    charts=[
        [
            BarChart('Bar', rand_df), LineChart('Line', rand_df, {'rows': 200})
        ],
        [
            ScatterChart('Scatter', rand_df, {'rows': 20, 'cumsum': False})
        ],
    ]
)


if __name__ == '__main__':
    dbaord.run(debug=True, port=8055)