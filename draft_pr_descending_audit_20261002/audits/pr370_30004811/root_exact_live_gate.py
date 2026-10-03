"""Root's independent literal Git/API/current-main acceptance gate; no merge."""
from pathlib import Path,PurePosixPath
import base64,concurrent.futures,datetime,hashlib,json,subprocess
A=Path(__file__).resolve().parent;R=A.parents[2];Q='unsolved_math_prioritization/QUEUE.md';PREFIX='problems/30004811_capacity_volume_mass/'
PRIVATE=A/'tmp/root_exact_live';PRIVATE.mkdir(parents=True,exist_ok=True)
checks=[]
def sha(b):return hashlib.sha256(b).hexdigest()
def blob(b):return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
def ck(v,label):
    assert v,label;checks.append({'label':label,'pass':True})
def cmd(args,tag=None):
    r=subprocess.run(args,cwd=R,capture_output=True)
    if tag:
        (PRIVATE/(tag+'.stdout')).write_bytes(r.stdout);(PRIVATE/(tag+'.stderr')).write_bytes(r.stderr)
    ck(r.returncode==0,repr(args));return r.stdout
def git(*args):return cmd(['git',*args])
def api(path,tag):return json.loads(cmd(['gh','api','repos/AlecKriebel/Math/'+path],tag))
def entries(rev):
    out={}
    for row in git('ls-tree','-rz','--full-tree',rev).split(b'\0'):
        if row:
            meta,path=row.split(b'\t',1);out[path.decode()]=meta.decode()
    return out
def get(rev,path):return git('show',rev+':'+path)
m=json.loads((A/'repaired_snapshot_manifest.json').read_bytes());original=json.loads((A/'snapshot_manifest.json').read_bytes())
HEAD=m['head'];BASE=m['base'];OLD=original['head'];body=(A/'accepted_pr_body.txt').read_bytes()
ck(OLD=='567c2e493854b32d0cd325ad96e4c5b69c9c1e1b','original mathematical head')
ck(BASE=='81185c796181151e49dcf7299a6567ad2abc9695' and HEAD=='af92cfc40bbd781fd9a2367214745f6f53a0b12e','literal root reviewed refresh pins')
ck(git('branch','--show-current').strip()==b'main','shared main branch')
cmd(['git','fetch','origin','main'], 'main_fetch')
ck(git('rev-parse','origin/main').decode().strip()==BASE,'actual remote main equals reviewed base')
first=api('pulls/370','pr_first')
def prcheck(p):
    ck(p['state']=='open' and not p['draft'],'actual open ready')
    ck(p['head']['sha']==HEAD and p['base']['sha']==BASE,'actual head and base')
    ck(p['body'].encode()==body,'literal complete PR body')
    ck(p['mergeable'] is True and p['mergeable_state']=='clean','actual merge readiness')
prcheck(first)
ck(api('git/ref/heads/main','main_first')['object']['sha']==BASE,'raw main ref')
base_entries=entries(BASE);head_entries=entries(HEAD);old_entries=entries(OLD)
changed={p for p in base_entries.keys()|head_entries.keys() if base_entries.get(p)!=head_entries.get(p)}
expected={r['path'] for r in m['files']};ck(changed==expected and len(expected)==19,'complete all-root mode/type/blob change scope19')
ck(expected=={r['path'] for r in original['files']},'original and refreshed literal path scope')
ck({p for p in head_entries if p.startswith(PREFIX)}==expected-{Q},'exact18 target scope')
file_checks=[]
for row in m['files']:
    path=row['path'];raw=get(HEAD,path)
    ck(len(raw)==row['bytes'] and sha(raw)==row['sha256'],'reviewed snapshot '+path)
    ck(raw==(A/'repaired_snapshot'/path).read_bytes(),'literal refreshed disk copy '+path)
    ck(head_entries[path].split()==['100644','blob',blob(raw)],'regular-file literal entry '+path)
    if path!=Q:
        ck(raw==get(OLD,path),'original mathematical bytes '+path)
        ck(head_entries[path]==old_entries[path],'original mode/type/blob '+path)
    file_checks.append({'path':path,'bytes':len(raw),'sha256':sha(raw),'git_entry':head_entries[path],'pass':True})
