from collections import OrderedDict

import pyproj 
import math

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

def flatten_keys(dictionary, sep='_', progress=None, base_key=''):
    """Generates a list of keys in a dictionary, using
    the separator value provided to build a path for
    nested keys.
    """
    if progress is None:
        progress = []

    for key in dictionary:
        my_key = ('%s%s%s' % (base_key, sep, key)) if base_key != '' else key
        if isinstance(dictionary[key], dict):
            flatten_keys(dictionary[key], sep, progress, my_key)
        else:
            progress.append(my_key)
    return progress

def flatten_vals(dictionary, progress=None):
    """Generates a list of values in a dictionary, hopefully
    indexed in the same order as flatten_keys!
    """
    if progress is None:
        progress = []

    for key in dictionary:
        if isinstance(dictionary[key], dict):
            flatten_vals(dictionary[key], progress)
        else:
            progress.append(dictionary[key])
    return progress

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

def order_cols(unordered_data, ordered_indexes):
    ordered_data = []
    for index in ordered_indexes:
        ordered_data.append(unordered_data[index])
    return ordered_data

def order_key_indexes(unordered_keys, ordered_keys):
    """Generates a list of integers (indexes), denoting
    the order find values matching the ordered_keys provided.

    e.g.
    unordered_keys = ['four', 'too', 'won', '5', 'six', 'tree']
    ordered_keys = ['won', 'too', 'tree', 'four']

    return [2, 1, 5, 0]
    """
    order = []
    for key in ordered_keys:
        try:
            single_index = unordered_keys.index(key)
            order.append(single_index)
        except ValueError:
            raise Exception("Missing item %s from order_key_indexes list" % key)
    return order

def flatten_ordered(data_dict, ordered_keys, sep='_'):
    """
    Flatten a dictionary by plucking the values in the
    order provided.
    """
    ordered = []
    if ordered_keys:
        for key in ordered_keys:
            ordered.append(pluck(data_dict, key, sep))
    return ordered

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
