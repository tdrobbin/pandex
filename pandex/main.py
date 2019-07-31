import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import dash_table

from datetime import datetime as dt
import pandas as pd
import numpy as np

from dataclasses import dataclass
import uuid

import plotly.express as px

from copy import copy


def _get_default_layout():
    return dict(
        autosize=True,
        height=500,
        # margin=dict(l=35, r=35, b=35, t=45),
        margin=dict(l=35, r=35, b=35, t=20),
        hovermode="closest",
        legend_orientation='v')


def _convert_col_count_to_html_class(col_count):
    num2words1 = {1: 'One', 2: 'Two', 3: 'Three', 4: 'Four', 5: 'Five', \
        6: 'Six', 7: 'Seven', 8: 'Eight', 9: 'Nine', 10: 'Ten', \
        11: 'Eleven', 12: 'Twelve'}

    html_col_count = num2words1[col_count].lower() + ' columns'

    return html_col_count


def make_px_tidy_df(df):
    df = df.copy()
    df.rename(columns=str, inplace=1)

    value_vars = df.columns.copy()
    df['index'] = df.index

    df2 = pd.melt(df, value_vars=value_vars, id_vars='index')

    # px.line(df2, x='index', y='value', color='variable')
    return df2


def make_return_px_tidy_df(func):
    def new_func(**kwargs):
        df = func(**kwargs)
        px_tidy_df = make_px_tidy_df(df)

        return px_tidy_df

    return new_func


def section(title):
    return html.H4(title, style={'text-align':'center', 'margin-top': '50px', 'margin-bottom': '0px'})


class PXChart(object):
    def __init__(
            self,
            chart_type,
            title,
            pd_obj,
            pd_obj_kwargs=None,
            id=None,
            layout=None,
            html_col_count=None,
            style=None,
            class_str=None,
            decimal_places=2,
            **kwargs):
        self.chart_type = chart_type
        self.title = title
        self.pd_obj = pd_obj
        self.pd_obj_kwargs = {} if pd_obj_kwargs is None else pd_obj_kwargs
        self.title = title
        self.html_col_count = html_col_count
        self.id = str(uuid.uuid1()) if id is None else id
        self.layout = {} if layout is None else layout
        self.style = {} if style is None else style
        self.class_str = '' if class_str is None else class_str
        self.class_str += ' element-pandex'
        self.kwargs = kwargs
        self.decimal_places = decimal_places

        self.pd_func = None if isinstance(pd_obj,
                                          (pd.DataFrame,
                                           pd.Series)) else copy(pd_obj)

    def _handle_pd_obj(self):
        if self.pd_func is not None:
            self.pd_obj = self.pd_func(**self.pd_obj_kwargs)

        self.pd_obj = self.pd_obj.round(self.decimal_places)

        if isinstance(self.pd_obj, pd.Series):
            sr_name = self.pd_obj.name
            self.pd_obj = pd.DataFrame({self.title: self.pd_obj})

            if sr_name is not None:
                self.pd_obj.columns = [sr_name]


    def get_figure(self, lgend_meta_labels=True, axis_labels=True):
        self._handle_pd_obj()

        px_func = getattr(px, self.chart_type)
        fig = px_func(self.pd_obj, **self.kwargs)

        fig.update_layout(**_get_default_layout())
        fig.update_layout(**self.layout)

        if not axis_labels:        
            fig.layout.xaxis.title = None
            fig.layout.yaxis.title = None

        if not lgend_meta_labels:       
            # https://github.com/plotly/plotly_express/issues/36
            fig.for_each_trace(lambda t: t.update(name=t.name.split('=')[1]))

        dcc_graph = dcc.Graph(id=self.id, figure=fig.to_dict())

        return html.Div(
            [html.H6(self.title, style={'text-align': 'center', 'margin-bottom' :'-.25rem'}), dcc_graph],
            className=_convert_col_count_to_html_class(self.html_col_count) + ' ' + self.class_str,
            style=self.style
        )

class PXTable(PXChart):
    def get_figure(self):
        self._handle_pd_obj()

        fig = dash_table.DataTable(
            columns=[{"name": i, "id": i} for i in self.pd_obj.columns],
            data=self.pd_obj.to_dict('records'),
            # style_table={'overflowX': 'scroll', 'overflowY': 'scroll', 'height': _get_default_layout()['height']},
            style_table={'height': _get_default_layout()['height']},

            # fixed_rows={ 'headers': True, 'data': 0 },
            # n_fixed_rows=1,
            **self.kwargs
        )

        return html.Div(
            [html.H6(self.title, style={'text-align': 'center', 'margin-bottom' :'-.25rem'}), fig],
            className=_convert_col_count_to_html_class(self.html_col_count) + ' ' + self.class_str,
            style=self.style
        )


