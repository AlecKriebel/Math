#!/usr/bin/env python3
"""Portable source-free route review. Never claims Linux whole-FS EROFS replay.

Before execution authenticate this script AND the review manifest against the
external delivery record. Trust the installed Python/stdlib and host account.
Run with -I -S -B. This is an independent profile, not a historical receipt edit.
"""
from pathlib import Path
import argparse,datetime,hashlib,json,os,platform,stat,subprocess,sys,tempfile,time
PINS_SHA='0c4b17383546ac260674a51788dccd871eb170e56434889833392685b058d188'
MATH_SHA='ff44cdce74d36b40995843f7bc450e31fcac532163f3a411da51f3244ea82601'
HEAD='989a532ae1d50894190d010a0a02ba8c3d71ee05'
HERE=Path(__file__).absolute().parent
class Reject(Exception):pass

def need(c,m):
    if not c:raise Reject(m)

def sha(b):return hashlib.sha256(b).hexdigest()

def unique(pairs):
    d={}
    for k,v in pairs:
        need(k not in d,'duplicate JSON key');d[k]=v
    return d

def parse(raw):
    return json.loads(raw,object_pairs_hook=unique,parse_constant=lambda x:(_ for _ in ()).throw(Reject('nonfinite JSON')))

def regular(p):
    s=p.lstat();need(stat.S_ISREG(s.st_mode),'nonregular member');return s

def safe_root(p):
    p=p.absolute()
    need(p.is_dir(),'missing directory')
    need(all(not q.is_symlink() for q in [p,*p.parents]),'symlink root or ancestor')
    return p

def inventory(root):
    files={};dirs=set()
    def visit(folder,prefix):
        for e in os.scandir(folder):
            n=prefix+e.name;s=e.stat(follow_symlinks=False)
            need(not stat.S_ISLNK(s.st_mode),'symlink member: '+n)
            if stat.S_ISDIR(s.st_mode):dirs.add(n);visit(Path(e.path),n+'/')
            else:
                need(stat.S_ISREG(s.st_mode),'nonregular member: '+n)
                need(s.st_size<=2000000,'oversized member: '+n)
                b=Path(e.path).read_bytes();files[n]={'bytes':len(b),'sha256':sha(b),'disk_mode':f'{stat.S_IMODE(s.st_mode):04o}'}
    visit(root,'');return files,dirs

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--packet',required=True,type=Path);p.add_argument('--work-dir',required=True,type=Path);a=p.parse_args()
    need(sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode,'launch requires -I -S -B')
    root=safe_root(a.packet);work=safe_root(a.work_dir)
    need(work!=root and not work.is_relative_to(root),'work directory must be outside packet')
    pp=HERE/'ORIGINAL_PAYLOAD_PINS.json';regular(pp);raw=pp.read_bytes();need(sha(raw)==PINS_SHA,'review pins mismatch')
    pins=parse(raw);need(type(pins) is dict and set(pins)=={'schema','head','files'} and pins['schema']=='pr952-original-payload-pins-v1' and pins['head']==HEAD,'review pin schema')
    expected=pins['files'];need(type(expected) is dict and len(expected)==33,'pin inventory')
    for n,e in expected.items():
        need(type(n) is str and n and not n.startswith('/') and '\\' not in n and all(x not in ('','.','..') for x in n.split('/')),'unsafe path')
        need(type(e) is dict and set(e)=={'bytes','sha256','disk_mode'},'entry keys')
        need(type(e['bytes']) is int and 0<=e['bytes']<=2000000 and type(e['sha256']) is str and len(e['sha256'])==64 and all(c in '0123456789abcdef' for c in e['sha256']) and e['disk_mode']=='0644','entry types')
    before,dirs=inventory(root);need(before==expected,'submitted byte/mode inventory differs')
    expected_dirs={str(q) for n in expected for q in Path(n).parents if str(q)!='.'};need(dirs==expected_dirs,'unexpected directory namespace')
    math=HERE/'independent_math.py';regular(math);need(sha(math.read_bytes())==MATH_SHA,'independent math pin mismatch')
    rows=[]
    with tempfile.TemporaryDirectory(prefix='portable-pr952-review-',dir=work) as temp:
        env=dict(os.environ,TMPDIR=temp)
        def execute(label,script,args,flags):
            t=time.perf_counter();r=subprocess.run([sys.executable,'-I','-S','-B',*flags,str(script),*map(str,args)],cwd=temp,env=env,capture_output=True,timeout=60)
            need(r.returncode==0 and not r.stderr,'supported stage failed: '+label)
            obj=parse(r.stdout);rows.append({'label':label,'mode':flags[0] if flags else 'normal','elapsed_seconds':round(time.perf_counter()-t,6),'stdout_sha256':sha(r.stdout),'result':obj})
            return r.stdout
        outputs={}
        for flags in [[],['-O'],['-OO']]:
            for label,script,args in [('independent-math',math,[]),('original-author',root/'author_v3/bootstrap.py',[root/'author_v3/packet']),('original-algebra-audit',root/'audit_algebra/audit_controls.py',[root/'author_v3']),('original-bridge-finite-algebra',root/'audit_source_bridge/independent_algebra.py',[])]:
                out=execute(label,script,args,flags)
                need(label not in outputs or outputs[label]==out,'optimization changed output: '+label);outputs[label]=out
    after,after_dirs=inventory(root);need((before,dirs)==(after,after_dirs),'packet changed during review')
    need(sha(math.read_bytes())==MATH_SHA and sha(pp.read_bytes())==PINS_SHA,'review controls changed during execution')
    return {'schema':'pr952-portable-review-profile-v1','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS_PORTABLE_FINITE_REVIEW','immutable_submitted_head':HEAD,'host':platform.platform(),'python':sys.version,'python_executable':sys.executable,'uid':os.getuid(),'authenticated_original_files':33,'source_free':True,'unix_mode_binding':'0644 exact','packet_bytes_and_modes_unchanged':True,'mode_matrix':rows,'whole_filesystem_readonly':'NOT_TESTED_BY_THIS_PROFILE','linux_bwrap_EROFS_errno30':'NOT_RUN','primary_source_inspection':'NOT_RUN','quantum_topology_reproof':'NOT_RUN','literature_priority_audit':'NOT_RUN','full_paper_acceptance':False,'trust_roots':['Externally authenticated profile and manifest delivery SHA-256','Pinned original payload inventory and independently authored math checker','Installed Python executable, standard library and host OS/account','Nonconcurrently replaced inputs; not race-resistant']}

if __name__=='__main__':
    try:print(json.dumps(main(),sort_keys=True))
    except (Reject,OSError,ValueError,TypeError,KeyError,subprocess.SubprocessError) as e:
        print('REJECT: '+str(e),file=sys.stderr);raise SystemExit(1)
