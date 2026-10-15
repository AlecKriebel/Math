"""Source-first static audit. Does not execute/import/compile foreign programs."""
from pathlib import Path
from datetime import datetime,timezone
import collections,hashlib,json,re,sqlite3,stat
root=Path(__file__).resolve().parent
audit=root.parent;repo=audit.parents[2];C=audit/'reviewed_candidate'
rows=[];checks=0
def demand(b,s):
 global checks
 checks+=1
 if not b:raise AssertionError(s)
def read(p):
 demand(p.is_file() and not p.is_symlink(),'regular '+str(p))
 b=p.read_bytes()
 rows.append({'path':str(p),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'classification':'foreign input, excluded from own authorship'})
 return b
def decode(b):
 def pairs(P):
  d={}
  for k,v in P:
   demand(k not in d,'duplicate JSON key');d[k]=v
  return d
 return json.loads(b,object_pairs_hook=pairs)
def J(p):return decode(read(p))
def checkrow(base,row):
 b=read(base/row['path']);demand(len(b)==row.get('bytes',row.get('size')) and hashlib.sha256(b).hexdigest()==row['sha256'],'exact pinned bytes '+row['path']);return b
def same(a,b):
 if type(a) is not type(b):return False
 if isinstance(a,dict):return a.keys()==b.keys() and all(same(a[k],b[k]) for k in a)
 if isinstance(a,list):return len(a)==len(b) and all(same(x,y) for x,y in zip(a,b))
 return a==b

mfraw=read(C/'MANIFEST.json');mf=decode(mfraw)
demand(hashlib.sha256(mfraw).hexdigest()=='09ac3a27edc2113da9574e57a13e7a0c99baa194fa50efb07548ec47fa7493de','actual frozen manifest')
expected={r['path'] for r in mf['files']}|{'MANIFEST.json'}
demand(len(expected)==386 and mf['files_count']==385,'385+self count')
actual={p.relative_to(C).as_posix() for p in C.rglob('*') if p.is_file()}
demand(actual==expected,'exact current closure')
demand(not any(p.is_symlink() for p in C.rglob('*')),'no symlinks')
for r in mf['files']:
 checkrow(C,r);demand(stat.S_IMODE((C/r['path']).stat().st_mode)==0o444,'exact 0444')
demand(stat.S_IMODE((C/'MANIFEST.json').stat().st_mode)==0o444,'manifest exact 0444')
deps=J(C/'CURRENT_DEPENDENCIES.json')
demand(repo/deps['anchor_repository_relative']==audit,'repository audit anchor')
demand(len(deps['files'])==len({r['path'] for r in deps['files']})==517,'unique517 dependencies')
for r in deps['files']:checkrow(audit,r)
foreign_only=[r['path'] for r in deps['files'] if 'foreign_primary_or_derivative_hash_only' in r['roles']]
for name in foreign_only:demand('family_evidence/'+name not in actual,'foreign not republished '+name)
native=J(C/'root_approval/ROOT_CURRENT_INPUT_PREIMAGES.json')
demand(len(native['files'])==13 and same(native['files'],deps['current_native13']),'fresh13')
for r in native['files']:checkrow(repo,r)
capture=J(audit/'root_current_freeze_actual_capture/CAPTURE.json')
for channel in ['stdout','stderr']:checkrow(audit/'root_current_freeze_actual_capture',capture[channel])
demand(capture['pid']==60795 and capture['exit_code']==0 and capture['actual_execution'] is True,'genuine ROOT build metadata')
demand(same(capture['native13_before'],capture['native13_after']) and same(capture['native13_after'],native['files']),'native13 freeze unchanged')
demand(capture['main_head_before']==capture['main_head_after']==native['current_head']=='c61dc0cb572de281b871264819c8b80d647d0373','current root head static capture')
for n in ['PRELAUNCH_OPERATOR.py','PRELAUNCH_SOURCE.py']:read(audit/'root_current_freeze_actual_capture'/n)
demand(hashlib.sha256(read(audit/'root_current_freeze_actual_capture/PRELAUNCH_SOURCE.py')).hexdigest()==capture['source_sha256'],'prelaunch builder hash')

snap=J(C/'original_snapshot_manifest.json')
demand(len(snap['files'])==17 and len(snap['changed_paths'])==18,'original17/diff18')
for r in snap['files']:checkrow(C/'original_archive',r)
diff=read(C/'original_diff.patch')
demand(len(diff)==snap['diff_bytes'] and hashlib.sha256(diff).hexdigest()==snap['diff_sha256'],'full original diff')
demand(len(re.findall(br'^diff --git ',diff,re.M))==18,'18 actual diff sections')
old=read(C/'original_archive/review/PARTIAL.md');final=read(C/'PARTIAL.md')
demand(old.replace(b'Separate adversarial review is pending.',b'Separate adversarial AI review passed; see [the report](review/REVIEW.md).')==final,'sole proof header replacement')
for name in ['PARTIAL.md','check_spectra.py','check_results.json','source_record.json','source_checksums.json','turns.jsonl','review/PARTIAL.md','review/independent_checks.py','review/independent_results.json','review/submitted_check_spectra.py','review/submitted_results.json']:
 demand(read(C/name)==read(C/'original_archive'/name),'current scientific bytes exact '+name)
