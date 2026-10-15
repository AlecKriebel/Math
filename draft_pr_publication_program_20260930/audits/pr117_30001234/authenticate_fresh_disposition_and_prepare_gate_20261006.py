"""Actual fresh-audit authentication and final prepared disposition, no services."""
from pathlib import Path
import datetime, hashlib, json, os, subprocess
A=Path(__file__).resolve().parent
F=A/'exact_prior_disposition_adversary_20261006'
PY='/opt/homebrew/Cellar/python@3.14/3.14.6/Frameworks/Python.framework/Versions/3.14/bin/python3.14'
OUT=A/'ROOT_FRESH_DISPOSITION_AUTHENTICATION_20261006.json'
J=A/'ROOT_FRESH_DISPOSITION_PROCESS_JOURNAL_20261006.json'
events=[]
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def require(value,label):
    if not value:raise ValueError(label)
def sha(body):return hashlib.sha256(body).hexdigest()
def dump(path,obj):path.write_text(json.dumps(obj,indent=2,sort_keys=True)+'\n')
def pin(path):
    require(path.is_file() and not path.is_symlink(),'Regular file required')
    body=path.read_bytes();return {'path':str(path.relative_to(A)),'bytes':len(body),'sha256':sha(body)}
require(not OUT.exists() and not J.exists(),'Existing actual fresh authentication; inspect before repeat')
manifest=F/'OUTPUT_MANIFEST.json'
require(sha(manifest.read_bytes())=='d59f9dfe58c6d00b3090cd3d325a8251d161579c81a2ba0497d228038ece64bc','Fresh manifest changed')
members=json.loads(manifest.read_text())['members'];require(len(members)==58,'Fresh member count')
pins=[]
for member in members:
    path=Path(member['path']);require(path.is_relative_to(F) and 'private' not in path.relative_to(F).parts,'Member outside public family')
    actual=pin(path);require(actual['bytes']==member['bytes'] and actual['sha256']==member['sha256'],'Fresh sealed member changed')
    pins.append(actual)
require(sha((F/'REPORT.md').read_bytes())=='42e4e95d10333332f3301ad1b80aaeb1f26d9b5fbb71551345bd2f8b419738e3','Fresh report changed')
verdict=json.loads((F/'RESULT.json').read_text())
require(verdict['verdict']=='PASS_PROPOSED_ALREADY_SOLVED_DISPOSITION' and not verdict['new_solution_publication_supported'],'Fresh disposition mismatch')
for item in json.loads((F/'DISPOSITION_INPUTS.json').read_text())['inputs']:
    path=Path(item['path']);body=path.read_bytes()
    require(len(body)==item['bytes'] and sha(body)==item['sha256'],'Reviewed proposal changed')
