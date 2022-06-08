# fpsync

Simplistic rsync-based filesystem synchronization utility.

**WARNING:** While some of us use these tools every single day and have done so for nearly 20 years, they are destructive, have no error checking, can and will eat your entire home directory if misused.

## Configuration

Copy `fpsyncrc.excludes` and `fpsyncrc.py` to `~/.config/fpsyncrc`.
Customize both to your liking.

Place `fpsync` (not `fpsyncrc.py`) on your path.  Run it as follows:

```
# Send to backup drive
fpsync up
```

```
# Sync *from* backup drive
fpsync down
```

```


## Notes

There's a core rsync wrapper that does all the low-level work, `dircopy`, and it's called by two other "everyday" tools:

- `fpsync`: meant to keep a whole home directory in sync between multiple computers, listing all subdirs and files to sync and exclusion patterns.

- `syncme`: meant to sync a *single* directory (the current one) between two computers.


For convenience, I call this via a utility wrapper in bash and in most cases, a couple of shorthand aliases. Modify the below to suit your needs and put it into your .bashrc:

```
# Convenience fpsync wrapper with message, wait and timing
function hsync {
    local host=${1:-"longs"}
    local mode=${2:-"sync"}

    if [[ "$mode" == "up" ]]; then
        echo "*** Destructive upload to: $host"
    elif [[ "$mode" == "down" ]]; then
        echo "*** Destructive download from: $host"
    else
        echo "*** Two-way sync with: $host"
    fi
    echo "*** Sleeping for 2 seconds..."
    sleep 2
    time fpsync --host $host $mode

}

# Sync with longs (my server, configured in my .ssh/config file)
alias longssync-up='hsync longs up'
alias longssync-down='hsync longs down'
```