ledger=[decode(line) for line in read(C/'turns.jsonl').splitlines()]
demand(len(ledger)==2 and [x['turn'] for x in ledger]==[1,2],'original two attempts')
rep=C/'root_evidence/root_original_actual_reproduction_v2';repmanifest=J(rep/'MANIFEST.json')
for r in repmanifest['files']:checkrow(rep,r)
result=J(rep/'RESULT.json');actual_runs=J(rep/'ACTUAL_RUNS.json')
demand(same(result['actual_outer_runs'],actual_runs) and len(actual_runs)==3,'whole run object equality')
for r in actual_runs:
 demand(r['actual_execution'] is True and r['completed'] is True and r['exit_code']==0 and r['pid']>0,'actual run fields')
 demand(datetime.fromisoformat(r['started_utc'])<=datetime.fromisoformat(r['finished_utc']),'ordered actual clocks')
 for key in ['source','stdout','stderr','output_file']:checkrow(rep,r[key])
saved=J(C/'check_results.json');ind=J(C/'review/independent_results.json')
reviewed=J(rep/'reviewed_author_private/check_results.json');fresh=J(rep/'current_author_private/check_results.json');actualind=J(rep/'original_independent_private/independent_results.json')
demand(same(reviewed,saved) and read(rep/'reviewed_author_private/check_results.json')==read(C/'check_results.json'),'whole saved vs actual reviewed author')
expect=dict(saved,partial_sha256=hashlib.sha256(final).hexdigest())
demand(same(fresh,expect) and fresh['assertions']==18306,'current author only qualified header hash difference')
demand(same(ind,actualind) and read(rep/'original_independent_private/independent_results.json')==read(C/'review/independent_results.json'),'whole actual independent typed and bytes')
demand(len(ind['checks'])==ind['passed']==1263 and ind['failed']==0 and all(type(v)is str and v=='PASS' for v in ind['checks'].values()),'every1263 recorded result')
demand(same(result['whole_original_ledger'],ledger),'whole reproduced ledger')

# Independently traverse the complete raw JSON and read-only SQLite join.
cache=repo/'unsolved_math_prioritization/cache'
rawbytes=read(cache/'problems.json');priorbytes=read(cache/'research_results.json')
raw=decode(rawbytes);prior=decode(priorbytes)
demand(len(rawbytes)+len(priorbytes)==149266659,'whole raw corpus bytes')
index={str(p['id']):p for p in raw};codes=collections.Counter(p['problem_number'] for p in raw)
demand(len(raw)==len(index)==15458 and len(prior)==6701,'whole corpus cardinalities')
con=sqlite3.connect((cache/'catalog.sqlite').as_uri()+'?mode=ro&immutable=1',uri=True)
con.execute('PRAGMA query_only=ON')
demand(con.execute('PRAGMA query_only').fetchone()==(1,),'SQL read only')
joined=con.execute('SELECT key,payload,report FROM records ORDER BY key').fetchall();con.close()
demand(len(joined)==15458,'all SQL joins')
for key,payload,report in joined:
 p=dict(index[key]);code=p['problem_number']
 if codes[code]>1 and code in prior:p['_ambiguous_report']=True
 expected_report={} if p.get('_ambiguous_report') else prior.get(code,{})
 demand(same(decode(payload),p) and same(decode(report),expected_report),'full typed raw SQL match '+key)
demand('EP-653' not in prior and same(index['2233'],J(C/'source_record.json')),'absent prior key and exact pinned problem')
demand(J(C/'root_evidence/pinned_prior_report.json')=={},'qualified SQL fallback')

# Verify both original closed families with all individually named exclusions.
family_counts={}
lit=audit/'literal_geometry_family';seal=J(lit/'final_seal.json')
for r in seal['first_party_closed_files']+seal['foreign_primary_excluded_files']:checkrow(lit,r)
for r in seal['foreign_immutable_original_files_read']:checkrow(audit/'source_snapshot_v2',r)
for r in seal['foreign_parent_inputs_excluded']:
 b=read(lit/r['path']);demand(hashlib.sha256(b).hexdigest()==r['sha256'],'literal external input')
