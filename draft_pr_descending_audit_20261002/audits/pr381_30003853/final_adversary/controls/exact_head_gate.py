#!/usr/bin/env python3
"""Read-only Git binding and private complete replay for the repaired head."""
from pathlib import Path
import hashlib,json,subprocess,sys,os,datetime
P=Path(__file__).resolve().parents[1]
ROOT=P.parents[3]
HEAD='89d5f156c4a2846d6ef0b840cd24c854677d07ca'
BASE='859a836402f92f3a78dd7aecd9199e973ab666fb'
ORIGINAL='5b7bd8db9f34294d10862fed0f723055da864df6'
MERGE382='568e2f38888221aa2ff9c5e86b940a309db2ddde'
TARGET='problems/30003853_thompson_subgroup_abelianization'
MAN=P.parent/'repaired_snapshot_manifest.json'
SNAP=P.parent/'repaired_snapshot'
PRIVATE=P/'private_replay';PRIVATE.mkdir(exist_ok=True)
PUB=P/'replay_outputs';PUB.mkdir(exist_ok=True)
def git(*args):return subprocess.check_output(['git',*args],cwd=ROOT)
def sha(b):return hashlib.sha256(b).hexdigest()
def blob(b):return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
def valid(e,b):
    assert len(b)==e['bytes'] and sha(b)==e['sha256'],e['path']
    if 'git_blob_sha' in e:assert blob(b)==e['git_blob_sha'],e['path']
    return True
s=json.loads((P/'INITIAL_SEAL.json').read_text())
for e in s['entries']:valid(e,(P/e['path']).read_bytes())
m=json.loads(MAN.read_text());assert m['head']==HEAD and m['base']==BASE
parents=git('show','-s','--format=%P',HEAD).decode().strip().split()
assert parents==[ORIGINAL,BASE]
assert git('show','-s','--format=%P',BASE).decode().strip()==MERGE382
for anc in [ORIGINAL,BASE,MERGE382]:
    assert subprocess.run(['git','merge-base','--is-ancestor',anc,HEAD],cwd=ROOT).returncode==0
inputs=[]
for e in m['files']:
    b=git('show',HEAD+':'+e['path']);valid(e,b);assert b==(SNAP/e['path']).read_bytes()
    q=PRIVATE/e['path'];q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(b)
    is_target=e['path'].startswith(TARGET+'/')
    unchanged=(b==git('show',ORIGINAL+':'+e['path'])) if is_target else None
    if is_target:assert unchanged
    inputs.append({**e,'git_blob_sha':blob(b),'snapshot_exact':True,'original_target_unchanged':unchanged})
assert len(inputs)==45 and sum(x['original_target_unchanged'] is True for x in inputs)==44
qpath='unsolved_math_prioritization/QUEUE.md'
before=git('show',BASE+':'+qpath);after=git('show',HEAD+':'+qpath)
bl=before.splitlines(keepends=True);al=after.splitlines(keepends=True)
assert len(bl)==len(al)
changed=[i+1 for i,(x,y) in enumerate(zip(bl,al)) if x!=y];assert changed==[419]
old=bl[418].split(b'|');new=al[418].split(b'|');assert len(old)==len(new)
cells=[i for i,(x,y) in enumerate(zip(old,new)) if x!=y];assert cells==[8,9]
assert old[8].strip()==b'queued' and old[9].strip()==b'0/5'
assert new[8].strip()==b'unsolved' and new[9].strip()==b'5/5'
reconstructed=b'|'.join(old[:8]+[new[8],new[9]]+old[10:])
assert reconstructed==al[418]
assert b''.join(bl[:418]+[reconstructed]+bl[419:])==after
p=PRIVATE/TARGET;nested=[]
for name in [f'TURN_{i}_MANIFEST.json' for i in range(1,6)]+['FINAL_AUTHOR_MANIFEST.json','PUBLICATION_MANIFEST.json','independent_review/REVIEW_MANIFEST.json']:
    d=json.loads((p/name).read_text());prefix=p/'independent_review' if name.startswith('independent_review/') else p
    for e in d['files']:
        valid(e,(prefix/e['path']).read_bytes());nested.append({'manifest':name,'path':e['path'],'valid':True})
    if 'previous_manifest_sha256' in d:
        prior=p/f"TURN_{d['turn']-1}_MANIFEST.json";assert sha(prior.read_bytes())==d['previous_manifest_sha256']
