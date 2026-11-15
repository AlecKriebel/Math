"""Pure offline preflight closure; no network, Git, PDF extraction or replay.
Byte/schema/result consistency is not a proof of all-history absence.
"""
from pathlib import Path
from copy import deepcopy
import hashlib,json,sys
O=Path(__file__).resolve().parent
TERMINAL={'OWNED_MANIFEST.json','SEAL.json','CLOSURE.json'};N=0
OLD='7a24ec1dcb73a5e06ba82ff9cccda54e73f9deec';CURRENT='4b890b5e4f583ed562ba7291ae367c6ff70c5090'
VERSIONS={'23430498':('1.0','2026-10-13'),'23149775':('1.0','2026-10-04'),'23331080':('1.0','2026-10-12')}
def ck(ok,msg):
 global N
 N+=1
 if not ok:raise ValueError(msg)
def j(p):return json.loads(Path(p).read_text())
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def native(name):
 r=j(O/name);ck(r.get('isError') is False,'successful retained GitHub GET '+name)
 return json.loads(r['structuredContent']['content'])
def bound(p,e):
 p=Path(p);ck(p.is_file() and not p.is_symlink(),'regular bound file '+str(p));ck(p.stat().st_size==e['bytes'] and sha(p)==e['SHA256'],'whole bytes/hash '+str(p))
def valid(v):
 assert v['schema']=='bounded_three_exact_paper_correspondence_v1'
 assert v['historical_docs_tree']==OLD and v['current_docs_tree']==CURRENT
 assert v['only_changed_path']=='docs/papers/gromov-unitary-lipschitz/index.html'
 assert v['worldwide_or_all_history_absence_claimed'] is False and v['current_single_leaf_delta_explicitly_qualified'] is True
 assert v['binary_archive_contents_searched'] is False and v['new_PDF_extractions']==v['source_program_replays']==0
 assert v['scientific_reassessment'] is False and v['production_docs_git_sheet_native_changes'] is False and v['outside_contact'] is False
 assert set(v['targets'])==set(VERSIONS)
 for rid,(version,date) in VERSIONS.items():
  t=v['targets'][rid];assert (t['native_version'],t['declared_date'])==(version,date)
  assert t['literal_disposition']=='NO_MATCH_FOUND_IN_AUTHENTICATED_RELEASED_DOCS_WITH_VERIFIED_SINGLE_LEAF_DELTA'
  for k in ('genuine_matching_article_found','unresolved_positive_identity_candidate','redirect_prepared','redirect_applied','live_newsite_replacement_verified_by_this_task','root_redirect_approval_obtained_by_this_task'):assert t[k] is False
  for k in ('matching_legacy_URL','candidate_redirect_destination','redirect_asset_plan'):assert t[k] is None
