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
import stat
import subprocess
import sys
import types

BASE = Path(__file__).absolute().parent
CASE = BASE.parent
PROGRAM = CASE.parents[1]
CHECKOUT = PROGRAM.parent
GH = '/opt/homebrew/Cellar/gh/2.85.0/bin/gh'
LOCK_BYTES = (b'PR publication program: stable Root cooperating global-five writer lock v1\n'
              b'Never unlink or replace this inode; every existing-view writer must flock it.\n')
# Filled only after the model source is sealed; no live source is loaded now.
MODEL_PIN = {'bytes': 28201, 'sha256': '7945042143c5486b9102a12b27703f5d521bf30bd0e2d666ad854072ed1f689e'}


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
    fd = os.open(path,os.O_RDONLY|os.O_NOFOLLOW|os.O_NONBLOCK)
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
    finally:
        os.close(fd)
    result = types.ModuleType('pr209_owned_conditional_model')
    result.__file__ = str(path)
    exec(compile(raw,str(path),'exec'),result.__dict__)
    return result


def durable_dir(path):
    fd = os.open(path,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)


def put(directory,name,value):
    need(directory.resolve() == directory and directory.is_dir()
         and Path(name).name == name, 'Canonical owned journal/basename required')
    fd = os.open(directory/name,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o444)
    try:
        with os.fdopen(fd,'wb',closefd=False) as stream:
            raw = enc(value)
            need(stream.write(raw) == len(raw), 'Short journal write')
            stream.flush()
            os.fchmod(fd,0o444)
            os.fsync(fd)
    finally:
        os.close(fd)
    durable_dir(directory)


def journal_new(name):
    need(type(name) is str and re.fullmatch('[A-Za-z0-9][A-Za-z0-9_-]{0,79}',name) is not None,
         'Fresh owned journal basename required')
    path = BASE/name
    need(BASE.resolve() == BASE and not path.exists() and not path.is_symlink(), 'Fresh exclusive journal required')
    path.mkdir(mode=0o700)
    durable_dir(path)
    durable_dir(BASE)
    return path


class API:
    """No ref/service route; no semantic or transport retry. Intents precede POST."""
    def __init__(self,h,journal,mutate=False):
        self.h,self.journal,self.mutate = h,journal,mutate
        self.number,self.failed = 0,False

    def __call__(self,method,path,body=None):
        h = self.h
        need(not self.failed, 'Attempt stopped; inspect same attempt read-only')
        get = path in ('git/ref/heads/main','pulls/209') or re.fullmatch(
            r'git/(?:commits|trees|blobs)/[0-9a-f]{40}',path) is not None or re.fullmatch(
            r'compare/[0-9a-f]{40}\.\.\.[0-9a-f]{40}',path) is not None
        need((method == 'GET' and get and body is None)
             or (method == 'POST' and self.mutate and path in ('git/blobs','git/trees','git/commits')
                 and type(body) is dict), 'No ref/service/other route exists')
        self.number += 1
        need(self.number <= 5000, 'Bounded native API call count')
        name = str(self.number).zfill(5)
        request = {'method':method,'path':path,'request_pin':pin(enc(body)) if body is not None else None}
        if method == 'POST':
            put(self.journal,name+'.OBJECT_INTENT.json',{
                **request,'semantics':'One dispatch only; uncertainty stops. Never automatically retry an immutable object.'})
        argv = [GH,'api','--method',method,'repos/AlecKriebel/Math/'+path]
        if body is not None:
            argv += ['--input','-']
        try:
            result = subprocess.run(argv,input=enc(body) if body is not None else None,
                                    capture_output=True,timeout=120)
            put(self.journal,name+'.API_RECEIPT.json',{
                **request,'exit':result.returncode,'stdout_pin':pin(result.stdout),'stderr_pin':pin(result.stderr)})
            need(result.returncode == 0, 'Native API failed; inspect receipt, no retry')
            need(len(result.stdout) <= 12_000_000, 'Bounded native API response')
            value = h.decode(result.stdout)
            need(type(value) is dict, 'Native API object required')
            if method == 'POST':
                need(h.hexid(value.get('sha')), 'Native object result SHA required')
                put(self.journal,name+'.OBJECT_RESULT.json',{**request,'returned_sha':value['sha']})
            return value
        except BaseException as error:
            self.failed = True
            put(self.journal,name+'.STOPPED.json',{
                **request,'outcome_unknown':True,'exception_type':type(error).__name__})
            raise RuntimeError('Attempt stopped; inspect existing object read-only; no automatic mutation retry') from None


def local_pin(h,path):
    need(path.resolve() == path, 'Canonical local view path required')
    if not path.exists():
        need(not path.is_symlink(), 'Absent view must not be symlink')
        return None
    need(stat.S_ISREG(path.lstat().st_mode), 'Ordinary local view required')
    raw = path.read_bytes()
    need(len(raw) <= h.MAX_BODY, 'Bounded local view required')
    return h.pin(raw)


def local_preimages(h,m,overlay,resume=False):
    for row in m['local_views']:
        now = local_pin(h,CHECKOUT/row['path'])
        need(now == row['preimage'] or (resume and now == h.pin(overlay[row['path']])),
             'Local view differs from explicit preimage/accepted postimage: '+row['path'])