before=get(BASE,Q);after=get(HEAD,Q);bl=before.splitlines(keepends=True);al=after.splitlines(keepends=True)
ck(len(bl)==len(al),'full queue line count')
changed_lines=[i for i,(x,y) in enumerate(zip(bl,al)) if x!=y];ck(len(changed_lines)==1,'only own queue line changes')
i=changed_lines[0];x=bl[i].split(b'|');y=al[i].split(b'|')
ck(x[2].strip().split(b' / ')[0]==b'30004811','exact own queue identifier')
ck([j for j,(u,v) in enumerate(zip(x,y)) if u!=v]==[8,9],'only exact status and turn cells')
ck([x[j].strip() for j in (8,9)]==[b'queued',b'0/5'] and [y[j].strip() for j in (8,9)]==[b'already_solved',b'1/5'],'exact already_solved1/5 transition')
ck(base_entries[Q].split()[:2]==head_entries[Q].split()[:2],'queue mode/type preserved')
v=git('merge-tree','--write-tree',BASE,HEAD).decode().splitlines()[0]
tree=git('show','-s','--format=%T',HEAD).decode().strip();ck(v==tree,'virtual integration equals literal reviewed tree')
test=api('git/commits/'+first['merge_commit_sha'],'test_merge')
ck([p['sha'] for p in test['parents']]==[BASE,HEAD] and test['tree']['sha']==tree,'actual GitHub test-merge parent order and tree')
ck(git('show','-s','--format=%P',HEAD).decode().strip().split()==[m.get('previous_review_head',OLD),BASE],'queue-refresh actual parent order')
target=A/'repaired_snapshot'/PREFIX;bindings=[]
for name,entry_root in [('FINAL_AUTHOR_MANIFEST.json',target),('PUBLICATION_MANIFEST.json',target),('REVIEW_MANIFEST.json',target/'review')]:
    obj=json.loads((entry_root/name).read_bytes());seen=set()
    for row in obj['files']:
        path=PurePosixPath(row['path']);ck(not path.is_absolute() and '..' not in path.parts and row['path'] not in seen,'safe mathematical manifest path');seen.add(row['path'])
        raw=(entry_root/path).read_bytes();ck(len(raw)==row['bytes'] and sha(raw)==row['sha256'],'manifest size and sha '+row['path'])
        bindings.append({'manifest':name,'path':(entry_root/path).relative_to(target).as_posix(),'bytes':len(raw),'sha256':sha(raw),'pass':True})
ck(len(bindings)==29,'all29 nested binding instances')
author='1901d52ea8b47b4dd3c843cb2e02be2c520da7cb'
author_files={PREFIX+r['path'] for r in json.loads((target/'FINAL_AUTHOR_MANIFEST.json').read_bytes())['files']}|{PREFIX+'FINAL_AUTHOR_MANIFEST.json'}
ck(len(author_files)==10,'ten actual author checkpoint files')
for path in sorted(author_files):ck(get(author,path)==get(OLD,path),'actual author checkpoint '+path)
ck(git('show','-s','--format=%P',OLD).decode().strip().split()==[original['base'],author],'original head actual parent order')
for path in sorted(expected-{Q}-author_files):
    ck(get(OLD,path)==(target/path.removeprefix(PREFIX)).read_bytes(),'review/final-only frozen-head provenance '+path)
mfchecks=[]
for family in ['asymptotic_normalization_review','priority_hypotheses_review','clean_final_adversary']:
    root=A/family;mf=root/'PUBLIC_MANIFEST.json';obj=json.loads(mf.read_bytes());seen=set()
    for row in obj['files']:
        p=PurePosixPath(row['path']);ck(not p.is_absolute() and '..' not in p.parts and p.as_posix()==row['path'] and row['path'] not in seen,'literal owned audit scope')
        seen.add(row['path']);f=root/p;ck(not f.is_symlink() and f.resolve().is_relative_to(root),'owned path without escape')
        raw=f.read_bytes();ck(len(raw)==row['bytes'] and sha(raw)==row['sha256'],'immutable independent audit '+family+'/'+row['path'])
    mfchecks.append({'family':family,'manifest_sha256':sha(mf.read_bytes()),'bound_files':len(seen),'pass':True})
