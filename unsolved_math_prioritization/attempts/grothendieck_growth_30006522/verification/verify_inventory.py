"""Fail closed: classify entire tree before opening any payload; exact inventory."""
import hashlib,json,os,pathlib,stat,sys

def classify(mode):
    if stat.S_ISREG(mode): return 'file'
    if stat.S_ISDIR(mode): return 'directory'
    raise ValueError('Forbidden filesystem object mode: '+oct(mode))

def inventory(root):
    root=pathlib.Path(root)
    if classify(root.lstat().st_mode)!='directory':raise ValueError('Root is not directory')
    pending=[root];files=[];dirs=[]
    while pending:
        directory=pending.pop()
        for item in sorted(os.scandir(directory),key=lambda x:x.name):
            info=item.stat(follow_symlinks=False);kind=classify(info.st_mode);path=pathlib.Path(item.path)
            if kind=='directory':dirs.append(path.relative_to(root).as_posix());pending.append(path)
            else:files.append((path,info))
    result=[]
    # No payload read occurs before the whole-tree lstat classification above succeeds.
    for path,info in sorted(files):
        fd=os.open(path,os.O_RDONLY|os.O_NOFOLLOW|os.O_NONBLOCK)
        with os.fdopen(fd,'rb') as f:
            now=os.fstat(f.fileno())
            if not stat.S_ISREG(now.st_mode) or (now.st_dev,now.st_ino,now.st_size,now.st_mtime_ns)!=(info.st_dev,info.st_ino,info.st_size,info.st_mtime_ns):raise ValueError('Object changed before read')
            data=f.read()
            after=os.fstat(f.fileno())
            if (after.st_size,after.st_mtime_ns)!=(now.st_size,now.st_mtime_ns):raise ValueError('Object changed during read')
        result.append({'path':path.relative_to(root).as_posix(),'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()})
    return {'directories':sorted(dirs),'files':result}

def main():
    if len(sys.argv)!=3:raise SystemExit('Usage: verify_inventory.py PACKAGE EXTERNAL_RECEIPT')
    observed=inventory(sys.argv[1]);receipt=json.loads(pathlib.Path(sys.argv[2]).read_text())
    if observed!=receipt['inventory']:raise SystemExit('FAIL: inventory differs')
    print('PASS: exact recursive inventory, bytes and hashes')
if __name__=='__main__':main()
