#!/usr/bin/env python3
"""Read-only independent snapshot/Git/history/QUEUE checks."""
import datetime,difflib,hashlib,json,subprocess
from pathlib import Path
ROOT=Path('/Users/alec/Documents/Math')
B=ROOT/'draft_pr_descending_audit_20261002/audits/pr385_2518'
OUT=B/'repaired_final_adversary'
SNAP=B/'repaired_snapshot'
P='problems/2518_free_pro_p_characteristic_intersections'
HEAD='2ef690a538338bc477a14c0d4aa1ee1f21e83833'
OLD='fd4a71f2f7e08ece5f0d34d9d0df3fb6f460d8bf'
MAIN='2b9d0234b1396fa84c4b34055b5e8e14c873588b'
WIP='647033115e08e03872c5fcf01953a505b8ab2f0a'
def git(*args):return subprocess.check_output(['git',*args],cwd=ROOT)
def sha(b):return hashlib.sha256(b).hexdigest()
def blob(b):return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
def binding(path,ref=HEAD):
    data=(SNAP/path).read_bytes();actual=git('show',ref+':'+path)
    obj=git('rev-parse',ref+':'+path).decode().strip()
    assert data==actual
    assert blob(data)==obj
    assert git('cat-file','blob',obj)==data
    return {'path':path,'bytes':len(data),'sha256':sha(data),'git_blob_sha':obj,'git_object_exact':True}
manifest=json.loads((B/'repaired_snapshot_manifest.json').read_text())
checks=[]
for e in manifest['files']:
    r=binding(e['path']);assert e['bytes']==r['bytes'] and e['sha256']==r['sha256'];checks.append(r)
assert len(checks)==45
files=[r['path'] for r in checks if r['path'].startswith(P+'/')];assert len(files)==44
for p in files:assert git('show',OLD+':'+p)==(SNAP/p).read_bytes()
parents=git('show','-s','--format=%P',HEAD).decode().strip().split()
assert parents==[OLD,MAIN]
changed=git('diff','--name-only',MAIN,HEAD).decode().splitlines()
assert set(changed)==set(r['path'] for r in checks)
q='unsolved_math_prioritization/QUEUE.md'
before=git('show',MAIN+':'+q).decode();after=git('show',HEAD+':'+q).decode()
oldline=next(l for l in before.splitlines() if l.startswith('| 413 | 2518 /'))
newline=oldline.replace('| queued | 0/5 |','| unsolved | 5/5 |')
assert oldline!=newline and after==before.replace(oldline,newline)
neighbor=next(l for l in before.splitlines() if l.startswith('| 414 | 2525 /'))
assert neighbor in after and '| unsolved | 5/5 |' in neighbor
queue_diff=''.join(difflib.unified_diff(before.splitlines(True),after.splitlines(True),fromfile=MAIN,tofile=HEAD))
(OUT/'queue_exact.diff').write_text(queue_diff)

pub=json.loads((SNAP/P/'PUBLICATION_MANIFEST.json').read_text())['files'];assert len(pub)==43
for e in pub:
    r=binding(P+'/'+e['path'])
    assert all(r[k]==e[k] for k in ['bytes','sha256','git_blob_sha'])
assert set(e['path'] for e in pub)|{'PUBLICATION_MANIFEST.json'}=={Path(p).relative_to(P).as_posix() for p in files}

am=json.loads((SNAP/P/'FINAL_AUTHOR_MANIFEST.json').read_text())['files']
author=[e['path'] for e in am]+['FINAL_AUTHOR_MANIFEST.json'];assert len(author)==36
for p in author:assert git('show',WIP+':'+P+'/'+p)==(SNAP/P/p).read_bytes()
rm=json.loads((SNAP/P/'independent_review/REVIEW_MANIFEST.json').read_text())['files']
review=[e['path'] for e in rm]+['REVIEW_MANIFEST.json'];assert len(review)==5
for e in rm:
    data=(SNAP/P/'independent_review'/e['path']).read_bytes()
    assert len(data)==e['bytes'] and sha(data)==e['sha256']
for p in review:assert git('show',OLD+':'+P+'/independent_review/'+p)==(SNAP/P/'independent_review'/p).read_bytes()
historical=0
for t in range(1,6):
    m=json.loads((SNAP/P/f'TURN_{t}_MANIFEST.json').read_text())
    if t>1:assert m['previous_manifest_sha256']==sha((SNAP/P/f'TURN_{t-1}_MANIFEST.json').read_bytes())
    for e in m['files']:
        data=(SNAP/P/e['path']).read_bytes()
        assert len(data)==e['bytes'] and sha(data)==e['sha256'] and blob(data)==e['git_blob_sha'];historical+=1

# Fresh local render/extraction comparisons. Never turn current render
# equality into a claim of complete twelve-input historical source replay.
mapping={'commensurators-free.pdf':'commensurators.pdf','commensurators-free.txt':'commensurators.txt',
 'kourovka21-oct2026.pdf':'kourovka21_october.pdf','kourovka21-oct2026.txt':'kourovka21_october.txt',
 'kourovka21-update-oct2026.pdf':'updates.pdf','kourovka21-update-oct2026.txt':'updates.txt',
 'nikolov-segal2007.pdf':'nikolov_segal.pdf','nikolov-segal2007.txt':'nikolov_segal.txt',
 'ns-p172.png':'ns_p172.png','printed177.png':'kourovka_p177.png','comm-p53.png':'comm_p53.png','comm-p18.png':'comm_p18.png'}
sources=[]
for n in ['SOURCE_MANIFEST.json','TURN_2_SOURCES.json','TURN_4_SOURCES.json']:
    for e in json.loads((SNAP/P/n).read_text())['files']:
        f=OUT/'sources'/mapping[Path(e['path']).name];data=f.read_bytes()
        sources.append({'historical_path':e['path'],'current_path':str(f.relative_to(OUT)),
         'historical_sha256':e['sha256'],'current_sha256':sha(data),'bytes':len(data),
         'fresh_matches_historical':len(data)==e['bytes'] and sha(data)==e['sha256']})
assert len(sources)==12 and sum(x['fresh_matches_historical'] for x in sources if x['historical_path'].endswith('.pdf'))==4
result={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'head':HEAD,'original':OLD,'main_parent':MAIN,
 'parents':parents,'all45_git_bytes_and_objects_exact':True,'all44_original_math_bytes_preserved':True,
 'publication43bindings_exact_including_git_objects':True,'author36_preserved_at_wip':True,'review5_preserved_at_original':True,
 'historical_turn_bindings':historical,'queue_current_main_exact_single_target_change':True,'adjacent_386_entry_preserved':neighbor,
 'fresh_source_pdfs_exact':4,'fresh_historical_source_matches':sum(x['fresh_matches_historical'] for x in sources),
 'full12_historical_optional_source_replay':False,'files':checks,'fresh_source_comparison':sources}
(OUT/'INPUT_BINDINGS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in ['files','fresh_source_comparison']},indent=2))
