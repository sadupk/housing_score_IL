import pyproj
import csv
import math

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

nw_corner = shapely.geometry.Point(-87.8, 41.88)
se_corner = shapely.geometry.Point(-87.73, 41.97)

step_size = 5000

maptools.grid_write_csv(nw_corner, se_corner, step_size)

with open('data/csv-out/score-out.csv','w') as score:
    fieldnames = ['lat', 'long', 'has_school']
    score_writer = csv.DictWriter(score, fieldnames=fieldnames)
    score_writer.writeheader()

    with open('data/csv-out/grid.csv', 'r') as grid_open:
        grid = csv.DictReader(grid_open)
        for grid_longlat in grid:
            print('Searching school around: {0}'.format(grid_longlat))
            school_nearby = False
            with open('data/csv-source/schools-IL.csv', 'r') as schools_open:
                schools_il = csv.DictReader(schools_open)
                if school_nearby == False:
                    for school_longlat in schools_il:
                        is_in_radius = maptools.range_test(grid_longlat['long'],
                        grid_longlat['lat'], school_longlat['LONCOD09'],
                        school_longlat['LATCOD09'],1000)
                        if is_in_radius == True:
                            school_nearby = True
                            print('School {0} within '
                            'radius!'.format(school_longlat['SCHNAM09']))
            score_writer.writerow(dict(grid_longlat, **{'has_school': school_nearby}))                       
