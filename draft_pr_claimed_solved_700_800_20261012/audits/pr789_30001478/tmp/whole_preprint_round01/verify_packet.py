"""Externally pinned flat audit custody and finite diagnostics; not formal proof/priority certification."""
from pathlib import Path,PurePosixPath
import argparse,hashlib,json,os,stat,subprocess,sys
HEAD='aa44dec3baf8c1cd179cf8b55f32be95c74ee81a'
SOURCE_MF='6287da0dabdad505f3d312dfeefc9e75f34caaeccb267fada3f9119502cfa6be'
SOURCE_CP='700eaab42e6d98589fb2f1c6fa4a3077b4dd74cad4f336a00cb53bd6dfe47489'
def need(ok,msg):
 if not ok:raise ValueError(msg)
def sha(b):return hashlib.sha256(b).hexdigest()
def pairs(xs):
 d={}
 for k,v in xs:need(k not in d,'duplicate JSON key');d[k]=v
 return d
def js(b):
 def bad(s):raise ValueError('nonfinite JSON')
 return json.loads(b,object_pairs_hook=pairs,parse_constant=bad)
def parents(p):
 p=Path(p).absolute()
 for q in [p,*p.parents]:need(stat.S_ISDIR(q.lstat().st_mode),'unsafe directory ancestry')
 return p
def read(p):
 p=Path(p).absolute();parents(p.parent);before=p.lstat()
 need(stat.S_ISREG(before.st_mode) and before.st_nlink==1,'nonregular or linked input')
 fd=os.open(p,os.O_RDONLY|os.O_NOFOLLOW|os.O_NONBLOCK)
 with os.fdopen(fd,'rb') as f:
  st=os.fstat(f.fileno());need((before.st_dev,before.st_ino)==(st.st_dev,st.st_ino),'changed before open');b=f.read();after=os.fstat(f.fileno())
 need((st.st_size,st.st_mtime_ns,st.st_ino)==(after.st_size,after.st_mtime_ns,after.st_ino) and len(b)==before.st_size,'changed during read')
 return b
def flat(n):
 need(isinstance(n,str) and bool(n) and '/' not in n and '\\' not in n and n not in ('.','..'),'unsafe flat filename');return n
def rel(n):
 p=PurePosixPath(n);need(isinstance(n,str) and bool(n) and '\\' not in n and not p.is_absolute() and all(x not in ('','.','..') for x in n.split('/')) and str(p)==n,'unsafe relative name');return n
def pinned_tree(s,pin):
 parents(s);files={};dirs=set()
 for cur,ds,fs in os.walk(s,followlinks=False):
  for n in ds:parents(Path(cur)/n);dirs.add((Path(cur)/n).relative_to(s).as_posix())
  for n in fs:
   p=Path(cur)/n;files[p.relative_to(s).as_posix()]=read(p)
 need(sha(files['MANIFEST.json'])==pin,'source manifest pin')
 mf=js(files['MANIFEST.json']);seen={}
 for r in mf['files']:
  n=rel(r['path']);need(n not in seen and n!='MANIFEST.json','source repeated row');seen[n]=r
 need(set(files)==set(seen)|{'MANIFEST.json'},'source closure')
 expected_dirs={str(p) for n in seen for p in PurePosixPath(n).parents if str(p)!='.'}
 need(dirs==expected_dirs,'source directory closure')
 for n,r in seen.items():need((len(files[n]),sha(files[n]))==(r['bytes'],r['sha256']),'source bytes')
 return files