def main():
 inputs=j(O/'INPUT_MANIFEST.json');owned=j(O/'OWNED_MANIFEST.json')
 for e in inputs['inputs']:bound(e['path'],e)
 actual={str(p.relative_to(O)) for p in O.rglob('*') if p.is_file() and str(p.relative_to(O)) not in TERMINAL}
 ck(actual=={e['path'] for e in owned['files']},'exact owned file set')
 for e in owned['files']:
  p=O/e['path'];ck(p.resolve().is_relative_to(O),'owned confinement');bound(p,e)
 targets=j(O/'TARGET_IDENTITIES.json')
 for rid,t in targets.items():
  original=Path(t['SOURCE_READY']['path']);bound(original,t['SOURCE_READY']);snapshot=Path(t['whole_SOURCE_READY_snapshot']);ck(original.read_bytes()==snapshot.read_bytes(),'whole literal SOURCE_READY snapshot/schema '+rid)
  d=j(snapshot)
  ck((t['version'],t['declared_date'])==VERSIONS[rid] and t['title']==d['title'],'exact native target/version '+rid)
  key='all_native_assets_in_original_order' if rid in ('23430498','23149775') else 'all_assets_in_original_order'
  ck([a['original_api_file_object'] for a in d[key]]==[a['original_native_file_object'] for a in t['native_assets_in_original_order']],'whole native asset object/order '+rid)
  for a in t['native_assets_in_original_order']:
   bound(a['path'],a);ck('md5:'+hashlib.md5(Path(a['path']).read_bytes()).hexdigest()==a['original_native_file_object']['checksum'],'native original MD5 '+rid)
 historical=j(O/'HISTORICAL_DOCS_BINDINGS.json');extracts=j(O/'REUSED_EXTRACT_BINDINGS.json')
 ck(len(historical)==254 and len(extracts)==76 and sum(e['pages'] for e in extracts)==854,'bounded old inventory/derivative counts')
 bypath={e['path']:e for e in historical}
 for e in extracts:
  p=Path(e['path']);ck(p.stat().st_size==e['bytes'] and sha(p)==e['sha256'],'reused complete derivative bytes '+e['public_path'])
  ck(bypath[e['public_path']]['blob']==e['pdf_blob'] and bypath[e['public_path']]['sha256']==e['pdf_sha256'],'PDF parent/object binding '+e['public_path'])
 tree=native('REMOTE_DOCS_TREE_GET.json');ck(tree['sha']==CURRENT and tree['truncated'] is False,'complete current recursive docs tree')
 new={'docs/'+e['path']:e for e in tree['tree'] if e['type']=='blob'};ck(new.keys()==bypath.keys() and len(new)==254,'no current added/removed blob paths')
 delta=[{'path':path,'old_blob':bypath[path]['blob'],'new_blob':new[path]['sha'],'bytes':new[path]['size']} for path in sorted(new) if new[path]['sha']!=bypath[path]['blob']]
 ck(delta==j(O/'CURRENT_DOCS_DELTA.json')==[{'path':'docs/papers/gromov-unitary-lipschitz/index.html','old_blob':'a19d14821dc44c36def20b345dcbcd82a85d572b','new_blob':'b3e1157aebc6b9a30fba4367a368c5be20de863d','bytes':913}],'exact single current leaf delta')
 for name in ('REMOTE_ROOT_TREE_GET.json','UNITARY_ROOT_TREE_GET.json','REMOTE_CLOSING_ROOT_TREE_GET.json'):
  r=native(name);ck(r['truncated'] is False and next(e['sha'] for e in r['tree'] if e['path']=='docs')==CURRENT,'observed epoch same current docs '+name)
 changed=(O/'current-unitary-leaf.html').read_bytes();ck(len(changed)==913 and hashlib.sha1(b'blob 913\0'+changed).hexdigest()=='b3e1157aebc6b9a30fba4367a368c5be20de863d','whole changed current leaf')
 selected=j(O/'SELECTED_CURRENT_IDENTITIES.json')
 for r in selected:
  b=Path(r['evidence_body']).read_bytes();ck(len(b)==r['bytes'] and hashlib.sha256(b).hexdigest()==r['SHA256'] and hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==r['blob']==new[r['public_path']]['sha'],'whole selected actual current body')
 searches=j(O/'SEARCH_RESULTS.json');receipt=j(O/'CORPUS_RECEIPT.json')
 for epoch in ('historical','current'):
  rows=searches[epoch];ck(len(rows)==260 and sum(r['kind']=='complete_reused_PDF_text' for r in rows)==76 and sum(r['kind']=='decoded_visible_HTML' for r in rows)==47,'exact searched epoch representations '+epoch)
  counts={g:sum(bool(r['groups'][g]) for r in rows) for g in searches['queries']};ck(counts==receipt[epoch+'_hit_representation_counts'],'complete stored query counts '+epoch)
  for rid in VERSIONS:ck(counts[rid+'_record_DOI_concept']==counts[rid+'_exact_title']==0,'no exact target title/identifier hit '+rid+' '+epoch)
 ck(receipt['native_full_asset_hash_matches']==[] and receipt['new_PDF_extractions']==0 and receipt['binary_support_archives_recursively_expanded_or_text_searched'] is False,'asset/coverage limits retained')
 ck(all(e['pass'] for e in j(O/'QUERY_CONTROLS.json')),'positive search controls retained')
 ck(len(j(O/'EXCLUSIONS.json'))==3 and all(e['not_mathematical_reassessment'] for e in j(O/'EXCLUSIONS.json')),'explicit actual false-candidate exclusions')
 v=j(O/'VERDICT.json');valid(v);ck(True,'literal bounded custom verdict')
 mutants=[]
 for key,value in [('worldwide_or_all_history_absence_claimed',True),('current_docs_tree',OLD),('current_single_leaf_delta_explicitly_qualified',False),('new_PDF_extractions',76),('binary_archive_contents_searched',True),('scientific_reassessment',True),('production_docs_git_sheet_native_changes',True)]:
  x=deepcopy(v);x[key]=value;mutants.append(x)
 for rid in VERSIONS:
  for key,value in [('genuine_matching_article_found',True),('redirect_prepared',True),('matching_legacy_URL','https://example.org/topic-only/'),('native_version','unverified latest')]:
   x=deepcopy(v);x['targets'][rid][key]=value;mutants.append(x)
 for x in mutants:
  try:valid(x)
  except AssertionError:ck(True,'synthetic scope/false-match/authorization mutant rejected')
  else:raise ValueError('accepted scope/false-match/authorization mutant')
 sealed=False
 if (O/'SEAL.json').exists():
  seal=j(O/'SEAL.json')
  for name,key in [('REPORT.md','REPORT_SHA256'),('VERDICT.json','VERDICT_SHA256'),('INPUT_MANIFEST.json','INPUT_MANIFEST_SHA256'),('OWNED_MANIFEST.json','OWNED_MANIFEST_SHA256'),('CLOSURE.json','CLOSURE_SHA256')]:ck(sha(O/name)==seal[key],'final seal '+name)
  sealed=True
 print(json.dumps({'status':'PASS','read_only':True,'network_Git_PDF_extraction_or_program_replay':False,'checks':N,'inputs':len(inputs['inputs']),'owned_files':len(owned['files']),'synthetic_mutants_rejected':len(mutants),'final_seal_checked':sealed,'scope':'custody, observed epochs and bounded stored-result consistency; not all-history absence'},indent=2))
if __name__=='__main__':
 try:main()
 except Exception as e:print(json.dumps({'status':'FAIL','checks_completed':N,'error':str(e)}));sys.exit(1)
