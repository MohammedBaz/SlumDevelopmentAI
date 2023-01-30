import ee

ee.Authenticate()
ee.Initialize()
dw = ee.ImageCollection('GOOGLE/DYNAMICWORLD/V1')

probability_bands = [
  'water', 'trees', 'grass', 'flooded_vegetation', 'crops',
  'shrub_and_scrub', 'built', 'bare', 'snow_and_ice',
]
palette = [
  '#419BDF', '#397D49', '#88B053', '#7A87C6', '#E49635', 
  '#DFC35A', '#C4281B', '#A59B8F', '#B39FE1'
]

start_date = '2019-04-01'
end_date = '2019-07-01'

# Filter image collections by time
dw_time_interval = dw.filter(ee.Filter.date(start_date, end_date))

# Select probability bands 
dw_time_series = dw_time_interval.select(probability_bands)

# Create a multi-band image summarizing probability 
# for each band across the time-period
mean_probability = dw_time_series.reduce(ee.Reducer.mean())

# Create a single band image containing the class with the top probability
top_probability = mean_probability.toArray().arrayArgmax().arrayGet(0).rename('label')
geometry = ee.Geometry.Polygon(
        [[[-77.26456078565367, 38.98239629898283],
          [-77.26456078565367, 38.24414499918236],
          [-76.27579125440367, 38.24414499918236],
          [-76.27579125440367, 38.98239629898283]]])

Latitude=21.0807514
Longitude= 40.2975893
PoI = ee.Geometry.Point(Longitude, Latitude)
RoI = PoI.buffer(1e4)
url = top_probability.getThumbURL({
  'region': RoI,
  'dimensions':'300',
  'min': 0,
  'max': 8,
  'palette': palette,
  'format': 'png'
})
