

Todo:
-implement a redis connection for session management after the program closes
-rewrite the interface to use direct vboxapi calls instead of running commands 
-seperate boot entry in configuration from disk so that machines that have an explicit list can also boot from iso.
-implement a gracefull exit on cases that machines are up and error occurs. for example during setup if disk configuration of one of the machines is wrong, the already started machines will remain started.
-convert all paths given in config file to absoloute paths.
-add copy_disk flag in configuration to allow disk file copying and multiple machines using the same starting disk.
-implement functionallity so that if one machine is down the up command just brings up that one
-cloning functionallity so cluster nodes can be defined once and then cloned