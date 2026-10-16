#!/usr/bin/env python3
"""Fixed-pin, fail-closed replay of accepted /3091 elementary partial results."""
from pathlib import Path,PurePosixPath
import argparse,hashlib,json,math,os,re,stat,subprocess,sys,tempfile
MANIFEST_SHA='3bd74b9cdaba22e6edd01f0961a72096c27c67d533ae4664ba01716630391c4b'
AUTHOR_SHA='4e3fb58491159e8892d218a8aeec1dc95174bf8b7243472d51c96c8fea64d4a8'
AUDIT_SHA='08909d0755aba8ea21ce78c8c609e0d8986dbe82acc9754409d2c817cbe92935'
class Reject(Exception):pass
def need(x,message):
    if not x:raise Reject(message)
def sha(b):return hashlib.sha256(b).hexdigest()
def pairs(items):
    d={}
    for k,v in items:
        need(k not in d,'duplicate JSON key');d[k]=v
    return d
def nonfinite(x):raise Reject('nonfinite JSON constant')
def finite_float(raw):
    value=float(raw);need(math.isfinite(value),'nonfinite JSON number');return value
def load(raw):return json.loads(raw,object_pairs_hook=pairs,parse_constant=nonfinite,parse_float=finite_float)
def equal(a,b):return type(a) is type(b) and a==b
def safe(n):return type(n) is str and bool(n) and '\\' not in n and not n.startswith('/') and all(x not in ('','.','..') for x in n.split('/'))
def validate_manifest(m):
    need(type(m) is dict and set(m)=={'schema','problem_id','rank','status','turns','full_target_resolved','files'},'manifest schema')
    for k,v in [('schema','empty-hexagons-publication-v1'),('problem_id',3091),('rank',1058),('status','exhausted'),('turns',5),('full_target_resolved',False)]:need(equal(m[k],v),'manifest identity: '+k)
    need(type(m['files']) is list and len(m['files'])==20,'manifest files')
    names=set()
    for row in m['files']:
        need(type(row) is dict and set(row)=={'path','bytes','sha256'},'entry schema')
        n=row['path'];need(safe(n) and n not in names and n not in {'BOOTSTRAP.py','VERIFY_PUBLICATION.py','PUBLICATION_MANIFEST.json'},'unsafe or duplicate path');names.add(n)
        need(type(row['bytes']) is int and 0<=row['bytes']<=2000000,'entry size type/range')
        need(type(row['sha256']) is str and re.fullmatch('[a-f0-9]{64}',row['sha256']) is not None,'entry hash type/format')
    return names

def inventory(root):
    need(not root.is_symlink() and root.is_dir(),'invalid packet root');files={};dirs=set()
    def walk(d,prefix):
        for e in os.scandir(d):
            n=prefix+e.name;s=e.stat(follow_symlinks=False)
            need(not stat.S_ISLNK(s.st_mode),'symlink: '+n)
            if stat.S_ISDIR(s.st_mode):dirs.add(n);walk(Path(e.path),n+'/')
            else:
                need(stat.S_ISREG(s.st_mode),'nonregular member: '+n);need(s.st_size<=2000000,'oversized member: '+n);files[n]=Path(e.path).read_bytes()
    walk(root,'');return files,dirs

def authenticate(root):
    f,dirs=inventory(root);need('PUBLICATION_MANIFEST.json' in f,'missing manifest')
    need(sha(f['PUBLICATION_MANIFEST.json'])==MANIFEST_SHA,'manifest trust anchor')
    m=load(f['PUBLICATION_MANIFEST.json']);names=validate_manifest(m)
    need(set(f)==names|{'BOOTSTRAP.py','VERIFY_PUBLICATION.py','PUBLICATION_MANIFEST.json'},'file inventory mismatch')
    need(dirs=={str(p) for n in f for p in PurePosixPath(n).parents if str(p)!='.'},'directory inventory mismatch')
    need(f['VERIFY_PUBLICATION.py']==Path(__file__).read_bytes(),'different verifier copy')
    for row in m['files']:
        b=f[row['path']];need(len(b)==row['bytes'] and sha(b)==row['sha256'],'payload binding: '+row['path'])
    # Parse every JSON member with duplicate-key/nonfinite rejection before native code.
    for n,b in f.items():
        if n.endswith('.json'):load(b)
    for prefix,pin,count in [('author/',AUTHOR_SHA,8),('audit/',AUDIT_SHA,6)]:
        raw=f[prefix+'PUBLIC_MANIFEST.json'];need(sha(raw)==pin,'public manifest pin')
        inner=load(raw);need(inner['schema']=='empty-hexagons-public-derivative-v1' and type(inner['problem_id']) is int and inner['problem_id']==3091,'inner manifest identity')
        need(inner['excluded_self']=='PUBLIC_MANIFEST.json' and type(inner['files']) is list and len(inner['files'])==count,'inner manifest scope')
        seen={prefix+'PUBLIC_MANIFEST.json'}
        for row in inner['files']:
            need(type(row) is dict and set(row)=={'name','bytes','sha256'},'inner entry schema')
            n=prefix+row['name'];need(safe(n) and n not in seen,'inner duplicate');seen.add(n)
            need(n in f and type(row['bytes']) is int and row['bytes']==len(f[n]) and type(row['sha256']) is str and row['sha256']==sha(f[n]),'inner payload binding')
        need(seen=={n for n in f if n.startswith(prefix)},'inner inventory')
    budget=load(f['author/BUDGET.json'])
    for k,v in [('problem_id',3091),('rank_at_assignment',1058),('substantive_approach_budget',5),('substantive_approaches_used',5),('full_target_resolved',False),('complete_candidate_saved',False),('recommended_status','exhausted'),('novelty_claimed',False)]:need(equal(budget[k],v),'budget scope: '+k)
    fixtures=load(f['author/fixtures.json']);need(type(fixtures) is dict and set(fixtures)=={'schema','provenance','point_sets'} and equal(fixtures['schema'],1),'fixture schema/type')
    need(type(fixtures['provenance']) is str and fixtures['provenance']=='All point coordinates authored for this report; no third-party datasets.','fixture provenance')
    need(type(fixtures['point_sets']) is dict and len(fixtures['point_sets'])==7,'fixture sets')
    for pts in fixtures['point_sets'].values():
        need(type(pts) is list and bool(pts),'point list')
        for p in pts:need(type(p) is list and len(p)==2 and all(type(c) is int for c in p),'exact integer point')
    need(load(f['author/SOURCE_MANIFEST.json'])['source_documents_in_packet'] is False,'source-free scope')
    need(load(f['audit/PUBLIC_MANIFEST.json'])['status']=='accepted_elementary_partials_full_target_unresolved','audit disposition')
    return f

