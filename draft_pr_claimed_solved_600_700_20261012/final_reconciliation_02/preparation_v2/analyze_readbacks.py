#!/usr/bin/env python3
"""Check saved read-only responses without mutations or new network requests."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,subprocess,re
import sys
sys.dont_write_bytecode=True
from scope_sheet_evidence import PRIVATE_KEYS,scoped_evidence
from metadata_rules import expected_metadata,description_rule_evidence,MetadataRuleError
OUT=Path(__file__).resolve().parent;ROOT=OUT.parent;REPO=ROOT.parent
N=(615,618,623,628,630,662,672,681)
def now():return datetime.now(timezone.utc).isoformat()
def load(p):return json.loads(p.read_text())
def dump(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
def sha(b):return hashlib.sha256(b).hexdigest()
def response(key):
 d=load((OUT/'tmp' if key in PRIVATE_KEYS else OUT)/(key+'.json'))
 if d.get('returncode',0)!=0 or 'error' in d:raise ValueError(f'Failed response {key}')
 return d['response']
def pad(r):return (r+['']*4)[:4]
def doi_value(v):return re.sub(r'^(?:https?://(?:dx\.)?doi\.org/|doi:\s*)','',v.strip(),count=1,flags=re.I).removesuffix('/').lower()
def git(args):
 p=subprocess.run(['git','--no-optional-locks',*args],cwd=REPO,capture_output=True,timeout=30)
 if p.returncode:raise ValueError(p.stderr.decode(errors='replace'))
 return p.stdout
checks=[]
def check(name,ok,detail=None):
 d={'check':name,'pass':bool(ok)}
 if detail is not None:d['detail']=detail
 checks.append(d)
 return bool(ok)
def native_normalized(d):
 m=d['metadata']
 return {
 'title':m['title'],'upload_type':'publication' if m['resource_type']['id'].startswith('publication-') else None,
 'publication_type':m['resource_type']['id'].removeprefix('publication-'),
 'publication_date':m['publication_date'],'version':m['version'],'description':m['description'],
 'creators':[{'name':x['person_or_org']['name'],'affiliation':x.get('affiliations',[{}])[0].get('name'),'orcid':next((i['identifier'] for i in x['person_or_org'].get('identifiers',[]) if i['scheme']=='orcid'),None)} for x in m['creators']],
 'access_right':'open' if d['access'].get('record')=='public' and d['access'].get('files')=='public' else None,
 'license':m['rights'][0]['id'],'keywords':[x['subject'] for x in m['subjects']],
 'related_identifiers':[{'identifier':x['identifier'],'scheme':x['scheme'],'relation':x['relation_type']['id'].lower()} for x in m['related_identifiers']]
 }
def metadata_input_normalized(m):
 r=dict(m);r['related_identifiers']=[dict(x,relation=x['relation'].lower()) for x in m['related_identifiers']];return r
if not (OUT/'EXPECTED_COMPLETED_EIGHT.json').exists():
 raise SystemExit('No completed-eight snapshot exists; collection requires all eight final receipts and explicit later authorization.')
entries=load(OUT/'EXPECTED_COMPLETED_EIGHT.json')['entries']
if tuple(x['pr'] for x in entries)!=N:
 raise SystemExit('Snapshot does not contain exactly the eight eligible PRs in order.')
binding=load(OUT/'INPUT_BINDINGS.json')['files'];results=[]
for e in entries:
 n=e['pr'];a=ROOT/e['audit_directory'];live=response(f'pr{n}_github');own={}
 check(f'PR{n}:number_and_url',live['number']==n and live['url']==f'https://github.com/AlecKriebel/Math/pull/{n}')
 check(f'PR{n}:accepted_or_original_head',live['headRefOid']==e['accepted_head'],{'expected':e['accepted_head'],'actual':live['headRefOid']})
 c=response(f'pr{n}_original_head_commit');check(f'PR{n}:original_commit_still_resolves',c['sha']==e['original_head'])
 if 'doi' not in e:
  check(f'PR{n}:closed_without_merge',live['state']=='CLOSED' and live['mergedAt'] is None and live['mergeCommit'] is None and live['closedAt']==e['closed_at'])
  comment=response(f'pr{n}_closure_comment');local=(ROOT/e['closure_body_file']).read_bytes();remote=comment['body'].encode()
  check(f'PR{n}:exact_closure_body_and_sha',remote==local and sha(remote)==e['closure_body_sha256'],{'sha256':sha(remote),'bytes':len(remote)})
  check(f'PR{n}:closure_comment_identity',comment['html_url']==e['comment_url'] and comment['issue_url']==f'https://api.github.com/repos/AlecKriebel/Math/issues/{n}')
  own={'pr':n,'disposition':'CLOSED_WITHOUT_MERGE','head':e['original_head'],'closed_at':live['closedAt'],'comment_url':comment['html_url'],'body_sha256':sha(remote)}
 else:
  check(f'PR{n}:merged_state_commit_and_timestamp',live['state']=='MERGED' and live['mergeCommit']['oid']==e['merge_commit'] and live['mergedAt']==e['merged_at'] and live['isDraft'] is False)
  c=response(f'pr{n}_accepted_head_commit');m=response(f'pr{n}_merge_commit')
  parents=[x['sha'] for x in m['parents']]
  check(f'PR{n}:accepted_and_merge_commit_resolve',c['sha']==e['accepted_head'] and m['sha']==e['merge_commit'])
  check(f'PR{n}:merge_parent_contains_accepted_head',e['accepted_head'] in parents)
  scope=[f'unsolved_math_prioritization/attempts/{e["problem_id"]}']
  if n in (662,681):scope.append(f'unsolved_math_prioritization/publications/{e["problem_id"]}')
  gitproof={'scope':scope,'accepted_tree':c['commit']['tree']['sha'],'merge_tree':m['commit']['tree']['sha'],'whole_trees_equal':c['commit']['tree']['sha']==m['commit']['tree']['sha'],'parents':parents}
  try:
   ah=git(['ls-tree','-r','-z',e['accepted_head'],'--',*scope]);mh=git(['ls-tree','-r','-z',e['merge_commit'],'--',*scope])
   check(f'PR{n}:own_accepted_and_actual_merge_inventory_equal',ah==mh and len(ah)>0,{'files':len(ah.split(b'\0'))-1,'inventory_sha256':sha(ah)})
   gitproof['scope_inventory_sha256']=sha(ah);gitproof['scope_file_count']=len(ah.split(b'\0'))-1
   (OUT/f'pr{n}_accepted_scope_ls_tree.txt').write_bytes(ah.replace(b'\0',b'\n'))
   (OUT/f'pr{n}_merge_scope_ls_tree.txt').write_bytes(mh.replace(b'\0',b'\n'))
   rows=[]
   for h in (e['accepted_head'],e['merge_commit']):
    q=git(['show',f'{h}:unsolved_math_prioritization/QUEUE.md']).decode()
    rs=[x for x in q.splitlines() if re.search(r'\|\s*'+re.escape(e['problem_id'])+r'\s*/',x)]
    if len(rs)!=1:raise ValueError('Selected target row not unique')
    rows.append(rs[0])
   check(f'PR{n}:accepted_and_actual_merge_target_queue_row_equal',rows[0]==rows[1])
   gitproof['selected_accepted_and_merged_queue_row']=rows[0]
  except Exception as ex:
   check(f'PR{n}:local_immutable_git_scope_readback_available',False,{'error':str(ex)})
  dump(OUT/f'pr{n}_IMMUTABLE_MERGE_SCOPE_CHECK.json',gitproof)
  if n==618:
   pins=load(a/'FINAL_PUBLICATION_GATE.json')['reviewed_hashes'];needed={k:v for k,v in pins.items() if k.startswith('publication/')}
   check(f'PR{n}:accepted_local_publication_pins',all(sha((a/k).read_bytes())==v for k,v in needed.items()),{'files':len(needed)})
  elif n==623:
   pins=load(a/'FINAL_PUBLICATION_GATE.json')['reviewed_inputs'];needed={k:v for k,v in pins.items() if k.startswith('publication/')}
   check(f'PR{n}:accepted_local_publication_pins',all(sha((a/k).read_bytes())==v['sha256'] and (a/k).stat().st_size==v['size'] for k,v in needed.items()),{'files':len(needed)})
  else:
   needed=load(a/'ACCEPTED_PUBLICATION_INPUTS.json')['files']
   check(f'PR{n}:accepted_local_publication_pins',all(sha((a/'publication'/k).read_bytes())==v['sha256'] and (a/'publication'/k).stat().st_size==v['bytes'] for k,v in needed.items()),{'files':len(needed)})
  native=response(f'pr{n}_zenodo_native');normalized=native_normalized(native);expected=metadata_input_normalized(e['metadata']['metadata'])
  try:
   expected=expected_metadata(n,expected,e['publication_receipt'])
   description_rule=description_rule_evidence(n,e['metadata']['metadata']['description'],e['publication_receipt'])
   check(f'PR{n}:actual_publication_receipt_authorizes_only_exact_recorded_description_rule',True,description_rule)
  except MetadataRuleError as exc:
   description_rule={'invalid_rule':str(exc)}
   check(f'PR{n}:actual_publication_receipt_authorizes_only_exact_recorded_description_rule',False,description_rule)
  mdiff={k:{'expected':expected.get(k),'actual':normalized.get(k)} for k in set(normalized)|set(expected) if normalized.get(k)!=expected.get(k)}
  dump(OUT/f'pr{n}_METADATA_COMPARISON.json',{'local_metadata_raw':e['metadata']['metadata'],'public_native_metadata_raw':native['metadata'],'expected_comparison_metadata':expected,'actual_comparison_metadata':normalized,'actual_publication_receipt_metadata_normalizations':e['publication_receipt'].get('metadata_normalizations'),'record_specific_description_rule':description_rule,'mismatches':mdiff,'all_other_fields_compared_exactly':True})
  check(f'PR{n}:every_supplied_metadata_field_matches_exact_native_schema_and_actual_record_specific_rule',not mdiff,{'mismatches':mdiff,'local_field_count':len(expected),'description_rule':description_rule})
  check(f'PR{n}:production_public_published_exact_DOI',native['is_published'] is True and native['status']=='published' and native['pids']['doi']['identifier']==e['doi'] and str(native['id'])==e['doi'].split('.')[-1] and str(native['id'])==str(e['publication_receipt']['id']) and native['access']['status']=='open')
  files=native['files']['entries'];published=e['publication_receipt']['files']
  check(f'PR{n}:public_exact_file_inventory',set(files)=={f['name'] for f in published} and native['files']['count']==len(published))
  fresults=[]
  for f in published:
   name=f['name'];d=load(OUT/f'pr{n}_public_{name}.json');local=(a/'publication'/name).read_bytes();remote=(OUT/d['temporary_path']).read_bytes();md5=hashlib.md5(local).hexdigest()
   good=d['http_status']==200 and remote==local and sha(remote)==f['sha256'] and len(remote)==f['size'] and files[name]['size']==f['size'] and files[name]['checksum']=='md5:'+md5
   check(f'PR{n}:public_file_exact_bytes_SHA256_MD5:{name}',good,{'sha256':sha(remote),'md5':md5,'bytes':len(remote)})
   fresults.append({'name':name,'bytes':len(remote),'sha256':sha(remote),'md5':md5})
  doi=load(OUT/f'pr{n}_doi_resolution.json')
  check(f'PR{n}:doi_resolves_exact_record_HTTP200',doi['http_status']==200 and doi['resolved_url'].rstrip('/')==e['record_url'])
  sr=response(f'pr{n}_tracker_exact');values=sr.get('values',[])
  check(f'PR{n}:exact_saved_tracker_range_and_row',len(values)==1 and pad(values[0])==e['tracker_row'] and sr['range']==e['tracker_range'],{'range':sr.get('range'),'row_sha256':sha(json.dumps(pad(values[0]),ensure_ascii=False).encode()) if values else None})
  allrows=response('tracker_all_A_D').get('values',[])
  hits=[i+1 for i,row in enumerate(allrows) if len(row)>2 and doi_value(row[2])==e['doi'].lower()]
  target=int(re.search(r'!A(\d+):D',e['tracker_range']).group(1))
  fullmatches=[i+1 for i,row in enumerate(allrows) if pad(row)==e['tracker_row']]
  check(f'PR{n}:globally_unique_DOI_and_exact_row',hits==[target] and fullmatches==[target],{'normalized_DOI_column_C_rows':hits,'exact_A_D_row_matches':fullmatches,'total_returned_rows':len(allrows)})
  own={'pr':n,'disposition':'MERGED_PUBLISHED_TRACKED','original_head':e['original_head'],'accepted_head':e['accepted_head'],'merge_commit':e['merge_commit'],'merged_at':live['mergedAt'],'doi':e['doi'],'record_url':e['record_url'],'metadata_fields_verified':len(expected),'metadata_receipt_normalizations':e['publication_receipt']['metadata_normalizations'],'description_comparison_rule':description_rule,'public_files':fresults,'tracker_range':e['tracker_range'],'global_DOI_rows':hits,'whole_merge_tree_equals_accepted':gitproof['whole_trees_equal'],'own_scoped_merge_files_verified':gitproof.get('scope_file_count')}
 results.append(own)
meta=response('tracker_metadata');sheets=[x['properties'] for x in meta['sheets'] if x['properties']['sheetId']==1254632077]
check('Tracker:spreadsheet_id_gid_and_tab_title',meta['spreadsheetId']=='1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20' and len(sheets)==1 and sheets[0]['title']=='Math Puzzles')
rows=response('tracker_all_A_D').get('values',[])
check('Tracker:exact_A_D_header',pad(rows[0])==['Original Problem','Solution Chat URL','DOI','Notes'])
changed=[]
for rel,pin in binding.items():
 p=ROOT/rel
 if not p.exists() or p.stat().st_size!=pin['bytes'] or sha(p.read_bytes())!=pin['sha256']:changed.append(rel)
private_pins=load(OUT/'INPUT_BINDINGS.json').get('private_readbacks',{})
for key in PRIVATE_KEYS:
 raw_path=OUT/'tmp'/(key+'.json');raw_bytes=raw_path.read_bytes();raw=load(raw_path)
 public=load(OUT/(key+'.json'))
 expected_public=scoped_evidence(key,raw,raw_bytes,entries)
 check(f'Sheet_privacy:{key}:only_allowlisted_own_evidence_published',public==expected_public)
 pin=private_pins.get('tmp/'+key+'.json',{})
 if pin.get('bytes')!=len(raw_bytes) or pin.get('sha256')!=sha(raw_bytes):changed.append('PRIVATE_READBACK:'+key)
ignored=git(['check-ignore','--no-index','--',*[str(OUT/'tmp'/(key+'.json')) for key in PRIVATE_KEYS]]).decode().splitlines()
check('Sheet_privacy:all_raw_spreadsheet_readbacks_ignored',len(ignored)==len(PRIVATE_KEYS) and (OUT/'.gitignore').read_text()=='tmp/\n')
check('All_read_local_input_receipts_and_files_remain_unchanged',not changed,{'files':len(binding),'private_readbacks':len(private_pins),'changed':changed})
failed=[x for x in checks if not x['pass']]
report={'completed_utc':now(),'scope':'Read-only final reconciliation of eight completed eligible PRs only; excludes every skipped PR. Does not itself complete or modify the persistent program goal.','status':'PASS' if not failed else 'MISMATCH_OR_LIMITATION','checks':len(checks),'passed_checks':len(checks)-len(failed),'mandatory_findings':len(failed),'failed_checks':failed,'entries':results,'all_checks':checks,'external_mutations_performed':False,'checkout_index_and_program_state_modified':False,'math_reaudited':False}
dump(OUT/'RECONCILIATION_RESULT.json',report)
print(json.dumps({'status':report['status'],'checks':len(checks),'failed':failed},indent=2,ensure_ascii=False))