source=[];mapping={'bieri-geoghegan-kochloukova2010.pdf':'bgk.pdf','bleak2006-algebraic.pdf':'bleak.pdf','kassabov-matucci.pdf':'km.pdf','guba-sapir2003.pdf':'gs.pdf','golan2026.pdf':'golan.pdf','farley2026.pdf':'farley.pdf','owr2018-26.pdf':'ems46748.pdf'}
for name in ['SOURCE_MANIFEST.json','TURN_3_SOURCES.json','TURN_5_SOURCES.json']:
    for e in json.loads((p/name).read_text())['files']:
        basename=Path(e['path']).name
        if basename in mapping:
            b=(P/'private_sources'/mapping[basename]).read_bytes();valid(e,b)
            status='fresh-primary-PDF-byte-exact'
        else:status='historical-processed-source-not-byte-reproduced; optional-public-binding-omitted'
        source.append({'manifest':name,**e,'verification_status':status})
assert len(source)==20
receipt={'timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'head':HEAD,'base':BASE,'original':ORIGINAL,'parents':parents,'actual_PR382_merge_ancestor':MERGE382,'initial_seal_valid':8,'snapshot_manifest_sha256':sha(MAN.read_bytes()),'inputs':inputs,'queue':{'changed_lines':changed,'changed_cells':cells,'before_row':bl[418].decode(),'after_row':al[418].decode(),'all_other_bytes_preserved':True},'nested_local_bindings':nested,'source_bindings':source,'raw_source_bindings_claimed_by_this_gate':7,'historical_processed_source_bindings_unreproduced':13}
(P/'INPUT_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1')
replays=[]
for name in [f'verify_turn{i}.py' for i in range(1,6)]+['independent_review/independent_check.py','REPLAY_ALL.py','verify_publication.py']:
    r=subprocess.run([sys.executable,str(p/name)],cwd=p,env=env,capture_output=True)
    label=name.replace('/','_').replace('.py','')
    (PUB/(label+'.stdout')).write_bytes(r.stdout);(PUB/(label+'.stderr')).write_bytes(r.stderr)
    assert r.returncode==0,name
    if name.startswith('verify_turn'):
        expected=(p/f"TURN_{name[len('verify_turn')]}_CHECKS.json").read_bytes()
        assert r.stdout==expected,name
    elif name=='independent_review/independent_check.py':
        assert r.stdout==(p/'independent_review/INDEPENDENT_CHECKS.json').read_bytes()
    elif name=='REPLAY_ALL.py':
        j=json.loads(r.stdout);expected=json.loads((p/'FINAL_REPLAY.json').read_text());expected['local_source_bindings']=0;assert j==expected
        other=json.loads((p/'independent_review/AUTHOR_REPLAY.json').read_text());other['local_source_bindings']=0;assert j==other
    assert not r.stderr,name
    replays.append({'name':name,'exit_code':r.returncode,'stdout_bytes':len(r.stdout),'stdout_sha256':sha(r.stdout),'stderr_bytes':len(r.stderr),'stderr_sha256':sha(r.stderr),'complete_stdout_preserved':str(PUB/(label+'.stdout'))})
(P/'REPLAY_RECEIPT.json').write_text(json.dumps({'timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'head':HEAD,'replays':replays,'author_assertions':562635,'historical_assertions':110736,'public_raw_source_bindings':0,'historical_raw_receipt_claim':20,'fresh_source_PDF_hash_matches':7,'counts_do_not_replace_output_inspection':True},indent=2)+'\n')
print(json.dumps({'head':HEAD,'git_inputs':len(inputs),'unchanged_target_files':44,'nested_local_manifest_bindings':len(nested),'source_manifest_entries':len(source),'fresh_PDF_matches':7,'unreproduced_processed_source_bytes':13,'queue_changes':changed,'queue_cells':cells,'replays':replays},indent=2))
