import hashlib,json,os,stat,subprocess,zipfile
from pathlib import Path
R=Path(__file__).absolute().parent; A=R.parent.parent
sha=lambda b:hashlib.sha256(b).hexdigest()
freeze=json.loads((A/'WHOLE_PACKAGE_REVIEW_INPUTS.json').read_bytes())
paths={**{'publication/'+n:p for n,p in freeze['publication_files'].items()},**{n:{'sha256':p} for n,p in freeze['helper_sha256'].items()},**freeze['gate_bindings']}
paths['WHOLE_PACKAGE_REVIEW_INPUTS.json']={'sha256':'5c8ce364581641c7259f8a1bd3c3999002ea60b1e0c82b499cee0177f32632f8'}
paths['../../../../zenodo_deposit_tool/zenodo.py']=freeze['zenodo_kit']
rows={}
for name,pin in paths.items():
 p=(A/name) if not name.startswith('../../') else A.parents[2]/'zenodo_deposit_tool/zenodo.py'
 b=p.read_bytes(); actual={'bytes':len(b),'sha256':sha(b)}
 if actual['sha256']!=pin['sha256'] or ('bytes'in pin and actual['bytes']!=pin['bytes']):raise RuntimeError(name)
 rows[str(p.absolute())]=actual
snapshot=json.loads((A/'SCOPE_AND_SNAPSHOT.json').read_bytes())
for name,pin in snapshot['original_blobs'].items():
 p=A/'native'/name;b=p.read_bytes();blob=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
 if len(b)!=pin['size'] or sha(b)!=pin['sha256'] or blob!=pin['git_blob'] or stat.S_IMODE(p.stat().st_mode)!=0o644:raise RuntimeError(name)
 rows[str(p)]={'bytes':len(b),'sha256':sha(b),'git_blob':blob,'mode':'100644'}
env=dict(os.environ,GIT_OPTIONAL_LOCKS='0')
repo=A.parents[2]
g=lambda *a:subprocess.check_output(['git',*a],cwd=repo,env=env).decode().strip()
index=repo/g('rev-parse','--git-path','index')
state={'head':g('rev-parse','HEAD'),'branch':g('symbolic-ref','HEAD'),'refs':g('show-ref'),'index_sha256':sha(index.read_bytes())}
ziprows=[]; target=R/'tmp/packet'
if target.exists():raise RuntimeError('extract target exists')
target.mkdir()
with zipfile.ZipFile(A/'publication/satoh_filtration_verification.zip')as z:
 for i in z.infolist():
  if i.filename.startswith('/') or '..'in Path(i.filename).parts or i.is_dir() or (i.external_attr>>16)!=0o100644:raise RuntimeError(i.filename)
  b=z.read(i);p=target/i.filename;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b);p.chmod(0o644)
  ziprows.append({'path':i.filename,'bytes':len(b),'sha256':sha(b),'mode':oct(i.external_attr>>16),'timestamp':i.date_time})
if len(ziprows)!=107:raise RuntimeError('ZIP count')
(R/'INPUT_PINS.json').write_text(json.dumps({'schema':'round2-independent-input-capture-v1','started_utc':'2026-10-15T06:45:23+00:00','files':rows,'shared_git_state':state},indent=2)+'\n')
(R/'ARCHIVE_INVENTORY.json').write_text(json.dumps(ziprows,indent=2)+'\n')
(R/'RESEARCH_LOG.md').write_text('# Second independent whole-package review\n\n2026-10-15T06:45:23+00:00 — Started after the first review completed. Read self-contained paper, complete four-page rendering, literal OWR pp.88–89 and all executed code before consulting round 1 controls. Research goal: falsify scientific deductions and safe publication preparation for exact PR681 head; no live write authorized. Completion estimate: 25%.\n')
(R/'tmp/.gitignore').write_text('*\n')
print(json.dumps({'status':'PASS','pinned_files':len(rows),'zip_members':len(ziprows),'shared_branch':state['branch']}))
