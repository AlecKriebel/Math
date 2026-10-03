#!/usr/bin/env python3
from pathlib import Path
import subprocess,json,hashlib,datetime
P=Path(__file__).resolve().parent;B=P.parent;HEAD='5f576c1b527f88730c7ee15fd204536069753f9a';ORIGINAL='967e8e489aa4599f712d5ddcde62e591827f7e38';BASE='86a2c300cfc07fb2fdb8ac3ab45544c5f3231828';PR384='3f18fa7b30851b165b604645d05f332263e9a301';TARGET='unsolved_math_prioritization/attempts/30004047/';QUEUE='unsolved_math_prioritization/QUEUE.md'
def git(*args):return subprocess.check_output(['git',*args],cwd=B)
def h(b):return hashlib.sha256(b).hexdigest()
def entry(path,b):return {'path':path,'bytes':len(b),'sha256':h(b)}
def validate(e,base):
 f=base/e['path'];b=f.read_bytes();assert len(b)==e['bytes'] and h(b)==e['sha256'],str(f);return entry(str(f.relative_to(B)) if f.is_relative_to(B) else str(f),b)
result={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'head':HEAD,'base':BASE}
m=json.loads((B/'repaired_snapshot_manifest.json').read_text());old=json.loads((B/'snapshot_manifest.json').read_text());assert m['head']==HEAD and m['base']==BASE
actual=set(git('diff','--name-only',BASE,HEAD).decode().splitlines());assert len(actual)==49 and actual=={e['path'] for e in m['files']}
rows=[]
for e in m['files']:
 b=git('show',HEAD+':'+e['path']);assert len(b)==e['bytes'] and h(b)==e['sha256'];assert b==(B/'repaired_snapshot'/e['path']).read_bytes();rows.append(entry(e['path'],b))
result['all49_exact_git_bindings']=rows
for e in old['files']:
 b=git('show',ORIGINAL+':'+e['path']);assert b==(B/'snapshot'/e['path']).read_bytes();assert len(b)==e['bytes'] and h(b)==e['sha256']
 if e['path']!=QUEUE:assert b==git('show',HEAD+':'+e['path'])
result['all48_original_target_bytes_preserved']=True
parents=git('show','-s','--format=%P',HEAD).decode().strip().split();assert parents==[ORIGINAL,BASE];result['actual_repair_parents']=parents
q=git('show',HEAD+':'+QUEUE).splitlines(keepends=True);qb=git('show',BASE+':'+QUEUE).splitlines(keepends=True);assert len(q)==len(qb)
changed=[i for i,(x,y) in enumerate(zip(q,qb),1) if x!=y];assert changed==[420];a=qb[419].split(b'|');c=q[419].split(b'|');assert len(a)==len(c);cellchanges=[i for i,(x,y) in enumerate(zip(a,c)) if x!=y];assert cellchanges==[8,9];assert c[8].strip()==b'unsolved' and c[9].strip()==b'5/5'
result['current_main_queue_projection']={'physical_changed_lines':changed,'changed_cells':cellchanges,'target_line':q[419].decode().rstrip(),'every_other_main_queue_byte_preserved':True}
assert subprocess.run(['git','merge-base','--is-ancestor',PR384,BASE],cwd=B).returncode==0
result['prior_pr384_merge_verified_readonly']={'merge':PR384,'parents':git('show','-s','--format=%P',PR384).decode().strip().split(),'ancestor_of_current_main':True}
D=B/'repaired_snapshot'/TARGET
nested=[]
for mn in [f'TURN_{i}_MANIFEST.json' for i in range(1,6)]+['FINAL_AUTHOR_MANIFEST.json','PUBLICATION_MANIFEST.json','review/REVIEW_MANIFEST.json']:
 v=json.loads((D/mn).read_text());base=D/'review' if mn.startswith('review/') else D
 checks=[validate(e,base) for e in v['files']];nested.append({'manifest':mn,'manifest_sha256':h((D/mn).read_bytes()),'bindings':checks})
 if 'previous_manifest_sha256' in v:
  i=int(mn.split('_')[1]);assert v['previous_manifest_sha256']==h((D/f'TURN_{i-1}_MANIFEST.json').read_bytes())
result['candidate_nested_manifests']=nested
for e in json.loads((D/'SOURCE_MANIFEST.json').read_text())['files']:
 f=P/'raw_primary'/({'OWR_2019_1.pdf':'owr.pdf','Concatenating_published_2022.pdf':'ejc.pdf'}[e['name']]);b=f.read_bytes();assert len(b)==e['bytes'] and h(b)==e['sha256']
result['fresh_exact_raw_source_bindings']=2
families=[]
for name,mn in [('sources_lp_review','OUTPUT_MANIFEST.json'),('maximal_types_review','AUDIT_MANIFEST.json'),('laminar_uncrossing_review','AUDIT_MANIFEST.json')]:
 f=B/name/mn;v=json.loads(f.read_text());checks=[validate(e,f.parent) for e in v['files']]
 if 'frozen_snapshot_manifest' in v:checks.append(validate(v['frozen_snapshot_manifest'],f.parent))
 families.append({'family':name,'manifest_sha256':h(f.read_bytes()),'binding_count':len(checks),'bindings':checks})
result['all_family_output_manifests']=families
rr=json.loads((B/'root_family_controls_receipt.json').read_text());streams=[]
for r in rr['runs']:
 f=B/r['family']/r['script'];assert h(f.read_bytes())==r['code_sha256'];name='root_'+r['family']+'_'+Path(r['script']).stem;stdout=B/(name+'.stdout');stderr=B/(name+'.stderr');assert not stderr.read_bytes();streams.append({'family':r['family'],'script':r['script'],'code_sha256':h(f.read_bytes()),'stdout_bytes':stdout.stat().st_size,'stdout_sha256':h(stdout.read_bytes()),'stderr_empty':True,'root_receipt_claims_full_equal':r['complete_result_equal']})
 # Family scripts may write a detailed JSON and print a summary; validate artifact independently via its manifest.
result['root_family_frozen_code_and_streams']=streams
rootpub=(B/'root_public_replay.stdout').read_bytes();rp=json.loads((B/'root_public_replay_receipt.json').read_text());assert h(rootpub)==rp['stdout_sha256'] and not (B/'root_public_replay.stderr').read_bytes();result['root_public_replay_receipt_hash_bound']=True
print(json.dumps(result,indent=2))
