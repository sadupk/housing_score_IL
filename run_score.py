from core import maptools

import shapely.geometry
import pyproj
import csv
import math

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
nw_corner = shapely.geometry.Point(-87.8, 41.88)
se_corner = shapely.geometry.Point(-87.73, 41.97)

step_size = 5000

proj_longlat = pyproj.Proj(init = 'epsg:4326')
proj_metric = pyproj.Proj(init = 'epsg:3857')

nw_metric = pyproj.transform(proj_longlat, proj_metric, nw_corner.x, nw_corner.y)
se_metric = pyproj.transform(proj_longlat, proj_metric, se_corner.x, se_corner.y)

gridpoints = []
x = nw_metric[0]
while x < se_metric[0]:
    y = nw_metric[1]
    while y < se_metric[1]:
        point_longlat = shapely.geometry.Point(pyproj.transform(proj_metric,
        proj_longlat, x, y))
        gridpoints.append(point_longlat)
        y += step_size
    x += step_size

with open('data/csv-out/score-out.csv', 'wb') as of:
    of.write('long,lat\n')
    for p in gridpoints:
        of.write('{0:f},{1:f}\n'.format(p.x, p.y))

print('Grid Complete')


with open('data/csv-out/final-score.csv','wb') as score:
    fieldnames = ['lat', 'long', 'has_school']
    score_writer = csv.DictWriter(score, fieldnames=fieldnames)
    score_writer.writeheader()

    with open('data/csv-out/score-out.csv', 'rb') as grid_open:
        grid = csv.DictReader(grid_open)
        for grid_longlat in grid:
            print('Searching school around: {0}'.format(grid_longlat))
            school_nearby = False
            with open('data/csv-source/schools-IL.csv', 'r') as schools_open:
                schools_il = csv.DictReader(schools_open)
                print('Opened Schools CSV')
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
