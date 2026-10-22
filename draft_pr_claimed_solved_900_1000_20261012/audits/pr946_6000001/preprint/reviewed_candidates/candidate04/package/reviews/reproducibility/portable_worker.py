"""Authenticated finite replay worker. Caller must externally authenticate this file."""
import sys
if not (sys.flags.isolated and sys.dont_write_bytecode and sys.flags.optimize==0 and __debug__):
 raise SystemExit('REJECTED: worker requires isolated nonoptimized Python with bytecode disabled')
import argparse,hashlib,json,runpy,subprocess,os
from pathlib import Path

def require(ok,msg):
 if not ok:raise RuntimeError(msg)
def sha(raw):return hashlib.sha256(raw).hexdigest()
def pairs(rows):
 out={}
 for key,value in rows:
  require(key not in out,'Duplicate JSON key');out[key]=value
 return out
def parse(raw):return json.loads(raw,object_pairs_hook=pairs,parse_constant=lambda x:(_ for _ in ()).throw(ValueError('Nonfinite JSON')))
def exact(actual,expected,path=()):
 require(type(actual) is type(expected),'Exact type mismatch '+str(path))
 if type(expected) is dict:
  require(set(actual)==set(expected),'Exact key mismatch '+str(path))
  for k in expected:exact(actual[k],expected[k],path+(k,))
 elif type(expected) is list:
  require(len(actual)==len(expected),'Exact list size mismatch '+str(path))
  for i,(a,e) in enumerate(zip(actual,expected)):exact(a,e,path+(i,))
 else:require(actual==expected,'Exact value mismatch '+str(path))
BOOT='''import sys,json,runpy
print(json.dumps(dict(optimize=sys.flags.optimize,debug=__debug__,isolated=sys.flags.isolated,bytecode_disabled=sys.dont_write_bytecode)),file=sys.stderr)
if sys.flags.optimize!=0 or not __debug__ or not sys.flags.isolated or not sys.dont_write_bytecode:raise SystemExit('REJECTED: unsafe original child mode')
p=sys.argv[1];sys.argv=sys.argv[1:];runpy.run_path(p,run_name='__main__')
'''
def main():
 p=argparse.ArgumentParser();p.add_argument('packet',type=Path);p.add_argument('comparator',type=Path);p.add_argument('comparator_sha256');p.add_argument('--test-false-assert',action='store_true');a=p.parse_args()
 if a.test_false_assert:assert False,'Intentional worker assertion control'
 require(sha(a.comparator.read_bytes())==a.comparator_sha256,'Comparator anchor mismatch')
 compare=runpy.run_path(str(a.comparator))['compare'];root=a.packet
 raw=(root/'PUBLIC_MANIFEST.json').read_bytes();require(sha(raw)=='29cb50b07af6a65b633516b5d86eed1dae93d57cf2abfb264b18eb9555a29903','Original manifest anchor')
 rows=parse(raw)['files'];before={'PUBLIC_MANIFEST.json':raw}
 for row in rows:
  raw=(root/row['path']).read_bytes();require(len(raw)==row['bytes'] and sha(raw)==row['sha256'],'Original payload hash');before[row['path']]=raw
 require({str(q.relative_to(root)) for q in root.rglob('*') if q.is_file()}==set(before),'Worker closed inventory')
 frozen={'public':'7df56d745e4c57a30d0303388b1adda3e52d1c99190d2f96fe50b6d616b1cf3f','independent_global_audit/public':'22d1bab327e70db3d594c2580f592256bb342bd33c1081fa07beb1c197f0edff','independent_audit_b/public':'8bbb5b62a4610881e7b1f78a52f7c208723529304dd0e8ab341a1be9f1283459'}
 checks=[('public/verify_packet.py',['--expected-manifest',frozen['public']],None),('independent_global_audit/public/verify_audit_packet.py',['--author-public',str(root/'public')],None),('independent_audit_b/public/verify_audit.py',['--expected-manifest',frozen['independent_audit_b/public'],'--author-dir',str(root/'public')],None),('public/verify_math.py',[],'public/VERIFICATION.json'),('independent_global_audit/public/independent_controls.py',[],'independent_global_audit/public/INDEPENDENT_CONTROLS.json'),('independent_audit_b/public/independent_checks.py',[],'independent_audit_b/public/INDEPENDENT_CHECKS.json')]
 records=[];env={k:v for k,v in os.environ.items() if not k.upper().startswith('PYTHON')}
 for name,extra,recorded in checks:
  cmd=[sys.executable,'-I','-B','-c',BOOT,str(root/name),*extra];r=subprocess.run(cmd,cwd=root.parent,env=env,capture_output=True,text=True,timeout=300)
  require(r.returncode==0,'Original child failed '+name+'\n'+r.stderr)
  flags=parse(r.stderr.splitlines()[0]);exact(flags,dict(optimize=0,debug=True,isolated=1,bytecode_disabled=True))
  actual=parse(r.stdout);require(actual.get('status',actual.get('verdict'))=='PASS','Original did not PASS')
  if recorded:
   expected=parse(before[recorded])
   if recorded=='public/VERIFICATION.json':compare(actual,expected)
   else:
    cleanA=dict(actual);cleanE=dict(expected)
    key='sympy_version' if recorded.endswith('INDEPENDENT_CONTROLS.json') else 'versions';cleanA.pop(key,None);cleanE.pop(key,None);exact(cleanA,cleanE)
  records.append(dict(script=name,status='PASS',actual_child_flags=flags,stdout_sha256=sha(r.stdout.encode()),comparison='12-explicit-float bounded comparator; other fields exact and typed' if recorded=='public/VERIFICATION.json' else 'version-only fields removed; all other fields exact and typed' if recorded else 'original authenticated inventory checker'))
 for name,raw in before.items():require((root/name).read_bytes()==raw,'Original copy changed during replay '+name)
 require({str(q.relative_to(root)) for q in root.rglob('*') if q.is_file()}==set(before),'Replay changed closed inventory')
 print(json.dumps(dict(status='PASS',actual_worker_flags=dict(optimize=sys.flags.optimize,debug=__debug__,isolated=sys.flags.isolated,bytecode_disabled=sys.dont_write_bytecode),original_files=33,replays=records,limitation='Finite identities and bounded numerical consistency only; no global proof, priority, OS sandbox, or byte-identical numeric replay claim.'),indent=2))
if __name__=='__main__':
 try:main()
 except Exception as exc:raise SystemExit('REJECTED: '+str(exc))
