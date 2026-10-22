from pathlib import Path
import sys,json,shutil,tempfile,subprocess,hashlib,os
R=Path(__file__).resolve().parent;A=R.parents[1];E=A.parents[1];P=E/'private/pr0280_package_adversary_03';base=R/'archive/birational-cycle-verification'
cases=[]
def run(label,mutate):
 for flags in [[],['-O']]:
  with tempfile.TemporaryDirectory(dir=P,prefix='archive_hostile_') as d:
   out=Path(d)/'pkg';shutil.copytree(base,out);m=json.loads((out/'MANIFEST.json').read_text());mutate(out,m)
   p=subprocess.run([sys.executable,*flags,'-B',str(out/'verify.py')],capture_output=True,text=True,timeout=20)
   if p.returncode==0:raise RuntimeError('Hostile case accepted: '+label)
   cases.append({'case':label,'optimization':bool(flags),'exit':p.returncode,'last_error':p.stderr.splitlines()[-1] if p.stderr else ''})
def mset(k,v):return lambda p,m:((m.update({k:v})),(p/'MANIFEST.json').write_text(json.dumps(m)))
run('schema_true',mset('schema',True));run('schema_float',mset('schema',1.0));run('schema_string',mset('schema','1'));run('schema_unknown',mset('schema',2));run('unknown_top_field',mset('extra',1))
for field,val,label in [('bytes',True,'bytes_bool'),('bytes',1.0,'bytes_float'),('sha256','0'*64,'hash_changed'),('path','../escape','path_traversal'),('path','/escape','absolute_path'),('path','a\\b','windows_path'),('path','./README.md','path_alias')]:
 def mut(p,m,field=field,val=val):m['files'][0][field]=val;(p/'MANIFEST.json').write_text(json.dumps(m))
 run(label,mut)
run('duplicate_manifest_entry',lambda p,m:(m['files'].append(dict(m['files'][0])),(p/'MANIFEST.json').write_text(json.dumps(m))))
run('entry_extra_field',lambda p,m:(m['files'][0].update(extra=1),(p/'MANIFEST.json').write_text(json.dumps(m))))
run('extra_file',lambda p,m:(p/'extra').write_text('x'))
run('deleted_payload',lambda p,m:(p/'README.md').unlink())
run('payload_tampered',lambda p,m:(p/'README.md').write_text('changed'))
run('extra_fifo',lambda p,m:os.mkfifo(p/'extra_fifo'))
def symlink_payload(p,m):q=p/'README.md';q.unlink();q.symlink_to(base/'README.md')
run('symlink_payload',symlink_payload)
def symlink_manifest(p,m):q=p/'MANIFEST.json';q.unlink();q.symlink_to(base/'MANIFEST.json')
run('symlink_manifest',symlink_manifest)
def wrong_expected(p,m):
 q=p/'expected_checks.json';v=json.loads(q.read_text());v['exact_checks']+=1;q.write_text(json.dumps(v));b=q.read_bytes()
 for e in m['files']:
  if e['path']=='expected_checks.json':e.update(bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
 (p/'MANIFEST.json').write_text(json.dumps(m))
run('rehashed_wrong_finite_expected',wrong_expected)
res={'status':'PASS','distinct_hostile_cases':len(cases)//2,'rejections':len(cases),'cases':cases,'scope':'Independent cases against copied current actual verifier; no canonical edits'}
(R/'HOSTILE_ARCHIVE_RESULTS.json').write_text(json.dumps(res,indent=2)+'\n');print(json.dumps({k:v for k,v in res.items() if k!='cases'}))
