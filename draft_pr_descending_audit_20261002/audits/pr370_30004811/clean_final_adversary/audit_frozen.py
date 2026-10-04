"""Read-only frozen audit with safe private scoped replay copies and retained streams."""
from pathlib import Path
import hashlib, json, shutil, subprocess, datetime

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
SNAP = HERE.parent/'snapshot'
TARGET = Path('problems/30004811_capacity_volume_mass')
P = SNAP/TARGET
PY = REPO/'draft_pr_descending_audit_20261002/audits/pr378_30004322/sources_effective_review/private_runtime/bin/python'
PRIVATE = HERE/'private'
HEAD = '567c2e493854b32d0cd325ad96e4c5b69c9c1e1b'
BASE = 'efd29c05204703acca9a0860812f54b94fae54b1'
def sha(b): return hashlib.sha256(b).hexdigest()
def run(name, argv, cwd=None):
    p=subprocess.run([str(a) for a in argv],cwd=cwd or REPO,capture_output=True)
    (PRIVATE/f'{name}.stdout').write_bytes(p.stdout)
    (PRIVATE/f'{name}.stderr').write_bytes(p.stderr)
    r={'argv':[str(a) for a in argv],'returncode':p.returncode,
       'stdout_sha256':sha(p.stdout),'stderr_sha256':sha(p.stderr)}
    if p.returncode==0:
        try: r['parsed_stdout']=json.loads(p.stdout)
        except (json.JSONDecodeError,UnicodeDecodeError): pass
    return r,p

files=sorted(x.relative_to(P).as_posix() for x in P.rglob('*') if x.is_file())
jsons={x:json.loads((P/x).read_text()) for x in files if x.endswith('.json')}
hashchecks=[]
for mf, root in [('FINAL_AUTHOR_MANIFEST.json',P),('PUBLICATION_MANIFEST.json',P),('review/REVIEW_MANIFEST.json',P/'review')]:
    for e in jsons[mf]['files']:
        b=(root/e['path']).read_bytes()
        hashchecks.append({'manifest':mf,'path':e['path'],'bytes_match':len(b)==e['bytes'],'sha256_match':sha(b)==e['sha256']})
assert all(e['bytes_match'] and e['sha256_match'] for e in hashchecks)
assert jsons['review/REVIEW_MANIFEST.json']['author_manifest_sha256']==sha((P/'FINAL_AUTHOR_MANIFEST.json').read_bytes())
pubpaths=sorted(e['path'] for e in jsons['PUBLICATION_MANIFEST.json']['files'])
assert files==sorted(pubpaths+['PUBLICATION_MANIFEST.json'])
(HERE/'JSON_AUDIT.json').write_text(json.dumps({'complete_candidate_json':jsons,'hash_checks':hashchecks,'public_files':files,'complete_public_manifest':True},indent=2,sort_keys=True)+'\n')

copies={}
for name in ['with_sources','without_sources','tampered_public','tampered_source']:
    dest=PRIVATE/name
    dest.mkdir(exist_ok=True)
    for rel in files:
        out=dest/rel; out.parent.mkdir(parents=True,exist_ok=True); shutil.copyfile(P/rel,out)
    copies[name]=dest
for name in ['with_sources','tampered_source']:
    d=copies[name]/'sources';d.mkdir(exist_ok=True)
    for e in jsons['SOURCE_MANIFEST.json']['files']:
        out=d/e['name']
        if name=='tampered_source': shutil.copyfile(PRIVATE/'sources'/e['name'],out)
        else:
            if not out.exists(): out.symlink_to(PRIVATE/'sources'/e['name'])
copies['tampered_public'].joinpath('TURN_1.md').write_bytes((P/'TURN_1.md').read_bytes()+b'\nTAMPER NEGATIVE CONTROL\n')
z=copies['tampered_source']/'sources'/'owr2021-40.pdf';z.write_bytes(z.read_bytes()+b'\nTAMPER NEGATIVE CONTROL\n')
runs={}
for name,argv,expect in [
 ('author',[PY,copies['without_sources']/'check_turn_1.py'],0),
 ('review_full_sources',[PY,copies['with_sources']/'review/check.py',copies['with_sources']],0),
 ('portable_without_sources',[PY,copies['without_sources']/'review/portable_check.py',copies['without_sources']],0),
 ('publication_without_sources',[PY,copies['without_sources']/'verify_publication.py'],0),
 ('publication_with_sources',[PY,copies['with_sources']/'verify_publication.py'],0),
 ('independent_controls',[PY,HERE/'independent_controls.py'],0),
 ('legacy_missing_sources',[PY,copies['without_sources']/'review/check.py',copies['without_sources']],1),
 ('negative_tampered_public',[PY,copies['tampered_public']/'verify_publication.py'],1),
 ('negative_tampered_source',[PY,copies['tampered_source']/'review/portable_check.py',copies['tampered_source']],1),
]:
    rec,p=run(name,argv);rec['expected_returncode']=expect;rec['expected_outcome']=p.returncode==expect;runs[name]=rec
