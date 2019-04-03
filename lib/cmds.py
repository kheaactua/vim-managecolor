#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import os
import glob
import re
import sys
import json
import random
import itertools

def _find_all_color_dirs(base):
    """ Find all the paths containing a 'color' directory """
    results = itertools.chain.from_iterable(glob.iglob(os.path.join(root, 'colors')) for root, dirs, files in os.walk(base))

    return list(results)

# TODO maybe replace with a dict?
class ColorScheme:
    def __init__(self, name='', path='', variants=[], defaultVariant=None, tags=[]):
        self.name = name

        # Relative to dotfiles!
        self.path = path

        self.variants = variants
        self.defaultVariant = defaultVariant

        # Tags such as 'whitelist', 'blacklist', etc, anything
        self.tags = list(set(tags))

class CSData:
    """ Basically the data structure we're going to read in and out of JSON """

    def __init__(self, path, colorSchemes = [], caches={'all': [], 'whitelist': [], 'blacklist': []}):
        self.path = path
        self.colorSchemes = colorSchemes
        self.caches        = caches

    def has(self, name):
        """ Check if we have a colourscheme by 'name' """
        return any(s.name == name for s in self.colorSchemes)

    def find(self, name):
        """ Check if we have a colourscheme by 'name' """
        for idx, s in enumerate(self.colorSchemes):
            if s.name == name:
                return idx

        return -1

    @staticmethod
    def load(path, verbose=False):
        """ Load in a cache file """
        if verbose:
            print('Attempting to load %s'%path)
        with open(path, 'r') as f: obj = json.load(f, object_hook=CSData.dict_to_obj)

        return obj

    def write(self):
        """ Output this structure to JSON """

        # Create the directory if it doesn't exist
        if not os.path.exists(os.path.dirname(self.path)):
            os.makedirs(os.path.dirname(self.path))

        with open(self.path, 'w') as outp:
            json.dump(self, outp, default=CSData.convert_to_dict, sort_keys=True, indent=2, separators=(',', ': '))

    def __str__(self):
        return json.dumps(self, sort_keys=True, default=CSData.convert_to_dict, indent=2, separators=(',', ': '))

    @staticmethod
    def convert_to_dict(obj):
        """
        A function takes in a custom object and returns a dictionary representation of the object.
        This dict representation includes meta data such as the object's module and class names.
        """

        #  Populate the dictionary with object meta data
        obj_dict = {
            "__class__": obj.__class__.__name__,
            "__module__": obj.__module__
        }

        #  Populate the dictionary with object properties
        obj_dict.update(obj.__dict__)

        return obj_dict

    @staticmethod
    def dict_to_obj(our_dict):
        """
        Function that takes in a dict and returns a custom object associated with the dict.
        This function makes use of the "__module__" and "__class__" metadata in the dictionary
        to know which object type to create.
        """
        if "__class__" in our_dict:
            # Pop ensures we remove metadata from the dict to leave only the instance arguments
            class_name = our_dict.pop("__class__")

            # Get the module name from the dict and import it
            module_name = our_dict.pop("__module__")

            # We use the built in __import__ function since the module name is not yet known at runtime
            module = __import__(module_name)

            # Get the class from the module
            class_ = getattr(module, class_name)

            # Use dictionary unpacking to initialize the object
            obj = class_(**our_dict)
        else:
            obj = our_dict
        return obj

def cmd_build_cache(data, search_path, verbose=True, dryrun=False):
    """ Build a new cache file, maintaining the data that's already in it though if any exists """

    paths = _find_all_color_dirs(search_path)

    def path_to_scheme(path):
        """ Convert the file name to a colour scheme name """
        path = path.strip()
        path = re.sub('\.vim$', '', os.path.basename(path))
        return path

    # Collect all the files in the paths
    if verbose:
        print('Searching %s for colour schemes'%search_path)
    for p in paths:
        for (dirpath, dirnames, filenames) in os.walk(p):
            for filename in filenames:
                name = path_to_scheme(filename)
                rel_dir = dirpath.replace(search_path, '')
                rel_dir = re.sub(r'^(\\|/)?', '', rel_dir)
                if data.has(name=name):
                    idx = data.find(name=name)
                    if data.colorSchemes[idx].path != rel_dir:
                        data.colorSchemes[idx].path = rel_dir
                else:
                    data.colorSchemes.append(ColorScheme(
                        name=name,
                        path=rel_dir,
                    ))

    # Build cache
    all_tags = set()
    for s in data.colorSchemes:
        for t in s.tags:
            all_tags.add(t)
        if s.name not in data.caches['all']:
            data.caches['all'].append(s.name)

    # Make unique
    data.caches['all'] = list(set(data.caches['all']))

    for t in all_tags:
        if t not in data.caches:
            data.caches[t] = []
        for s in data.colorSchemes:
            # Add to our tag caches if it's missing
            if t in s.tags and s.name not in data.caches[t]:
                data.caches[t].append(s.name)

        # Remove from our cache lists if it no longer exists
        for s_name in data.caches[t]:
            if not data.has(s_name):
                data.caches[t].remove(s)

    _write_output(data, verbose=verbose, dryrun=dryrun)

def _loadCSData(path, verbose=False):
    """ Attempt to load cache file """
    if os.path.exists(path):
        try:
            if verbose:
                print("Loading %s"%os.path.abspath(path))
            data = CSData.load(path, verbose)
        except ValueError as e:
            print('Could not load cached file "%s"'%path, e, file=sys.stderr)
            sys.exit(1)

    else:
        if verbose:
            print("%s doesn't exist, loading new colour scheme data"%path)
        data = CSData(path=path)

    return data

def cmd_load_data(cache_file_path, verbose=False):
    """ Public function to load colour scheme cache file """
    return _loadCSData(cache_file_path, verbose=verbose)

def cmd_get_random_colo(data, tag=None, verbose=False):
    """ Randomely select a colour scheme """
    if not tag:
        tag = 'all'

    if tag not in data.caches:
        print('No such tag', file=sys.stderr)
        print('default')
        return
    if not data.caches[tag]:
        print('Tag %s is empty'%tag, file=sys.stderr)
        print('default')
        return
    print(random.choice(data.caches[tag]))

def _write_output(data, verbose=False, dryrun=False):
    """ Little helper function to output if dryrun and verbose are right """
    if not dryrun:
         data.write()
    else:
        if verbose:
            print(data)

# vim:set expandtab sw=4 ts=4 sts=0 ffs=unix :
