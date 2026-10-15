"""ROOT mathematical gate after independent proofs and guarded fresh reproduction."""
from pathlib import Path
from hashlib import sha256
from datetime import datetime, timezone
import json, os
A=Path(__file__).resolve().parent.parent
def require(v,msg):
    if not v:raise RuntimeError(msg)
def read(p):return json.loads(p.read_bytes())
def pin(p):
    require(p.is_file() and not p.is_symlink(),'regular evidence')
    b=p.read_bytes();return {'path':str(p.relative_to(A)),'bytes':len(b),'sha256':sha256(b).hexdigest()}
def check(p,sha,size=None):
    r=pin(p);require(r['sha256']==sha and (size is None or r['bytes']==size),'evidence changed: '+str(p));return r
manifest=A/'ORIGINAL_SUBMITTED_ATTEMPT_MANIFEST.json';check(manifest,'efd273eb031989bddae0ae89cad8d2e92cc6f531d2076d20d09155a8b508cb02')
for r in read(manifest)['original_files']:check(A/'original_submitted_attempt'/r['path'],r['sha256'],r['bytes'])
initial=A/'ROOT_INITIAL_REVIEW_READBACK_20261008.json';check(initial,'e6e3a2224d44c5f4d1434f9d2d77765580251a7c510b5f481b42f7716f5f73f9')
support=A/'verification_code_adversary_20261008/support_checker_hardening_20261008'
check(support/'SUPPORT_FINAL_REPORT.md','5dc82aa60044efa2357dbc22f45a39c408d1c94aee896e5e01f2d2307f92fa67')
for r in read(support/'SUPPORT_ARTIFACT_INVENTORY.json'):check(support/r['path'],r['sha256'],r['bytes'])
children=[]
for d in sorted((support/'raw_runs').iterdir()):
    r=read(d/'process_receipt.json')
    require(r['wait_completed_and_reaped'] is True and r['group_absent_after_wait'] is True and r['termination_reason'] is None and r['exit_expectation_met'] is True,'support child closure')
    for kind in ('stdout','stderr'):check(d/(kind+'.txt'),r['raw_'+kind+'_sha256'],r['raw_'+kind+'_bytes'])
    require(r['raw_stdout_bytes']+r['raw_stderr_bytes']<=r['raw_output_cap_bytes'],'support raw cap')
    children.append({'label':r['label'],'PID':r['pid'],'receipt':pin(d/'process_receipt.json')})
require(len(children)==61,'support child count')
fresh=A/'math_operations_20261008/private/ROOT_GUARDED_SUPPORT_02/RECEIPT.json'
check(fresh,'e592ee25820b793556bbaf8b67ddde36af77054fe17d0747be0148d0ef7cf749')
repro=read(fresh);require(repro['status']=='PASS_GUARDED_SUPPORT_FRESH_CLOSED_REPRODUCTION' and repro['all_obtained_children_complete'] is True and len(repro['children'])==8,'actual ROOT reproduction')
for r in repro['children']:
    require(r['child_reaped'] is True and r['process_group_absent'] is True and r['exit_code']==0 and r['fresh_output_and_scientific_data_verified'] is True,'ROOT scientific child closure')
    d=fresh.parent/r['label']
    for kind in ('stdout','stderr'):check(d/(kind+'.txt'),r[kind]['sha256'],r[kind]['bytes'])
