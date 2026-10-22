"""Optional PR204 immutable nonrecursive native-tree cache. Offline-reviewed only.
Only exact GET git/trees/<40 lowercase hex>, body=None is cached. No retries.
Install after Root review, after the ordinary -B native loader returns c,h,rv,n.
"""
from pathlib import Path
from contextlib import contextmanager
import copy,fcntl,gzip,hashlib,io,json,os,re,stat,threading,uuid
D=Path(__file__).resolve().parent
REPO='AlecKriebel/Math';API_ROOT='https://api.github.com/repos/'+REPO+'/git/'
SHA=re.compile(r'[0-9a-f]{40}\Z');REQUEST=re.compile(r'git/trees/([0-9a-f]{40})\Z')
MAX_JSON=4*1024*1024;MAX_GZIP=1024*1024;MAX_FILES=4096;MAX_TOTAL_GZIP=24*1024*1024
MODES={'040000':'tree','100644':'blob','100755':'blob','120000':'blob','160000':'commit'}
def require(ok,msg):
    if not ok:raise RuntimeError(msg)
def canonical(j):return json.dumps(j,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode('utf-8')
def unique_object(pairs):
    result={}
    for key,value in pairs:require(key not in result,'Duplicate JSON key');result[key]=value
    return result
def parse_json(b):
    return json.loads(b.decode('utf-8'),object_pairs_hook=unique_object,parse_constant=lambda s:(_ for _ in ()).throw(RuntimeError('Nonfinite JSON constant')))
def validate_tree(sha,j):
    require(isinstance(sha,str) and SHA.fullmatch(sha) is not None,'Exact requested native SHA required')
    require(isinstance(j,dict) and set(j)=={'sha','url','tree','truncated'},'Nonrecursive tree API schema')
    require(j['sha']==sha and j['truncated'] is False and j['url']==API_ROOT+'trees/'+sha,'Requested SHA/truncation/tree URL mismatch')
    require(isinstance(j['tree'],list),'Tree entries must be a list');raw=[];keys=[];names=set()
    for x in j['tree']:
        require(isinstance(x,dict) and {'path','mode','type','sha','url'}<=set(x)<= {'path','mode','type','sha','url','size'},'Native entry schema')
        name=x['path'];mode=x['mode'];kind=x['type'];oid=x['sha']
        require(isinstance(name,str) and name not in ['', '.', '..'] and '/' not in name and '\0' not in name,'Noncanonical native name')
        encoded=name.encode('utf-8',errors='strict');require(name not in names,'Duplicate native tree name');names.add(name)
        require(isinstance(mode,str) and mode in MODES and MODES[mode]==kind,'Canonical mode/type mismatch')
        require(isinstance(oid,str) and SHA.fullmatch(oid) is not None,'Canonical native object ID')
        endpoint={'tree':'trees','blob':'blobs','commit':'commits'}[kind]
        require(x['url']==API_ROOT+endpoint+'/'+oid,'Native entry URL mismatch')
        if kind=='blob':require(type(x.get('size')) is int and x['size']>=0,'Blob metadata size schema')
        else:require('size' not in x,'Unexpected nonblob size metadata')
        keys.append(encoded+(b'/' if kind=='tree' else b''));raw.append(mode.lstrip('0').encode()+b' '+encoded+b'\0'+bytes.fromhex(oid))
    require(keys==sorted(keys),'Noncanonical native entry order')
    body=b''.join(raw);require(hashlib.sha1(b'tree '+str(len(body)).encode()+b'\0'+body).hexdigest()==sha,'Full native Git tree content identity mismatch')
    data=canonical(j);require(len(data)<=MAX_JSON,'Tree response exceeds bounded JSON size');return data
class TreeCache:
    def __init__(self,original,root=None):
        require(callable(original),'Original API transport required');self.original=original
        self.root=Path(root) if root is not None else D/'private_tree_cache'
        require(self.root.is_absolute() and self.root.parent==D and self.root.name.startswith('private_') and self.root.name not in ['.','..'],'Cache must be a direct owned private child of transport folder')
        try:os.mkdir(self.root,0o700)
        except FileExistsError:pass
        ls=os.lstat(self.root);require(stat.S_ISDIR(ls.st_mode) and ls.st_uid==os.getuid() and stat.S_IMODE(ls.st_mode)==0o700,'Cache root must be owned nonsymlink0700')
        self.fd=os.open(self.root,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW|os.O_CLOEXEC);fs=os.fstat(self.fd)
        require((fs.st_dev,fs.st_ino)==(ls.st_dev,ls.st_ino),'Cache root race')
        self._locks={};self._guard=threading.Lock();self.stats={'tree_misses':0,'tree_hits':0,'forwarded_other':0,'original_tree_calls':0}
    def close(self):
        if self.fd is not None:os.close(self.fd);self.fd=None
    def __enter__(self):return self
    def __exit__(self,*args):self.close()
    def _file_check(self,fd,regular=True):
        s=os.fstat(fd);require(stat.S_ISREG(s.st_mode) and s.st_uid==os.getuid() and stat.S_IMODE(s.st_mode)==0o600 and s.st_nlink==1,'Cache/lock file must be owned regular0600 with one link');return s
    @contextmanager
    def _locked(self,name):
        require(self.fd is not None,'Private cache is closed')
        with self._guard:lock=self._locks.setdefault(name,threading.Lock())
        with lock:
            fd=os.open(name,os.O_RDWR|os.O_CREAT|os.O_NOFOLLOW|os.O_CLOEXEC,0o600,dir_fd=self.fd)
            try:
                self._file_check(fd);fcntl.flock(fd,fcntl.LOCK_EX)
                try:yield
                finally:fcntl.flock(fd,fcntl.LOCK_UN)
            finally:os.close(fd)
    def _read(self,sha):
        try:fd=os.open(sha+'.json.gz',os.O_RDONLY|os.O_NOFOLLOW|os.O_CLOEXEC,dir_fd=self.fd)
        except FileNotFoundError:return None
        try:
            s=self._file_check(fd);require(s.st_size<=MAX_GZIP,'Compressed cache object too large')
            with os.fdopen(os.dup(fd),'rb') as f:compressed=f.read(MAX_GZIP+1)
            require(len(compressed)<=MAX_GZIP,'Compressed cache read bound')
        finally:os.close(fd)
        try:
            with gzip.GzipFile(fileobj=io.BytesIO(compressed),mode='rb') as g:data=g.read(MAX_JSON+4097)
        except Exception as e:raise RuntimeError('Corrupt immutable gzip cache') from e
        require(len(data)<=MAX_JSON+4096,'Inflated cache exceeds bound');envelope=parse_json(data)
        require(isinstance(envelope,dict) and set(envelope)=={'requested_sha','api_json_sha256','api_json'} and envelope['requested_sha']==sha,'Cache envelope/request identity')
        tree=envelope['api_json'];raw=validate_tree(sha,tree)
        require(envelope['api_json_sha256']==hashlib.sha256(raw).hexdigest(),'Full API JSON checksum mismatch')
        return tree
    def _write(self,sha,j,raw):
        payload=canonical({'requested_sha':sha,'api_json_sha256':hashlib.sha256(raw).hexdigest(),'api_json':j});require(len(payload)<=MAX_JSON+4096,'Cache envelope exceeds bound')
        compressed=gzip.compress(payload,compresslevel=6,mtime=0);require(len(compressed)<=MAX_GZIP,'Compressed immutable object exceeds bound')
        temporary='.'+sha+'.'+uuid.uuid4().hex+'.tmp'
        with self._locked('_budget.lock'):
            count=0;total=0
            for name in os.listdir(self.fd):
                if re.fullmatch('[0-9a-f]{40}\\.json\\.gz',name):
                    st=os.stat(name,dir_fd=self.fd,follow_symlinks=False);require(stat.S_ISREG(st.st_mode),'Nonregular cache object in budget');count+=1;total+=st.st_size
            require(count<MAX_FILES and total+len(compressed)<=MAX_TOTAL_GZIP,'Private cache budget exhausted; no eviction or fallback')
            fd=os.open(temporary,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW|os.O_CLOEXEC,0o600,dir_fd=self.fd)
            try:
                with os.fdopen(fd,'wb') as f:f.write(compressed);f.flush();os.fsync(f.fileno())
                # Exclusive hardlink publish is atomic; per-SHA advisory lock keeps
                # adapter readers out until temp unlink restores link count1.
                os.link(temporary,sha+'.json.gz',src_dir_fd=self.fd,dst_dir_fd=self.fd,follow_symlinks=False)
                os.unlink(temporary,dir_fd=self.fd);os.fsync(self.fd)
            except BaseException:
                try:os.unlink(temporary,dir_fd=self.fd)
                except FileNotFoundError:pass
                raise
    def __call__(self,endpoint,method='GET',body=None):
        match=REQUEST.fullmatch(endpoint) if isinstance(endpoint,str) else None
        if method!='GET' or body is not None or match is None:
            with self._guard:self.stats['forwarded_other']+=1
            return self.original(endpoint,method,body)
        sha=match.group(1)
        with self._locked(sha+'.lock'):
            j=self._read(sha)
            if j is not None:
                with self._guard:self.stats['tree_hits']+=1
                return j
            with self._guard:self.stats['tree_misses']+=1;self.stats['original_tree_calls']+=1
            j=copy.deepcopy(self.original(endpoint,method,body)) # Exactly once. No shared mutable result or retry.
            raw=validate_tree(sha,j);self._write(sha,j,raw);return copy.deepcopy(j)
def install_loaded(c,h,cache_root=None):
    """Install on all six observed aliases, including base function globals.
    No directory/lookup/warm/diff/cache validator is replaced or weakened.
    Caller must use only after Root review. Restorer restores every alias.
    """
    mods=[h,h.m,h.m.m,h.m.m.h,h.m.m.h.m,h.m.m.h.m.m];require(len({id(x) for x in mods})==6,'Unexpected native-loader graph')
    original=h.api;require(not isinstance(original,TreeCache) and all(x.api is original for x in mods),'Already wrapped/divergent original API bindings; stop for review')
    base=mods[-1];directory=h.lookup.__globals__.get('directory')
    require(base.REPO=='repos/'+REPO,'Native API repository differs from cache namespace')
    require(h.lookup.__globals__ is base.__dict__ and directory is base.directory and directory.__globals__ is base.__dict__ and h.changed_leaves.__globals__ is base.__dict__,'Lookup/directory/diff globals no longer match audited graph')
    warm=mods[3].warm_selected_directories
    require(warm.__globals__ is mods[3].__dict__ and mods[3].m.m.directory is directory,'Warm-selected directory binding changed')
    require(h.m.native_tree_cache is base.TREE_CACHE and callable(h.m.verify_tree_object) and callable(c.selected_current),'Native cache/validation graph changed')
    for sha,rows in base.TREE_CACHE.items():h.m.verify_tree_object(sha,rows)
    cache=TreeCache(original,cache_root)
    for mod in mods:mod.api=cache
    require(base.__dict__['api'] is cache and directory.__globals__['api'] is cache and h.api is cache,'Nested API installation incomplete')
    def restore():
        for mod in mods:
            require(mod.api is cache,'API alias changed during cached phase');mod.api=original
        cache.close()
    return cache,restore