def process(script,args,cwd):
    flags=[] if sys.flags.optimize==0 else ['-O' if sys.flags.optimize==1 else '-OO']
    env={'PATH':'/usr/bin:/bin','HOME':str(cwd),'LANG':'C.UTF-8','PYTHONNOUSERSITE':'1','PYTHONDONTWRITEBYTECODE':'1','PYTHONSAFEPATH':'1'}
    p=subprocess.run([sys.executable,'-I','-S','-B',*flags,str(script),*map(str,args)],cwd=cwd,env=env,capture_output=True,timeout=240)
    need(p.returncode==0 and p.stderr==b'','native replay process failure: '+script.name)
    raw=p.stdout.decode('utf8');result=load(raw)
    return {'exit_code':p.returncode,'stdout':raw,'stderr':'','result':result}

def optional_inputs(f,a):
    out={'fresh_sources':'NOT_RUN','fresh_corpora':'NOT_RUN','fresh_source_inspection':'NOT_RUN','fresh_download':'NOT_RUN','fresh_record_join':'NOT_RUN','sat_replay':'NOT_RUN','lean_build':'NOT_RUN','witness_29_validation':'NOT_RUN'}
    def match(path,row):
        need(not path.is_symlink() and path.is_file(),'missing/nonregular optional input')
        need(stat.S_ISREG(path.stat().st_mode),'nonregular optional input');need(path.stat().st_size==row['bytes'],'optional input byte mismatch')
        b=path.read_bytes();need(sha(b)==row['sha256'],'optional input hash mismatch')
        return {'bytes':len(b),'sha256':sha(b)}
    if a.source_dir is not None:
        need(not a.source_dir.is_symlink() and a.source_dir.is_dir(),'invalid source directory')
        rows=[r for r in load(f['author/SOURCE_MANIFEST.json'])['sources'] if r.get('retrieved_bytes_verified') is True]
        out['source_matches']=[{'title':r['title'],'url':r['url'],**match(a.source_dir/r['retrieval_label'],r)} for r in rows]
        need(len(rows)==9,'source count');out['fresh_sources']='PASS_CURRENT_BYTE_REHASH'
    if a.problems is not None:
        rows=load(f['audit/DATASET_CHECKS.json'])['datasets']
        out['corpus_matches']=[{'name':r['name'],**match(p,r)} for p,r in zip([a.problems,a.research_results],rows)]
        need(len(rows)==2,'corpus count');out['fresh_corpora']='PASS_CURRENT_BYTE_REHASH'
    return out

def same_tree(a,b):
    if type(a) is not type(b):return False
    if type(a) is dict:return set(a)==set(b) and all(same_tree(a[k],b[k]) for k in a)
    if type(a) is list:return len(a)==len(b) and all(same_tree(x,y) for x,y in zip(a,b))
    return a==b

def compare_outputs(native,audit,receipt,probes,expected,mode):
    need(type(expected) is dict and set(expected)=={'schema','python_version','normalization','native_geometry','audit_driver','public_audit_receipt','cwd_write_probes'},'expected output schema')
    need(expected['schema']=='empty-hexagons-complete-expected-public-outputs-v1' and expected['python_version']=='3.12.14','expected output identity')
    need(same_tree(native,expected['native_geometry'][str(mode)]),'complete native geometry output mismatch')
    need(same_tree(audit,expected['audit_driver']),'complete audit driver output mismatch')
    need(same_tree(receipt,expected['public_audit_receipt']),'complete public audit output mismatch')
    need(same_tree(probes,expected['cwd_write_probes']),'complete cwd probe output mismatch')

