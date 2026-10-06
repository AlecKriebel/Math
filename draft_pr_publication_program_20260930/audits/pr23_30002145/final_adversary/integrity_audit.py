#!/usr/bin/env python3
"""Read-only exact-head, current-package, and pinned-corpus acceptance audit."""
import datetime, hashlib, json, pathlib, re, subprocess

OUT=pathlib.Path(__file__).resolve().parent
AUDIT=OUT.parent
REPO=OUT.parents[3]
HEAD='ea6b192f7e3bc094b78bbc416bf61c609ffa5b2d'
BASE='60292bed09f59236aa192cb17aa138f7b4750e1a'
PID=30002145
CODE='OWR-12008-005'
TITLE='Rigidity of Symmetric-Gradient Differential Inclusions'
PREFIX='unsolved_math_prioritization/'
sha=lambda b:hashlib.sha256(b).hexdigest()
def cmd(*args): return subprocess.check_output(args,cwd=REPO)
def gf(p): return cmd('git','show',HEAD+':'+p)
def values(x):
    if isinstance(x,dict):
        for v in x.values(): yield from values(v)
    elif isinstance(x,list):
        for v in x: yield from values(v)
    else: yield str(x)
def failif(test): assert test

branch=cmd('git','branch','--show-current').decode().strip()
failif(branch=='main')
live=json.loads(cmd('gh','pr','view','23','--repo','AlecKriebel/Math','--json','number,url,title,body,state,isDraft,headRefOid,baseRefOid,files'))
(OUT/'LIVE_PR_READBACK.json').write_text(json.dumps(live,indent=2)+'\n')
failif(live['headRefOid']==HEAD and live['baseRefOid']==BASE)
snapshot=json.loads((AUDIT/'snapshot_manifest.json').read_bytes())
current=AUDIT/'reviewed_candidate'
manifest_bytes=(current/'MANIFEST.json').read_bytes()
failif(sha(manifest_bytes)=='40d0e7dbcf5f8d15d8383c882994af6d2d9e47852d0f3595a07fff9baf653ad3')
manifest=json.loads(manifest_bytes)
failif(len(manifest['files'])==18)
bound=[]
for e in manifest['files']:
    b=(current/e['path']).read_bytes()
    failif(len(b)==e['bytes'] and sha(b)==e['sha256'])
    bound.append(e)
failif(sha((current/'SOURCE_STATUS.md').read_bytes())=='f3c383ff5a55ac755994b9af0108e9453f9715dc22d5b51f412ac5b15b2832eb')
frozen=[]
for e in snapshot['files']:
    b=(AUDIT/'source_snapshot'/e['path']).read_bytes()
    h=gf(PREFIX+'attempts/'+str(PID)+'/'+e['path'])
    failif(b==h and sha(b)==e['sha256'] and len(b)==e['bytes'])
    frozen.append(e)
failif(len(frozen)==14)
original_map={'PR_DRAFT.md':'ORIGINAL_PR_DRAFT.md','provenance.json':'ORIGINAL_provenance.json'}
retained=[]
edited=[]
for e in snapshot['files']:
    rel=e['path']; original=(AUDIT/'source_snapshot'/rel).read_bytes()
    if rel in original_map:
        failif((current/original_map[rel]).read_bytes()==original)
        edited.append(rel)
    elif rel in ('README.md','SOURCE_STATUS.md'):
        edited.append(rel)
        if rel=='SOURCE_STATUS.md':
            failif(original[original.index(b'## 1.'):]==(current/rel).read_bytes()[(current/rel).read_bytes().index(b'## 1.'):])
    else:
        failif((current/rel).read_bytes()==original)
        retained.append(rel)
mergebase=cmd('git','merge-base',HEAD,BASE).decode().strip()
paths=cmd('git','diff','--name-only',mergebase,HEAD).decode().splitlines()
failif(sorted(paths)==sorted(x['path'] for x in live['files']))
failif(paths==snapshot['changed_paths'])
qd=cmd('git','diff','--unified=0',mergebase,HEAD,'--',PREFIX+'QUEUE.md').decode()
changed_rows=[line for line in qd.splitlines() if line.startswith(('+','-')) and not line.startswith(('+++','---'))]
failif(len(changed_rows)==2 and all(str(PID) in row for row in changed_rows))
failif('already_solved' in changed_rows[1] and '0/5' in changed_rows[1])
failif(live['body']==(current/'PR_DRAFT.md').read_text())
failif('QUEUE.md' in live['body'] and 'selected30002145 row' in live['body'])
failif('arbitrary nonconvex domains' in live['body'] and 'No paper' in live['body'])
failif('already_solved' in (current/'SOURCE_STATUS.md').read_text())
turns=json.loads((current/'turns.json').read_text())
failif(turns['used']==0 and turns['limit']==5 and turns['substantive_proof_attempts']==[])
pin=json.loads(gf(PREFIX+'manifest.json'))
failif(pin['revision']=='37e53eabe540fb458758e198be61634bd02ee008')
corpus={}; data={}
for name in ('problems.json','research_results.json'):
    b=(REPO/PREFIX/'cache'/name).read_bytes()
    failif(sha(b)==pin['files'][name]['sha256'] and len(b)==pin['files'][name]['bytes'])
    corpus[name]={'sha256':sha(b),'bytes':len(b)}
    data[name]=json.loads(b)