demand({p.relative_to(lit).as_posix() for p in lit.rglob('*') if p.is_file()}=={r['path'] for r in seal['first_party_closed_files']+seal['foreign_primary_excluded_files']}|{'final_seal.json'},'literal exact original closure')
family_counts['literal_geometry_family']={'own_excluding_manifest':len(seal['first_party_closed_files']),'foreign_inside':len(seal['foreign_primary_excluded_files']),'foreign_original':17}
ex=audit/'exact_spectrum_family';exseal=J(ex/'OWN_CLOSED_MANIFEST.json')
for key in ['own_files_including_self','foreign_files_inside_root_individually_excluded','foreign_external_read_files_individually_pinned_and_excluded']:
 for r in exseal[key]:
  if r.get('sha256') is None:continue
  p=Path(r['path']);b=read(p);demand(len(b)==r['bytes'] and hashlib.sha256(b).hexdigest()==r['sha256'],'exact family individual '+str(p))
demand({p.relative_to(ex).as_posix() for p in ex.rglob('*') if p.is_file()}=={r['relative_path'] for r in exseal['own_files_including_self']+exseal['foreign_files_inside_root_individually_excluded']},'exact family original closure')
family_counts['exact_spectrum_family']={'own_including_manifest':len(exseal['own_files_including_self']),'foreign_inside':len(exseal['foreign_files_inside_root_individually_excluded']),'foreign_external':len(exseal['foreign_external_read_files_individually_pinned_and_excluded'])}

for n in ['readiness.json','status.json','review/verdict.json']:
 o=J(C/n)
 demand(o['full_problem_solved'] is False and o['novelty_claimed'] is False and o['historical_runtime_certified'] is False and o['historical_verdict_transferred'] is False,'qualified '+n)
 demand(all(o[k] is None for k in ['current_model','current_reasoning_effort','current_deadline_utc','current_verdict']),'current unknowns '+n)
 demand(o['original_substantive_attempts']==2 and o['substantive_attempt_limit']==5 and o['new_substantive_attempts']==0 and o['audit_turns']==0,'attempt accounting')
 demand(o['current_gate']=='PENDING_NEW_WHOLE_CURRENT_SOURCE_FIRST_ADVERSARY','NEW gate pending')
science=J(C/'root_approval/ROOT_SCIENCE_CARD.json');reading=J(C/'root_approval/ROOT_PRIMARY_READ_LEDGER.json')
for obj in [science,reading]:demand(len(obj['root_flags'])==8 and all(type(v)is bool and v is True for v in obj['root_flags'].values()),'eight explicit completed ROOT flags')
demand(science['scope_certificate_sha256']==hashlib.sha256(read(C/'root_approval/ROOT_CURRENT_PARTIAL_SCOPE_CERTIFICATE.md')).hexdigest(),'genuine scope pin')
patch=J(C/'CURRENT_QUEUE_PATCH.json');before=read(C/'queue_proposal/QUEUE_PREIMAGE.md');after=read(C/'queue_proposal/QUEUE_PROSPECTIVE.md')
demand(before==read(repo/'unsolved_math_prioritization/QUEUE.md'),'actual fresh whole queue')
demand(before.count(patch['row_before'].encode())==1 and before.replace(patch['row_before'].encode(),patch['row_prospective'].encode())==after,'sole whole queue row replacement')
oldcols=patch['row_before'].split('|');newcols=patch['row_prospective'].split('|')
demand([i for i,(a,b) in enumerate(zip(oldcols,newcols)) if a!=b]==[8,9,11],'only Status Turns Findings columns')

unique={r['path']:r for r in rows}
(root/'FOREIGN_INPUT_ROWS.json').write_text(json.dumps({'utc':datetime.now(timezone.utc).isoformat(),'rule':'individual actual byte reads, foreign inputs excluded from own authorship; no input copied','files':list(unique.values())},indent=2)+'\n')
output={'status':'PASS_OWN_WHOLE_CURRENT_STATIC_CONTROLS','checks':checks,'candidate_manifest_sha256':hashlib.sha256(mfraw).hexdigest(),'candidate_members_excluding_self':385,'all_candidate_modes':'stat.S_IMODE 0444','dependencies':517,'foreign_hash_only_inside_dependencies':len(foreign_only),'fresh_native_inputs':13,'original_files':17,'diff_sections':18,'typed_saved_actual_author_assertions':18306,'typed_saved_actual_independent_entries':1263,'raw_bytes':149266659,'SQL_rows_typed_compared':len(joined),'closed_family_counts':family_counts,'individual_foreign_input_files':len(unique),'candidate_or_original_programs_imported_compiled_executed':False,'current_positive_approval_authored':False,'limit':'hashes and saved metadata verify present evidence; no historical runtime or outside theorem certification'}
(root/'PACKET_CONTROL_RESULTS.json').write_text(json.dumps(output,indent=2)+'\n');print(json.dumps(output,indent=2))
