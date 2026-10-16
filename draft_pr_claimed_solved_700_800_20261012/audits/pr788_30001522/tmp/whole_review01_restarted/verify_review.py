"""Verify a closed whole-review packet against external manifest and checker pins.

Optional primary custody checks concern the newly fetched 23 files only, never the
historical 76-file bank. A successful integrity replay does not certify topology.
"""
import argparse,hashlib,json,os,stat,subprocess,sys
from pathlib import Path,PurePosixPath
sys.dont_write_bytecode=True

def need(x,m):
    if not x:raise ValueError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
def ident(b):return {'bytes':len(b),'sha256':sha(b)}
def unique(pairs):
    d={}
    for k,v in pairs:need(k not in d,'Duplicate JSON key');d[k]=v
    return d
def parse(b):
    def reject(x):raise ValueError('Nonfinite JSON')
    return json.loads(b,object_pairs_hook=unique,parse_constant=reject)
def name(n):
    need(isinstance(n,str)and n and not PurePosixPath(n).is_absolute()and'\\'not in n and all(p not in('','.','..')for p in n.split('/'))and str(PurePosixPath(n))==n,'Unsafe relative name');return n
def read(p):
    need(stat.S_ISREG(p.lstat().st_mode),'Nonregular input')
    fd=os.open(p,os.O_RDONLY|os.O_NOFOLLOW|os.O_NONBLOCK)
    with os.fdopen(fd,'rb')as f:need(stat.S_ISREG(os.fstat(f.fileno()).st_mode),'Nonregular opened input');return f.read()
def at(root,n):
    p=root
    for part in name(n).split('/'):
        p=p/part;need(not p.is_symlink(),'Input symlink')
    return read(p)
def pin(p):need(isinstance(p,str)and len(p)==64 and all(c in'0123456789abcdef'for c in p),'Invalid external pin')
def verify(a):
    pin(a.manifest_sha256);pin(a.checker_sha256)
    root=a.packet_root.absolute();need(root.is_dir()and not root.is_symlink(),'Packet root')
    need(sha(read(root/'verify_review.py'))==a.checker_sha256,'Checker external pin mismatch')
    raw=read(root/'MANIFEST.json');need(sha(raw)==a.manifest_sha256,'Manifest external pin mismatch')
    m=parse(raw);need(m['schema']=='whole-preprint-review-closed-v1','Manifest schema')
    expected={}
    for r in m['files']:
        n=name(r['path']);need('/'not in n and n!='MANIFEST.json'and n not in expected,'Nonflat/repeated/self manifest entry')
        need(set(r)=={'path','bytes','sha256'}and type(r['bytes'])is int and r['bytes']>=0,'Manifest entry');pin(r['sha256']);expected[n]={'bytes':r['bytes'],'sha256':r['sha256']}
    children=list(root.iterdir());need({p.name for p in children}==set(expected)|{'MANIFEST.json'},'Packet inventory differs')
    payload={p.name:read(p)for p in children}
    for n,e in expected.items():need(ident(payload[n])==e,'Packet payload differs: '+n)
    binds=parse(payload['INPUT_BINDINGS.json']);p=a.preprint_root.absolute();need(p.is_dir()and not p.is_symlink(),'Preprint root')
    for r in binds['preprint_files']:need(ident(at(p,r['path']))=={k:r[k]for k in('bytes','sha256')},'Release/inventory bytes differ: '+r['path'])
    source=p/'source';need(source.is_dir()and not source.is_symlink(),'Source root')
    rows=binds['closed_source_files'];expected_names={name(r['path'])for r in rows};need(len(expected_names)==len(rows),'Repeated source binding')
    actual=set();directories=set()
    for q in source.rglob('*'):
        need(not q.is_symlink(),'Source symlink')
        if q.is_dir():directories.add(q.relative_to(source).as_posix())
        else:actual.add(q.relative_to(source).as_posix())
    need(actual==expected_names,'Closed source inventory differs')
    needed_dirs={z.as_posix()for n in expected_names for z in Path(n).parents if z.as_posix()!='.'}
    need(directories==needed_dirs,'Unexpected empty source directory')
    for r in rows:need(ident(at(source,r['path']))=={k:r[k]for k in('bytes','sha256')},'Source bytes differ: '+r['path'])
    need(sha(at(source,'MANIFEST.json'))==binds['target']['source_manifest_sha256'],'Source manifest target pin')
    ledger=parse(payload['SOURCE_READ_LEDGER.json']);primary_count=0
    if a.primary_root:
        pr=a.primary_root.absolute();need(pr.is_dir()and not pr.is_symlink(),'Fresh primary root')
        for r in ledger['fresh_optional_primary_files']:
            need(ident(at(pr,r['path']))=={k:r[k]for k in('bytes','sha256')},'Fresh primary bytes differ: '+r['path']);primary_count+=1
    replays=[]
    if a.replay:
        for o in(False,True):
            cmd=[sys.executable,'-I','-B']+(['-O']if o else[])+[str(root/'independent_checks.py')]
            r=subprocess.run(cmd,cwd='/',capture_output=True,text=True,timeout=60)
            need(r.returncode==0 and not r.stderr,'Independent diagnostic execution')
            need(parse(r.stdout)==parse(payload['INDEPENDENT_CHECK_RESULTS.json']),'Independent diagnostic result differs');replays.append({'kind':'independent','optimized':o,'status':'PASS'})
        cmd=[sys.executable,'-I','-B',str(source/'verify_source.py'),'--expected-manifest-sha256',binds['target']['source_manifest_sha256'],'--pdf',str(p/'output/pdf/paper.pdf'),'--replay']
        r=subprocess.run(cmd,cwd='/',capture_output=True,text=True,timeout=300)
        need(r.returncode==0 and not r.stderr,'Portable source replay')
        out=parse(r.stdout);need(out['result']=='PASS'and out['source_files']==192 and out['original_files']==48 and out['authored_input_bindings_checked']==183 and out['external_evidence_files_rehashed']==0 and len(out['finite_replay_processes'])==10,'Source replay scope')
        replays.append({'kind':'portable_source','status':'PASS','finite_processes':10,'historical_external_files_rehashed':0})
    for n,e in expected.items():need(ident(read(root/n))==e,'Packet changed during replay')
    need(read(root/'MANIFEST.json')==raw,'Manifest changed during replay')
    return {'result':'PASS','packet_files_including_manifest':len(payload),'source_files':len(rows),'release_and_inventory_files':len(binds['preprint_files']),'fresh_primary_files_rehashed':primary_count,'historical_76_custody_reproduced':False,'replays':replays,'scope':'Externally pinned authored custody and finite replay; written mathematics, human read scopes and unresolved priority require substantive assessment.'}
def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--packet-root',type=Path,default=Path(__file__).absolute().parent)
    p.add_argument('--preprint-root',type=Path,required=True)
    p.add_argument('--manifest-sha256',required=True);p.add_argument('--checker-sha256',required=True)
    p.add_argument('--primary-root',type=Path);p.add_argument('--replay',action='store_true');a=p.parse_args()
    try:out=verify(a)
    except Exception as e:print(json.dumps({'result':'FAIL','error':str(e)}));return 1
    print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=='__main__':sys.exit(main())
