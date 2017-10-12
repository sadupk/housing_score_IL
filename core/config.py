import json

from os import path
from collections import OrderedDict

import core.maptools as maptools

from core.singleton import Singleton


class AppConfig(Singleton):

    def __init__(self, args=None):
        """Attempt to load the config for the options
        supplied.

        Expects a well-named json file to exist.

        NOTE: args is required for 1st instantiation, but
        is not for further requests, as this is a
        Singleton and will simply fetch the instance.
        """
        if not self._initialized():
            project_root = path.abspath("%s/../" % path.dirname(__file__))
            self._base_path = "%s/config" % project_root

            # Loading configs merges them in order...
            # Load global, env, subenv
            self._config = { 'project_root': project_root }
            self._load_config('global')

    def get(self, path, default=None):
        """Use dot-delimited path to get config value.

        config.get('my.little.pony')
        """
        return maptools.pluck(self._config, path, '.', default)

    def _load_config(self, relative_path):
        config_path = "%s/%s.json" % (
                self._base_path,
                relative_path)

        # Let exceptions bubble up?
        config_file = open(config_path, 'r')
        tmp_config = json.load(config_file, object_pairs_hook=OrderedDict)
        config_file.close()

        maptools.merge_graceful(self._config, tmp_config)