class WriterLock:
    def __enter__(self):
        self.path = PROGRAM/'ROOT_GLOBAL_FIVE_WRITER.lock'
        need(self.path.resolve() == self.path, 'Existing canonical stable lock required')
        self.fd = os.open(self.path,os.O_RDONLY|os.O_NOFOLLOW|os.O_NONBLOCK)
        s = os.fstat(self.fd)
        self.identity,self.pid = (s.st_dev,s.st_ino),os.getpid()
        try:
            self.check()
            fcntl.flock(self.fd,fcntl.LOCK_EX|fcntl.LOCK_NB)
            self.check()
            return self
        except BaseException:
            os.close(self.fd)
            raise

    def check(self):
        a,b = os.fstat(self.fd),self.path.lstat()
        need(os.getpid() == self.pid and self.path.resolve() == self.path
             and stat.S_ISREG(a.st_mode) and stat.S_ISREG(b.st_mode)
             and (a.st_dev,a.st_ino) == (b.st_dev,b.st_ino) == self.identity
             and stat.S_IMODE(a.st_mode) == stat.S_IMODE(b.st_mode) == 0o444
             and os.pread(self.fd,len(LOCK_BYTES)+1,0) == LOCK_BYTES, 'Stable lock inode/payload changed')

    def __exit__(self,*unused):
        try:
            self.check()
        finally:
            try:
                fcntl.flock(self.fd,fcntl.LOCK_UN)
            finally:
                os.close(self.fd)


def candidate(h,load,api,journal):
    c,m,overlay,pre,reused = load()
    local_preimages(h,m,overlay)
    s = h.state(c,m,overlay,pre,reused,api)
    need(bool(s['changed']), 'Empty candidate refused')
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
                load()
                need(api('GET','git/ref/heads/main')['object']['sha'] == s['parent'], 'Lease lost before binary blob')
                result = api('POST','git/blobs',{'content':base64.b64encode(body).decode('ascii'),'encoding':'base64'})
                need(result.get('sha') == oid, 'Binary object result differs')
                binary.add(oid)
            entry['sha'] = oid
        entries.append(entry)
    load()
    local_preimages(h,m,overlay)
    need(api('GET','git/ref/heads/main')['object']['sha'] == s['parent'], 'Lease lost before tree object')
    result = api('POST','git/trees',{'base_tree':s['parent_tree'],'tree':entries})
    need(result.get('sha') == s['wanted'], 'Tree object result differs')
    load()
    need(api('GET','git/ref/heads/main')['object']['sha'] == s['parent'], 'Lease lost before commit object')
    result = api('POST','git/commits',{'message':m['commit_message'],'tree':s['wanted'],'parents':s['parents']})
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
    with WriterLock() as lock:
        load()
        actual_acceptance(h,m,wanted,actual_name,actual_pin)
        local_preimages(h,m,overlay,resume=True)
        put(journal,'LOCAL_FIVE_SYNC_INTENT.json',{'acceptance_pin':actual_pin,'candidate':a['candidate'],
            'semantics':'Stable-inode cooperating lock; five per-file atomic installs; not a five-file transaction.'})
        for index,row in enumerate(m['local_views']):
            path,body = CHECKOUT/row['path'],overlay[row['path']]
            post = h.pin(body)
            lock.check()
            now = local_pin(h,path)
            if now != post:
                need(now == row['preimage'] and path.parent.resolve() == path.parent, 'Local preimage changed before install')
                temp = path.parent/('.pr209-native-'+journal.name+'-'+str(index)+'.tmp')
                fd = os.open(temp,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o444)
                try:
                    with os.fdopen(fd,'wb',closefd=False) as stream:
                        need(stream.write(body) == len(body), 'Short local view write')
                        stream.flush()
                        os.fchmod(fd,0o444)
                        os.fsync(fd)
                finally:
                    os.close(fd)
                lock.check()
                need(local_pin(h,path) == row['preimage'], 'Local preimage changed before atomic installation')
                if row['preimage'] is None:
                    os.link(temp,path,follow_symlinks=False)
                    temp.unlink()
                else:
                    os.replace(temp,path)
                durable_dir(path.parent)
            need(local_pin(h,path) == post, 'Installed view postimage differs')
            put(journal,'VIEW_'+str(index)+'.json',{'path':row['path'],'postimage':post})
        lock.check()
        need(api('GET','git/ref/heads/main')['object']['sha'] == a['candidate'], 'MAIN moved before actual pointer')
        need(all(local_pin(h,CHECKOUT/path) == h.pin(overlay[path]) for path in h.VIEWS), 'Exact five postimages required')
        receipt = {'schema':'pr209-native-actual-five-sync-v1','evidence_scope':'ACTUAL_ROOT_RECEIPT',
                   'PR':209,'phase':m['phase'],'facts':m['facts'],'candidate':a['candidate'],'tree':a['tree'],
                   'acceptance_pin':actual_pin,'manifest_pin':wanted,
                   'all_five_local_files_match_actual_checkpoint':True,
                   'files':[{'path':path,'postimage':h.pin(overlay[path])} for path in h.VIEWS]}
        put(journal,'LOCAL_GLOBAL_FIVE_SYNC.json',receipt)
        lock.check()
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
