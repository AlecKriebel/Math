"""Check existing immutable actual streams; no fabricated executions or verdicts."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json
A=Path(__file__).resolve().parent
S=A/'snapshot/unsolved_math_prioritization/attempts/20000450'
sha=lambda b:hashlib.sha256(b).hexdigest()
rows=[]
for label,D,program,expected in [
    ('original_author',A/'root_replays_private/author001',S/'verify_turn1.py',S/'TURN_1_CHECKS.json'),
    ('inherited_reviewer',A/'root_runs_private/inherited_verifier001',S/'review/independent_checks.py',S/'review/independent_output.json')]:
    j=json.loads((D/'execution.json').read_bytes())
    assert j['exit_code']==0
    stdout=(D/'stdout.bin').read_bytes();stderr=(D/'stderr.bin').read_bytes()
    assert not stderr
    for k,b in [('stdout',stdout),('stderr',stderr)]:
        assert sha(b)==j[k+'_sha256'] and len(b)==j[k+'_bytes']
    assert stdout==expected.read_bytes()
    rows.append({'label':label,'program_path':str(program.relative_to(A)),
        'program_bytes':program.stat().st_size,'program_sha256':sha(program.read_bytes()),
        'actual_execution':j,'actual_stdout':json.loads(stdout),
        'matches_original_frozen_expected_stream_byte_for_byte':True,
        'root_full_code_and_complete_actual_stdout_stderr_read':True})
j={'utc':datetime.now(timezone.utc).isoformat(),
    'status':'PASS_NATIVE_FROZEN_ORIGINAL_VERIFIER_REPLAYS',
    'candidate_head':'96395a4f506af6a6045e3cd59afcba2db6b7e2e7',
    'actual_replays':rows,
    'independent_geometry_closure_sha256':sha((A/'ROOT_GEOMETRY_CLOSURE.json').read_bytes()),
    'limits':'Counts certify reproducible successful checks only. They do not alone establish proofs, priority, full arithmetic, full preprint review or publication readiness.',
    'mathematical_acceptance':False,'publication_ready':False,'original_author_turn_count':'1/5'}
(A/'ROOT_NATIVE_REPLAY_SUMMARY.json').write_text(json.dumps(j,indent=2)+'\n')
print(json.dumps({'utc':j['utc'],'status':j['status'],'original_author_check_count':rows[0]['actual_stdout']['exact_assertions'],'whole_candidate_accepted':False},indent=2))
