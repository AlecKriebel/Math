"""Inactive future PR209 native executor. Import is inert; no ref writer exists.

This source has not been operationally authorized. Every CLI action requires
sealed actual Root envelopes and the exact two source/manifest audit bindings.
Candidate alone may dispatch immutable Git objects once. Sync requires separate
actual Root expected-SHA/force-false CAS acceptance and full native readback.
"""
import argparse
import base64
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import selectors
import stat
import subprocess
import sys
import time
import types

BASE = Path(__file__).absolute().parent
CASE = BASE.parent
PROGRAM = CASE.parents[1]
CHECKOUT = PROGRAM.parent
GH = '/opt/homebrew/Cellar/gh/2.85.0/bin/gh'
LOCK_BYTES = (b'PR publication program: stable Root cooperating global-five writer lock v1\n'
              b'Never unlink or replace this inode; every existing-view writer must flock it.\n')
# Filled only after the model source is sealed; no live source is loaded now.
MODEL_PIN = {'bytes': 35600, 'sha256': '207f30fc102f634dddf843b0f31d9b939a5e4dbc376b8ad8eff83537236c8c14'}


def need(ok,message):
    if type(ok) is not bool or not ok:
        raise RuntimeError(message)


def pin(raw):
    return {'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}


def enc(value):
    return (json.dumps(value,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()


def model():
    need(type(MODEL_PIN) is dict, 'Unsealed preparation source cannot execute')
    path = BASE/'native209_model.py'
    need(path.resolve() == path, 'Canonical model source required')
    with ParentHandle(path) as parent:
        fd = os.open(path.name,os.O_RDONLY|os.O_NOFOLLOW|os.O_NONBLOCK,dir_fd=parent.fd)
        try:
            before = os.fstat(fd)
            need(stat.S_ISREG(before.st_mode) and stat.S_IMODE(before.st_mode) == 0o444
                 and before.st_size == MODEL_PIN['bytes'], 'Exact readonly model file required')
            with os.fdopen(fd,'rb',closefd=False) as stream:
                raw = stream.read(before.st_size+1)
            after = os.fstat(fd)
            entry = path.lstat()
            fields = lambda s: (s.st_dev,s.st_ino,s.st_size,s.st_mtime_ns,s.st_ctime_ns)
            need(fields(before) == fields(after) == fields(entry) and pin(raw) == MODEL_PIN,
                 'Pinned model source changed')
            parent.check()
        finally:
            os.close(fd)
    result = types.ModuleType('pr209_owned_conditional_model')
    result.__file__ = str(path)
    exec(compile(raw,str(path),'exec'),result.__dict__)
    return result


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


class API:
    """No ref/service route; no semantic or transport retry. Intents precede POST."""
    def __init__(self,h,journal,mutate=False):
        self.h,self.journal,self.mutate = h,journal,mutate
        self.number,self.failed = 0,False
        self._immutable_cache,self._cache_bytes = {},0

    def __call__(self,method,path,body=None,expected_oid=None):
        h = self.h
        need(not self.failed, 'Attempt stopped; inspect same attempt read-only')
        get = path in ('git/ref/heads/main','pulls/209') or re.fullmatch(
            r'git/(?:commits|trees|blobs)/[0-9a-f]{40}',path) is not None or re.fullmatch(
            r'compare/[0-9a-f]{40}\.\.\.[0-9a-f]{40}',path) is not None
        need((method == 'GET' and get and body is None)
             or (method == 'POST' and self.mutate and path in ('git/blobs','git/trees','git/commits')
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
        argv = [GH,'api','--method',method,'repos/AlecKriebel/Math/'+path]
        if body is not None:
            argv += ['--input','-']
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
            put(self.journal,name+'.API_RECEIPT.json',receipt)
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


def local_preimages(h,m,overlay,resume=False):
    for row in m['local_views']:
        now = local_pin(h,CHECKOUT/row['path'])
        need(now == row['preimage'] or (resume and now == h.pin(overlay[row['path']])),
             'Local view differs from explicit preimage/accepted postimage: '+row['path'])


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


def candidate(h,load,api,journal):
    c,m,overlay,pre,reused = load()
    need(journal == BASE/m['candidate_journal'], 'Only exact one-use manifest-bound candidate journal allowed')
    local_preimages(h,m,overlay)
    s = h.state(c,m,overlay,pre,reused,api)
    need(bool(s['changed']), 'Empty candidate refused')
    commit_body,commit_oid = h.commit_request(m,s['wanted'],s['parents'])
    put(journal,'CANDIDATE_DISPATCH_RESERVATION.json',{'manifest_candidate_journal':m['candidate_journal'],
        'expected_commit':commit_oid,'exact_commit_request':commit_body,
        'semantics':'Exclusive one-use candidate attempt. Never reuse this or another journal for this manifest after uncertainty.'})
    def effect_guard():
        load()
        local_preimages(h,m,overlay)
        need(api('GET','git/ref/heads/main')['object']['sha'] == s['parent'], 'Fresh MAIN lease lost before object effect')
        h.pr_identity(h.GetOnly(api),m)
        local_preimages(h,m,overlay)
        load()
        need(api('GET','git/ref/heads/main')['object']['sha'] == s['parent'], 'Lease lost immediately before object effect')
    entries,binary = [],set()
    for path,body in sorted(overlay.items()):
        try:
            value = body.decode('utf-8')
            inline = '\0' not in value
        except UnicodeError:
            inline = False
        entry = {'path':path,'mode':'100644','type':'blob'}
        if inline:
            entry['content'] = value
        else:
            oid = h.native('blob',body)
            if oid not in binary:
                effect_guard()
                result = api('POST','git/blobs',{'content':base64.b64encode(body).decode('ascii'),'encoding':'base64'},expected_oid=oid)
                need(result.get('sha') == oid, 'Binary object result differs')
                binary.add(oid)
            entry['sha'] = oid
        entries.append(entry)
    effect_guard()
    result = api('POST','git/trees',{'base_tree':s['parent_tree'],'tree':entries},expected_oid=s['wanted'])
    need(result.get('sha') == s['wanted'], 'Tree object result differs')
    effect_guard()
    result = api('POST','git/commits',commit_body,expected_oid=commit_oid)
    oid = result.get('sha')
    need(h.hexid(oid), 'Commit response native identity')
    put(journal,'CANDIDATE_IDENTITY.json',{'parent':s['parent'],'parents':s['parents'],'candidate':oid,'tree':s['wanted']})
    read_api = API(h,journal,mutate=False)
    read_api.number = api.number
    result = h.verify(c,m,overlay,pre,reused,read_api,oid)
    put(journal,'CANDIDATE_VERIFIED.json',result)
    return result


def actual_acceptance(h,m,wanted,name,expected):
    a = h.decode(h.sealed(name,expected))
    h.matches(a,{'schema':'pr209-root-native-actual-CAS-acceptance-v1',
                 'evidence_scope':'ACTUAL_ROOT_RECEIPT','PR':209,'phase':m['phase'],'accepted':True,
                 'manifest_pin':wanted,'helper_pin':m['helper_pin'],'executor_pin':m['executor_pin'],
                 'core_pin':h.CORE_PIN,'facts':m['facts'],'parent':m['expected_parent'],
                 'original_head':h.ORIGINAL,'prepared_head':h.PREPARED,
                 'full_scope_verified':True,'all_selected_native_bodies_verified':True,
                 'foreign_native_tuples_preserved':True}, 'External actual Root CAS acceptance required')
    need(type(a.get('facts')) is dict and set(a['facts']) == set(m['facts']), 'Actual CAS exact fact fields')
    h.matches(a['facts'],m['facts'],'Actual CAS fact types')
    need(h.hexid(a.get('candidate')) and h.hexid(a.get('tree'))
         and a.get('actual_MAIN_observed') == a['candidate'], 'Actual candidate/tree/readback required')
    h.matches(a.get('Root_ref_update'),{'expected_sha':a['parent'],'sha':a['candidate'],'force':False,
              'success_confirmed_by_actual_native_readback':True}, 'Only actual external Root expectedSHA forcefalse CAS accepted')
    return a


def sync(h,load,api,journal,wanted,actual_name,actual_pin):
    c,m,overlay,pre,reused = load()
    a = actual_acceptance(h,m,wanted,actual_name,actual_pin)
    need(api('GET','git/ref/heads/main')['object']['sha'] == a['candidate'], 'Actual MAIN is not accepted candidate')
    result = h.verify(c,m,overlay,pre,reused,api,a['candidate'],after_ref=True)
    need(result['tree'] == a['tree'], 'Actual full native readback differs')
    pointer = BASE/('ROOT_ACTUAL_'+m['phase'].upper()+'_POINTER.json')
    need(not pointer.exists() and not pointer.is_symlink(), 'Phase pointer already exists')
    with WriterLock(m['writer_lock']) as lock:
        def effect_guard():
            load()
            current = actual_acceptance(h,m,wanted,actual_name,actual_pin)
            need(h.exact(current,a), 'Actual Root CAS acceptance changed')
            need(api('GET','git/ref/heads/main')['object']['sha'] == a['candidate'], 'Actual MAIN moved before local effect')
            h.pr_identity(h.GetOnly(api),m,after_ref=True)
            local_preimages(h,m,overlay,resume=True)
            lock.check()
            need(api('GET','git/ref/heads/main')['object']['sha'] == a['candidate'], 'Actual MAIN moved immediately before local effect')
        effect_guard()
        put(journal,'LOCAL_FIVE_SYNC_INTENT.json',{'acceptance_pin':actual_pin,'candidate':a['candidate'],
            'semantics':'Stable-inode cooperating lock; five per-file atomic installs; not a five-file transaction.'})
        for index,row in enumerate(m['local_views']):
            path,body = CHECKOUT/row['path'],overlay[row['path']]
            post = h.pin(body)
            effect_guard()
            now = local_pin(h,path)
            if now != post:
                need(now == row['preimage'], 'Local preimage changed before install')
                with ParentHandle(path) as parent:
                    temp = '.pr209-native-'+journal.name+'-'+str(index)+'.tmp'
                    effect_guard()
                    parent.check()
                    fd = os.open(temp,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o444,dir_fd=parent.fd)
                    try:
                        with os.fdopen(fd,'wb',closefd=False) as stream:
                            need(stream.write(body) == len(body), 'Short local view write')
                            stream.flush()
                            os.fchmod(fd,0o444)
                            os.fsync(fd)
                    finally:
                        os.close(fd)
                    effect_guard()
                    parent.check()
                    need(local_pin(h,path) == row['preimage'], 'Local preimage changed before atomic installation')
                    if row['preimage'] is None:
                        os.link(temp,path.name,src_dir_fd=parent.fd,dst_dir_fd=parent.fd,follow_symlinks=False)
                        os.unlink(temp,dir_fd=parent.fd)
                    else:
                        os.replace(temp,path.name,src_dir_fd=parent.fd,dst_dir_fd=parent.fd)
                    parent.check()
                    os.fsync(parent.fd)
            need(local_pin(h,path) == post, 'Installed view postimage differs')
            effect_guard()
            put(journal,'VIEW_'+str(index)+'.json',{'path':row['path'],'postimage':post})
        effect_guard()
        need(all(local_pin(h,CHECKOUT/path) == h.pin(overlay[path]) for path in h.VIEWS), 'Exact five postimages required')
        receipt = {'schema':'pr209-native-actual-five-sync-v1','evidence_scope':'ACTUAL_ROOT_RECEIPT',
                   'PR':209,'phase':m['phase'],'facts':m['facts'],'candidate':a['candidate'],'tree':a['tree'],
                   'acceptance_pin':actual_pin,'manifest_pin':wanted,
                   'all_five_local_files_match_actual_checkpoint':True,
                   'files':[{'path':path,'postimage':h.pin(overlay[path])} for path in h.VIEWS]}
        put(journal,'LOCAL_GLOBAL_FIVE_SYNC.json',receipt)
        effect_guard()
        need(all(local_pin(h,CHECKOUT/path) == h.pin(overlay[path]) for path in h.VIEWS), 'Exact all-five before pointer')
        put(BASE,pointer.name,{'schema':'pr209-native-actual-pointer-v1','evidence_scope':'ACTUAL_ROOT_RECEIPT',
             'PR':209,'phase':m['phase'],'facts':m['facts'],'candidate':a['candidate'],'tree':a['tree'],
             'acceptance_pin':actual_pin,'manifest_pin':wanted,'sync_path':str(journal/'LOCAL_GLOBAL_FIVE_SYNC.json'),
             'sync_pin':pin(enc(receipt)),'recorded_only_after_actual_ref_readback_and_exact_all_five_files':True})
    return receipt


def main():
    need(sys.flags.ignore_environment and sys.flags.no_site and sys.dont_write_bytecode
         and sys.flags.safe_path and not sys.flags.optimize, 'Ordinary Python -E -S -B -P without -O required')
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action',choices=('dry','plan','candidate','verify','sync'))
    parser.add_argument('--manifest',required=True)
    parser.add_argument('--manifest-bytes',type=int,required=True)
    parser.add_argument('--manifest-sha256',required=True)
    parser.add_argument('--Root-acceptance',dest='root_acceptance',required=True)
    parser.add_argument('--Root-acceptance-bytes',dest='root_acceptance_bytes',type=int,required=True)
    parser.add_argument('--Root-acceptance-sha256',dest='root_acceptance_sha256',required=True)
    parser.add_argument('--journal')
    parser.add_argument('--candidate')
    parser.add_argument('--after-ref',action='store_true')
    parser.add_argument('--actual-CAS-acceptance',dest='actual_cas')
    parser.add_argument('--actual-CAS-acceptance-bytes',dest='actual_cas_bytes',type=int)
    parser.add_argument('--actual-CAS-acceptance-sha256',dest='actual_cas_sha256')
    args = parser.parse_args()
    h = model()
    wanted = h.bytepin({'bytes':args.manifest_bytes,'sha256':args.manifest_sha256})
    accepted = h.bytepin({'bytes':args.root_acceptance_bytes,'sha256':args.root_acceptance_sha256})
    load = lambda: h.load_inputs(args.manifest,wanted,args.root_acceptance,accepted)
    c,m,overlay,pre,reused = load()
    need(not args.after_ref or args.action == 'verify', 'After-ref is read-only verify only')
    if args.action == 'dry':
        local_preimages(h,m,overlay)
        print(h.compact({'status':'OFFLINE_DRY_ONLY','phase':m['phase'],'facts':m['facts'],
              'files':len(overlay),'bytes':sum(map(len,overlay.values())),
              'actual_acceptance_inferred':False,'ref_actions_performed':False}))
        return
    if args.action == 'candidate':
        need(args.journal == m['candidate_journal'], 'Only manifest-bound one-use candidate journal allowed')
    journal = journal_new(args.journal)
    put(journal,'FROZEN_INPUT.json',{'manifest':args.manifest,'manifest_pin':wanted,
         'Root_acceptance':args.root_acceptance,'Root_acceptance_pin':accepted,
         'helper_pin':m['helper_pin'],'executor_pin':m['executor_pin'],'action':args.action,'after_ref':args.after_ref})
    api = API(h,journal,mutate=args.action == 'candidate')
    if args.action == 'plan':
        local_preimages(h,m,overlay)
        result = h.plan(c,m,overlay,pre,reused,api)
        put(journal,'PLAN.json',result)
    elif args.action == 'candidate':
        result = candidate(h,load,api,journal)
    elif args.action == 'verify':
        result = h.verify(c,m,overlay,pre,reused,api,args.candidate,args.after_ref)
        put(journal,'VERIFIED.json',result)
    else:
        need(args.actual_cas is not None and args.actual_cas_bytes is not None
             and args.actual_cas_sha256 is not None, 'Externally pinned actual Root CAS acceptance required')
        result = sync(h,load,api,journal,wanted,args.actual_cas,
                      h.bytepin({'bytes':args.actual_cas_bytes,'sha256':args.actual_cas_sha256}))
    print(h.compact(result))


if __name__ == '__main__':
    main()