env={'PATH':'/usr/bin:/bin','LANG':'C','LC_ALL':'C','TZ':'UTC','__CF_USER_TEXT_ENCODING':'0x1F5:0x0:0x0'}
mutants=['omit_third_pair_swap','paired_equals_blocked','third_internal_plus_sign','ambient_c1','strict_constraints','drop_generator_rows','redundant_fourth_generator','nonnegative_is_positive']
baselines=[]
for optimized in [False,True]:
    prefix=[PY,'-E','-S','-B','-P']+(['-O'] if optimized else [])
    for mutant in [None,*mutants]:
        argv=prefix+[str(F/'verify_bridge.py')]+(['--mutant',mutant] if mutant else [])
        start=now();child=subprocess.Popen(argv,cwd=F,env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        out,err=child.communicate()
        events.append({'argv':argv,'PID':child.pid,'UTC_start':start,'UTC_end':now(),'exit_code':child.returncode,
          'stdout_bytes':len(out),'stdout_sha256':sha(out),'stdout':out.decode('utf-8','replace'),
          'stderr_bytes':len(err),'stderr_sha256':sha(err),'stderr':err.decode('utf-8','replace'),
          'optimized':optimized,'mutant':mutant})
        dump(J,{'actual_operator_PID':os.getpid(),'events':events})
        if mutant:
            require(child.returncode==2 and json.loads(err)['status']=='rejected','Mutant not rejected')
        else:
            require(child.returncode==0,'Fresh baseline failed')
            result=json.loads(out)
            require(result['active_bases_examined']==5005 and result['feasible_vertices']==15 and result['rational_segment_controls']==495,'Fresh exact mathematical result mismatch')
            result.pop('debug_enabled');baselines.append(result)
require(baselines[0]==baselines[1],'Normal and optimized mathematical results differ')
original=A/'original_head_authentication_20261006'
auth=json.loads((original/'ORIGINAL_AUTHENTICATION.json').read_text())
for item in auth['original_files']:
    path=original/'original_attempt'/item['path'];body=path.read_bytes()
    require(len(body)==item['bytes'] and sha(body)==item['sha256'],'Original body changed')
receipt={'schema':'pr117-root-fresh-disposition-authentication/v1','UTC':now(),'actual_operator_PID':os.getpid(),
 'manifest':pin(manifest),'authenticated_public_members':pins,'authenticated_member_count':58,
 'root_read_full_report_result_and_effective_checker':True,'actual_child_process_count':len(events),
 'both_normal_optimized_baselines_passed':True,'sixteen_mutants_rejected':True,'all20_original_bodies_unchanged':True,
 'fresh_disposition_review_PASS':True,'exact_prior_same_example_authenticated':True,
 'classification':'already_solved exact original target','mathematics_valid':True,'novel_resolution_publication_authorization':False,
 'no_blocking_comment_correction':True,'service_or_native_action_performed':False}
dump(OUT,receipt)
proposal=A/'root_priority_audit_20261006/PROPOSED_CLOSURE_COMMENT.md'
final=A/'CLOSURE_COMMENT_FINAL_20261006.md'
require(not final.exists(),'Existing final comment')
final.write_text('<!-- pr117-exact-takagi-prior-disposition-20261006 -->\n\n'+proposal.read_text())
disposition=A/'ROOT_PRIORITY_DISPOSITION_20261006.md'
disposition.write_text('# PR117: final exact-prior disposition\n\nMathematics and source scope PASS. Three distinct priority families and a fresh independent disposition adversary, all root-authenticated and reproduced in actual normal/optimized processes, establish already_solved for the exact original target. Takagi Example4.4 is in the actual30April2011 arXivv1 p19 and formal2013 Algebra & Number Theory7(4), p940, DOI10.2140/ant.2013.7.917. The c=0 ambient specialization and term permutation(0,3,1,4,5,2) preserve all constraints, objective and every augmented-image fiber; the third generator changes only by unit-1.\n\nThe elementary full-face proof and checks are valid useful exposition. No substantively novel original-target resolution is established. Reasonable attribution/status and guard-only diagnostic repair cannot restore openness or newness of the same published negative answer. Apply an additive native already_solved assessment and the reviewed explanatory comment; close the same head without merging. No manuscript, Zenodo record, DOI or tracker row for117. Immutable20 originals/source/prior/ledger1/5 preserved; proof-search turns added0.\n\nPublished p937 matrix is triangle-labelled; extraction-as4 citations in the sealed historical determinantal report are corrected additively here. Root rejected the out-of-scope Yuen2006 r>s>=3 lead and an unrelated guessed MSP URL. Exact earliest global discovery date is not asserted. The verified2011/2013 explicit prior suffices; no source-access question remains.\n\nRoot actual custody receipts: ROOT_PRIORITY_FAMILY_AUTHENTICATION_20261006.json (99public members,12actual checker processes) and ROOT_FRESH_DISPOSITION_AUTHENTICATION_20261006.json (58public members,18actual checker processes). Closure/native/checkpoint/readback/release remain operational actions and are not claimed executed by this decision.\n')
ready={'schema':'pr117-final-prepared-disposition-gate/v1','UTC':now(),'actual_operator_PID':os.getpid(),
 'PR':117,'original_head':'8163ee0dc7a0f944570925984cef2dc0fb291ad8','problem_id':30001234,
 'mathematical_clearance':True,'fresh_disposition_review_PASS':True,'exact_prior_same_example_authenticated':True,
 'native_status_correction_supported':True,'supported_classification':'already_solved',
 'fresh_disposition_review':'audits/pr117_30001234/exact_prior_disposition_adversary_20261006/REPORT.md',
 'publication_authorization':False,'closing_comment_file':final.name,'closing_comment_sha256':sha(final.read_bytes()),
 'prepared_comment_substantive_body_identical_to_reviewed_proposal':True,'priority_reasoning':pin(disposition),
 'fresh_authentication':pin(OUT),'original_budget':'1/5','new_central_proof_turns':0,
 'math_source_percent':100,'priority_audit_percent':100,'workflow_percent':75,
 'closure_and_native_actions_performed':False,'program_completed':19,'published':11,'persistent_goal_status':'active'}
dump(A/'ROOT_DISPOSITION_READY_20261006.json',ready)
with (A/'RESEARCH_LOG.md').open('a') as h:
    h.write('\n'+now()+': Fresh independent disposition PASS root-authenticated58members, actual normal/O exact baselines and16mutant failures; all20originals unchanged. Three prior families99members already authenticated/replayed. Final exact-prior already_solved decision and reviewed comment prepared; no blocking correction or source-access gap. Math/source/priority100%, workflow75%, program19/99=19.19%,11published; goal active. Closure/native/main checkpoint/release remain unperformed operational actions.\n')
print(json.dumps({k:v for k,v in ready.items() if k not in {'fresh_authentication','priority_reasoning'}},sort_keys=True))