def main():
    ap=argparse.ArgumentParser();ap.add_argument('root',type=Path);ap.add_argument('--integrity-only',action='store_true');ap.add_argument('--source-dir',type=Path);ap.add_argument('--problems',type=Path);ap.add_argument('--research-results',type=Path);a=ap.parse_args()
    need((a.problems is None)==(a.research_results is None),'both corpus inputs required')
    need(not a.integrity_only or (a.source_dir is None and a.problems is None),'optional inputs require full replay')
    root=a.root.absolute();before=authenticate(root)
    if a.integrity_only:return {'status':'PASS_PUBLICATION_INTEGRITY','problem_id':3091,'files':len(before),'full_target_resolved':False}
    need(os.getuid()==1000 and os.geteuid()==1000,'full replay requires actual/effective UID 1000')
    need(sys.version.split()[0]=='3.12.14','full expected-output replay requires Python 3.12.14')
    # Native readonly probes test genuine filesystem denials; this wrapper never chmods input.
    need(root.stat().st_mode & 0o222==0,'packet root has write bits')
    for p in root.rglob('*'):need(p.stat().st_mode & 0o222==0,'packet member has write bits')
    with tempfile.TemporaryDirectory(prefix='empty-hexagons-replay-') as td:
        temp=Path(td);cwd=temp/'readonly-cwd';cwd.mkdir();sentinel=cwd/'existing.txt';sentinel.write_text('read-only cwd probe\n');sentinel.chmod(0o444);cwd.chmod(0o555)
        probes=[]
        try:
            for target,mode in [(sentinel,'r+'),(cwd/'new.txt','x')]:
                try:fh=target.open(mode)
                except PermissionError:probes.append({'target':target.name,'operation':mode,'result':'PermissionError'})
                else:fh.close();raise Reject('cwd write probe succeeded')
            native=process(root/'author/check_geometry.py',['--readonly'],cwd)
            need(native['result']['status']=='PASS' and native['result']['uid']==1000 and native['result']['euid']==1000,'native identity/status')
            need(len(native['result']['write_probes'])==2 and all(r['result']=='PermissionError' for r in native['result']['write_probes']),'native write probes')
            output=temp/'audit.json';audit=process(root/'audit/replay_geometry.py',[root/'author',output],cwd)
            receipt=load(output.read_bytes());need(receipt['status']=='PASS' and receipt['public_author_unchanged'] is True,'audit replay status')
            expected={'native_geometry_passes':3,'independent_geometry_passes':3,'denied_write_probes':6,'semantic_control_rejections':24,'arbitrary_crashes_accepted':0}
            need(receipt['summary']==expected and all(type(v) is int for v in receipt['summary'].values()),'audit counts')
            need(len(receipt['runs'])==3 and [r['mode'] for r in receipt['runs']]==['normal','O','OO'],'audit modes')
            for row in receipt['runs']:
                for name in ['native_geometry','independent_geometry']:
                    r=row[name];need(equal(r['exit_code'],0) and r['stderr']=='' and r['result']['status']=='PASS' and load(r['stdout'])==r['result'],'whole native output')
                for name,count in [('semantic_controls',8)]:
                    need(len(row[name])==count,'mutation coverage')
                    for r in row[name]:need(equal(r['exit_code'],2) and r['stderr']=='' and r['result']['status']=='FAIL' and r['result']['error']==r['expected_error'] and load(r['stdout'])==r['result'],'specific mutation rejection')
            expected=load(before['EXPECTED_OUTPUTS.json'])
            compare_outputs(native,audit,receipt,probes,expected,sys.flags.optimize)
            optional=optional_inputs(before,a)
        finally:cwd.chmod(0o755)
    need(authenticate(root)==before,'input changed')
    return {'schema':'empty-hexagons-publication-replay-v1','status':'PASS_ACCEPTED_PARTIALS_REPLAY','problem_id':3091,'rank':1058,'disposition':'exhausted','turns':5,'full_target_resolved':False,'novelty_claimed':False,'formal_proof':False,'scope':'public derivative only; no original private-packet integrity claim','uid':os.getuid(),'euid':os.geteuid(),'optimization':sys.flags.optimize,'manifest_sha256':MANIFEST_SHA,'cwd_write_probes':probes,'native_geometry':native,'audit_driver':audit,'full_public_audit_receipt':receipt,'optional_inputs':optional,'originals_unchanged':True,'complete_expected_output_comparison':'PASS','expected_outputs_sha256':sha(before['EXPECTED_OUTPUTS.json']),'normalization':'none'}
if __name__=='__main__':
    try:print(json.dumps(main(),sort_keys=True,indent=2))
    except (Reject,OSError,ValueError,TypeError,KeyError,UnicodeError,subprocess.SubprocessError) as e:
        print('REJECT: '+str(e),file=sys.stderr);sys.exit(1)
