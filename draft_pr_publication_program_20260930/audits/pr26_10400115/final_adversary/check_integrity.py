#!/usr/bin/env python3
"""Read-only acceptance input audit; writes only this family's receipt."""
from pathlib import Path
from hashlib import sha256, sha1
from datetime import datetime, timezone
import json, re, sqlite3, subprocess

REPO=Path('/Users/alec/Documents/Math')
BASE=REPO/'draft_pr_publication_program_20260930/audits/pr26_10400115'
OWN=Path(__file__).resolve().parent
HEAD='762f5808268a85a5cb5373d3f7d60ad160b828f5'
MERGE_BASE='c6975ca76f9f667f1250ba403d0e6da2aafe14d0'
Q=REPO/'unsolved_math_prioritization'
ID='10400115'
def read(p): return json.loads(p.read_text())
def digest(p): return sha256(p.read_bytes()).hexdigest()
def git(*args):
    return subprocess.run(['git',*args],cwd=REPO,check=True,capture_output=True).stdout
def entry(root,e):
    p=root/e['path']; data=p.read_bytes()
    got={'path':str(p.relative_to(REPO)),'bytes':len(data),'sha256':sha256(data).hexdigest()}
    got['pass']=got['bytes']==e['bytes'] and got['sha256']==e['sha256']
    assert got['pass'],got
    return got

assert git('branch','--show-current').decode().strip()=='main'
snapshot=read(BASE/'snapshot_manifest.json')
assert len(snapshot['files'])==14
frozen=[]
for e in snapshot['files']:
    got=entry(BASE/'source_snapshot',e)
    data=(BASE/'source_snapshot'/e['path']).read_bytes()
    gitdata=git('show',HEAD+':unsolved_math_prioritization/attempts/'+ID+'/'+e['path'])
    got['git_byte_equal']=data==gitdata
    got['git_blob_sha1']=sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
    assert got['git_byte_equal'] and got['git_blob_sha1']==e['git_blob_sha1']
    frozen.append(got)
assert git('merge-base',MERGE_BASE,HEAD).decode().strip()==MERGE_BASE
changed=git('diff','--name-only',MERGE_BASE,HEAD).decode().splitlines()
assert len(changed)==15 and changed==snapshot['changed_paths']
assert not git('ls-tree','-r','--name-only',MERGE_BASE,'--','unsolved_math_prioritization/attempts/'+ID).strip()
queue_h=git('show',HEAD+':unsolved_math_prioritization/QUEUE.md').decode()
queue_b=git('show',MERGE_BASE+':unsolved_math_prioritization/QUEUE.md').decode()
qb=[x for x in queue_b.splitlines() if ID in x]; qh=[x for x in queue_h.splitlines() if ID in x]
diff=git('diff',MERGE_BASE,HEAD,'--','unsolved_math_prioritization/QUEUE.md').decode()
difflines=[x for x in diff.splitlines() if x.startswith(('+','-')) and not x.startswith(('+++','---'))]
assert len(qb)==len(qh)==1 and len(difflines)==2
assert '| queued | 0/5 |' in qb[0] and '| unsolved | 1/5 |' in qh[0]
candidate=BASE/'reviewed_candidate'; cm=read(candidate/'MANIFEST.json')
assert digest(candidate/'MANIFEST.json')=='4ee40ce21d6f59c56da8fad1a604ffb4669c063932bbcf7be1988e91b7ca2a12'
assert len(cm['files'])==23
current=[entry(candidate,e) for e in cm['files']]
assert {str(p.relative_to(candidate)) for p in candidate.rglob('*') if p.is_file()}=={e['path'] for e in cm['files']}|{'MANIFEST.json'}
archives={'OBSTRUCTION.md':'ORIGINAL_OBSTRUCTION.md','README.md':'ORIGINAL_README.md','readiness.json':'ORIGINAL_readiness.json'}
for e in snapshot['files']:
    old=(BASE/'source_snapshot'/e['path']).read_bytes()
    dest=candidate/archives.get(e['path'],e['path'])
    assert dest.read_bytes()==old,str(dest)