class _SimpleChart(object):
    def  __init__(self, title, pd_obj, pd_obj_kwargs=None, html_col_count=None, **kwargs):
        self.title=title
        self.pd_obj = pd_obj
        self.pd_obj_kwargs = {} if pd_obj_kwargs is None else pd_obj_kwargs
        self.html_col_count = html_col_count
        self.style = {}
        self.class_str = ' element-pandex'
        self.kwargs = kwargs
        self.layout = {}

        if isinstance(pd_obj, (pd.DataFrame, pd.Series)):
            self.pd_obj =  make_px_tidy_df(pd_obj)

        else:
            self.pd_obj = make_return_px_tidy_df(pd_obj)

    def chart_type(self):
        raise NotImplementedError
    
    def _set_px_chart_kwargs(self):
        pass

    def get_figure(self):
        # raise NotImplementedError
        self._set_px_chart_kwargs()

        px_chart = PXChart(
            title=self.title,
            chart_type=self.chart_type(),
            pd_obj=self.pd_obj,
            pd_obj_kwargs=self.pd_obj_kwargs,
            html_col_count=self.html_col_count,
            x='index',
            y='value',
            color='variable',
            layout=self.layout,
            **self.kwargs
        )

        return px_chart.get_figure(lgend_meta_labels=False, axis_labels=False)


class ScatterChart(_SimpleChart):
    def chart_type(self):
        return 'scatter'


class LineChart(_SimpleChart):
    def chart_type(self):
        return 'line'


class BarChart(_SimpleChart):
    def chart_type(self):
        return 'bar'
    
    def _set_px_chart_kwargs(self):
        self.kwargs.update(barmode='group')


class Heatmap(_SimpleChart):
    def chart_type(self):
        return 'density_heatmap'


class SimpleDashboard(object):
    def __init__(self, title, charts, reload_interval='page_refresh', dark_theme=False, **dash_kwargs):
        self.title = title
        self.charts = charts
        self.reload_interval = reload_interval
        self.app = dash.Dash(__name__, **dash_kwargs)
        self.dark_theme = dark_theme

    def _convert_pandex_charts_to_dash(self):
        array_of_dash_rows = []

        for row in self.charts:
            graph_count = len(row)

            if graph_count > 4:
                raise ValueError('can only have max 4 graphs per row')

            html_col_count = int(12 / graph_count)

            charts_in_row = []
            for chart in row:
                if isinstance(chart, (PXChart, _SimpleChart)):
                    if chart.html_col_count is None:
                        chart.html_col_count = html_col_count

                        pass 
                        # style = {
                        #     # 'margin-left': '0px',
                        #     'width': str(100 / graph_count) + '%'
                        # }
                    else:
                        pass
                        # style = {
                        #     'width': str(12 / chart.html_col_count) + '%'
                        # }
                    
                    style = {}
                    chart.style.update(**style)

                    # if chart.style is None:
                    #     chart.style = style

                    if self.dark_theme:

                        if isinstance(chart, PXTable):
                            chart.kwargs.update(dict(
                                style_header={
                                    'backgroundColor': 'rgb(25, 25, 25)',
                                    'border': '1px solid #283442',
                                },
                                style_cell={
                                    'backgroundColor': 'rgb(35, 35, 35)',
                                    'color': 'white',
                                    'border': '1px solid #283442',
                                },)
                            )

                        else:
                            chart.layout.update(template='plotly_dark')

                    fig = chart.get_figure()

                else:
                    fig = chart

                charts_in_row.append(fig)

            dash_row = html.Div(charts_in_row, className='row')

            array_of_dash_rows.append(dash_row)

        return array_of_dash_rows


    def _make_layout(self):
        def get_layout():
            return html.Div(
            [
                html.H2(self.title, style={'margin-top':'60px', 'margin-bottom':'40px', 'text-align': 'center'}),
                html.Div(self._convert_pandex_charts_to_dash())
            ],
            id='main-pandex',
            className='twelve columns' + ' dark-theme' if self.dark_theme else '',
            )

        if isinstance(self.reload_interval, str):
            if self.reload_interval == 'page_refresh':
                self.app.layout = get_layout

            elif self.reload_interval == 'never':
                self.app.layout = get_layout()

        else:
            raise ValueError('not yet supported')

    def run(self, use_waitress=False, debug=False, **kwargs):
        self._make_layout()

        if debug:
            self.app.run_server(debug=True, **kwargs)

        else:
            if use_waitress:
                from waitress import serve
                serve(self.app.server, **kwargs)

            else:
                self.app.run_server(debug=False, **kwargs)

