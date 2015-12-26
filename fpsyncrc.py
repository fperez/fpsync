"""Configuration file for the laptop-update.py script.  This file should be
named either ~/.laptop-updaterc.py or ~/usr/etc/laptop-updaterc.py to be found
by default.  Otherwise its location must be given at runtime as the -config
option.

Some file/directory which must exist for the script to run at all.  Useful to
prevent it from running if some NFS mount is missing, for example."""

def fexists(arg):
    """Expand ~ and $ variables in a string and find if it's an existing file"""

    import os

    return os.path.exists(os.path.expanduser(os.path.expandvars(arg)))

# Otherwise, we default to an ssh channel.  The trailing dot is there to
# give properly assembled paths starting at $HOME if / is added

server_home = 'SERVER:.'  # BIDS
excludes = '~/usr/etc/fpsyncrc.excludes'


MUST_EXIST  = '~/.ssh'

"""
List of things to update.  It is made of dicts:

dict(dir1 = '~',
     dir2 = '~/foo',
     to_update = ('bar','baz'),
     exclude_from = None,
     )

- dir1/2 are the directories to update.

- to_update is a tuple of files and
 directories which must exist in both dir1 and dir2.  They are updated from
 one to the other based on the selected mode: 'up': 1->2, 'down': 2->1.

 Note that the entries in to_update CAN NOT have subdirectories in them. If
 you put A/B in your list, B/ will end up at the top level 'dir2' target.  For
 updating a directory which lives in dir1/A/B to dir2/A/B, make another entry
 in the TO_UPDATE list with only one level.

- exclude_from: if not None, it must be the name of a file with exclusions
 to be passed to rsync.

 WARNING: because of the semantics of rsync, the files and directories listed
 must NEVER end in '/'.  """

home = dict(dir1 = '~',
            dir2 = server_home,

            to_update = """
            .bash_profile .bashrc 
            .emacs .emacs.conf.d .fonts
            .gitconfig .gitignore .gitk  .hgrc .hgignore
            .profile .pycheckrc .pypirc .pythonstartup.py .Rprofile
            .sig .starcluster-completion.sh .ssh .tmux.conf
            Desktop Documents Pictures
            """.split(),
            exclude_from = excludes,
            )

import platform as p
if p.platform().startswith('Linux'):
    home['to_update'].append('R')

    
config = dict(dir1 = '~/.config',
              dir2 = server_home + '/.config',
              to_update = ['mc'],
              exclude_from = excludes,
              )

# Create the list of configs to use in the update process
TO_UPDATE = [config, home]
