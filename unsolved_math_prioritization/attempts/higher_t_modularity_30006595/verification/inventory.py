"""Fail-closed inventory. Inspect the complete tree before reading any file bytes.
No symlink traversal, special-file reads, or socket creation. Uses descriptor-relative
O_NOFOLLOW opens and identity checks to fail closed if an entry changes during scan.
"""
import hashlib,json,os,stat,sys

def kind(mode):
    if stat.S_ISDIR(mode): return 'directory'
    if stat.S_ISREG(mode): return 'file'
    raise ValueError('Rejected symlink or special file')

def snapshot(root):
    records={}
    def scan(fd,prefix):
        for name in sorted(os.listdir(fd)):
            rel=prefix+name
            s=os.stat(name,dir_fd=fd,follow_symlinks=False)
            k=kind(s.st_mode)
            records[rel]=(k,s.st_dev,s.st_ino,s.st_size,s.st_mtime_ns)
            if k=='directory':
                child=os.open(name,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW,dir_fd=fd)
                try:
                    t=os.fstat(child)
                    if (t.st_dev,t.st_ino)!=(s.st_dev,s.st_ino): raise ValueError('Directory changed')
                    scan(child,rel+'/')
                finally: os.close(child)
    rootfd=os.open(root,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW)
    try:
        scan(rootfd,'') # Entire recursive type census precedes first content read.
        result={}
        for rel,(k,dev,ino,size,mtime) in records.items():
            if k=='directory':
                result[rel]={'type':k};continue
            parent=os.dup(rootfd)
            try:
                parts=rel.split('/')
                for part in parts[:-1]:
                    child=os.open(part,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW,dir_fd=parent)
                    os.close(parent);parent=child
                fd=os.open(parts[-1],os.O_RDONLY|os.O_NOFOLLOW|os.O_NONBLOCK,dir_fd=parent)
                try:
                    s=os.fstat(fd)
                    if kind(s.st_mode)!='file' or (s.st_dev,s.st_ino,s.st_size,s.st_mtime_ns)!=(dev,ino,size,mtime): raise ValueError('File changed before read')
                    h=hashlib.sha256();total=0
                    while True:
                        chunk=os.read(fd,1048576)
                        if not chunk:break
                        h.update(chunk);total+=len(chunk)
                    t=os.fstat(fd)
                    if (t.st_size,t.st_mtime_ns)!=(size,mtime) or total!=size: raise ValueError('File changed during read')
                    result[rel]={'type':'file','bytes':total,'sha256':h.hexdigest()}
                finally:os.close(fd)
            finally:os.close(parent)
        # Recheck structural census so additions/removals are not silently accepted.
        before=dict(records);records.clear();scan(rootfd,'')
        if before!=records:raise ValueError('Tree changed during inventory')
        return result
    finally:os.close(rootfd)

def verify(root,receipt):
    expected=json.loads(open(receipt).read())['inventory']
    actual=snapshot(root)
    if actual!=expected:raise ValueError('Frozen inventory mismatch')
    return {'status':'PASS','entries':len(actual),'files':sum(v['type']=='file' for v in actual.values())}
if __name__=='__main__':
    print(json.dumps(verify(sys.argv[1],sys.argv[2]),indent=2))
