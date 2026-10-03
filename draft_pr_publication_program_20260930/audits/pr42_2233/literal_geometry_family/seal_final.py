"""Verify the initial closure is untouched and seal all final audit artifacts."""
import datetime, hashlib, json, os, pathlib
ROOT=pathlib.Path(__file__).resolve().parent
initial=json.loads((ROOT/'initial_seal.json').read_text())
for row in initial['first_party_closed_files']+initial['foreign_primary_excluded_files']:
 p=ROOT/row['path'];data=p.read_bytes()
 assert len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256'],row['path']
def entry(p):
 data=p.read_bytes()
 return {'path':str(p.relative_to(ROOT)),'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()}
files=sorted(p for p in ROOT.rglob('*') if p.is_file() and p.name!='final_seal.json')
first=[entry(p) for p in files if 'foreign_primary' not in p.relative_to(ROOT).parts]
foreign=[entry(p) for p in files if 'foreign_primary' in p.relative_to(ROOT).parts]
snapshot=json.loads((ROOT/'candidate_inventory.json').read_text())
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
seal={'sealed_utc':now,'seal_pid':os.getpid(),'scientific_completion_percent':5,'audit_completion_percent':100,
 'status':'SCOPED_MATHEMATICS_CHECKED_WITH_PRIOR_PROVENANCE_CORRECTION',
 'original_head':snapshot['original_head'],'actual_base':snapshot['actual_base'],
 'initial_closure_unchanged':True,'new_substantive_attempts':0,'additional_original_audit_turns':0,
 'initial_seal_sha256':hashlib.sha256((ROOT/'initial_seal.json').read_bytes()).hexdigest(),
 'first_party_closed_files':first,'foreign_primary_excluded_files':foreign,
 'foreign_immutable_original_files_read':snapshot['files'],
 'foreign_parent_inputs_excluded':[{'path':'../snapshot_manifest_v2.json','sha256':snapshot['snapshot_manifest_sha256']},
 {'path':'../pinned_problem.json','sha256':hashlib.sha256((ROOT.parent/'pinned_problem.json').read_bytes()).hexdigest()},
 {'path':'../pinned_prior_report.json','sha256':hashlib.sha256((ROOT.parent/'pinned_prior_report.json').read_bytes()).hexdigest(),'qualification':'SQL fallback {}, raw prior key ROOT-reported absent, not a fetched result'}],
 'historical_limits':'No original model/runtime/search-history attestation, no complete EF/CI or Janzer proof reading, no novelty or papers/DOI claimed',
 'independence_limit':initial['independence_limit'],
 'self_exclusion':'final_seal.json is the final seal record and does not hash itself; no future head verdict synthesized'}
(ROOT/'final_seal.json').write_text(json.dumps(seal,indent=2)+'\n')
print(json.dumps({'sealed_utc':now,'pid':os.getpid(),'first_party_files':len(first),'foreign_primary_files':len(foreign),
 'immutable_original_files':len(snapshot['files']),'final_seal_sha256':hashlib.sha256((ROOT/'final_seal.json').read_bytes()).hexdigest()},indent=2))