old=A/'math_operations_20261008/private/ROOT_GUARDED_SUPPORT_01/author_normal/PROCESS_RECEIPT.json'
failed=read(old);require(failed['exit_code']==0 and failed['child_reaped'] is True and failed['process_group_absent'] is True,'initial wrapper child was not closed')
failed_assessment={'schema':'pr148-root-wrapper-diagnostic/v1','UTC':datetime.now(timezone.utc).isoformat(),'actual_ROOT_PID':os.getpid(),'cause':'ROOT wrapper expected generic PASS instead of preserved PASS_EXACT_SIX_PERIOD_COUNTEREXAMPLE. Scientific child exit0 and its output matches expected numerical receipt; wrapper rejected, no global PASS accepted. Corrected exact status schema and used fresh ROOT_GUARDED_SUPPORT_02 directory.','child_receipt':pin(old),'provider_or_native_mutation':False}
(A/'ROOT_GUARDED_SUPPORT_DIAGNOSTIC_20261008.json').write_text(json.dumps(failed_assessment,indent=2,sort_keys=True)+'\n')
families=[{'identity':'pr148_geometry_falsification_20261008','mechanism':'Finite chord restrictions, full physical reflection, strict convexity and outer intersections in exact quadratic fields; smooth chord-midpoint map with independent polynomial divisibility gives T^3=antipode.','report':pin(A/'geometry_falsification_20261008/GEOMETRY_AUDIT.md'),'status':'PASS','gap':'No mathematical gap in the assigned counterexample scope. Initial input read exposed elementary author prose, explicitly disclosed; no original executable was consulted.'},
{'identity':'pr148_analytic_family_adversary_20261008','mechanism':'Projective tangent correspondence and Vieta-product polynomial identity, support-area formulas and half-angle normal identity; recovers both orbit lists from one connected physical return map.','report':pin(A/'analytic_family_adversary_20261008/ANALYTIC_AUDIT.md'),'status':'PASS','gap':'No mathematical gap in assigned scope; historical priority and workflow excluded.'},
{'identity':'pr148_verification_code_adversary_20261008','mechanism':'Distinct inherited exact scaled metrics and fresh author reproduction; meaningful false geometry, value, polynomial, field, square-root and receipt controls normal/-O.','report':pin(A/'verification_code_adversary_20261008/AUDIT_REPORT.md'),'support_report':pin(support/'SUPPORT_FINAL_REPORT.md'),'status':'PASS_AFTER_GUARDED_SUPPORT_INTEGRATION','gap':'Original assert-only scripts remain historical; active sources use explicit guards and fresh current-run receipt binding.'}]
gate={'schema':'pr148-root-mathematical-gate/v1','UTC':datetime.now(timezone.utc).isoformat(),'actual_ROOT_PID':os.getpid(),'PR':148,'original_head':'538fd2584f7dc7375e4eaa91d73daddde3d073cd','status':'PASS_LITERAL_K108_COUNTEREXAMPLE','mathematical_clearance':True,'mandatory_mathematical_findings':[],
'target':'Literal Table2 k108=(A\u2032/A)/product sin(theta_i/2), N=2 mod4, ordinary original internal polygon angles; conjectured constancy on each fixed confocal billiard family.',
'strongest_verified_result':'Two strict convex primitive six-period physical billiard orbits on E:x^2/4+y^2=1 with the same nondegenerate nested confocal caustic x^2/(32/9)+y^2/(5/9)=1 lie on one smooth connected directed family, and have quotients11664/3125 and3645/1024, positive difference553311/3200000. Direct T^3(p)=-p proof establishes family membership without a porism black box.',
'source_convention_refinement':'Section3.1 calls theta polygon angles; ordinary internal-angle interpretation is calibrated by source k101=sumcos(theta)=JL-N. Do not misquote internal as an explicit Section3.1 adjective. Table2 assertion is experimental/unproved, not an established theorem.',
'scope_limits':['This single admissible N6 counterexample refutes the universal printed assertion; it does not derive a corrected invariant for every period.','Shared product5/9 and area product320/9 are two-member controls only.','No official erratum, absolute/exclusive priority, independence of discovery or conventional human refereeing is certified.'],
'approach_families':families,'initial_review_readback':pin(initial),'guarded_support_source_manifest':pin(A/'guarded_support_v1/SOURCE_MANIFEST.json'),'actual_ROOT_reproduction':pin(fresh),'closed_support_adversarial_children':children,
'original_effort':'1/5','original_author_approach_ledger_present':True,'original_author_approach_ledger_path':'turns.json','original_reported_substantive_approach_count':1,'actual_timestamped_author_chat_turn_ledger_present':False,'original_native_transition_ledger_present':False,'new_central_proof_search_turns':0,'original20_preserved':True,'mathematical_audit_percent':100,'PR148_best_guess_workflow_percent':30,'priority_acceptance':None,'publication_acceptance':None,'native_acceptance':None,'persistent_goal_complete':False}
out=A/'ROOT_MATHEMATICAL_GATE_20261008.json';require(not out.exists(),'gate already exists')
out.write_text(json.dumps(gate,indent=2,sort_keys=True)+'\n')
with (A/'RESEARCH_LOG.md').open('a') as f:f.write('\n'+gate['UTC']+' — Mathematical/source checkpoint100%; PR148 workflow estimate30%; program26/99=26.26%,14published, persistentgoalACTIVE unfinished. Two independent physical-family proofs and exact geometry calculations pass. Original291/inherited272 controls reproduced; original optimization/receipt/staleness issues demonstrated and active support repaired with explicit guards, frozen source pins and8 fresh closed ROOT normal/-O reproductions. Supplemental61 adversarial children closed; original20 and all reviewer sources unchanged. First ROOT wrapper status-schema diagnostic retained honestly; no science contradiction or stale success accepted. Priority now next; no paper/DOI/tracker/native/PR action. Original1/5 is one reported approach, not timestamped chat/native history; zero new central proof-search turns. Gate '+pin(out)['sha256']+'.\n')
print(json.dumps({'status':gate['status'],'gate':pin(out),'workflow_percent':30}))
