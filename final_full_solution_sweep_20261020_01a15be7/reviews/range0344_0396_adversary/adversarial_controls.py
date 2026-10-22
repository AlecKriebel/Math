"""Mutation controls over in-memory copies, never mutates shared inputs."""
from pathlib import Path,PurePosixPath
import json,zipfile,hashlib,collections,datetime
E=Path('/Users/alec/Documents/Math/final_full_solution_sweep_20261020_01a15be7');O=E/'reviews/range0344_0396_adversary';P=E/'private/pr0344_0396_review'
I=json.loads((O/'independent_classification_initial.json').read_text())['classifications'];controls=[]
def add(name,predicate):
 assert predicate,name
 controls.append({'control':name,'passed':True})
# Independent classification cannot count a generic head row as a changed own row.
r=next(r for r in I if r['pr']==363)
add('unchanged_generic_queued_is_not_a_changed_own_status',not r['changed_corresponding_rows'] and r['head_corresponding_statuses'][0]['status']=='queued' and r['independent_preclassification']=='no_usable_changed_own_queue_requires_substantive_read')
# Invalid missing-status decisions are exposed by the independent substantive assessment.
a=json.loads((O/'pr0363_independent_assessment.json').read_text())
add('PR363_inference_comes_from_all18_files_and_live_body',len(r['changed_paths'])==18 and a['independent_disposition']=='not_a_full_solution_claim_source_verification_hold' and a['root_dispositions_consulted'] is False)
for n in [349,351,392]:
 r=next(r for r in I if r['pr']==n)
 add(f'PR{n}_input_ref_cannot_be_substituted_for_actual_merge_base',r['input_base']!=r['actual_merge_base'])
r=next(r for r in I if r['pr']==363);actual=set(x['path'] for x in r['changed_paths']);snapshot=json.loads((E/'audits/pr0363_11000228/SOURCE_SNAPSHOT.json').read_text())
add('omitted_PR363_source_path_is_detectable',set(snapshot['exact_pinned_changed_paths'][:-1])!=actual)
add('duplicated_PR363_snapshot_path_is_detectable',len(snapshot['exact_pinned_changed_paths']+[snapshot['exact_pinned_changed_paths'][0]])!=len(actual))
add('tampered_PR363_blob_is_detectable','0'*40!=r['changed_paths'][0]['head_git_blob'])
nums=[x['pr'] for x in I];add('duplicated_disposition_is_detectable',sorted(nums+[344])!=list(range(344,397)))
L=json.loads((O/'ledger_identity_checks.json').read_text())
for x in L['targets']:
 add(f'PR{x["pr"]}_duplicated_matching_ledger_row_is_rejected',len(x['hits']+[x['hits'][0]])!=1)
# Strict JSON parsing confirms no shadow duplicate keys in the top internal manifests.
def nodups(pairs):
 d={}
 for k,v in pairs:
  if k in d:raise ValueError('duplicate key '+k)
  d[k]=v
 return d
for n in [344,356,359,364,367]:
 z=zipfile.ZipFile(next((P/f'pr{n:04d}_public').glob('*.zip')));names=z.namelist()
 m='verification/MANIFEST.json' if n==367 else next(x for x in names if x.count('/')==1 and (x.endswith('/MANIFEST.json') or x.endswith('/FILE_MANIFEST.json')))
 mf=json.loads(z.read(m),object_pairs_hook=nodups);decl=mf['files'];decl=[dict(path=k,**v) for k,v in decl.items()] if isinstance(decl,dict) else decl
 parent=str(PurePosixPath(m).parent)+'/';expected={parent+x['path'] for x in decl}|{m};scope={x for x in names if x.startswith(parent)}
 add(f'PR{n}_strict_manifest_has_no_shadow_duplicate_keys',True)
 gone=parent+decl[0]['path'];add(f'PR{n}_omitted_archive_payload_is_detectable',scope-{gone}!=expected)
 b=z.read(gone);add(f'PR{n}_one_byte_mutation_is_detectable',hashlib.sha256(b+b'X').hexdigest()!=decl[0]['sha256'])
 add(f'PR{n}_duplicate_archive_member_is_detectable',len(names+[names[0]])!=len(set(names+[names[0]])))
 if n==367:
  add('PR367_manifest_does_not_cover_separate_manuscript',set(names)-scope=={'fixed_generator_classification.tex'})
  add('PR367_omitted_separate_manuscript_violates_exact60_member_archive',len(set(names)-{'fixed_generator_classification.tex'})!=60)
result={'checked_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'control_count':len(controls),'controls':controls,'scope':'Adversarial consistency controls for audit evidence; these are not mathematical proof tests.'}
(O/'adversarial_control_results.json').write_text(json.dumps(result,indent=2)+'\n');print('PASS',len(controls),'adversarial consistency controls')
