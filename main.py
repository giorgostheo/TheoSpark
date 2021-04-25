import threading
import paramiko
import json
import os


def sync(nickname, hostname, uname, port, tspath, files, partition, inputname):
    
    print(f'## SFTPing to {nickname} ##')
    
    rsapath = os.path.join(os.environ["HOME"], ".ssh", "id_rsa")

        # Open a transport
    transport = paramiko.Transport((hostname,port))

    # Auth    
    transport.connect(None,uname, pkey=paramiko.RSAKey.from_private_key_file(rsapath))

    # Go!    
    sftp = paramiko.SFTPClient.from_transport(transport)
    
    try:
        sftp.mkdir(tspath)
        print(f'[+] Created directory {tspath} at {nickname}')
    except:
        pass

    # Upload
    for fileattr in sftp.listdir(tspath):
        sftp.remove(tspath+fileattr)
        print(f'[-] Deleted {fileattr} from {nickname}')

    for file in files:
        
        sftp.put(file,tspath+file.split('/')[-1])
        print(f'[+] Uploaded {file} to {nickname}')

#             replace = True
#             tspath = host_dict['theosparkpath']

#             for fileattr in sftp.listdir_attr(tspath):
#         #         print(fileattr.filename)
#                 if fileattr.filename==file and fileattr.st_mtime >= os.stat(file).st_mtime:
#                     replace=False
#                     print('will not replace ', file)
#                     continue

#             if replace:
#                 print('replacing ', file)
#                 sftp.put(localpath,tspath+file)

    sftp.put(partition,tspath+inputname)
    print(f'[+] Datafile - Uploaded {partition} as {inputname} to {nickname}')

    # Close
    print('## Closing ##')
    if sftp: sftp.close()
    if transport: transport.close()


def fetch(nickname, hostname, uname, port, tspath, output):
    
    print(f'## SFTPing to {nickname} ##')
    
    rsapath = os.path.join(os.environ["HOME"], ".ssh", "id_rsa")

        # Open a transport
    transport = paramiko.Transport((hostname,port))

    # Auth    
    transport.connect(None,uname, pkey=paramiko.RSAKey.from_private_key_file(rsapath))

    # Go!    
    sftp = paramiko.SFTPClient.from_transport(transport)

    sftp.get(tspath+output, 'outputs/'+f'{nickname}_{output}')
    print(f"[+] Fetching {tspath+output} to local as {'outputs/'+f'{nickname}_{output}'}")

    # Close
    print('## Closing ##')
    if sftp: sftp.close()
    if transport: transport.close()


def run_command(nickname, hostname, uname, port, tspath, command='ls'):
    rsapath = os.path.join(os.environ["HOME"], ".ssh", "id_rsa")

    print(f'## SSHing to {nickname} ##')
    s = paramiko.SSHClient()
    s.load_system_host_keys()

    key = paramiko.RSAKey.from_private_key_file(rsapath)
    s.connect(hostname=hostname, port=port, username=uname, pkey=key)
#     command = 'ls
    print('[+] Executing command -> ',command)
    (stdin, stdout, stderr) = s.exec_command(command)
    print('[+] stdout: ',stdout.read() )
#     for line in stdout.readlines():
#         print (line)
    print('## Closing ##')
    s.close()


def pipeline(host, hd, ep, partition, files, cmd=None):

    print(hd)
# sync theospark dir
    sync(host, hd['hostname'], hd['uname'], hd['port'], hd['theosparkpath'], files, partition, ep['inputname'])

    # exec command
    if type(ep['command']) == dict:
        comm = ep['command'][host]
    else:
        comm = ep['command']

    if cmd is not None:
        comm = cmd

    run_command(host, hd['hostname'], hd['uname'], hd['port'], hd['theosparkpath'], f'cd {hd["theosparkpath"]}; {comm}')

    # fetch results
    if cmd is not None:
        return

    fetch(host, hd['hostname'], hd['uname'], hd['port'], hd['theosparkpath'], ep['output'])


exec_plan = os.environ['EP']
cmd = os.getenv('CMD', None)


# create dir if the command is the distributed one
if cmd is None:
    try:
        os.mkdir('outputs/')
    except:
        pass

# transfer syncs and script + partition
ep = json.load(open(exec_plan))
hosts = json.load(open(ep['hosts']))

threads = []
files = open(ep['sync']).read().splitlines()+[ep['script']]

partitions = os.listdir(ep['inputdir'])

if len(partitions)!=len(hosts):
    print('wrong you stupid bitch')
    sys.exit(1)

for i, host in enumerate(hosts):
    partition = ep['inputdir']+partitions[i]
    hd = hosts[host]

    #t = threading.Thread(target=pipeline, args=(host, hd, ep, partition, files, cmd))
    #t.start()
    #threads.append(t)
#for t in threads:
    #t.join()
    pipeline(host, hd, ep, partition, files, cmd=cmd)

