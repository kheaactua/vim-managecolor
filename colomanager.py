#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import os
import sys
import argparse

sys.path.append(os.path.abspath('lib'))
import cmds as cololib


def main():
    """ User CLI interface to colour scheme lib """

    dotfiles_location = os.path.expanduser('~') + '/dotfiles'
    default_bundles_location = dotfiles_location + '/bundles/dein/repos'

    parser = argparse.ArgumentParser(
        description='Build a cache of available colours schemes, output them into a JSON file for vim plugins to read'
    )

    parser.add_argument('-n', '--dryrun',
        action='store_true',
        dest='dryrun',
        required=False,
        help='Dryrun mode (do not write to cache file)'
    )

    parser.add_argument('-v', '--verbose',
        action='store_true',
        dest='verbose',
        required=False,
        help='Increase verbosity'
    )

    parser.add_argument('-c', '--cache',
        action='store',
        dest='cache_file',
        required=False,
        metavar='CACHE_FILE',
        default=dotfiles_location + '/colos.json',
        help='Cache file name'
    )

    parser.add_argument(
        action='store',
        dest='command', # maybe use an action to validate the commands with their args?
        nargs=1,
        help='Command to issue: generate, whitelist <name>, blacklist <name>, toggle-variant <name>'
    )

    parser.add_argument(
        dest='args',
        nargs='*'
    )

    try:
        args = parser.parse_args()
    except ValueError as e:
        print('Invalid options.', e, file=sys.stderr)
        sys.exit(1)


    data = cololib.cmd_load_data(args.cache_file, verbose=args.verbose)

    if 'build_cache' == args.command[0]:
        cololib.cmd_build_cache(
            # data=args.cache_file,
            data=data,
            search_path=default_bundles_location,
            verbose=args.verbose, dryrun=args.dryrun
        )
    elif 'get_random' == args.command[0]:
        if args.args:
            tag = args.args[0]
        else:
            tag = None
        cololib.cmd_get_random_colo(data=data, tag=tag, verbose=args.verbose)
    else:
        print('Unknown command "%s"'%(args.command[0]), file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()

# vim:set expandtab sw=4 ts=4 sts=0 ffs=unix :
