import pyproj 
import csv
import math
import shapely
import pandas as pd

from core import maptools
from core.config import AppConfig
'''
nw_corner = input("NW corner coordinates (long,lat): ")
print("NW corner = " + str(nw_corner))
nw_corner = shapely.geometry.Point(nw_corner)

se_corner = input("SE corner coordinates (long,lat): ")
print("SE corner = " + str(se_corner))
se_corner = shapely.geometry.Point(se_corner)

step_size = input("Step size in meters: ")
print("Step size  = " + str(step_size))
'''

app_config = AppConfig()
google_api_key = app_config.get('google_api.api_key')
print(google_api_key)

sw_corner = shapely.geometry.Point(-87.8, 41.88)
ne_corner = shapely.geometry.Point(-87.73, 41.97)
step_size = 1000

maptools.grid_write_csv(sw_corner, ne_corner, step_size)

grid_path = app_config.get('output_relative_path.grid')
score_out = pd.read_csv(grid_path)

schools_path = app_config.get('data_sources.schools.relative_path')
schools = pd.read_csv(schools_path)

pre_path = app_config.get('data_sources.day_care.relative_path')
day_cares = pd.read_csv(pre_path)

score_out['has_school'] = [False]*score_out.shape[0]
score_out['has_day_care'] = [False]*score_out.shape[0]

for i_score, score_row in score_out.iterrows():
    grid_long, grid_lat = score_row[['long','lat']]
    print('Searching school around longitude, latitude'
    '{0},{1}'.format(grid_long, grid_lat))
    for i_school, school in schools.iterrows():
        school_long, school_lat, school_name = school[['LONCOD09','LATCOD09', 'SCHNAM09']]
        if score_out.get_value(i_score,'has_school') == False:
            is_in_radius = maptools.range_test(grid_long,
                    grid_lat, school_long, school_lat, 1000)
            if is_in_radius == True:
                score_out.set_value(i_score, 'has_school', True)
                print('School {0} within radius!'.format(school_name))
                break 
    for i_day_care, day_care in day_cares.iterrows():
        day_care_long, day_care_lat, day_care_name = day_care[['longitude','latitude', 'name']]
        if score_out.get_value(i_score,'has_day_care') == False:
            is_in_radius = maptools.range_test(grid_long,
                    grid_lat, day_care_long, day_care_lat, 1000)
            if is_in_radius == True:
                score_out.set_value(i_score, 'has_day_care', True)
                print('Day care {0} within radius!'.format(day_care_name))
                break 
score_out.to_csv(app_config.get('output_relative_path.score'))
