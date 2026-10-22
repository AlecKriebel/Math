"""Reviewed generic bounded native/descriptor primitives for inactive PR212 protocol."""
import fcntl,hashlib,json,os,re,selectors,stat,subprocess,sys,time,types
from pathlib import Path
BASE=Path(__file__).absolute().parent
CASE=BASE.parent
PROGRAM=CASE.parents[1]
CHECKOUT=PROGRAM.parent
GH='/opt/homebrew/Cellar/gh/2.85.0/bin/gh'
LOCK_BYTES=(b'PR publication program: stable Root cooperating global-five writer lock v1\n'
 b'Never unlink or replace this inode; every existing-view writer must flock it.\n')

def need(ok,message):
    if type(ok) is not bool or not ok:
        raise RuntimeError(message)


def pin(raw):
    return {'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}


def enc(value):
    return (json.dumps(value,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()


def put(directory,name,value):
    need(directory.is_absolute() and directory.is_relative_to(BASE)
         and Path(name).name == name, 'Owned journal directory/basename required')
    raw = enc(value)
    need(len(raw) <= 20_000_000, 'Bounded durable exact-request journal record')
    with ParentHandle(directory/name) as parent:
        parent.check()
        fd = os.open(name,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o444,dir_fd=parent.fd)
        try:
            with os.fdopen(fd,'wb',closefd=False) as stream:
                need(stream.write(raw) == len(raw), 'Short journal write')
                stream.flush()
                os.fchmod(fd,0o444)
                os.fsync(fd)
        finally:
            os.close(fd)
        parent.check()
        os.fsync(parent.fd)


def journal_new(name):
    need(type(name) is str and re.fullmatch('[A-Za-z0-9][A-Za-z0-9_-]{0,79}',name) is not None,
         'Fresh owned journal basename required')
    path = BASE/name
    with ParentHandle(path) as parent:
        parent.check()
        os.mkdir(name,mode=0o700,dir_fd=parent.fd)
        fd = os.open(name,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW,dir_fd=parent.fd)
        try:
            a,b = os.fstat(fd),path.lstat()
            need(stat.S_ISDIR(a.st_mode) and stat.S_ISDIR(b.st_mode)
                 and (a.st_dev,a.st_ino) == (b.st_dev,b.st_ino), 'New journal identity changed')
            os.fsync(fd)
        finally:
            os.close(fd)
        parent.check()
        os.fsync(parent.fd)
    return path


def api_argv(method,path,has_body):
    """Canonical GitHub host is explicit, independent of GH_HOST."""
    return [GH,'api','--hostname','github.com','--method',method,
            'repos/AlecKriebel/Math/'+path]+(['--input','-'] if has_body else [])


class API:
    """No ref/service route; no semantic or transport retry. Intents precede POST."""
    def __init__(self,h,journal,mutate=False):
        self.h,self.journal,self.mutate = h,journal,mutate
        self.number,self.failed = 0,False
        self._immutable_cache,self._cache_bytes = {},0
        self.actual_GET_origins={}

    def __call__(self,method,path,body=None,expected_oid=None):
        h = self.h
        need(not self.failed, 'Attempt stopped; inspect same attempt read-only')
        get = path in ('git/ref/heads/main','pulls/212') or re.fullmatch(
            r'git/(?:commits|trees|blobs)/[0-9a-f]{40}',path) is not None or re.fullmatch(
            r'compare/[0-9a-f]{40}\.\.\.[0-9a-f]{40}',path) is not None
        need((method == 'GET' and get and body is None)
             or (method == 'POST' and self.mutate and path in ('git/trees','git/commits')
                 and type(body) is dict and h.hexid(expected_oid)), 'No ref/service/other route exists')
        self.number += 1
        need(self.number <= 5000, 'Bounded native API call count')
        name = str(self.number).zfill(5)
        request = {'method':method,'path':path,'request_pin':pin(enc(body)) if body is not None else None}
        immutable = re.fullmatch(r'git/(?:commits|trees|blobs)/([0-9a-f]{40})',path) if method == 'GET' else None
        if method == 'POST':
            put(self.journal,name+'.OBJECT_INTENT.json',{
                **request,'exact_request':body,'expected_oid':expected_oid,
                'semantics':'One dispatch only; uncertainty stops. Reconcile this expected oid with GET; never automatically retry.'})
        argv = api_argv(method,path,body is not None)
        try:
            if immutable is not None and path in self._immutable_cache:
                raw,expected,origin = self._immutable_cache[path]
                need(type(raw) is bytes and h.exact(pin(raw),expected), 'Immutable GET cache bytes changed')
                value = h.decode(raw)
                need(type(value) is dict and value.get('sha') == immutable.group(1), 'Cached route identity differs')
                put(self.journal,name+'.IMMUTABLE_GET_CACHE_HIT.json',{
                    **request,'canonical_cache_pin':expected,'actual_response_origin':origin,
                    'semantics':'In-memory immutable-SHA GET reuse only; caller revalidates native contents; fresh decoded copy returned.'})
                return value
            result = run_bounded(argv,enc(body) if body is not None else None)
            receipt = {**request,'exit':result.returncode,'stdout_pin':pin(result.stdout),'stderr_pin':pin(result.stderr)}
            # Retain exact actual envelopes, not receipt pins alone.
            raw_path=name+'.RAW_STDOUT.json';err_path=name+'.RAW_STDERR.txt'
            put_raw(self.journal,raw_path,result.stdout)
            put_raw(self.journal,err_path,result.stderr)
            receipt.update(raw_stdout={'path':str(self.journal/raw_path),**pin(result.stdout)},
                           raw_stderr={'path':str(self.journal/err_path),**pin(result.stderr)})
            put(self.journal,name+'.API_RECEIPT.json',receipt)
            if method == 'GET' and immutable is not None:
                self.actual_GET_origins[path]={'receipt':str(self.journal/(name+'.API_RECEIPT.json')),
                    'receipt_pin':pin(enc(receipt)),'raw_response':receipt['raw_stdout'],'raw_stderr':receipt['raw_stderr'],'method':'GET',
                    'hostname':'github.com','repository':'AlecKriebel/Math','route':path}
            need(result.returncode == 0, 'Native API failed; inspect receipt, no retry')
            value = h.decode(result.stdout)
            need(type(value) is dict, 'Native API object required')
            if immutable is not None:
                need(value.get('sha') == immutable.group(1), 'Successful native GET response SHA differs from route')
                raw = enc(value)
                if len(self._immutable_cache) < 2000 and self._cache_bytes+len(raw) <= 32_000_000:
                    origin = {'receipt':name+'.API_RECEIPT.json','actual_stdout_pin':receipt['stdout_pin']}
                    self._immutable_cache[path] = (raw,pin(raw),origin)
                    self._cache_bytes += len(raw)
                return h.decode(raw)
            if method == 'POST':
                need(h.hexid(value.get('sha')), 'Native object result SHA required')
                put(self.journal,name+'.OBJECT_RESULT.json',{**request,'returned_sha':value['sha'],'expected_oid':expected_oid})
                need(value['sha'] == expected_oid, 'Native object result differs from predicted content identity')
            return value
        except BaseException as error:
            self.failed = True
            put(self.journal,name+'.STOPPED.json',{
                **request,'expected_oid':expected_oid,'outcome_unknown':True,'exception_type':type(error).__name__,
                'bounded_transport_receipt':getattr(error,'receipt',None)})
            raise RuntimeError('Attempt stopped; inspect existing object read-only; no automatic mutation retry') from None


class BoundedTransportFailure(RuntimeError):
    def __init__(self,category,stdout,stderr):
        super().__init__(category)
        self.receipt = {'category':category,'stdout_pin':pin(stdout),'stderr_pin':pin(stderr),
                        'stdout_cap':12_000_000,'stderr_cap':65536,'process_killed_and_reaped':True}


def run_bounded(argv,request):
    """Stream stdin/stdout/stderr concurrently; cap before buffer allocation."""
    need(request is None or (type(request) is bytes and len(request) <= 16_000_000), 'Bounded exact API request')
    process = subprocess.Popen(argv,stdin=subprocess.PIPE if request is not None else subprocess.DEVNULL,
                               stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    selector = selectors.DefaultSelector()
    out,err,offset = bytearray(),bytearray(),0
    deadline = time.monotonic()+120
    try:
        for stream,label in ((process.stdout,'stdout'),(process.stderr,'stderr')):
            os.set_blocking(stream.fileno(),False)
            selector.register(stream,selectors.EVENT_READ,label)
        if request is not None:
            if request:
                os.set_blocking(process.stdin.fileno(),False)
                selector.register(process.stdin,selectors.EVENT_WRITE,'stdin')
            else:
                process.stdin.close()
        while selector.get_map():
            remaining = deadline-time.monotonic()
            if remaining <= 0:
                raise TimeoutError('Bounded native transport timeout')
            for key,unused in selector.select(min(remaining,0.25)):
                stream,label = key.fileobj,key.data
                if label == 'stdin':
                    try:
                        offset += os.write(stream.fileno(),memoryview(request)[offset:offset+65536])
                    except BrokenPipeError:
                        offset = len(request)
                    if offset == len(request):
                        selector.unregister(stream)
                        stream.close()
                else:
                    chunk = os.read(stream.fileno(),65536)
                    if not chunk:
                        selector.unregister(stream)
                        stream.close()
                        continue
                    buffer,cap = (out,12_000_000) if label == 'stdout' else (err,65536)
                    need(len(buffer)+len(chunk) <= cap, 'Bounded '+label+' capture exceeded')
                    buffer.extend(chunk)
        remaining = deadline-time.monotonic()
        if remaining <= 0:
            raise TimeoutError('Bounded native transport timeout')
        code = process.wait(timeout=remaining)
        return types.SimpleNamespace(returncode=code,stdout=bytes(out),stderr=bytes(err))
    except BaseException as error:
        if process.poll() is None:
            process.kill()
        process.wait(timeout=5)
        raise BoundedTransportFailure(type(error).__name__,bytes(out),bytes(err)) from None
    finally:
        selector.close()
        for stream in (process.stdin,process.stdout,process.stderr):
            if stream is not None and not stream.closed:
                stream.close()


class ParentHandle:
    """Pinned nofollow directory descriptor chain for local view operations."""
    def __init__(self,path):
        self.path,self.handles = path,[]

    def __enter__(self):
        need(self.path.is_absolute() and self.path.is_relative_to(CHECKOUT)
             and self.path.resolve() == self.path, 'Canonical local view within fixed checkout required')
        try:
            current = Path('/')
            fd = os.open(current,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW)
            self.handles.append((current,fd))
            for part in self.path.parent.parts[1:]:
                current = current/part
                fd = os.open(part,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW,dir_fd=fd)
                self.handles.append((current,fd))
            self.fd = fd
            self.identities = [(os.fstat(descriptor).st_dev,os.fstat(descriptor).st_ino) for path,descriptor in self.handles]
            self.check()
            return self
        except BaseException:
            self.__exit__()
            raise

    def check(self):
        for (path,fd),identity in zip(self.handles,self.identities):
            a,b = os.fstat(fd),path.lstat()
            need(stat.S_ISDIR(a.st_mode) and stat.S_ISDIR(b.st_mode)
                 and (a.st_dev,a.st_ino) == (b.st_dev,b.st_ino) == identity,
                 'Local view ancestor identity changed')

    def __exit__(self,*unused):
        for path,fd in reversed(self.handles):
            os.close(fd)
        self.handles = []


def local_pin(h,path):
    with ParentHandle(path) as parent:
        try:
            fd = os.open(path.name,os.O_RDONLY|os.O_NOFOLLOW|os.O_NONBLOCK,dir_fd=parent.fd)
        except FileNotFoundError:
            parent.check()
            try:
                path.lstat()
            except FileNotFoundError:
                return None
            raise RuntimeError('Local view appeared during absence check')
        try:
            before = os.fstat(fd)
            need(stat.S_ISREG(before.st_mode) and before.st_size <= h.MAX_BODY, 'Bounded ordinary local view required')
            with os.fdopen(fd,'rb',closefd=False) as stream:
                raw = stream.read(h.MAX_BODY+1)
            after,entry = os.fstat(fd),path.lstat()
            fields = lambda s:(s.st_dev,s.st_ino,s.st_size,s.st_mtime_ns,s.st_ctime_ns)
            need(fields(before) == fields(after) == fields(entry) and stat.S_ISREG(entry.st_mode)
                 and len(raw) == after.st_size, 'Local view changed during descriptor read')
            parent.check()
            return h.pin(raw)
        finally:
            os.close(fd)


class WriterLock:
    def __init__(self,expected):
        need(type(expected) is dict and set(expected) == {'path','device','inode','bytes','sha256'}
             and all(type(expected[k]) is int and expected[k] > 0 for k in ('device','inode','bytes'))
             and type(expected['path']) is str and type(expected['sha256']) is str
             and re.fullmatch('[0-9a-f]{64}',expected['sha256']) is not None, 'Exact typed pinned writer lock fields')
        self.expected = expected

    def __enter__(self):
        self.path = PROGRAM/'ROOT_GLOBAL_FIVE_WRITER.lock'
        need(self.path.resolve() == self.path, 'Existing canonical stable lock required')
        self.parent = ParentHandle(self.path).__enter__()
        self.fd = None
        try:
            self.fd = os.open(self.path.name,os.O_RDONLY|os.O_NOFOLLOW|os.O_NONBLOCK,dir_fd=self.parent.fd)
            self.identity,self.pid = (self.expected['device'],self.expected['inode']),os.getpid()
            self.check()
            fcntl.flock(self.fd,fcntl.LOCK_EX|fcntl.LOCK_NB)
            self.check()
            return self
        except BaseException:
            if self.fd is not None:
                os.close(self.fd)
            self.parent.__exit__()
            raise

    def check(self):
        self.parent.check()
        a,b = os.fstat(self.fd),self.path.lstat()
        need(os.getpid() == self.pid and self.path.resolve() == self.path
             and stat.S_ISREG(a.st_mode) and stat.S_ISREG(b.st_mode)
             and (a.st_dev,a.st_ino) == (b.st_dev,b.st_ino) == self.identity
             and stat.S_IMODE(a.st_mode) == stat.S_IMODE(b.st_mode) == 0o444
             and a.st_size == b.st_size == self.expected['bytes']
             and pin(os.pread(self.fd,len(LOCK_BYTES)+1,0)) == {k:self.expected[k] for k in ('bytes','sha256')}
             and os.pread(self.fd,len(LOCK_BYTES)+1,0) == LOCK_BYTES, 'Pinned stable lock inode/payload changed')

    def __exit__(self,*unused):
        try:
            self.check()
        finally:
            try:
                fcntl.flock(self.fd,fcntl.LOCK_UN)
            finally:
                os.close(self.fd)
                self.parent.__exit__()


def put_raw(directory,name,raw):
    need(type(raw) is bytes and len(raw)<=12_000_000 and directory.is_absolute()
         and directory.is_relative_to(BASE) and Path(name).name==name,'Owned bounded raw envelope')
    with ParentHandle(directory/name) as parent:
        parent.check()
        fd=os.open(name,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o444,dir_fd=parent.fd)
        try:
            with os.fdopen(fd,'wb',closefd=False) as stream:
                need(stream.write(raw)==len(raw),'Short raw envelope')
                stream.flush();os.fchmod(fd,0o444);os.fsync(fd)
        finally:os.close(fd)
        parent.check();os.fsync(parent.fd)