def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--packet-root',type=Path,required=True);ap.add_argument('--expected-manifest-sha256',required=True);ap.add_argument('--expected-checker-sha256',required=True);ap.add_argument('--replay',action='store_true');ap.add_argument('--preprint-root',type=Path);a=ap.parse_args()
 root=parents(a.packet_root);selfpath=Path(__file__).absolute();need(selfpath==root/'verify_packet.py','checker/root mismatch')
 need(sha(read(selfpath))==a.expected_checker_sha256,'checker pin')
 raw=read(root/'MANIFEST.json');need(sha(raw)==a.expected_manifest_sha256,'external audit manifest pin')
 mf=js(raw);need(set(mf)=={'schema','files'} and mf['schema']=='whole-preprint-round01-closed/v1','audit schema')
 names=set();data={}
 for r in mf['files']:
  need(set(r)=={'path','bytes','sha256'} and type(r['bytes']) is int and r['bytes']>=0,'audit row schema')
  n=flat(r['path']);need(n not in names and n!='MANIFEST.json','audit repeated row');names.add(n);data[n]=read(root/n)
  need((len(data[n]),sha(data[n]))==(r['bytes'],r['sha256']),'audit bytes: '+n)
 need({p.name for p in root.iterdir()}==names|{'MANIFEST.json'},'flat packet closure')
 v=js(data['VERDICT.json']);need(v['head']==HEAD and v['pr']==789 and v['problem']==30001478 and v['prepared_version']=='1.0','target')
 need(v['result']=='PASS_WITH_NONBLOCKING_PORTABILITY_NOTE' and v['mathematical_issues']==[] and v['required_repairs']==[] and v['blocking_source_credit_priority_package_issues']==[],'verdict scope')
 need(v['priority']=='UNRESOLVED' and all(v[k] is False for k in ['firstness_certified','exhaustive_absence_certified','current_worldwide_open_status_certified']),'unsupported priority promotion')
 need(v['source_manifest_sha256']==SOURCE_MF and v['source_checker_sha256']==SOURCE_CP,'source pins')
 runs=js(data['SOURCE_REPRODUCTION_RUNS.json']);need(len(runs)==4 and all(r['returncode']==0 and r['stderr_bytes']==0 for r in runs),'four source runs')
 for r in runs:
  b=data[r['mode']+'.stdout.json'];need(sha(b)==r['stdout_sha256'],'source stdout binding');x=js(b)
  need(x['result']=='PASS' and x['source_files']==151 and x['original_files']==58 and x['external_evidence_files_rehashed']==0 and x['exact_head']==HEAD and len(x['finite_replay_processes'])==10,'source replay scope')
  need(all(t['status']=='PASS' and t['external_evidence_files_rehashed']==0 for t in x['finite_replay_processes']),'inner source status')
 need(js(data['OPTIONAL_BODY_CUSTODY.json'])['external_evidence_files_rehashed']==139,'optional count')
 need(js(data['PACKAGE_CHECKS.json'])['result']=='PASS' and len(js(data['PACKAGE_CHECKS.json'])['rebuilt_files'])==6,'package receipt')
 original=js(data['ORIGINAL_PUBLICATION_CONTROLS.json'])['runs'];need(original[0]['returncode']!=0 and 'nonregular invocation ancestry' in original[0]['stderr'],'default tmp caveat')
 need(len(original)==4 and all(r['returncode']==0 and js(r['stdout'])['named_control_count']==24 for r in original[1:]),'ordinary temp controls')
 source_count=distribution_count=0
 if a.preprint_root:
  p=parents(a.preprint_root);f=pinned_tree(p/'source',SOURCE_MF);need(len(f)==151 and sha(f['verify_source.py'])==SOURCE_CP,'source identity')
  identity=js(f['audit/intake/ROOT_SOURCE_IDENTITY.json']);need(identity['reviewed_head']==HEAD and len(identity['original_files'])==58,'original identity')
  for r in identity['original_files']:
   b=f['audit/intake/original/'+r['path']];need((len(b),sha(b))==(r['bytes'],r['sha256']) and hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==r['git_blob'],'original blob')
  rec=js(f['audit/intake/SELECTED_PUBLIC_RECORD.json']);need(sha(json.dumps([rec['problem'],rec['prior_research']],sort_keys=True).encode())=='cf0071b62b0e096c74205deac1c8f7cad50cbbf50b4f37d8400170a2d742848f','selected full pair')
  for r in js(data['PACKAGE_CHECKS.json'])['rebuilt_files']:
   b=read(p/rel(r['path']));need((len(b),sha(b))==(r['bytes'],r['sha256']),'distribution bytes')
  source_count=151;distribution_count=6
 if a.replay:
  for opt in [False,True]:
   cmd=[sys.executable,'-I','-B']+(['-O']if opt else[])+[str(root/'check_independent.py')]
   p=subprocess.run(cmd,cwd='/',capture_output=True,timeout=60);need(p.returncode==0 and not p.stderr,'independent replay')
   need(js(p.stdout)==js(data['INDEPENDENT_CHECKS.json'])==js(data['INDEPENDENT_CHECKS_OPTIMIZED.json']),'independent receipt')
 print(json.dumps({'result':'PASS','authored_files':len(data)+1,'fresh_source_files_authenticated':source_count,'fresh_distribution_files_authenticated':distribution_count,'external_body_files_freshly_hashed_by_this_checker':0,'recorded_optional_body_count':139,'independent_diagnostics_replayed':a.replay,'priority':'UNRESOLVED','nonblocking_findings':1,'scope':'Closed audit custody, recorded receipts and optional finite diagnostics/current-source authentication; not formal proof, exhaustive literature or firstness certification.'},sort_keys=True))
if __name__=='__main__':
 try:main()
 except Exception as e:print('REJECT: '+str(e),file=sys.stderr);sys.exit(1)
