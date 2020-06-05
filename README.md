# facebook_data_analysis

## Installation
Using python 3.7+ (3.6 should work)

`make install`

## Running the script
### Get your Facebook data
Go to https://www.facebook.com/dyi to request a copy of your data.
It should be available for download within a few hours.

### Run the script
From the root of the repo

Fro the app with a front:
```python -m facebook_data_analysis.app'```

For the (deprecated) script:
```python -m facebook_data_analysis.main -f my_data_folder -n 'My Facebook Name'```

NB: a few interesting things are only generated in the script for now
(ip connections map, friends network graph)

## Contribute
### TODO:

#### Big changes
- Add temporal graphs (activity over time) to the app
- Make a mosaic with the pictures, possibly organized by conversation or in chronological order
- Improve the friends network graph (make it interactive to improve readability, change the distance
computation)
- Make a plot message reacts

#### Small changes
- Add an option to cut off messages before a set date

### A few pointers
For the app, the complicated stuff mostly happens in the logic of the home tab.
At the end of the home tab flow,
the `common` module is filled with the data needed for the rest of the computations (all messages +
some aggregations by conversation)

If you want to add some graphs, you can create a new tab by taking inspiration from the
`friend_detail` module.
If you want to add a graph to an existing tab, it is even simpler:
add a graph-generator function to one of
the `graphs.py` files, and the rest will take care of itsel.

The app is built using Plotly's Dash, which uses logic based on callbacks.
It is fairly simple but may require some
 getting used to: feel free to check out the [Dash documentation](https://dash.plotly.com/)
