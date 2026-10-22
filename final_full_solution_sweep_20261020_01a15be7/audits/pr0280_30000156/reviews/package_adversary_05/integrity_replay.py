#!/usr/bin/env python3
import ast,hashlib,json,os,stat,subprocess,sys,zipfile
from pathlib import Path,PurePosixPath
from datetime import datetime,timezone
A=Path(__file__).resolve().parents[2]; R=A.parents[1]; W=R/'private/pr0280_package05'; OUT=Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
def check(v,m):
 if not v:raise RuntimeError(m)
def record(p):
 b=p.read_bytes();return {'path':str(p),'bytes':len(b),'sha256':sha(b)}
def write(n,d):(OUT/n).write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
manifest=A/'ops_record_url_repair_20261021/MANIFEST.json';d=json.loads(manifest.read_text());check(sha(manifest.read_bytes())=='b12e7262026d780029a7eeee1fb8d0c8a514c4a2ab382faadebad40a84dba55d','repair seal')
entries=[]
for e in d['files']:
 p=A/e['path'];check(not p.is_symlink() and p.is_file(),'regular sealed file');b=p.read_bytes();check(len(b)==e['bytes'] and sha(b)==e['sha256'],'seal '+str(p));entries.append(e)
check(len(entries)==390 and len({e['path'] for e in entries})==390,'390unique')
write('INPUT_BINDING_BEFORE.json',{'timestamp':datetime.now(timezone.utc).isoformat(),'repair_manifest':record(manifest),'all390_verified':True,'files':entries})
rel=A/'preprint/publication';rr=json.loads((rel/'RELEASE_FILES.json').read_text());check(sha((rel/'RELEASE_FILES.json').read_bytes())=='548b7a4ae1f13a92029255fc9ef485002b7c33376b9dd9168ffcdb532fc4c20e','release')
for e in rr['files']:
 b=(rel/e['path']).read_bytes();check(len(b)==e['bytes'] and sha(b)==e['sha256'],'release payload')
z=zipfile.ZipFile(rel/'fixed-birational-cycle-nonlimit-verification.zip');names=z.namelist();check(len(names)==65 and len(set(names))==65 and z.testzip() is None,'zip')
for i in z.infolist():
 q=PurePosixPath(i.filename);check(not q.is_absolute() and '..' not in q.parts and '\\' not in i.filename and not i.is_dir() and stat.S_IFMT(i.external_attr>>16)!=stat.S_IFLNK,'zip safe');b=z.read(i);s=b.decode();
 if i.filename.endswith('.json'):json.loads(s)
 if i.filename.endswith('.py'):ast.parse(s)
extract=W/'extract';extract.mkdir(parents=True,exist_ok=True);z.extractall(extract);P=extract/'birational-cycle-verification';md=json.loads((P/'MANIFEST.json').read_text());check(len(md['files'])==64,'64')
for e in md['files']:
 b=(P/e['path']).read_bytes();check(len(b)==e['bytes'] and sha(b)==e['sha256'],'inner hash')
check((P/'paper/main.tex').read_bytes()==(rel/'fixed-birational-cycle-nonlimit.tex').read_bytes(),'tex')
ss=json.loads((A/'SOURCE_SNAPSHOT.json').read_text());env={**os.environ,'GIT_OPTIONAL_LOCKS':'0'}
def git(*args):return subprocess.check_output(['git',*args],cwd=R.parent,env=env)
head=ss['head'];parent=git('show','-s','--format=%P',head).decode().strip();check(parent=='c053681c57cb775eaa8782312e98db430e40b43b','sole parent')
for e in ss['files']:
 b=(A/e['snapshot']).read_bytes();check(len(b)==e['bytes'] and sha(b)==e['sha256'] and hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==e['git_blob'],'original snapshot');check(git('show',head+':'+e['path'])==b,'git body');check((P/e['snapshot']).read_bytes()==b,'zip original')
queue='unsolved_math_prioritization/QUEUE.md'; rows={}
for ref in [parent,head]:
 b=git('show',ref+':'+queue);row=[v for v in b.splitlines(keepends=True) if b'| 30000156 / OWR-768-006 |' in v];check(len(row)==1,'queue one');rows[ref]=row[0].decode()
check('| queued | 0/5 |  |  |  |' in rows[parent] and '| claimed_solved | 1/5 |  | Reviewed counterexample' in rows[head],'queue accounting')
# Already-pushed child is not a local object; separate authenticated GET evidence handles it.
state=R.parent/'.zenodo-state'; states=[{'path':p.relative_to(R.parent).as_posix(),'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())} for p in sorted(state.glob('*.json'))];(W/'STATE_INVENTORY_BEFORE.json').write_text(json.dumps({'count':len(states),'files':states},indent=2)+'\n')
write('INTEGRITY.json',{'repair390':True,'release5':rr['files'],'archive_members':65,'payloads':64,'original17_and_git_objects':True,'soleparent':parent,'queue_rows':rows,'already_pushed_child_local_object_available':False,'archive_text_json_python_all_read':True,'state_count':len(states)})
replays=[]
for py in [sys.executable,str(R.parent/'.venv/bin/python'),'/Users/alec/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3']:
 for mode in [[],['-O']]:
  r=subprocess.run([py,'-B',*mode,'verify.py'],cwd=P,capture_output=True,text=True);check(r.returncode==0,'actual replay '+py+r.stderr);replays.append({'python':py,'mode':mode,'version':subprocess.check_output([py,'--version'],text=True).strip(),'output':json.loads(r.stdout)})
write('ARCHIVE_REPLAYS.json',replays)
legacy=[]
py=str(R.parent/'.venv/bin/python')
for script,baseline in [('original/checks/verify.py','original/checks/output.json'),('original/independent_review/independent_check.py','original/independent_review/INDEPENDENT_CHECKS.json')]:
 r=subprocess.run([py,'-B',str(P/script)],cwd=P,capture_output=True,text=True);check(r.returncode==0,'legacy normal');actual=json.loads(r.stdout);expected=json.loads((P/baseline).read_text());check(actual==expected,'legacy baseline');legacy.append({'script':script,'normal_only':True,'output':actual})
write('LEGACY_REPLAYS.json',legacy)
print(json.dumps({'390':True,'64':True,'17':True,'actual_verifier_runs':len(replays),'legacy_normal_runs':len(legacy),'all_pass':True}))
