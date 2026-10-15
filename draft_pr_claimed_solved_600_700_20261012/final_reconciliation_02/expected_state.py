#!/usr/bin/env python3
"""Offline, fail-closed expectation builder for exactly eight completed PRs."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,re
from metadata_rules import expected_metadata,description_rule_evidence,MetadataRuleError
NUMBERS=(615,618,623,628,630,662,672,681)
SHEET='1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20'
EXPECTED_681_ORIGINAL='e92320ea5979c812089780a982fbd88136a26522'
class NotReady(RuntimeError):pass
def now():return datetime.now(timezone.utc).isoformat()
def sha(data):return hashlib.sha256(data).hexdigest()
def require(condition,message):
 if not condition:raise NotReady(message)
def valid_oid(value):return isinstance(value,str) and re.fullmatch('[0-9a-f]{40}',value) is not None
def normalize_doi(value):return re.sub(r'^(?:https?://(?:dx\.)?doi\.org/|doi:\s*)','',value.strip(),count=1,flags=re.I).removesuffix('/').lower()
def build_expected(root):
 """Read only local completed state/receipts; never execute a CLI or network call."""
 root=Path(root);state_path=root/'PROGRAM_STATE.json'
 state_bytes=state_path.read_bytes();state=json.loads(state_bytes)
 completed=state.get('completed',[]);numbers=[x.get('pr') for x in completed]
 require(len(numbers)==len(set(numbers)),'Duplicate PR entries in completed program state')
 require(set(numbers)==set(NUMBERS),f'All eight eligible PRs must be completed before collection; missing: {sorted(set(NUMBERS)-set(numbers))}; unexpected completed entries: {sorted(set(numbers)-set(NUMBERS))}')
 ordered=[next(x for x in completed if x['pr']==n) for n in NUMBERS]
 files={'PROGRAM_STATE.json':{'bytes':len(state_bytes),'sha256':sha(state_bytes)}}
 def bind(path):
  require(path.is_file(),f'Required completed receipt/file is pending: {path.relative_to(root)}')
  data=path.read_bytes();files[str(path.relative_to(root))]={'bytes':len(data),'sha256':sha(data)}
  return json.loads(data) if path.suffix=='.json' else data
 entries=[]
 for entry in ordered:
  n=entry['pr'];matches=list((root/'audits').glob(f'pr{n}_*'))
  require(len(matches)==1,f'Audit directory for PR{n} is not unique')
  a=matches[0];e=dict(entry,audit_directory=str(a.relative_to(root)))
  if n==615:
   c=bind(a/'CLOSURE_RECEIPT.json');e['original_head']=e['accepted_head']=c['headRefOid'];e['closed_at']=c['closedAt']
   body=a/'CLOSURE_COMMENT_SENT.md';b=bind(body);e['closure_body_file']=str(body.relative_to(root));e['closure_body_sha256']=sha(b)
  elif n in (628,630):
   s=bind(a/'SCOPE_AND_SNAPSHOT.json');c=bind(a/'CLOSURE_RECEIPT.json');e['original_head']=e['accepted_head']=s['original_head'];e['closed_at']=c['pr']['closedAt'];e['closure_body_sha256']=c['comment']['body_sha256']
   body=a/'CLOSURE_COMMENT_CANDIDATE.md';bind(body);e['closure_body_file']=str(body.relative_to(root))
   require(c['pr']['headRefOid']==e['original_head'] and c['pr']['state']=='CLOSED' and c['pr']['mergedAt'] is None,f'PR{n} closure receipts disagree')
  elif n==672:
   s=bind(a/'SCOPE_AND_SNAPSHOT.json');c=bind(a/'FINAL_DISPOSITION.json');close=bind(a/'CLOSE_RECEIPT.json');comment=bind(a/'CLOSURE_COMMENT_RECEIPT.json')
   require(c['status']=='COMPLETE_CLOSED_WITHOUT_MERGE_PRIORITY_FAILURE',f'PR{n} final disposition is not complete')
   e['original_head']=e['accepted_head']=s['original_head'];e['closed_at']=c['closed_at'];e['closure_body_sha256']=c['body_sha256']
   body=a/'CLOSURE_COMMENT.md';bind(body);e['closure_body_file']=str(body.relative_to(root))
   require(close['metadata']['headRefOid']==e['original_head'] and close['metadata']['state']=='CLOSED' and comment['body_sha256']==e['closure_body_sha256'],f'PR{n} closure receipts disagree')
  elif n==618:
   c=bind(a/'MERGE_RECEIPT.json');i=bind(a/'INTEGRATION_RECEIPT.json');g=bind(a/'FINAL_PUBLICATION_GATE.json')
   e['original_head']=i['existing_pr_head'];e['accepted_head']=c['headRefOid'];e['merged_at']=c['mergedAt']
   require(g['live_pr_gate']['headRefOid']==e['original_head'] and i['integration_commit']==e['accepted_head'] and c['state']=='MERGED' and c['mergeCommit']['oid']==e['merge_commit'],f'PR{n} accepted integration receipts disagree')
  elif n==623:
   s=bind(a/'LIVE_SCOPE_GATE.json');c=bind(a/'MERGE_RECEIPT.json');i=bind(a/'INTEGRATION_PUSHED_RECEIPT.json');bind(a/'FINAL_PUBLICATION_GATE.json')
   e['original_head']=s['head'];e['accepted_head']=c['accepted_head'];e['merged_at']=c['merged_at']
   require(i['integration_commit']==e['accepted_head'] and c['merge_commit']==e['merge_commit'] and c['state']=='MERGED',f'PR{n} accepted integration receipts disagree')
  elif n in (662,681):
   s=bind(a/'SCOPE_AND_SNAPSHOT.json');c=bind(a/'FINAL_DISPOSITION.json');g=bind(a/'GH_MERGE_RECEIPT.json');i=bind(a/'INTEGRATION_PUSHED_RECEIPT.json');accepted=bind(a/'ACCEPTED_PUBLICATION_INPUTS.json');bind(a/'FINAL_PUBLICATION_GATE.json')
   status=c.get('status','')
   require(status.startswith('COMPLETE') and all(word in status for word in ('PUBLISHED','TRACKED','MERGED')),f'PR{n} final published/tracked/merged disposition is pending')
   require('doi' in e and 'merge_commit' in e and 'record_url' in e and 'tracker_range' in e,f'PR{n} completed program entry lacks publication outcome')
   e['original_head']=s['original_head'];e['accepted_head']=c['accepted_head'];e['merged_at']=g['mergedAt']
   if n==681:require(e['original_head']==EXPECTED_681_ORIGINAL,'PR681 immutable original head differs from assigned shard head')
   require(g['state']=='MERGED' and g['headRefOid']==e['accepted_head'] and g['mergeCommit']['oid']==e['merge_commit'] and c['merge_commit']==e['merge_commit'],f'PR{n} final and GitHub merge receipts disagree')
   require(c['doi']==e['doi'] and c['record_url']==e['record_url'] and c['tracker_range']==e['tracker_range'],f'PR{n} final publication fields disagree with completed program state')
   require(i['integration_commit']==e['accepted_head'] and i['existing_pr_head']==e['original_head'] and i.get('pushed') is True,f'PR{n} pushed integration receipt disagrees with accepted/original heads')
   require(accepted.get('ready_for_publication') is True and bool(accepted.get('files')),f'PR{n} accepted publication input gate is incomplete')
  else:raise NotReady(f'Unexpected PR{n}')
  require(valid_oid(e['original_head']) and valid_oid(e['accepted_head']),f'PR{n} immutable head pin malformed')
  if 'doi' not in e:
   require(entry.get('disposition')=='closed_without_merge_priority_failure' and entry.get('publication') is None,f'PR{n} program closure disposition inconsistent')
   require(e['comment_url'].startswith(f'https://github.com/AlecKriebel/Math/pull/{n}#issuecomment-'),f'PR{n} closure URL mismatch')
   require(sha((root/e['closure_body_file']).read_bytes())==e['closure_body_sha256'],f'PR{n} saved exact comment body hash differs')
  else:
   require('merged' in entry.get('disposition',''),f'PR{n} program merge disposition inconsistent')
   require(valid_oid(e['merge_commit']),f'PR{n} merge commit pin malformed')
   require(re.fullmatch(r'10\.5281/zenodo\.\d+',e['doi']) is not None and e['record_url']=='https://zenodo.org/records/'+e['doi'].split('.')[-1],f'PR{n} production DOI/record URL malformed')
   row_match=re.fullmatch(r"'Math Puzzles'!A(\d+):D(\d+)",e['tracker_range'])
   require(row_match is not None and row_match.group(1)==row_match.group(2),f'PR{n} tracker range must be one exact authorized A:D row')
   z=bind(a/'ZENODO_PUBLICATION_RECEIPT.json');t=bind(a/'TRACKER_RECEIPT.json');meta=bind(a/'publication/zenodo-deposit.json')
   require(z['environment']=='production' and z['state']=='published' and z['doi']==e['doi'] and z['record_url']==e['record_url'],f'PR{n} production publication receipt is pending or inconsistent')
   require(t.get('applied') is True and t['spreadsheet_id']==SHEET and t['sheet_id']==1254632077 and t['updated_range']==e['tracker_range'],f'PR{n} tracker receipt is pending or inconsistent')
   require(len(t['row'])==4 and normalize_doi(t['row'][2])==e['doi'].lower() and t['read_back']==[t['row']],f'PR{n} exact tracker row/DOI readback differs')
   require(z['title']==meta['metadata']['title'] and len(z['files'])==2,f'PR{n} publication title/file inventory differs')
   try:
    expected_metadata(n,meta['metadata'],z)
    e['metadata_comparison_rule']=description_rule_evidence(n,meta['metadata']['description'],z)
   except MetadataRuleError as exc:raise NotReady(f'PR{n} actual publication metadata normalization is not authorized: {exc}') from exc
   e['publication_receipt']=z;e['metadata']=meta;e['tracker_row']=t['row'];e['tracker_range']=t['updated_range']
   require({x['name'] for x in z['files']}=={Path(x.get('name',x['path'])).name for x in meta['files']},f'PR{n} metadata file names differ')
   for f in z['files']:
    require(re.fullmatch(r'[A-Za-z0-9_.-]+\.(?:pdf|zip)',f['name']) is not None,f'PR{n} publication file name outside allowed PDF/ZIP basenames')
    path=a/'publication'/f['name'];b=bind(path)
    require(len(b)==f['size'] and sha(b)==f['sha256'],f'PR{n} accepted/publication receipt file pin differs: {f["name"]}')
    files[str(path.relative_to(root))]['md5']=hashlib.md5(b).hexdigest()
   if n==618:pinmap=bind(a/'FINAL_PUBLICATION_GATE.json')['reviewed_hashes'];pins={k:v for k,v in pinmap.items() if k.startswith('publication/')}
   elif n==623:pinmap=bind(a/'FINAL_PUBLICATION_GATE.json')['reviewed_inputs'];pins={k:v['sha256'] for k,v in pinmap.items() if k.startswith('publication/')}
   else:pins={'publication/'+k:v['sha256'] for k,v in bind(a/'ACCEPTED_PUBLICATION_INPUTS.json')['files'].items()}
   require(bool(pins),f'PR{n} accepted publication pins are empty')
   for rel,expected in pins.items():
    path=a/rel;require(path.resolve().is_relative_to((a/'publication').resolve()),f'PR{n} accepted pin escapes its publication directory');bind(path);require(sha(path.read_bytes())==expected,f'PR{n} accepted input changed: {rel}')
  entries.append(e)
 require(tuple(x['pr'] for x in entries)==NUMBERS,'Expected entries lost shard order')
 require(len([e for e in entries if 'doi' in e])==4,'Four actual publication outcomes are required for this reconciliation; do not assume a different PR681 outcome')
 require(state_path.read_bytes()==state_bytes,'Program state changed during offline preflight; collect a fresh stable snapshot')
 return {'created_utc':now(),'entries':entries,'program_state_sha256':sha(state_bytes),'program_completed_snapshot':{'captured_utc':now(),'program_state_sha256':sha(state_bytes),'completed':ordered},'input_bindings':{'created_utc':now(),'files':files}}
