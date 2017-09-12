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

def range_test(long1, lat1, long2, lat2, radius):
    # Tests if two coordinates are within a radius (in m) of each other
    x1,y1 = pyproj.transform(proj_longlat, proj_metric, long1, lat1)
    x2,y2 = pyproj.transform(proj_longlat, proj_metric, long2, lat2)
    distance = math.sqrt((x2-x1)**2+(y2-y1)**2)
    if distance <= radius:
        return True
        print('School distance: {0}'.format(distance))
    else:
        return False

with open('data/csv-out/score-out.csv', 'rwb') as grid_open:
    grid = csv.DictReader(grid_open)
    for grid_longlat in grid:
        print('Searching school around: {0}'.format(grid_longlat))
        with open('data/csv-source/schools-IL.csv', 'r') as schools_open:
            schools_il = csv.DictReader(schools_open)
            print('Opened Schools CSV')
            for school_longlat in schools_il:
                is_in_radius = range_test(grid_longlat['long'],
                grid_longlat['lat'], school_longlat['LONCOD09'],
                school_longlat['LATCOD09'],1000)
                if is_in_radius == True:
                    print('School {0} within '
                    'radius!'.format(school_longlat['SCHNAM09']))
                   


    
