import json
from collections import OrderedDict

global_path = "/home/pk/src/housing_score_IL/config/global.json"
config_file = open(global_path, 'rb')
print(config_file)
#tmp_config = json.loads(config_file, 'utf-8', object_pairs_hook=OrderedDict)

tmp_config = json.load(config_file, object_pairs_hook = OrderedDict)
print(tmp_config)
