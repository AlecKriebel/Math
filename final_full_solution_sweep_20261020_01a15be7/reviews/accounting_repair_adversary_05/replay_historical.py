from pathlib import Path
import datetime as dt,hashlib,json,os,subprocess,sys
Q=Path(__file__).resolve().parent
def now():return dt.datetime.now(dt.timezone.utc).isoformat()
def sha(b):return hashlib.sha256(b).hexdigest()
def save(p,d):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(d,indent=2)+'\n')
# Correctly preserve the captured old code separately from deliberately replaced mounts.
m=json.loads((Q/'INPUT_MANIFEST.json').read_text());mounts=[]
for e in m['files']:
 if e['path'].startswith('replay/') and e['path'].endswith('/inputs/current/coverage_snapshot.py'):
  old=Path(e['source']).read_bytes();assert len(old)==e['bytes'] and sha(old)==e['sha256'];name=e['path'].split('/')[1];p=Q/'mount_originals'/name/'coverage_snapshot.py';p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(old);mounted_path=e['path'];e['path']=str(p.relative_to(Q));new=(Q/mounted_path).read_bytes();mounts.append(dict(path=mounted_path,bytes=len(new),sha256=sha(new),source='inputs/current/coverage_snapshot.py',purpose='Only code under test replaced; historical inputs/expectations unmodified'))
save(Q/'INPUT_MANIFEST.json',m);save(Q/'REPLAY_MOUNTS.json',dict(at=now(),mounts=mounts,note='Capture program originally recorded historical code at its later replaced mount path. Before any replay, old code bytes were preserved separately and input-manifest paths corrected; historical test logic/expectations/results unchanged.'))
results=[]
for folder,name in [('prior','controls.py'),('prior','supplementary.py'),('new03','new_controls.py'),('new04','new_controls.py')]:
 p=Q/'replay'/folder;x=subprocess.run([sys.executable,'-B',str(p/name)],cwd=p,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1','GIT_OPTIONAL_LOCKS':'0'},capture_output=True);(p/(name+'.stdout')).write_bytes(x.stdout);(p/(name+'.stderr')).write_bytes(x.stderr);assert x.returncode==0,(folder,name,x.stderr.decode()[-1000:]);print(folder,name,'complete',flush=True)
for rel in ['prior/CONTROL_RESULTS.json','prior/SUPPLEMENTARY_RESULTS.json','new03/NEW_CONTROL_RESULTS.json','new04/NEW_CONTROL_RESULTS.json']:
 p=Q/'replay'/rel;a=json.loads(p.read_text())['results'];bad=[]
 for x in a:
  exploratory=x['expected_reject'] is None or (rel.startswith('new04/') and x.get('family')=='source_semantics')
  if not exploratory and x['accepted']==x['expected_reject']:bad.append(x['name'])
 assert not bad,(rel,bad);results.append(dict(path=str(p.relative_to(Q)),executions=len(a),sha256=sha(p.read_bytes()),pass_=True))
save(Q/'HISTORICAL_REPLAY.json',dict(at=now(),results=results,executions=sum(x['executions'] for x in results),adjudication='new04 source_semantics is exploratory under unchanged sealed CONTROL_ADJUDICATION; none of those historical assertions/outputs rewritten. Other None cases also exploratory.'))
print(json.dumps(results))
