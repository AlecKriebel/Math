"""Freeze actual remote PR file objects without reading mathematical result prose."""
from pathlib import Path
import datetime,hashlib,json,subprocess,sys
P=Path(__file__).resolve().parent;n=int(sys.argv[1]);problem=sys.argv[2]
assert n!=8
A=P/'audits'/f'pr{n}_{problem}';A.mkdir(parents=True,exist_ok=True)
assert not (A/'snapshot_manifest.json').exists()
def run(args,label):
 r=subprocess.run(args,capture_output=True);(A/(label+'.stdout')).write_bytes(r.stdout);(A/(label+'.stderr')).write_bytes(r.stderr)
 assert r.returncode==0,(label,r.returncode,r.stderr.decode());return r.stdout
meta=json.loads(run(['gh','api',f'repos/AlecKriebel/Math/pulls/{n}'],'freeze_metadata'))
assert meta['state']=='open' and meta['draft'];head=meta['head']['sha'];base=meta['base']['sha']
pages=json.loads(run(['gh','api','--paginate','--slurp',f'repos/AlecKriebel/Math/pulls/{n}/files'],'freeze_files'))
files=[e for page in pages for e in page];paths=[e['filename'] for e in files];assert len(paths)==len(set(paths))
queue='unsolved_math_prioritization/QUEUE.md';prefixes={str(Path(p).parent) for p in paths if p!=queue}
if all(p.startswith(f'unsolved_math_prioritization/attempts/{problem}/') for p in paths if p!=queue):prefix=f'unsolved_math_prioritization/attempts/{problem}'
else:
 candidates={p.split('/')[1] for p in paths if p.startswith('problems/')};assert len(candidates)==1 and next(iter(candidates)).startswith(problem+'_');prefix='problems/'+next(iter(candidates))
assert queue in paths and all(p==queue or p.startswith(prefix+'/') for p in paths),paths
run(['git','fetch','origin',f'refs/pull/{n}/head'],'freeze_fetch')
git=lambda *args:subprocess.check_output(['git',*args])
assert git('rev-parse','FETCH_HEAD').decode().strip()==head
assert set(git('diff','--name-only',base,head).decode().splitlines())==set(paths)
out=[];S=A/'snapshot'
for e in sorted(files,key=lambda x:x['filename']):
 path=e['filename'];assert '..' not in Path(path).parts and not Path(path).is_absolute()
 b=git('show',head+':'+path);blob=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest();assert blob==e['sha']
 f=S/path;f.parent.mkdir(parents=True,exist_ok=True);f.write_bytes(b)
 out.append({'path':path,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'git_blob_sha':blob,'status':e['status']})
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
(A/'remote_original.json').write_text(json.dumps(meta,indent=2)+'\n')
(A/'snapshot_manifest.json').write_text(json.dumps({'pr':n,'head':head,'base':base,'frozen_utc':now,'target_prefix':prefix,'files':out},indent=2)+'\n')
(A/'README.md').write_text(f'# Descending audit PR{n}: {problem}\n\nFrozen head `{head}`, base `{base}`. All{len(out)} actual Git/API bindings preserved. Workflow5%, original resolution0%. No candidate proof/code/historical review read; exact problem and claims remain hypotheses until source-first validation.\n')
(A/'RESEARCH_LOG.md').write_text(f'# PR{n} research log\n\n{now}: workflow5%, original resolution0%. Freeze{len(out)} actual Git/API paths/{len(out)-1} target files before mathematical reading. Main remains unchanged, no external individual communication. Only live PR body/metadata and filenames read for routing.\n')
print(json.dumps({'pr':n,'head':head,'base':base,'prefix':prefix,'paths':len(out),'target':len(out)-1,'workflow_percent':5}))
