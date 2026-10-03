"""ROOT records genuine completed reading, exact evidence and current native preimages."""
from pathlib import Path
import datetime as dt,hashlib,json,os,stat,subprocess
A=Path(__file__).resolve().parent;R=A.parents[2];S=A/'current_preparation_family';F=A/'current_source_adversary_family'
def sha(b):return hashlib.sha256(b).hexdigest()
def load(p):return json.loads(p.read_bytes())
def ref(p):
 b=p.read_bytes();return {'path':p.relative_to(A).as_posix(),'bytes':len(b),'sha256':sha(b)}
def dump(name,j):
 with (A/name).open('x') as f:json.dump(j,f,indent=2);f.write('\n')
def closure(d,name,pinned,count):
 m=load(d/name);assert sha((d/name).read_bytes())==pinned and len(m['files'])==count
 names={z['path'] for z in m['files']}|{name};assert len(names)==count+1 and {p.relative_to(d).as_posix() for p in d.rglob('*') if p.is_file()}==names
 assert {p.relative_to(d).as_posix() for p in d.rglob('*') if p.is_dir()}=={q.as_posix() for n in names for q in Path(n).parents if str(q)!='.'}
 for p in d.rglob('*'):assert not p.is_symlink() and (p.is_dir() or stat.S_IMODE(p.stat().st_mode)==0o444)
 for z in m['files']:
  b=(d/z['path']).read_bytes();assert type(z['bytes']) is int and len(b)==z['bytes'] and sha(b)==z['sha256']
 assert stat.S_IMODE((d/name).stat().st_mode)==0o444
 return ref(d/name)
assert __debug__;src=Path(__file__).read_bytes();(A/'ROOT_CURRENT_PREREQUISITES_PRELAUNCH_SOURCE.py').write_bytes(src)
sources=[closure(S,'PREPARATION_MANIFEST.json','be1217cc9c67dad1d5e528b547d332463e0b742dd1592602efe601b4c2d165a1',47),closure(F,'OWN_CLOSURE.json','bc8495cf37aae77021d2ef10f0868f0b69eefbff02131ae979b9de354814203b',70)]
assert sha((S/'prepare_current_packet.py').read_bytes())=='7bde800ce050ddf1a9ac071ff54551813e87309eae9834805b3ef632b4342aff' and sha((S/'capture_root_builder_operation.py').read_bytes())=='7f9c717bd3b8ef32160d4388f38ddaf3617c04c1e5c8c3884dd04725684acd3f'
verdict=load(F/'VERDICT.json');assert verdict['verdict']=='PASS_SOURCE_ONLY_QUALIFIED_NO_MANDATORY_CORRECTION' and verdict['mandatory_source_corrections']==verdict['mandatory_mathematical_corrections']==[]
caps=[]
for z in load(F/'OWN_CLOSURE.json')['own_actual_control_captures']:
 d=F/z['directory'];c=load(d/'CAPTURE.json');assert sha((d/'CAPTURE.json').read_bytes())==z['capture_sha256'] and c['pid']==z['child_pid'] and c['exit_code']==z['exit_code'] and c['actual_execution'] is c['completed'] is True and c['source_unchanged'] is c['operator_unchanged'] is True and c['status']=='PASS_OWN_EXPECTED_CONTROL_OUTCOME'
 assert sha((d/'PRELAUNCH_SOURCE.py').read_bytes())==c['source_sha256'] and sha((d/'PRELAUNCH_OPERATOR.py').read_bytes())==c['operator_sha256']
 assert dt.datetime.fromisoformat(c['started_utc'])<dt.datetime.fromisoformat(c['finished_utc'])<=dt.datetime.now(dt.timezone.utc)
 for k in ['stdout','stderr']:
  b=(d/c[k]['path']).read_bytes();assert len(b)==c[k]['bytes'] and sha(b)==c[k]['sha256']
 caps.append(c)
