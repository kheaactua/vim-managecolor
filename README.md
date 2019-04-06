# vim-managecolor

Plugin to easily apply a random colour scheme to your vim session.  It functions by first producing a cache by searching through your installed plugins for all colour schemes, and then when requested, choosing a random scheme from this list.

The motivation came because I had installed a plugin that brought over 600 colour schemes, and I needed an easy way to experience with them.  Personally, the ideal use case is when you have multiple vim sessions open across many tmux session, windows, and panes, and need to be able to visually distinguish one file from another.  I also get bored of a colour scheme quickly.

This plugin allows you to add tags to different colour schemes (currently by manually editing the cache, so *TODO*).  There are two hard coded tags by default, "`whitelist`" and "`blacklist`".  The "`whitelist" tag is a list that the plugin already has a command todraw from.  The "`blacklist`" list is used to filter out random general returns.

## Installation

Add `kheaactua/vim-managecolor' to your plugin manager.  _e.g._ with dein, add:

```vim
call dein#add('kheaactua/vim-managecolor')
```

## Setup/Usage

Before using the plugin, you must build a cache of colour schemes.  This cache can be built in two ways:

### Vim

```vim
call Build_colo_cache()
```

### CLI

In the base of the plugin directory, you can use the CLI interface
```sh
python colomanager.py -c <full cache file path> build_cache
```

## Configuration

Cache file location (useful for moving it into a `dotfiles` repo or somewhere more permanent)

`g:colo_cache_file`, _e.g.:

```vim
let g:colo_cache_file  = $HOME . '/dotfiles/colos.json'
```

Plugin install directory to search for colour schemes (`color/` directories)

`g:colo_search_path`, _e.g.:

```vim
let g:colo_search_path = $HOME . '/dotfiles/bundles/dein'
```

## Default Mappings

`<Leader>wcs`: `:call Get_random_colo('whitelist')`: Load a random colour scheme from the "`whitelist`" cache
`<Leader>rcs`: `:call Get_random_colo('whitelist')`: Load a random (non-blacklisted) colour scheme from the entire cache.

## CLI Interface

Fundamentally this plugin is designed to simply select a random element from a
JSON file, as such the Vim code in this plugin simply interacts with a python
API which it self is simply a friendly way of reading and writing the JSON
data.

As such, a CLI interface named `colomanager.py` exists in the root of the
plugin interface which provides direct access to the python API of this plugin.  You can see the available commands by issueing a `--help`, _e.g._

```sh
python colomanager.py --help
```

## TODO

- [ ] Command to tag current whitespace and write to the cache
- [ ] Implement log of recently used colour schemes


## License

Copyright (c) Matthew Russell.  Distributed under the same terms as Vim itself.
