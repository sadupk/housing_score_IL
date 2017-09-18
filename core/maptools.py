from collections import OrderedDict

import pyproj 
import math
import shapely.geometry

def grid_write_csv(nw_corner, se_corner, step_size): 
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

    with open('data/csv-out/grid.csv', 'w') as of:
        of.write('long,lat\n')
        for p in gridpoints:
            of.write('{0:f},{1:f}\n'.format(p.x, p.y))

    print('Grid Complete')
    return

def range_test(long1, lat1, long2, lat2, radius):
    """ Generates a True of False result based on a tests if two coordinates are within a radius (in m) of each other
    """
    proj_longlat = pyproj.Proj(init = 'epsg:4326')
    proj_metric = pyproj.Proj(init = 'epsg:3857')
    x1,y1 = pyproj.transform(proj_longlat, proj_metric, long1, lat1)
    x2,y2 = pyproj.transform(proj_longlat, proj_metric, long2, lat2)
    distance = math.sqrt((x2-x1)**2+(y2-y1)**2)
    if distance <= radius:
        return True
        print('School distance: {0}'.format(distance))
    else:
        return False

def merge_graceful(defaults, overrides):
    """Merge overrides dict into defaults dict
    such that overrides are "gracefully" added
    to the defaults.

    Each node will merge rather than replacing,
    preferring the override when keys collide,
    or are of different types.
    """
    for key, val in overrides.items():
        if key not in defaults:
            defaults[key] = val
        else:
            override_type = type(val)
            default_type = type(defaults[key])
            if (override_type is dict and default_type is dict) or \
                   (override_type is OrderedDict and default_type is OrderedDict):
                merge_graceful(defaults[key], val)
            else:
                defaults[key] = val


def pluck(data_dict, key, sep='.', default=None):
    try:
        parts = key.split(sep)
    except TypeError:
        parts = [key]

    cursor = data_dict
    for part in parts:
        try:
            cursor = cursor[part]
        except KeyError:
            cursor = default
            break
    return cursor