oldbody=(BASE/'source_snapshot/OBSTRUCTION.md').read_text()
newbody=(candidate/'OBSTRUCTION.md').read_text()
assert oldbody[oldbody.index('## 2.'):] == newbody[newbody.index('## 2.'):]
families=[]; first=[]; foreign=[]
for family,name,key in [('specialization_family','FIRST_PARTY_SHA256_MANIFEST.json','files'),('modular_family','artifact_manifest.json','files'),('primary_scope_family','FIRST_PARTY_MANIFEST.json','first_party_files')]:
    root=BASE/family; manifest=read(root/name)
    rows=[entry(root,e) for e in manifest[key]]
    src=[entry(root,e) for e in manifest.get('third_party_source_evidence',[])]
    first.extend(rows);foreign.extend(src)
    families.append({'family':family,'manifest_sha256':digest(root/name),'listed_first_party':len(rows),'separate_foreign':len(src)})
assert len(first)==67 and len(foreign)==28
supports=[entry(REPO,e) for e in read(candidate/'CURRENT_PROOF_DEPENDENCIES.json')['supporting_first_party_files']]
seals=[]
for family,sealname in [('specialization_family','EARLY_SEAL.json'),('modular_family','early_seal_receipt.json'),('primary_scope_family','EARLY_SEAL.json')]:
    seals.append({'family':family,'seal':read(BASE/family/sealname),'sha256':digest(BASE/family/sealname)})
for record in seals:
    family=record['family'];seal=record['seal']
    if family=='specialization_family':assert digest(BASE/family/seal['path'])==seal['criteria_sha256']
    elif family=='modular_family':assert digest(BASE/family/seal['file'])==seal['sha256']
    else:
        assert digest(BASE/family/seal['criterion_file'])==seal['criterion_sha256']
        for name,h in seal['primary_source_files'].items():assert digest(BASE/family/'primary_sources'/name)==h
rootseal=read(BASE/'ROOT_RECONSTRUCTION_SEAL.json')
assert digest(BASE/rootseal['file'])==rootseal['sha256']
recon=BASE/'specialization_family/append_only_reconciliation'
reconciliation=read(recon/'RECONCILIATION.json')
reconciliation_entries=[entry(recon,e) for e in read(recon/'RECONCILIATION_SEAL.json')['files']]
assert reconciliation['matches'] and reconciliation['actual_source_context_sha256']=='16717ef9457560e93f7f319a303a38bc2693cf47ed6bd54c70a429f019d60420'
sr=read(candidate/'source_record.json');pr=read(candidate/'prior_report.json')
binding=sha256(json.dumps([sr,pr],sort_keys=True).encode()).hexdigest()
assert binding==read(candidate/'readiness.json')['review_hash']==read(candidate/'ORIGINAL_readiness.json')['review_hash']
ledger=[json.loads(x) for x in (candidate/'turns.jsonl').read_text().splitlines() if x.strip()]
assert len(ledger)==1 and ledger[0]['turn']==1
assert read(candidate/'readiness.json')['budget']['used_substantive_attempts']==1
assert read(candidate/'readiness.json')['budget']['maximum_substantive_attempts']==5
manifest=read(Q/'manifest.json')
raw=read(Q/'cache/problems.json'); reports=read(Q/'cache/research_results.json')
rawhash=[]
for name,e in manifest['files'].items():
    p=Q/'cache'/name
    assert p.stat().st_size==e['bytes'] and digest(p)==e['sha256']
    rawhash.append({'name':name,**e})
db=sqlite3.connect('file:'+str(Q/'cache/catalog.sqlite')+'?mode=ro',uri=True)
count=db.execute('select count(*) from records').fetchone()[0]
revision=db.execute('select revision from metadata').fetchone()[0]
assert count==len(raw)==15458==manifest['records'] and revision==manifest['revision']
selected=[x for x in raw if str(x['id'])==ID]; assert len(selected)==1
row=db.execute('select payload,report from records where key=?',(ID,)).fetchone()
assert json.loads(row[0])==sr==selected[0] and json.loads(row[1])==pr==reports[sr['problem_number']]
normalized=lambda s: ''.join(re.findall('[a-z0-9]+',s.casefold()))
duplicates={k:[x['id'] for x in raw if f(x)] for k,f in {'numeric_id':lambda x:str(x['id'])==ID,'code':lambda x:x['problem_number']==sr['problem_number'],'literal_statement':lambda x:x.get('statement')==sr['statement'],'normalized_statement':lambda x:normalized(x.get('statement',''))==normalized(sr['statement'])}.items()}
assert all(v==[10400115] for v in duplicates.values())
raw_prior_codes=[key for key,value in reports.items() if value==pr]
assert raw_prior_codes==[sr['problem_number']]
sqlite_matches={k:[] for k in ('code','literal_statement','normalized_statement','literal_prior')}
for key,payload,report in db.execute('select key,payload,report from records'):
    p=json.loads(payload);r=json.loads(report)
    if p.get('problem_number')==sr['problem_number']:sqlite_matches['code'].append(key)
    if p.get('statement')==sr['statement']:sqlite_matches['literal_statement'].append(key)
    if normalized(p.get('statement',''))==normalized(sr['statement']):sqlite_matches['normalized_statement'].append(key)
    if r==pr:sqlite_matches['literal_prior'].append(key)
