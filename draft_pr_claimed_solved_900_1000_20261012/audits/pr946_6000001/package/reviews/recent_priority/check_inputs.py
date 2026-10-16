"""Authenticate this audit's frozen inputs using actual read-only Git objects."""
import pathlib, subprocess, hashlib, json, datetime
ROOT = pathlib.Path(__file__).resolve().parents[5]
BASE = pathlib.Path(__file__).resolve().parent
AUDIT = BASE.parents[1]
HEAD = '7d3adb0e500b0414a49a449e7981d34ade329427'
PROOF = 'unsolved_math_prioritization/attempts/6000001/public/PROOF.md'
def git(*a): return subprocess.check_output(['git', *a], cwd=ROOT)
def digest(b): return {'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}
def main():
    original = git('show', HEAD+':'+PROOF)
    frozen = (AUDIT/'original'/PROOF).read_bytes()
    queue = git('show', HEAD+':unsolved_math_prioritization/QUEUE.md')
    rows = [x for x in queue.decode().splitlines() if '| 6000001 / AMR-059-0001 |' in x]
    assert len(rows) == 1
    fields = [x.strip() for x in rows[0].split('|')]
    report = {
      'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
      'actual_git': True, 'branch': git('branch','--show-current').decode().strip(),
      'working_head_observed': git('rev-parse','HEAD').decode().strip(),
      'frozen_head': HEAD, 'git_object_type':git('cat-file','-t',HEAD).decode().strip(),
      'proof_git_object': digest(original), 'proof_frozen_disk':digest(frozen),
      'git_disk_equal': original==frozen,
      'immutable_queue': digest(queue), 'immutable_queue_row': rows[0],
      'immutable_status':fields[8], 'immutable_declared_budget':fields[9],
      'native_original_events': 'absent/not authenticated',
      'new_proof_attempt_responses':0,
      'identity_gate_read': 'TARGET_IDENTITY_PREFLIGHT.json',
      'source_record_full_read':True,'proof_full_read':True,
      'classical_priority_work_read':False, 'other_shards_or_outside_individuals_contacted':False,
      'mutations': 'only this recent_priority/ directory',
      'inputs':{}
    }
    for n in ('source_record_private.txt','RESEARCH_CHARTER.md','PRIORITY_CHARTER.md','MATHEMATICAL_GATE.json','TARGET_IDENTITY_PREFLIGHT.json'):
        report['inputs'][n] = digest((AUDIT/n).read_bytes())
    assert original == frozen and digest(original)['sha256'] == 'a26c1755bc6f61085db4c01b6579701ff380822f2cc58a3ffbfb4acfa49370a2'
    assert fields[8:10] == ['claimed_solved','4/5']
    assert report['branch'] == 'main'
    (BASE/'INPUT_AUTHENTICATION.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:report[k] for k in ('utc','branch','git_disk_equal','immutable_status','immutable_declared_budget')}))
if __name__ == '__main__': main()
