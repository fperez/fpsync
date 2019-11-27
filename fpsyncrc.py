"""
Configuration file for the laptop-update.py script.  This file should be named
either `~/.fpsyncrc.py` or `~/usr/etc/fpsyncrc.py` to be found by default.
Otherwise its location must be given at runtime as the `--config` option.

This file will be `exec`'d by the calling script in a namespace that has the following variables defined by default:

- host
- start_dir
- excludes

These can be redefined here as desired to set up noew configurations.
"""

from os.path import join as pjoin

# Some file/directory which must exist for the script to run at all.  Useful to
# prevent it from running if some NFS mount is missing, for example.

MUST_EXIST  = '~/.ssh'

server_home = f'{host}:{start_dir}'


"""
List of things to update.  It is made of dicts:

dict(dir1 = '~',
     dir2 = '~/lw',
     to_update = ('code','research'),
     exclude_from = None,
     )

- dir1/2 are the directories to update.

- to_update is a tuple of files and
 directories which must exist in both dir1 and dir2.  They are updated from
 one to the other based on the selected mode: 'up': 1->2, 'down': 2->1.

 Note that the entries in to_update CAN NOT have subdirectories in them. If you
 put A/B in your list, B/ will end up at the top level 'dir2' target.  For
 updating a directory which lives in dir1/A/B to dir2/A/B, make another entry
 in the TO_UPDATE list with only one level.

- exclude_from: if not None, it must be the name of a file with exclusions
 to be passed to rsync.

 WARNING: because of the semantics of rsync, the files and directories listed
 must NEVER end in '/'.
"""

# Main home directory sync, broken up  into several blocks, as I'm getting weird
# failures that could be caused by the main one having become too large

base = {
    'dir1': '~',
    'dir2': server_home,
    'exclude_from': excludes
}

home = {
    **base,
    'to_update': """
        .bash_profile .bashrc .bashrc_virtualenv
        .bash_utils .bash_virtualenv_utils .bash_git_completion
        .emacs .emacs.conf.d .fonts
        .gitconfig .gitignore .gitk  .hgrc .hgignore
        .ipython .inputrc .ispell_english .ispell_spanish
        .jed .less .lesskey .lyx
        .mrconfig .nose.cfg .noserc
        .profile .pycheckrc .pypirc .pythonstartup.py .Rprofile
        .sig .starcluster-completion.sh .ssh .tmux.conf
        Desktop Documents Pictures""".split()
}

import platform as p
if p.platform().startswith('Linux'):
    home['to_update'].append('R')

dirs = """dev ipython jupyter misc prof ref research scratch
          talks teach texmf usr www
          """.split()

other_homedirs = [{**base, 'to_update': [d]} for d in dirs]

# .config directory
config = {
    'dir1': pjoin('~', '.config'),
    'dir2': pjoin(server_home, '.config'),
    'to_update' = ['mc', 'flake8'],
    'exclude_from' = excludes
}

# First-level subdirs of ~/Library
lib_path = 'Library'
library = {
    'dir1': pjoin('~', lib_path),
    'dir2': pjoin(server_home, lib_path),
    'to_update': ['Jupyter'],
    'exclude_from': excludes
}

# Create the list of configs to use in the update process
TO_UPDATE = [
    config,
    library,
    home
] + other_homedirs
