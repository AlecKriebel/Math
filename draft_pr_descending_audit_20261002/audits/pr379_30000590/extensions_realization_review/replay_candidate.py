#!/usr/bin/env python3
"""Replay the private frozen copy and retain every complete stdout/stderr."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib,json,subprocess,sys

HERE=Path(__file__).resolve().parent
P=HERE/'private/candidate_snapshot/problems/30000590_group_ring_cohomology'
OUT=HERE/'private/replay_outputs'
OUT.mkdir(exist_ok=True)
rows=[]

def run(name, args, expected=None):
    proc=subprocess.run([sys.executable]+[str(x) for x in args],cwd=HERE,
                        capture_output=True,timeout=120)
    (OUT/(name+'.stdout')).write_bytes(proc.stdout)
    (OUT/(name+'.stderr')).write_bytes(proc.stderr)
    row={'name':name,'exit_code':proc.returncode,'stdout_bytes':len(proc.stdout),
         'stdout_sha256':hashlib.sha256(proc.stdout).hexdigest(),
         'stderr_bytes':len(proc.stderr)}
    if expected is not None:
        row['expected_path']=str(expected.relative_to(P))
        row['byte_exact']=proc.stdout==expected.read_bytes()
        assert row['byte_exact'],name
    assert proc.returncode==0,name
    rows.append(row)
    return proc.stdout

total=0
for i in range(1,6):
    out=run('author_turn_'+str(i),[P/f'check_turn_{i}.py'],P/f'TURN_{i}_CHECKS.json')
    j=json.loads(out);total+=j.get('exact_assertions',j.get('assertions'))
out=run('old_independent',[P/'review/independent_checks.py'],P/'review/INDEPENDENT_CHECKS.json')
old_count=json.loads(out)['exact_assertions']
packet=json.loads(run('verify_packet_without_sources',[P/'verify_packet.py']))
run('verify_review',[P/'review/verify_review.py','--author',P])
run('verify_publication_without_sources',[P/'verify_publication.py'])

# The stored original FINAL_REPLAY predates freezing its final manifest;
# byte-replay of receipts is exact, while verifier counts evolve as stated.
original=json.loads((P/'FINAL_REPLAY.json').read_bytes())
old_author=json.loads((P/'review/AUTHOR_REPLAY.json').read_bytes())
comparisons={}
for name,old in [('FINAL_REPLAY.json',original),('review/AUTHOR_REPLAY.json',old_author)]:
    comparisons[name]={
        'current_source_files_checked':packet['source_files_checked'],
        'stored_source_files_checked':old['source_files_checked'],
        'current_all_verified_file_bindings':packet['all_verified_file_bindings'],
        'stored_all_verified_file_bindings':old['all_verified_file_bindings'],
        'same_author_assertions':packet['author_assertions']==old['author_assertions'],
        'same_historical_bindings':packet['historical_file_bindings']==old['historical_file_bindings'],
        'same_full_replay_array':packet['replays']==old['replays']}
    assert all(comparisons[name][k] for k in ['same_author_assertions','same_historical_bindings','same_full_replay_array'])
receipt={'utc':datetime.now(timezone.utc).isoformat(),'private_copy_only':True,
         'author_assertions':total,'old_independent_assertions':old_count,
         'author_and_old_independent_stdout_byte_exact':True,
         'raw_source_reverification_by_candidate_scripts':False,
         'candidate_script_sources_checked':packet['source_files_checked'],
         'three_sources_freshly_retrieved_by_this_audit':'EMS, Sharifi, Davis IGAP; see source receipt',
         'old_complete_output_comparisons':comparisons,'runs':rows}
assert total==747103 and old_count==23463 and packet['source_files_checked']==0
(HERE/'CANDIDATE_REPLAY_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2))
