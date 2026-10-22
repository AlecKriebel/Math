"""Adapted from sealed05 replayed04_extended_transport_controls.py SHA256 c1996551845a37c5112a73e4a1f04859a61fb14f8bf8b45b5184ac7e149c91b1. Only owned scratch/output path changes. All external clients fake.
"""
import sys
if not sys.flags.isolated:raise RuntimeError('Use -I')
from pathlib import Path
import base64,datetime,hashlib,json,os,shutil,subprocess
R=Path('/Users/alec/Documents/Math');O=Path(__file__).absolute().parent;PK=O/'private/cold';Y=R/'draft_pr_claimed_solved_900_1000_20261012/audits/pr906_30006419/reviews/computation_family/tmp/venv/bin/python'
def h(b):return hashlib.sha256(b).hexdigest()
m=json.loads((PK/'PACKAGE_MANIFEST.json').read_bytes());assert h((PK/'PACKAGE_MANIFEST.json').read_bytes())=='52165ba2410fa32238244feef20820e5bca9971f60c90542a2360f4d44e6c4ec'
for n,pin in m['files'].items():
 b=(PK/n).read_bytes();assert len(b)==pin['bytes'] and h(b)==pin['sha256']
T=O/'private/extended_package_retry';shutil.copytree(PK,T);env={k:v for k,v in os.environ.items() if not k.upper().startswith('PYTHON')};env['TMPDIR']=str(O/'private/temp');BOOT='import sys,base64;raw=base64.b64decode(sys.argv[1],validate=True);p=sys.argv[2];sys.argv=sys.argv[2:];exec(compile(raw,p,"exec"),dict(__name__="__main__",__file__=p))';rows=[]
for name,args in [('original/unsolved_math_prioritization/attempts/6000001/mutation_tests.py',['29cb50b07af6a65b633516b5d86eed1dae93d57cf2abfb264b18eb9555a29903',str(T/'original/unsolved_math_prioritization/attempts/6000001')]),('reviews/reproducibility/repair_v2/test_nonblocking.py',[]),('reviews/reproducibility/repair_v2/test_links.py',[])]:
 b=(T/name).read_bytes();pin=m['files'][name];assert h(b)==pin['sha256'];p=subprocess.run([str(Y),'-I','-S','-B','-c',BOOT,base64.b64encode(b).decode(),str(T/name),*args],capture_output=True,text=True,cwd=T,env=env,timeout=1200)
 (O/'private'/('extended_'+Path(name).stem+'.stdout')).write_text(p.stdout);(O/'private'/('extended_'+Path(name).stem+'.stderr')).write_text(p.stderr)
 if p.returncode:raise RuntimeError(name+' '+p.stderr+' '+p.stdout)
 if name.endswith('mutation_tests.py'):r=json.loads(p.stdout);(O/'ORIGINAL_MUTATIONS_REPLAY.json').write_text(json.dumps(r,indent=2)+'\n');count=r['negative_controls']
 else:
  report=T/'reviews/reproducibility/repair_v2/evidence'/('NONBLOCKING_TESTS.json' if 'nonblocking' in name else 'LINK_TESTS.json');r=json.loads(report.read_bytes());count=r['nonblocking_negative_controls'] if 'nonblocking' in name else r['negative_controls'];(O/('V2_NONBLOCKING_REPLAY.json' if 'nonblocking' in name else 'V2_LINK_REPLAY.json')).write_text(json.dumps(r,indent=2)+'\n')
 rows.append({'script':name,'script_sha256':h(b),'returncode':p.returncode,'negative_controls':count});print(name,count,'PASS',flush=True)
(O/'EXTENDED_TRANSPORT_CONTROLS.json').write_text(json.dumps({'status':'PASS','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'controls':rows,'execution':'Captured authenticated code; entire own package copy; scripts unmodified, all scratch/evidence writes only to own mirror. OS temp children redirected by TMPDIR.','canonical_writes':0},indent=2)+'\n')