D=A/'root_original_actual_reproduction';m=load(D/'MANIFEST.json');closure(D,'MANIFEST.json',sha((D/'MANIFEST.json').read_bytes()),m['files_count']);summary=load(D/'ROOT_CURRENT_REPRODUCTION_SUMMARY.json')
assert summary['actual_reproductions_completed'] is True and summary['prior_raw_key_present'] is True and len(summary['actual_replay_captures'])==2 and summary['actual_replay_captures'][0]['path']!=summary['actual_replay_captures'][1]['path']
notes=(A/'ROOT_SOURCE_MATCH_AND_PROOF_NOTES.md').read_text();assert len(notes)>8000 and not notes.startswith('# DRAFT')
now=dt.datetime.now(dt.timezone.utc).isoformat();head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=R).decode().strip();assert subprocess.check_output(['git','branch','--show-current'],cwd=R).strip()==b'main'
reading_notes='ROOT personally read original partial proof, both helper sources, complete old report/verdict and source/metadata/ledger, recovered primary Section3, full six-page CNRS preprint, and bounded Asmussen pp739–741 OCR with pp740–741 pixels. ROOT independently derived finite-window TV, full-path conditional projection and finite-history L1 proof for every fixed joining, stated metric law, dependent finite/tight offset bounds and setwise boundary. Entire actual885/885/3044 outputs byte-exact under88783 and full149266659 raw/prior and15458SQL under89614 were checked; prior key is PRESENT matching the wrapper upstream dict. Actual97408 validates original18/whole19diff reconstruction, both full family closures, original auxiliary186 and64 excluded foreign bodies, SOURCE47 and newsource70+self, plus complete first-party ROOT closure. ROOT fully read631-line builder/129-line operator, contract, qualifications, drafts, handwritten private controls and complete new source report/verdict. Source trust boundary remains honest ROOT personal attestation; actual distinct replay roles and exact new-adversary hashes are separately recorded. No novel result/full characterization/paper/newDOI/tracker; NEW whole-current review PENDING. Own failed wrapper88914 and closure96803 are preserved with separately successful corrected actual89614/97408; empty common stderr bytes are not foreign-body copying.'
scope='# ROOT PR45 scoped synchronous-obstruction acceptance\n\nROOT_SCOPE_ACCEPTED_SYNCHRONOUS_OBSTRUCTION_ONLY\n\nPR45 / 9900007 / AMR-098-0007\nHead: d9b4acf5d070d1f04ffac86a4f08916a5629ff16\nGitHub base: c6975ca76f9f667f1250ba403d0e6da2aafe14d0\nActual merge base: 01358d66fc67d1c462bddf31c0d4ee5b120e6737\nStatus: unsolved\nOriginal turns: 1/5; new: 0; audit: 0\nFull problem solved: false\nNovelty: false\nNEW whole-current review: PENDING\nPaper/new DOI/tracker: false\n\n'+reading_notes+'\n'
with (A/'ROOT_CURRENT_PARTIAL_SCOPE_CERTIFICATE.md').open('x') as f:f.write(scope)
evidence={'schema':'PR45_ROOT_EVIDENCE_BINDINGS_v1','approved_by_root':True,'created_utc':now,'notes':'Entire actual first-party ROOT closure is separately checked; two distinct genuine C1 roles and all inner outputs are preserved. Foreign64 primary/access/OCR bodies and whole raw caches/SQL are excluded. Present source record has nested problem/upstream with PRESENT prior dict, not absent fallback.','manifest':ref(D/'MANIFEST.json'),'proof_notes':ref(A/'ROOT_SOURCE_MATCH_AND_PROOF_NOTES.md'),'summary':ref(D/'ROOT_CURRENT_REPRODUCTION_SUMMARY.json')};dump('ROOT_EVIDENCE_BINDINGS.json',evidence)
paths=['draft_pr_publication_program_20260930/inventory.json']+['unsolved_math_prioritization/'+n for n in ['QUEUE.md','state.json','history.jsonl','catalog.json','assessments.json','queue.py','policy.json','manifest.json','cache/problems.json','cache/research_results.json','cache/catalog.sqlite','review_v2/related_target_groups.json']]
fresh={'schema':'PR45_ROOT_FRESH13_INPUT_PREIMAGES_v1','approved_by_root':True,'created_utc':now,'reason':'Actual present main and whole thirteen current native/program bodies after verified PR43 acceptance and published checkpoints; earlier foreign hashes are historical evidence only, these actual preimages govern this administrative freeze.','current_head':head,'files':[]}
for n in sorted(paths):
 p=R/n;b=p.read_bytes();assert not p.is_symlink();fresh['files'].append({'path':n,'bytes':len(b),'sha256':sha(b)})
dump('ROOT_CURRENT_INPUT_PREIMAGES.json',fresh)
ledger=load(S/'DRAFT_ROOT_READ_LEDGER.json');ledger.update(created_utc=now,reading_completed=True,root_flags={k:True for k in ledger['root_flags']},reading_notes=reading_notes,scope_certificate_sha256=sha(scope.encode()),preparation_manifest_sha256=sources[0]['sha256'],source_qualification_sha256=sha((S/'SOURCE_PRECISION_QUALIFICATIONS.md').read_bytes()),evidence_bindings_sha256=sha((A/'ROOT_EVIDENCE_BINDINGS.json').read_bytes()),family_manifest_sha256={n:info['manifest']['sha256'] for n,info in load(S/'STATIC_INPUT_BINDINGS.json')['families'].items()});dump('ROOT_PRIMARY_READ_LEDGER.json',ledger)
science=load(S/'DRAFT_ROOT_SCIENCE_CARD.json');science.update({k:v for k,v in ledger.items() if k!='schema'});science.update(partial_valid=True,read_ledger_sha256=sha((A/'ROOT_PRIMARY_READ_LEDGER.json').read_bytes()),current_input_manifest_sha256=sha((A/'ROOT_CURRENT_INPUT_PREIMAGES.json').read_bytes()));dump('ROOT_SCIENCE_CARD.json',science)
for z in fresh['files']:b=(R/z['path']).read_bytes();assert len(b)==z['bytes'] and sha(b)==z['sha256']
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=R).decode().strip()==head and Path(__file__).read_bytes()==src
result={'schema':'pr45-root-complete-current-source-inspection/v1','status':'PASS','utc':now,'source_closures':sources,'entire_source_verdict':verdict,'complete_actual_source_captures':caps,'source_adversary_report':ref(F/'REPORT.md'),'source_adversary_verdict':ref(F/'VERDICT.json'),'personally_complete_source_report_read':True,'first_party_exclusions_and_distinct_actual_replay_roles_checked':True,'new_whole_current_gate':'PENDING','original_attempts':1,'new_substantive_attempts':0,'audit_turns':0,'full_problem_solved':False,'real_prerequisites':[ref(A/n) for n in ['ROOT_CURRENT_PARTIAL_SCOPE_CERTIFICATE.md','ROOT_PRIMARY_READ_LEDGER.json','ROOT_SCIENCE_CARD.json','ROOT_CURRENT_INPUT_PREIMAGES.json','ROOT_EVIDENCE_BINDINGS.json']]};dump('ROOT_SOURCE_SAFETY_INSPECTION.json',result)
print(json.dumps({'status':'PASS_REAL_ROOT_CURRENT_PREREQUISITES','head':head,'inspection':ref(A/'ROOT_SOURCE_SAFETY_INSPECTION.json'),'all_nine_genuine_ROOT_reading_flags':True,'prior_key_present':True}))
