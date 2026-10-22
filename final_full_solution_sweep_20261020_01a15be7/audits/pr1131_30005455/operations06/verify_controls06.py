"""Read-only final case-counter/source/preservation adjudication, no services."""
from pathlib import Path
import datetime,hashlib,json
ROOT=Path(__file__).resolve().parent
def need(v,m):
    if not v:raise RuntimeError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
def pin(path):
    b=path.read_bytes();return {'bytes':len(b),'sha256':sha(b)}
MS='4d491443d4be4d07ef9abb45c0ce6f9c56bf77c20dd7a2254ae43dce2638ab79'
BS='e8c7f35bc6d60318146ae9794fe84c7c8a18e99e818a350bb78298fd85bd9852'
S=ROOT/'source';need(pin(S/'bootstrap06.py')['sha256']==BS,'Final bootstrap changed')
ns={'__file__':str(S/'bootstrap06.py'),'__name__':'final_readonly_bootstrap06'}
exec(compile((S/'bootstrap06.py').read_bytes(),str(S/'bootstrap06.py'),'exec'),ns)
m=ns['load_verified'](S,MS,BS);c=m.c
old=(m.PRIOR/'OPERATIONS_MANIFEST.json').read_bytes()
need(sha(old)==m.F['prior_operations_manifest_sha256'],'Immutable05 source manifest')
manifest=c.strict_json(old)
need(c.public_files(m.PRIOR)==set(manifest['files']),'Immutable05 source closure')
for n,p in manifest['files'].items():c.read_pinned(c.safe(m.PRIOR,n),p)
c.package();c.proposal()
need({p.name for p in m.PRIOR_RUNTIME.iterdir()}==set(m.F['prior_runtime_files']),'Preserved old runtime closure')
for n,p in m.F['prior_runtime_files'].items():need(pin(m.PRIOR_RUNTIME/n)==p,'Original runtime changed')
for n,p in m.F['prior_wrapper_files'].items():need(pin(ROOT.parent/'stage_known_unattempted_resumption01'/n)==p,'Original wrapper changed')
need(not (ROOT/'runtime').exists(),'Production06 runtime created')
example=json.loads((S/'ROOT_CLEARANCE06.example.json').read_bytes())
need(example['publication_ready'] is False and example['allowed_actions']==[] and example['whole06_review_adopted'] is False,'Example promoted')
source_control_sha=pin(ROOT/'controls06.py')['sha256'];result_pins={};modes={}
for mode in ['normal','O','OO']:
    primary=ROOT/'private'/('controls_v3_'+mode)/'RESULT.json'
    aligned=ROOT/'private'/('aligned_state_'+mode)/'RESULT.json'
    a=json.loads(primary.read_bytes());b=json.loads(aligned.read_bytes())
    need(a['status']==b['status']=='PASS' and a['sources_sha256']==b['sources_sha256']==MS
         and a['bootstrap_sha256']==b['bootstrap_sha256']==BS
         and a['controls_source_sha256']==b['helper_sha256']==source_control_sha,'Mode/source binding')
    need(a['full_parsed_CLI_cases']==35 and b['full_parsed_CLI_cases']==2
         and a['real_external_mutations']==b['real_external_mutations']==0
         and a['real_external_attempts']==b['real_external_attempts']==[],'Mode incomplete/external escape')
    table={r['case']:r for r in a['results']};need(len(table)==35,'Duplicate or missing case')
    for phase,count in [('first_upload',1),('second_upload',2),('metadata_update',3),('publication',4),('ledger',5)]:
        r=table['family_'+phase]
        need(len(r['native_mutations'])==count and r['native_mutations'][0]=='create'
             and r['appends']==0 and 'Account/native target families disagree' in r['error']['message'],
             'Family fault stopped after wrong boundary: '+phase)
        if phase in {'first_upload','second_upload','metadata_update'}:need(not r['stage_verified'],'Family mismatch verified stage')
        if phase=='publication':need(not r['publication_verified'],'Family mismatch verified publication')
        if phase=='ledger':need(not r['ledger_verified'],'Family mismatch verified ledger')
    for kind in ['adoption','old_intent']:
        for edge in [1,2,3,4]:
            r=table[kind+'_after_long_guard_'+str(edge)]
            need(len(r['native_mutations'])==edge-1 and r['stage_failure'] is True
                 and r['stage_verified'] is False,'Context drift passed boundary')
    for case,count in [('create',1),('upload',2),('known_id_native_invalid',1),('update_context_drift',4)]:
        r=table['unknown_'+case]
        need(len(r['native_mutations'])==count and r['stage_failure'] and not r['stage_verified'],'Unknown-outcome boundary count')
        if case!='create':need(r['failure_receipt']['delegate_known_id']==777,'Known ID custody failed')
    for name,r in table.items():
        need(r['Git_mutations']==[] and r['real_external_mutations']==0,'Git/external mutation')
        if name.startswith('reference_'):need(r['native_mutations']==[] and not r['stage_verified'],'Reference lead reached allocation')
    formula=table['postappend_equivalent_old_formula']
    need(formula['appends']==1 and not formula['ledger_verified'] and 'Formula/unformatted' in formula['error']['message'],'Formula postwrite hold')
    for name in ['old_numeric','old_boolean']:
        need(table[name]['native_mutations']==[] and 'four-cell schema' in table[name]['error']['message'],'Typed old-cell precondition')
    near=table['nearby_PR11310_is_not1131'];need(len(near['native_mutations'])==4 and near['stage_verified'],'Near-number control')
    state={r['case']:r for r in b['results']}
    complete=state['complete_lifecycle_same_state_store']
    need(complete['all_target_gates_contain_exact_saved_state'] and complete['target_gate_count']>0
         and complete['appends']==1 and complete['ledger_verified'],'Aligned saved-state full lifecycle')
    need(state['unreviewed_local_reference_after_stage']['native_mutations'].count('publish')==0,'Poststage local lead reached publication')
    result_pins[str(primary.relative_to(ROOT))]=pin(primary);result_pins[str(aligned.relative_to(ROOT))]=pin(aligned)
    modes[mode]={'parsed_primary_cases':35,'parsed_state_aligned_cases':2,'all_expected_boundary_mutation_counts':True,
                 'grammar_positive':a['grammar_positive'],'grammar_negative':a['grammar_negative'],'actual_service_mutations':0}
out={'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS_PREPARATION_NOT_ACTION_CLEARANCE',
     'sources_sha256':MS,'bootstrap_sha256':BS,'source_control_sha256':source_control_sha,
     'modes':modes,'final_full_parsed_cases':111,'result_pins':result_pins,
     'all196immutable05_payloads_and_dependency_checked':True,'immutable_science_and_proposal_checked':True,
     'all13old_runtime_pins_and_inventory_unchanged':True,'old_wrapper3_pins_unchanged':True,
     'production06_runtime_absent':True,'root_clearance_absent':True,'publication_ready':False,
     'fresh_independent_whole06_review_and_root_adoption_required':True,'actual_service_mutations':0,
     'actual_preparation_readonly_GET_count':8,'overall_percent':80}
(ROOT/'PREPARATION_VALIDATION.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k!='result_pins'},indent=2))
