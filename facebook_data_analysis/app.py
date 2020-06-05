import dash
import dash_core_components as dcc
import dash_html_components as html
from facebook_data_analysis.app_components import home_tab
from facebook_data_analysis.app_components.conv_detail_tab import (
    component as conv_detail_tab,
)
from facebook_data_analysis.app_components.friend_detail_tab import (
    component as friend_detail_tab,
)
from facebook_data_analysis.app_components.overview_tab import component as overview_tab

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]


app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(
    children=[
        html.H1(children="Facebook Data Analysis"),
        dcc.Tabs(
            children=[
                home_tab.attach(app),
                overview_tab.attach(app),
                friend_detail_tab.attach(app),
                conv_detail_tab.attach(app),
            ]
        ),
    ]
)


if __name__ == "__main__":
    app.run_server(debug=True)
