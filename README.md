# Project made by (...names)

# How to use



# aliases
When starting .bash_aliases are automatically sourced
in .bash_aliases is a piece of code that will automatically open Destop/UltraSonicFluids where
git pull is autmatically ran

'la' is list all
'pull' automatically pulls

# aliases that still need to work
'main' pulls everything, then runs python main.py and then pushes the data to github


# Fix desyncing 
The time should be synced with the Network Time Protocol (NTP). When the time difference between 'timedatectl' and the time of the debian server pool the time will not sync. A quick fix for this is to manually set the time.

Run the following commands as root:
'timedatectl set-time YYYY-MM-DD'

'timedatectl set-time HH:MM:SS' 

