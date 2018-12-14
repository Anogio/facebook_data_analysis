import plotly.offline as py
import os

def make_map(coordinates_df):
    data = [dict(
        type='scattergeo',
        lon=coordinates_df['lon'],
        lat=coordinates_df['lat'],
        text=coordinates_df['city'] + ', ' + coordinates_df['country'],
        mode='markers',
        marker=dict(
            size=8,
            opacity=0.8,
            reversescale=True,
            autocolorscale=False,
            symbol='circle',
            line=dict(
                width=1,
                color='rgba(102, 102, 102)'
            ),
        ))]

    layout = dict(
        title='Connexion locations based on IP addresses',
        geo=dict(
            scope='world',
            projection=dict(type='winkel tripel'),
            showcountries=True,
            showland=True,
            landcolor="rgb(250, 250, 250)",
            subunitcolor="rgb(217, 217, 217)",
            countrycolor="rgb(217, 217, 217)",
        ),
    )

    fig = dict(data=data, layout=layout)
    py.plot(fig, filename=os.path.join('Output', 'ip_locations.html'))
