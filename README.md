# facebook_data_analysis

## Installation
`make install`

## Running the script
### Get your Facebook data
Go to https://www.facebook.com/dyi to request a copy of your data.
It should be available for download within a few hours.

### Run the script
From the root of the repo

```python -m facebook_data_analysis.main -f my_data_folder -n 'My Facebook Name'```

## Contribute
### TODO:

#### Big changes
- Make a front that makes it possible to visualize all the graphs, and to have a dropdown
to choose which friend is shown in the 'single person' graph (use Dash ? It is possible to
display images directly, not just plotly graphs cf https://github.com/plotly/dash/issues/71)
- Add a 'single conversation' graph that shows activity and person
rankings for a selected conversation
- Make a mosaic with the pictures, possibly organized by conversation or in chronological order
- Improve the friends graph (make it interactive to improve readability, change the distance
computation)
- Make a plot for reacts

#### Small changes
- Post-process the names of the conversations so that they are more readable
- Add an option to cut off messages before a set date
- Improve the visuals of the graphs (possible to use Plotly, to make it look nicer and ease the
transition to dash)
