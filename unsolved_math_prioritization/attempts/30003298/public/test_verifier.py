from pathlib import Path
import hashlib,json,shutil,subprocess,sys,tempfile,os
ROOT=Path(__file__).resolve().parent
BASE=ROOT

def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def rebind(p):
 m=json.loads((p/'MANIFEST.json').read_text())
 for e in m['files']:
  f=p/e['name']
  if f.is_file(): e.update(bytes=f.stat().st_size,sha256=digest(f))
 (p/'MANIFEST.json').write_text(json.dumps(m,indent=2)+'\n')
def claim(p,key,value):
 c=json.loads((p/'CLAIMS.json').read_text());c[key]=value
 (p/'CLAIMS.json').write_text(json.dumps(c));rebind(p)
def edit_manifest(p,fn):
 m=json.loads((p/'MANIFEST.json').read_text());fn(m)
 (p/'MANIFEST.json').write_text(json.dumps(m))
def bad_json(p):
 (p/'CLAIMS.json').write_text('{');rebind(p)
def duplicate_json(p):
 s=(p/'CLAIMS.json').read_text();(p/'CLAIMS.json').write_text(s.replace('{','{"problem_id": 30003298,',1));rebind(p)
def changed_proof(p):
 (p/'PROOF.md').write_text((p/'PROOF.md').read_text()+'\nChanged.\n')
def extra_source(p):(p/'source.pdf').write_bytes(b'%PDF-1.4 fake')
def symlink(p):
 (p/'README.md').unlink();(p/'README.md').symlink_to(BASE/'README.md')
MUTATIONS=[
 ('wrong-solved-genus',lambda p:claim(p,'target_solved_genera',[2,3])),
 ('wrong-general-solution',lambda p:claim(p,'general_target_solved',True)),
 ('wrong-coefficient',lambda p:claim(p,'coefficient','H^(2g-2)(C_g;Z)')),
 ('wrong-proved-degree',lambda p:claim(p,'proved_degree',[2,-1])),
 ('wrong-review-status',lambda p:claim(p,'independent_review','accepted')),
 ('wrong-approach-count',lambda p:claim(p,'approaches',4)),
 ('malformed-claim-type',lambda p:claim(p,'genus_min',True)),
 ('extra-claim-field',lambda p:claim(p,'unsupported',True)),
 ('malformed-claim-json',bad_json),('duplicate-json-key',duplicate_json),
 ('changed-proof-without-rebinding',changed_proof),('unexpected-source-file',extra_source),
 ('symlink-member',symlink),('missing-proof',lambda p:(p/'PROOF.md').unlink()),
 ('manifest-byte-mismatch',lambda p:edit_manifest(p,lambda m:m['files'][0].update(bytes=0))),
 ('manifest-hash-mismatch',lambda p:edit_manifest(p,lambda m:m['files'][0].update(sha256='0'*64))),
 ('manifest-unsafe-path',lambda p:edit_manifest(p,lambda m:m['files'][0].update(name='../PROOF.md'))),
 ('manifest-duplicate-path',lambda p:edit_manifest(p,lambda m:m['files'][0].update(name=m['files'][1]['name']))),
 ('malformed-manifest-schema',lambda p:edit_manifest(p,lambda m:m.update(schema=True))),
 ('missing-manifest',lambda p:(p/'MANIFEST.json').unlink()),
]
report={'modes':[],'negative_tests_per_mode':len(MUTATIONS),'read_only_relocation':True,'not_formal_math_verification':True}
outputs=[]
for mode in [[],['-O'],['-OO']]:
 with tempfile.TemporaryDirectory(prefix='mapping-cohomology-test-') as t:
  tmp=Path(t);good=tmp/'read-only-packet';shutil.copytree(BASE,good)
  before={p.name:digest(p) for p in good.iterdir()}
  for p in good.iterdir():p.chmod(0o444)
  good.chmod(0o555)
  probe=subprocess.run([sys.executable,'-c',f"from pathlib import Path; Path({str(good/'write-probe')!r}).write_text('bad')"],capture_output=True,text=True)
  if probe.returncode==0:raise RuntimeError('read-only permission probe unexpectedly wrote')
  command=[sys.executable,*mode,'-B',str(good/'verify.py')]
  result=subprocess.run(command,cwd=tmp,capture_output=True,text=True)
  if result.returncode:raise RuntimeError(result.stderr)
  if before!={p.name:digest(p) for p in good.iterdir()}:raise RuntimeError('verifier wrote to read-only packet')
  outputs.append(result.stdout)
  good.chmod(0o755)
  for p in good.iterdir():p.chmod(0o644)
  failures=[]
  for name,mutate in MUTATIONS:
   target=tmp/name;shutil.copytree(BASE,target);mutate(target)
   r=subprocess.run([sys.executable,*mode,'-B',str(target/'verify.py')],cwd=tmp,capture_output=True,text=True)
   if r.returncode==0:raise RuntimeError('negative control accepted: '+name+' '+str(mode))
   failures.append({'name':name,'returncode':r.returncode,'stderr':r.stderr.strip()})
  report['modes'].append({'mode':' '.join(mode) or 'normal','output':json.loads(result.stdout),'negative_controls':failures,'read_only_write_probe_rejected':True})
if len(set(outputs))!=1:raise RuntimeError('optimized output mismatch')
report['all_mode_outputs_identical']=True
print(json.dumps({'status':'PASS','checks_per_mode':report['modes'][0]['output']['checks'],'modes':3,'negative_controls_per_mode':len(MUTATIONS),'read_only_relocation':True,'same_outputs':True}))