published=json.loads((A.parents[1]/'checkpoint_370_math_public_allowlist.json').read_bytes())
audit_prefix=A.relative_to(R).as_posix()+'/'
for path in published['explicit_owned_paths']:
    if path.startswith(audit_prefix) and path!=audit_prefix+'acceptance_criteria.json':
        ck(get(BASE,path)==(R/path).read_bytes(),'published immutable audit preimage '+path)
source=json.loads((A/'root_original_reproduction_receipt.json').read_bytes())
ck(source['status']=='PASS' and len(source['checks'])==135 and all(r['passed'] for r in source['checks']),'root complete frozen reproduction135')
ck(source['binding_count']==29 and len(source['primary_sources'])==7,'all seven historical sources and29 bindings')
for row in source['primary_sources']:
    path=A/'raw_sources'/row['name']
    if row['name']=='owr2021-40.pdf':path=A/'raw_sources/OWR2021-40.pdf'
    raw=path.read_bytes();ck(len(raw)==row['bytes'] and sha(raw)==row['sha256'],'fresh root source '+row['name'])
own=json.loads((A/'clean_final_adversary/SOURCE_ACQUISITION.json').read_bytes())
ck(len(own['files'])==7,'seven independently downloaded whole-review sources')
for row in own['files']:
    raw=(A/'clean_final_adversary/private/sources'/row['name']).read_bytes();ck(len(raw)==row['bytes'] and sha(raw)==row['sha256'],'fresh whole source '+row['name'])
control=json.loads((A/'root_family_control_reproduction.json').read_bytes())
ck(control['status']=='PASS' and control['new_controls_total']==48 and sum(f['bound_files'] for f in control['families'])==51,'three-family complete new-control replay')
remote_rows=[]
def remote_file(row):
    path=row['path'];obj=json.loads(subprocess.check_output(['gh','api','repos/AlecKriebel/Math/contents/'+path+'?ref='+HEAD],cwd=R));raw=base64.b64decode(obj['content'])
    return {'path':path,'bytes':len(raw),'sha256':sha(raw),'blob':obj['sha'],'pass':len(raw)==row['bytes'] and sha(raw)==row['sha256'] and obj['sha']==blob(raw)}
remote_rows=list(concurrent.futures.ThreadPoolExecutor(6).map(remote_file,m['files']))
ck(len(remote_rows)==19 and all(r['pass'] for r in remote_rows),'all19 actual reviewed remote file bytes')
last=api('pulls/370','pr_last');prcheck(last)
ck(last['merge_commit_sha']==first['merge_commit_sha'],'test merge stable')
ck(api('git/ref/heads/main','main_last')['object']['sha']==BASE,'late actual main ref stable')
out={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS_ROOT_EXACT_LIVE','reviewed_head':HEAD,'base':BASE,'reviewed_tree':tree,'test_merge':first['merge_commit_sha'],'body_sha256':sha(body),'checks':checks,'check_count':len(checks),'files':file_checks,'nested_bindings':bindings,'audit_manifests':mfchecks,'actual_remote_files':remote_rows,'queue_line':i+1,'only_queue_cells':[8,9],'all_other_queue_bytes_preserved':True,'all_seven_historical_primary_pdf_identities_recertified':True,'actual_merge_approval_math':str(A/'DECISION.md'),'no_mathematical_replay_needed': 'All18 original files remain literal; root complete original and new-control replays independently verified.'}
(A/'root_exact_live_receipt.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:out[k] for k in ['status','reviewed_head','base','reviewed_tree','test_merge','check_count','queue_line']},indent=2))
