"""ROOT final adjudication after personal source/report/operator reading."""
from pathlib import Path
import hashlib, json, datetime as dt, sys

assert __debug__ and sys.flags.ignore_environment and sys.flags.dont_write_bytecode
A=Path(__file__).resolve().parent;P=A.parents[1];R=P.parent
F=A/'prior_disposition_fresh_adversary_20261004'
PREP=A/'attributed_integration_preparation_20261004'
V2=A/'attributed_prior_result_preparation_v2_20261004'
OUT=A/'ROOT_fresh_disposition_custody_readback_20261004'
OUT.mkdir(exist_ok=False)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_bytes())
def check(p,row):
    assert p.is_file() and not p.is_symlink(),str(p)
    assert p.stat().st_size==row['bytes'] and sha(p)==row['sha256'],str(p)
def pin(p):return {'path':str(p.relative_to(R)),'bytes':p.stat().st_size,'sha256':sha(p)}
freshmanifest=read(F/'FINAL_MANIFEST.json')
assert sha(F/'FINAL_MANIFEST.json')=='17b44950495deda4ce0eebe49888afe78c830d388ed2fbe498210d37c0e01ba0'
for x in freshmanifest['files']:check(F/x['path'],x)
for packet in freshmanifest['audited_packets']:
    for x in packet['files']:check(Path(packet['directory'])/x['path'],x)
private=read(F/'FINAL_PRIVATE_SOURCE_PINS.json')['files']
for x in private:check(Path(x['path']),x)
receiptrows=[];narrow=[]
for path in sorted((F/'receipts').glob('*.json')):
    d=read(path)
    if 'streams' not in d or 'argv' not in d:
        narrow.append({'path':str(path.relative_to(R)),'kind':'narrow input metadata, not full process receipt'})
        continue
    assert dt.datetime.fromisoformat(d['utc_start'])<=dt.datetime.fromisoformat(d['utc_end'])
    for x in d['streams'].values():check(F/x['path'],x)
    pid=d.get('actual_child_pid')
    if pid is not None:assert type(pid) is int and pid>0
    receiptrows.append({'path':str(path.relative_to(R)),'exit':d['exit_code'],'observed_child_pid':pid,
                        'metadata_limit':None if pid else 'Original receipt omitted PID; no invented value'})
assert sha(F/'FIRST_CONCLUSION.md')==freshmanifest['first_conclusion_sha256']=='f53d0551b2286ff7c2e297ec9d1c56d247ed70c38f17d96a6bef49b017e8b406'
prepm=read(PREP/'PREPARATION_MANIFEST.json')
assert sha(PREP/'PREPARATION_MANIFEST.json')=='c5cbe3eee7910fe02a7400c649ad220ae1b57cdf60c0f04f74d6b0fdfaeb699b'
for x in prepm['files']:check(R/x['path'],x)
prepcommands=[]
for name in ['PREPARATION_ACTUAL_COMMANDS.json','FINAL_PREPARATION_ACTUAL_COMMANDS.json']:
    for d in read(PREP/name):
        assert d['actual_child_pid']>0 and d['cwd']
        assert dt.datetime.fromisoformat(d['started_utc'])<=dt.datetime.fromisoformat(d['finished_utc'])
        for k in ['stdout','stderr']:check(Path(d[k]['path']),d[k])
        prepcommands.append({'pid':d['actual_child_pid'],'exit':d['exit_code']})
plan=read(PREP/'OPERATIONAL_BYTE_PLAN_V2.json')
assert plan['scientific_changes'] is False and plan['version']==2
for row in plan['files']:
    source=R/row['source_path'];check(source,{'bytes':row['source_bytes'],'sha256':row['source_sha256']})
    text=source.read_text()
    for edit in row['literal_edits']:
        assert edit['required_occurrences']==1 and text.count(edit['old'])==1
        text=text.replace(edit['old'],edit['new'])
    final=R/row['planned_path'];check(final,{'bytes':row['planned_bytes'],'sha256':row['planned_sha256']})
    assert final.read_bytes()==text.encode()
verdict=read(F/'VERDICT.json')
assert verdict['verdict']=='PASS_ATTRIBUTED_PRIOR_RESULT_NO_MATERIAL_REPAIR'
assert verdict['audit_completion_percent']==100 and verdict['required_material_repairs']==[]
assert verdict['both_v1_and_final_v2_packets_read_completely'] is True and verdict['v2_prior_even_ingredient_corollary_verified'] is True
assert read(A/'ROOT_completed_priority_family_readback_20261004/READBACK.json')['verdict']=='PASS'
custody={'UTC':dt.datetime.now(dt.timezone.utc).isoformat(),'status':'PASS',
        'fresh_manifest':pin(F/'FINAL_MANIFEST.json'),'fresh_artifact_count':len(freshmanifest['files']),
        'private_source_pin_count':len(private),'fresh_receipts':receiptrows,'narrow_metadata_only':narrow,
        'preparation_manifest':pin(PREP/'PREPARATION_MANIFEST.json'),'preparation_artifact_count':len(prepm['files']),
        'preparation_actual_commands':prepcommands,'stage_only_final_byte_transforms_verified':True,
        'no_unknown_child_environment_certified':True}
