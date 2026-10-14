"""Authenticate completed family artifacts; emit a bounded mathematical gate."""
from pathlib import Path
import datetime, hashlib, json, os

ROOT=Path(__file__).resolve().parent
def pin(path):
    body=path.read_bytes()
    return {'path':str(path.relative_to(ROOT)),'bytes':len(body),'sha256':hashlib.sha256(body).hexdigest()}

expected_manifests=[
 ('global_flow_attractor_adversary_20261006','e3984bee41d28a5591fff4c1770d922b0e279d16e6dc8fb2e8d58e4cf685f281'),
 ('lyapunov_dimension_adversary_20261006','5bcf9cc8650fca547fd8f367efacd33bf4ea6ca8178836dfb8a86f1a0f73b8f8'),
 ('primary_source_scope_adversary_20261006','76c529cfd9c3161a401bd29955e5d1cccdb5507b0b9915f474c385183ddb6335'),
]
family_records=[]
for name, expected in expected_manifests:
    folder=ROOT/name
    manifest=folder/'OUTPUT_MANIFEST.json'
    if pin(manifest)['sha256']!=expected:
        raise RuntimeError('Offered family manifest changed: '+name)
    metadata=json.loads(manifest.read_text())
    records=[]
    for item in metadata.get('members',metadata.get('files',[])):
        path=Path(item['path'])
        path=path if path.is_absolute() else folder/path
        if not path.resolve().is_relative_to(folder.resolve()):
            raise RuntimeError('Manifest member outside family')
        actual=pin(path)
        if any(actual[k]!=item[k] for k in ['bytes','sha256']):
            raise RuntimeError('Family body pin mismatch: '+str(path))
        records.append(actual)
    if not records:
        raise RuntimeError('Empty family manifest')
    family_records.append({'family':name,'manifest':pin(manifest),'members':records})

auth=json.loads((ROOT/'original_head_authentication_20261006/ORIGINAL_AUTHENTICATION.json').read_text())
original_records=[]
for item in auth['all_original_files']:
    path=ROOT/'original_head_authentication_20261006/original_attempt'/item['path']
    actual=pin(path)
    if any(actual[k]!=item[k] for k in ['bytes','sha256']):
        raise RuntimeError('Immutable original changed')
    original_records.append(actual)
if len(original_records)!=17 or auth['literal_original_status']!='claimed_solved' or auth['original_effort']!='2/5':
    raise RuntimeError('Original intake identity failure')
v2=ROOT/'repaired_diagnostics_v2/COUNTEREXAMPLE.md'
if pin(v2)['sha256']!='0e2e4e1484193c304cb2394142e24460c89a50f6ab3bb58ad838624cabb9035f':
    raise RuntimeError('Final diagnostic changed')
source_v2=ROOT/'primary_source_scope_adversary_20261006/v2_framing_readback_20261006'
v2result=json.loads((source_v2/'RESULT.json').read_text())
if v2result['verdict']!='PASS_PINNED_V2_FRAMING' or v2result['mandatory_corrections'] or v2result['priority_clearance']:
    raise RuntimeError('Source framing gate failed or overstates priority')
for key in ['review_pin','actual_checks_pin']:
    item=v2result[key]
    if any(pin(source_v2/item['path'])[k]!=item[k] for k in ['bytes','sha256']):
        raise RuntimeError('V2 source review body changed')
replay=json.loads((ROOT/'ROOT_INDEPENDENT_CONTROLS_REPRODUCTION_20261006.json').read_text())
if [r['checks'] for r in replay['families']]!=[4082,515,11762] or not all(r['all_checks_passed'] for r in replay['families']):
    raise RuntimeError('Root replay incomplete')
rejection=json.loads((ROOT/'repaired_diagnostics_v1/REJECTED_AFTER_HIGH_RESOLUTION_SOURCE_CHECK.json').read_text())
if rejection['promotion_authorized_for_v1']:
    raise RuntimeError('False v1 was not rejected')

utc=datetime.datetime.now(datetime.timezone.utc).isoformat()
out={
 'schema':'pr111-root-mathematical-source-admissibility-gate/v1',
 'UTC':utc,'actual_root_PID':os.getpid(),'PR':111,'problem_id':4900006,
 'original_head':auth['original_head'],'original_status':'claimed_solved','original_effort':'2/5',
 'verdict':'PASS for the explicitly unrestricted target; priority gate may begin',
 'all_mathematical_findings_resolved':True,'mandatory_findings_remaining':[],
 'original17_full_body_records':original_records,'authenticated_families':family_records,
 'corrected_v2':pin(v2),'source_v2_result':pin(source_v2/'RESULT.json'),
 'source_v2_review':pin(source_v2/'REVIEW.md'),'source_v2_controls':pin(source_v2/'CHECKS.json'),
 'root_replay':pin(ROOT/'ROOT_INDEPENDENT_CONTROLS_REPRODUCTION_20261006.json'),
 'root_reasoning':pin(ROOT/'ROOT_MATHEMATICAL_REASONING_20261006.md'),
 'rejected_false_v1':pin(ROOT/'repaired_diagnostics_v1/REJECTED_AFTER_HIGH_RESOLUTION_SOURCE_CHECK.json'),
 'exact_asymptotic_maximum':'203/50','maximum_locus':'aperiodic radius-one product torus',
 'finite_time_claim':'inf_t>0 sup_A dKY(t,x)>=203/50; no equality asserted',
 'excluded_claims':['historical original-thesis quantifiers','1994 origin provenance','Lorenz-specific or chaotic/strange/typical/generic/transitive variants','finite-time infimum equality','novel priority','human peer review','whole-publication package clearance'],
 'new_central_proof_search_turns':0,'native_assessment_performed':False,
 'priority_cleared':False,'publication_or_merge_authorized_by_this_gate':False,
 'mathematical_phase_completion_percent':100,'priority_phase_completion_percent':0,
 'overall_PR_workflow_best_guess_percent':30,'program_completed_count':18,'dated_program_denominator':99,
}
destination=ROOT/'ROOT_MATHEMATICAL_GATE_20261006.json'
if destination.exists():
    raise RuntimeError('Gate already exists')
destination.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
with (ROOT/'RESEARCH_LOG.md').open('a') as handle:
    handle.write('\n'+utc+': Mathematical/source gate PASS after three independent analytic families, full body authentication, root exact replays4082/515/11762, and source v2 readback. Original17 preserved; false v1 source reading withdrawn and explicitly rejected. Exact unrestricted maximum203/50 is only aperiodic; historical Lorenz/chaotic/typical/thesis variants excluded. Math100%, priority0%, PR workflow30%; program18/99=18.18%, goal active. No new central proof turn; no PR/service write. Bounded priority may begin.\n')
print(json.dumps({'gate':pin(destination),'authenticated_family_members':sum(len(x['members']) for x in family_records),'originals':len(original_records),'math_percent':100,'priority_percent':0,'actual_root_PID':os.getpid()}))