assert all(v==[ID] for v in sqlite_matches.values())
neighbor=next(x for x in raw if str(x['id'])=='10400109')
assert 'Temperley' in neighbor['statement'] and neighbor['statement']!=sr['statement']
related=read(Q/'review_v2/related_target_groups.json')
related_selected=[g for g in related['groups'] if ID in g.get('ids',[]) or '10400109' in g.get('ids',[])]
assert not related_selected
db.close()
canonical={}
for name in ['state.json','catalog.json','assessments.json','history.jsonl','assessment_history.jsonl']:
    p=Q/name
    if name.endswith('jsonl'): rows=[json.loads(x) for x in p.read_text().splitlines() if x.strip() and str(json.loads(x).get('id'))==ID]
    else:
        obj=read(p);rows=obj.get(ID) if isinstance(obj,dict) else [x for x in obj if str(x.get('id'))==ID]
    canonical[name]={'sha256':digest(p),'selected':rows}
canonical['QUEUE.md']={'sha256':digest(Q/'QUEUE.md'),'selected':[x for x in (Q/'QUEUE.md').read_text().splitlines() if ID in x]}
currentpr=subprocess.run(['gh','pr','view','26','--repo','AlecKriebel/Math','--json','number,url,title,body,state,isDraft,headRefOid,baseRefOid,files'],cwd=REPO,check=True,capture_output=True,text=True)
live=json.loads(currentpr.stdout)
assert live['headRefOid']==HEAD and live['baseRefOid']==MERGE_BASE and live['isDraft'] and live['state']=='OPEN'
assert sorted(x['path'] for x in live['files'])==sorted(changed)
assert '14 files' in live['body'] and 'QUEUE.md' in live['body'] and 'pending' in live['body'] and 'No paper' in live['body']
fresh=[]
for name,stored in [('ohtsuki-fresh.pdf','ohtsuki2002_s.pdf'),('scherich-fresh.pdf','scherich2023_s.pdf')]:
    p=OWN/'tmp'/name;s=BASE/'primary_scope_family/primary_sources'/stored
    assert digest(p)==digest(s)
    fresh.append({'url':'https://msp.org/'+('gtm/2002/04/gtm-2002-04-024s.pdf' if name.startswith('ohtsuki') else 'agt/2023/23-5/agt-v23-n5-p03-s.pdf'),'bytes':p.stat().st_size,'sha256':digest(p),'matches_stored':True})
out={'utc':datetime.now(timezone.utc).isoformat(),'status':'PASS','branch':'main','original_head':HEAD,'actual_merge_base':MERGE_BASE,'original_files':frozen,'original_changed_paths':changed,'selected_queue_base':qb,'selected_queue_head':qh,'queue_only_selected_row_change':True,'candidate_manifest_sha256':digest(candidate/'MANIFEST.json'),'candidate_files':current,'all_original_archives_exact':True,'scientific_sections_2_to_5_byte_exact':True,'families':families,'all_67_first_party_entries':first,'all_28_separate_source_entries':foreign,'current_proof_dependency_entries':supports,'early_seals':seals,'root_seal':rootseal,'reconciliation':reconciliation,'reconciliation_sealed_entries':reconciliation_entries,'correct_readiness_source_pair_hash':binding,'ledger_1_of_5':True,'raw_corpus':{'records':count,'revision':revision,'files':rawhash,'duplicates':duplicates,'raw_literal_prior_codes':raw_prior_codes,'full_sqlite_matches':sqlite_matches,'distinct_neighbor':{'id':neighbor['id'],'statement':neighbor['statement']},'related_selected_groups':related_selected},'canonical_snapshot':canonical,'live_pr':live,'fresh_primary_retrievals':fresh,'scope':'Read-only verification of exact current candidate, all original/family/source members and current live PR. Future canonical/state/header edits require separate administrative checks; no blanket certificate for unseen bytes.'}
(OWN/'INTEGRITY_RECEIPT.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:out[k] for k in ['utc','status','candidate_manifest_sha256','all_original_archives_exact','scientific_sections_2_to_5_byte_exact','ledger_1_of_5']}))
