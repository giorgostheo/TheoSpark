![Honest Logo](logo.png)

# TheoSpark
Spark is the worst and I hate it. Let's make something better. 

# How to use

Run this first !!!!
```bash
git clone https://github.com/giorgostheo/TheoSpark.git
cd TheoSpark
pip/conda install paramiko
```

All you need is a pair of dicts. One that looks like this
```python
# hosts.json
{
    "Server1 nickname ":{
        "hostname": "ip-address",
        "uname": "username",
        "port": 22,
        "theosparkpath": "/home/"user"/.theospark/"
    },
    "Server2 nickname ":{
        "hostname": "ip-address",
        "uname": "username",
        "port": 22,
        "theosparkpath": "..path/.theospark/"
    },
    .
    .
    .
}
```
and contains all the hosts that are part of your clusters, and one that looks like this
```python
{
    "command": {
        "Server1 nickname": "python sample.py",
        "Server2 nickname": "/home/me/anaconda3/bin/python sample.py"
    },
    "script": "sample.py",
    "inputdir": "data/",
    "inputname": "data.txt",
    "output": "result.pkl",
    "hosts": "hosts.json",
    "sync": "files_to_sync.txt"
}
```
that contains all the info about your script.

Figure out the rest

--- old ---

This needes to be very simple and quick to write. Essentially, what you need is a pyfile with some computation. This pyfile reads from a file, performs some computation and then outputs a result. 

TheoSpark will do the following:

## Setup




- The user will create a file that will contain all the IPs of the slaves. This NEEDS to be VERY VERY SIMPLE because spark needs setup and i hate that with all my soul. File should be like IP-PW-PORT-UNAME (or with keys and no pw even better). 
- For every slave, check if a connection is possible and if not, stop.
- Theoretically, TheoSpark should be able to clone python envs and install-remove packages but who has time. A simple fix is to supply the desired python path for the computation at runtime (for each slave as part of the file mentioned above).
- Create a dotdir at /home/user that will be used for every computation. Maybe we keep X runs as backup, maybe we dont, i'll think about it. 

## Sync the workspaces
- Create a file that contains the filenames of all the files that will be cloned. Big files (>X MBs) will not be autocloned. The user, however, could bypass this and force the sync of a large file. Of course, if a file is identical, there will be no copying (not stupid). This sync file should NOT contain the main dataset that needs to be distributed. 
- Clone the files that are stated on the syncfile.
## Distribute data
- Determine which file is the one that needs to be distributed (who knows how, envvars?, arg? will solve when i get there). TheoSpark will support id based partitioning and prepartitioned files (a dir that contains X number of files for X machines. This I like very much because it bery simple). Range based should be supported but who cares.
- Distribute the file/s to the remote machines.
## Run code
- Run the pyfile that is specified (the one with the computation that we want to distribute). On each slave, this file will read its respective partition and output a result that will be saved as a pickle. 
## Collect
- Each slave returns its output file to the master and the script (when all the results are fetchs and all computation is finished) marges them to one object. This needs to be simple, so just throw all the results to a list/dict or smth.
## DONE NO NEED FOR SPARK LOL

So in the end, you have full control of all the moving parts of this. If you want more machines, add the IPs and youre ready. No need for DevOps and such poop. Also, you can use multiprocessing to utilize every core of each machine, or use optimised code that might be written in C for example (like cKDTree...) and have the best of every world. Fast, simple, easy to deploy.


And always remember. Spark is THE WORST.    
    
