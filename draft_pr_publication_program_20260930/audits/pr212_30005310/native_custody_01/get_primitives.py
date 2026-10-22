"""Finite AST-identical GET/JSON/descriptor primitives from pinned after211 helper."""
import datetime,hashlib,json,math,os,re,selectors,stat,subprocess,sys,time,types
from pathlib import Path
MAX_BODY=16_000_000
def need(value,message):
    if type(value) is not bool or not value:raise RuntimeError(message)


def pin(raw):return {'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}


def native(kind,raw):return hashlib.sha1(kind.encode()+b' '+str(len(raw)).encode()+b'\0'+raw).hexdigest()


def hexid(value,n=40):return type(value) is str and re.fullmatch('[0-9a-f]{'+str(n)+'}',value) is not None


def exact(a,b):
    if type(a) is not type(b):return False
    if type(a) is dict:return set(a)==set(b) and all(exact(a[k],b[k]) for k in a)
    if type(a) is list:return len(a)==len(b) and all(exact(x,y) for x,y in zip(a,b))
    return a==b


def decode(raw):
    def pairs(rows):
        out={}
        for key,value in rows:need(key not in out,'Duplicate JSON key');out[key]=value
        return out
    def finite(value):
        out=float(value);need(math.isfinite(out),'Nonfinite JSON number');return out
    return json.loads(raw,object_pairs_hook=pairs,parse_float=finite,parse_constant=lambda _:need(False,'Nonfinite JSON constant'))


def regular(path,immutable=True):
    need(path.is_absolute() and path.resolve()==path,'Canonical immutable record required')
    fd=os.open('/',os.O_RDONLY|os.O_DIRECTORY);parents=[]
    try:
        for part in path.parts[1:-1]:
            nxt=os.open(part,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW,dir_fd=fd);parents.append(fd);fd=nxt
        leaf=os.open(path.name,os.O_RDONLY|os.O_NOFOLLOW|os.O_NONBLOCK,dir_fd=fd)
        try:
            before=os.fstat(leaf);need(stat.S_ISREG(before.st_mode) and (not immutable or stat.S_IMODE(before.st_mode)==0o444) and before.st_size<=MAX_BODY,'Bounded immutable ordinary file')
            raw=os.read(leaf,MAX_BODY+1)
            identity=lambda s:(s.st_dev,s.st_ino,s.st_size,s.st_mtime_ns,s.st_ctime_ns,s.st_mode)
            need(identity(before)==identity(os.fstat(leaf))==identity(os.stat(path.name,dir_fd=fd,follow_symlinks=False)) and len(raw)==before.st_size,'Immutable record changed during read')
            need(path.resolve()==path,'Immutable record ancestor changed');return raw
        finally:os.close(leaf)
    finally:
        os.close(fd)
        for ancestor in reversed(parents):os.close(ancestor)


def bounded_get(argv):
    process=subprocess.Popen(argv,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    selector=selectors.DefaultSelector();out=bytearray();err=bytearray();deadline=time.monotonic()+120
    try:
        for stream,label in ((process.stdout,'stdout'),(process.stderr,'stderr')):
            os.set_blocking(stream.fileno(),False);selector.register(stream,selectors.EVENT_READ,label)
        while selector.get_map():
            left=deadline-time.monotonic();need(left>0,'Bounded GET timeout')
            for key,_ in selector.select(min(left,0.25)):
                chunk=os.read(key.fileobj.fileno(),65536)
                if not chunk:selector.unregister(key.fileobj);key.fileobj.close();continue
                target,cap=(out,12000000) if key.data=='stdout' else (err,65536)
                need(len(target)+len(chunk)<=cap,'Bounded GET output exceeded');target.extend(chunk)
        left=deadline-time.monotonic();need(left>0,'Bounded GET timeout')
        return types.SimpleNamespace(returncode=process.wait(timeout=left),stdout=bytes(out),stderr=bytes(err))
    except BaseException:
        if process.poll() is None:process.kill()
        process.wait(timeout=5);raise
    finally:
        selector.close()
        for stream in (process.stdout,process.stderr):
            if not stream.closed:stream.close()