record=json.loads((current/'source_record.json').read_bytes())
matches=[p for p in data['problems.json'] if p.get('id')==PID]
failif(len(matches)==1 and record==matches[0])
norm=lambda v:re.sub(r'\s+',' ',v).strip().casefold()
duplicates=[p['id'] for p in data['problems.json'] if p.get('id')!=PID and norm(p.get('statement',''))==norm(record['statement'])]
code_matches=[p['id'] for p in data['problems.json'] if p.get('problem_number')==CODE]
queries={needle:[k for k,v in data['research_results.json'].items() if needle in k or any(needle in t for t in values(v))] for needle in (str(PID),CODE,TITLE)}
groups=json.loads(gf(PREFIX+'review_v2/related_target_groups.json'))
group_matches=[v for v in values(groups) if str(PID) in v or CODE in v or TITLE in v]
state=json.loads(gf(PREFIX+'state.json')).get(str(PID),{})
history=[json.loads(line) for line in gf(PREFIX+'history.jsonl').decode().splitlines() if str(PID) in line]
assessment=json.loads(gf(PREFIX+'assessments.json')).get(str(PID),{})
catalog=[p for p in json.loads(gf(PREFIX+'catalog.json')) if str(p.get('id'))==str(PID)]
failif(len(catalog)==1)
failif(not duplicates and code_matches==[PID] and all(not v for v in queries.values()) and not group_matches)
failif(not state and not history)
old_review=json.loads((current/'review/review_summary.json').read_text())
failif(old_review['target_sha256']['SOURCE_STATUS.md']==sha((AUDIT/'source_snapshot/SOURCE_STATUS.md').read_bytes()))
failif(old_review['target_sha256']['SOURCE_STATUS.md']!=sha((current/'SOURCE_STATUS.md').read_bytes()))
receipts=json.loads((OUT/'PRIMARY_DOWNLOADS.json').read_text())
histpdf=old_review['source_pdf_sha256']
newpdf={r['name']:r['sha256'] for r in receipts}
failif(histpdf['dpr2020.pdf']==newpdf['arxiv2020.pdf'] and histpdf['owr2012.pdf']==newpdf['owr.pdf'] and histpdf['rindler2011.pdf']==newpdf['rindler2011.pdf'])
prior_manifests=[]
for family,name,key in [('primary_scope_family','MANIFEST.json','files'),('signed_measure_family','HASH_MANIFEST.json','files'),('compatibility_family','artifact_manifest.json','files')]:
    m=json.loads((AUDIT/family/name).read_text())
    entries=m.get('files',m.get('first_party_files',[]))
    for e in entries:
        b=(AUDIT/family/e['path']).read_bytes()
        failif(sha(b)==e['sha256'] and len(b)==e['bytes'])
    prior_manifests.append({'family':family,'manifest_sha256':sha((AUDIT/family/name).read_bytes()),'files_verified':len(entries),'manifest':m})
result={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'pass':True,'branch':branch,'original_head':HEAD,'base':BASE,'merge_base':mergebase,'live_pr_head_confirmed':True,'live_body_equals_current_draft':True,'original14':frozen,'current18':bound,'current_manifest_sha256':sha(manifest_bytes),'current_source_status_sha256':sha((current/'SOURCE_STATUS.md').read_bytes()),'unchanged_original_paths':retained,'superseded_original_paths':edited,'original_mathematical_sections_byte_identical':True,'changed_paths':paths,'queue_changed_rows':changed_rows,'pin_revision':pin['revision'],'corpus':corpus,'exact_record_equality':True,'source_record_sha256':sha((current/'source_record.json').read_bytes()),'source_record_historical_extraction_defect':'domain, regularity and conclusion absent; CURRENT_SOURCE_SCOPE qualifies self-contained historical assertion','normalized_statement_duplicates':duplicates,'code_matches':code_matches,'report_queries':queries,'related_group_matches':group_matches,'exact_head_state':state,'exact_head_history':history,'exact_head_assessment':assessment,'exact_head_catalog':catalog,'turns':turns,'legacy_state_boundary':'Manual selected queue status is explicit; original exact-head machine default is queued. Parent separately owns durable accepted-state infrastructure. No generator invoked.','old_review_binds_original_only':True,'primary_pdf_historical_hashes_match':True,'prior_manifest_receipts':prior_manifests,'mutation_policy':'Only own final_adversary files written; no Git/PR/global/canonical mutation, install or publishing.'}
(OUT/'INTEGRITY_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'pass':True,'original_files':len(frozen),'current_files':len(bound),'head':HEAD,'mergebase':mergebase,'report_queries':queries,'original_budget':'0/5','live_scope_repaired':True},indent=2))