assert all(r['expected_outcome'] for r in runs.values())
assert (PRIVATE/'author.stdout').read_bytes()==(P/'TURN_1_CHECKS.json').read_bytes()
assert json.loads((PRIVATE/'review_full_sources.stdout').read_bytes())==jsons['review/CHECKS.json']
(HERE/'REPRODUCTION.json').write_text(json.dumps({'recorded_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'runs':runs,'all_expected_outcomes':True,'author_byte_exact':True,'historical_review_complete_json_exact':True},indent=2,sort_keys=True)+'\n')

gitchecks=[]
for rel in files+['../../unsolved_math_prioritization/QUEUE.md']:
    path=TARGET/rel if not rel.startswith('../') else Path('unsolved_math_prioritization/QUEUE.md')
    b=(P/rel).read_bytes() if not rel.startswith('../') else (SNAP/path).read_bytes()
    rec,p=run('git_blob_'+str(len(gitchecks)),['git','show',f'{HEAD}:{path.as_posix()}'])
    assert p.returncode==0
    gitchecks.append({'path':path.as_posix(),'snapshot_sha256':sha(b),'git_sha256':sha(p.stdout),'equal':b==p.stdout})
assert all(x['equal'] for x in gitchecks)
rec,p=run('git_changed_paths',['git','diff','--name-only',BASE,HEAD]);assert p.returncode==0
changed=p.stdout.decode().splitlines()
assert sorted(changed)==sorted([str(TARGET/x) for x in files]+['unsolved_math_prioritization/QUEUE.md'])
rec,p=run('git_queue_diff',['git','diff',BASE,HEAD,'--','unsolved_math_prioritization/QUEUE.md']);assert p.returncode==0
queue_diff=p.stdout.decode()
rec,p=run('git_head_parents',['git','show','-s','--format=%P',HEAD]);assert p.returncode==0
parents=p.stdout.decode().split()
assert parents==[BASE,'1901d52ea8b47b4dd3c843cb2e02be2c520da7cb']
rec,p=run('live_api',['gh','api','repos/AlecKriebel/Math/pulls/370']);api=json.loads(p.stdout) if p.returncode==0 else None
live={k:api[k] for k in ['number','html_url','state','draft','merged','mergeable','mergeable_state','title','updated_at']} if api else None
if api:
    live['head']={k:api['head'][k] for k in ['ref','sha']}
    live['base']={k:api['base'][k] for k in ['ref','sha']}
api_files_rec,ap=run('live_api_files',['gh','api','repos/AlecKriebel/Math/pulls/370/files','--paginate'])
api_files=json.loads(ap.stdout) if ap.returncode==0 else []
body_scoped={'mentions_two_claims':bool(api and 'nonnegative' in api['body'] and '−7/4' in api['body']),'full_body_sha256':sha(api['body'].encode()) if api else None}
out={'recorded_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'frozen_head':HEAD,'frozen_base':BASE,'git_parents':parents,'git_snapshot_byte_checks':gitchecks,'changed_paths':changed,'queue_diff':queue_diff,'live_api':live,'live_api_capture':rec,'live_api_files_capture':api_files_rec,'live_file_metadata':[{k:e[k] for k in ['filename','status','additions','deletions','changes']} for e in api_files],'body_scope_probe':body_scoped,'exact_live_approval':'PENDING_ADDITIVE_FINAL_LIVE_GATE_AFTER_ROOT_CHECKPOINT_QUEUE_REFRESH'}
(HERE/'PROVENANCE.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(json.dumps({'status':'PASS','manifest_entries_checked':len(hashchecks),'candidate_public_files':len(files),'reproduction_runs':len(runs),'git_snapshot_files':len(gitchecks),'live_api_available':bool(api),'exact_live_approval':'PENDING'},indent=2))