(OUT/'READBACK.json').write_text(json.dumps(custody,indent=2)+'\n')
now=dt.datetime.now(dt.timezone.utc).isoformat()
goal=Path('/Users/alec/.codex/attachments/4df73d3d-641f-4907-b9ad-c47c468f2589/goal-objective.md')
assert sha(goal)=='1e29852cafce156dbc3b745f9d1b7bf973b6d07e4a3c924b901ad27754128d04'
gate={'PR':66,'expected_original_head':'78f4a7fadac0fd24e147a617956cb409eb6a579e',
      'UTC':now,'minimum_writer_ack_utc':now,'audited_outcome':'already_solved',
      'accepted_as':'attributed_partial_prior_result','mathematics_percent':100,'bounded_priority_percent':100,
      'original_proof_turns':'1/5','new_original_proof_turns':0,'goal_objective_sha256':sha(goal),
      'scope_interpretation':'Only initial literal claimed_solved intake; original human clause allows a verified eligible submission whose audited outcome is already_solved to merge as attributed partial progress without paper. Initially nonclaim PRs skipped entirely.',
      'exact_even_formula_earlier_explicitly_printed_meaning':'Not located or certified; no absence claim.',
      'tournament_mechanism_novelty':'unestablished','earliest_priority_certified':False,
      'v2_creation_authority':'MANIFEST.created_utc; DISPOSITION.utc preserves initial v1 proposal timestamp',
      'source_read_scope':'FS author title and printed4–8 text/5–8 pixels; Stoimenow2003 printed245 Lemma3.2 pixels; source-first independent primary confirmation, no whole-paper reading invented',
      'new_DOI':None,'prospective_packet_directory':str(V2.relative_to(R)),
      'prospective_manifest':pin(V2/'MANIFEST.json'),
      'bound_prospective_inputs':[pin(V2/x['name']) for x in read(V2/'MANIFEST.json')['files']],
      'operational_byte_plan':pin(PREP/'OPERATIONAL_BYTE_PLAN_V2.json')}
for key in ['ROOT_authorizes_guarded_attributed_prior_result_acceptance','fresh_final_adversary_clean',
            'ROOT_personally_read_all_required_reports','candidate_mathematics_verified',
            'prior_resolution_of_exact_original_problem_verified','ROOT_reviewed_exact_operational_byte_plan',
            'initial_literal_claimed_solved_gate_only','initially_nonclaim_targets_untouched','even_prior_ingredient_verified']:
    gate[key]=True
for key in ['new_solution_priority_clearance','publication_authorized','new_paper','tracker_append',
            'PR50_exception_extended','exact2000printedbody_read','stronger_prior_p8_extremality_certified',
            'exact_even_formula_earlier_explicitly_printed']:
    gate[key]=False
current=['ROOT_FULL_MATHEMATICAL_GATE_20261004.json','ROOT_PRIMARY_ARROW_BRIDGE_READING_20261004.json',
         'ROOT_original_custody_readback_20261004/READBACK.json','ROOT_completed_math_family_readback_20261004/READBACK.json',
         'ROOT_completed_priority_family_readback_20261004/READBACK.json',
         'ROOT_fresh_disposition_custody_readback_20261004/READBACK.json',
         'ROOT_priority_audit_20261004/ROOT_PRIOR_BINOMIAL_SPECIALIZATION_20261004.json',
         'ROOT_priority_audit_20261004/ROOT_EVEN_PRIOR_INGREDIENT_READING_20261004.json',
         'exact_target_priority_20261004/PRIORITY_REPORT.md','exact_target_priority_20261004/BIBLIOGRAPHY.json',
         'exact_target_priority_20261004/MANIFEST.json','mechanism_priority_20261004/REPORT.md','mechanism_priority_20261004/MANIFEST.json',
         'prior_disposition_fresh_adversary_20261004/FINAL_REPORT.md','prior_disposition_fresh_adversary_20261004/VERDICT.json',
         'prior_disposition_fresh_adversary_20261004/FINAL_MANIFEST.json','prior_disposition_fresh_adversary_20261004/POST_FIRST_EVEN_PRIOR_COROLLARY.md',
         'prior_disposition_fresh_adversary_20261004/OPINION_EXPOSURE_RECORD.json',
         'arrow_formula_scope_adversary_20261004/FORMULA_SCOPE_REPORT.md',
         'tournament_domination_adversary_20261004/GRAPH_AUDIT_REPORT.md',
         'jones_algebraic_calibration_adversary_20261004/FINAL_REPORT.md',
         'fresh_graph_proof_adversary_20261004/ADVERSARIAL_REPORT.md']
gate['bound_current_evidence']=[pin(A/x) for x in current]
S=A/'original_source_authentication_20261004'
original=[S/'ORIGINAL_AUTHENTICATION.json',S/'ORIGINAL_BLOB_MANIFEST.json',S/'original/unsolved_math_prioritization/QUEUE.md']
original += [S/'original/unsolved_math_prioritization/attempts/10400033'/x for x in ['CANDIDATE.md','source_record.json','status.json','turns.jsonl']]
gate['bound_original_evidence']=[pin(x) for x in original]
operational=[PREP/x for x in ['ROOT_integrate_attributed_prior_result_20261004.py','ROOT_readback_attributed_acceptance_20261004.py',
                            'OPERATIONAL_BYTE_PLAN_V2.json','GATE_SCHEMA.md','README.md','PREPARATION_REPORT.json','PREPARATION_MANIFEST.json']]
operational += [R/x['planned_path'] for x in plan['files']]
gate['bound_operational_preparation']=[pin(x) for x in operational]
dest=A/'ROOT_FINAL_PRIOR_DISPOSITION_20261004.json'
with dest.open('x') as f:f.write(json.dumps(gate,indent=2)+'\n')
print(json.dumps({'status':'PASS','final_gate':str(dest),'UTC':now,'gate_sha256':sha(dest),
                  'current_science_and_priority_percent':100,'current_workflow_percent':75,
                  'fresh_receipts_verified':len(receiptrows),'preparation_receipts_verified':len(prepcommands),
                  'fresh_writer_ack_required':True,'native_acceptance':False,'new_paper':False},indent=2))
