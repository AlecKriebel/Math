#!/usr/bin/env python3
"""Independent actual-triple controls; no closure or production helper import."""
from pathlib import Path
from datetime import datetime, timezone
import copy
import hashlib
import json
import math
import os
import stat
import sys

assert __debug__ and sys.flags.optimize == 0
F = Path(__file__).resolve().parent
R = Path('/Users/alec/Documents/Math')
assert F == R / 'draft_pr_publication_program_20260930/audits/pr46_30004438/acceptance_source_adversary_family'
started = datetime.now(timezone.utc).isoformat()
count = 0
reads = set()
read_bytes = 0
rejected = []


def require(value, why):
    global count
    count += 1
    assert value, why


def load(raw):
    def unique(items):
        result = {}
        for key, item in items:
            require(key not in result, 'duplicate JSON key')
            result[key] = item
        return result
    def invalid(value):
        raise ValueError(value)
    def finite(value):
        result = float(value)
        require(math.isfinite(result), 'finite JSON float')
        return result
    return json.loads(raw, object_pairs_hook=unique, parse_constant=invalid, parse_float=finite)


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def body(path):
    global read_bytes
    require(path.is_absolute() and path.resolve() == path, 'literal absolute path')
    require(not path.is_symlink() and stat.S_ISREG(path.lstat().st_mode), 'regular file')
    require(all(not parent.is_symlink() for parent in path.parents), 'no symlink ancestor')
    raw = path.read_bytes()
    reads.add(str(path))
    read_bytes += len(raw)
    return raw


def own(ref):
    path = Path(ref['path'])
    if not path.is_absolute():
        require('..' not in path.parts, 'no relative escape')
        path = F / path
    require(F in path.parents, 'own path')
    raw = body(path)
    require(type(ref['bytes']) is int and len(raw) == ref['bytes'], 'own exact bytes')
    require(digest(raw) == ref['sha256'], 'own exact full SHA')
    return raw


def live(ref):
    raw = body(Path(ref['path']))
    require(type(ref['bytes']) is int and len(raw) == ref['bytes'], 'live exact bytes')
    require(digest(raw) == ref['sha256'], 'live exact full SHA')
    require(type(ref['full_mode']) is int and stat.S_IMODE(Path(ref['path']).stat().st_mode) == ref['full_mode'], 'live full mode')
    return raw


def utc(text):
    require(type(text) is str, 'clock string type')
    result = datetime.fromisoformat(text)
    require(result.tzinfo is not None and result.utcoffset().total_seconds() == 0, 'aware UTC clock')
    require(result <= datetime.now(timezone.utc), 'no future evidence clock')
    return result


c_raw = body(F / 'CHILD_OBSERVATION_CLOCK_QUALIFICATION_V3.json')
c = load(c_raw)
q_raw = own(c['dated_native_qualification'])
q = load(q_raw)
actual_cap = load(own(c['original_primary_capture']))
actual_pre = load(own(c['original_primary_prelaunch']))
actual_child = load(own(c['original_primary_child_result']))
require(digest(q_raw) == '31dd1f9857c4dcb04138d30d8fb480a97d860bcd5f74a4a32eadb554d032ee94', 'entire unmodified dated qualifier')


def triple(cap, pre, child, observation):
    require(cap['schema'] == 'pr46-source-adversary-real-command-capture/v1', 'real actual capture class')
    require(pre['schema'] == 'pr46-source-adversary-real-prelaunch/v1', 'real original prelaunch class')
    require(type(child['actual_pid']) is int and child['actual_pid'] == 55086, 'actual child result PID')
    require(type(cap['child_pid']) is int and cap['child_pid'] == child['actual_pid'], 'capture child PID binding')
    require(type(cap['operator_pid']) is int and cap['operator_pid'] == 55085, 'actual operator distinct PID')
    require(type(pre['operator_pid']) is int and pre['operator_pid'] == cap['operator_pid'], 'prelaunch operator binding')
    require(type(cap['exit_code']) is int and cap['exit_code'] == 0 and cap['status'] == 'PASS_EXPECTED_EXIT', 'actual completed success')
    require(type(cap['expected_exit']) is int and cap['expected_exit'] == 0, 'typed expected exit')
    require(cap['argv'] == pre['argv'] and cap['cwd'] == pre['cwd'] == str(R), 'literal actual command and cwd')
    require(observation['observation_started_utc'] == '2026-10-03T06:33:25.440121+00:00', 'fixed actual observed child start')
    require(observation['observation_finished_utc'] == '2026-10-03T06:33:30.393867+00:00', 'fixed actual observed child finish')
    require(child['started_utc'] == observation['observation_started_utc'], 'exact child-result start equals unmodified qualifier')
    require(child['finished_utc'] == observation['observation_finished_utc'], 'exact child-result finish equals unmodified qualifier')
    values = [pre['created_utc'], cap['started_utc'], child['started_utc'], child['finished_utc'], cap['finished_utc']]
    times = [utc(value) for value in values]
    require(times == sorted(times), 'prelaunch/operator/child/child/operator containment')
    return values


real_chain = triple(actual_cap, actual_pre, actual_child, q)
old_equality = actual_cap['started_utc'] == q['observation_started_utc'] and actual_cap['finished_utc'] == q['observation_finished_utc']
require(old_equality is False, 'real completed triple falsifies V2 operator-child equality assumption')
for key in ['operator','prelaunch','child_source','stdout','stderr']:
    own(actual_cap[key])
require(own(actual_cap['prelaunch']) == own(c['original_primary_prelaunch']), 'exact completed prelaunch full bytes')
for ref in c['new_fixed_external_receipts']:
    live(ref)
root = Path(c['new_fixed_external_receipts'][0]['path']).parent
failed = load(body(root / 'CAPTURE.json'))
require({p.name for p in root.iterdir()} == {'CAPTURE.json','prelaunch_operator.py','stdout.bin','stderr.bin'}, 'literal ROOT failed four-member class')
require(failed['schema'] == 'root-explicit-command-capture/v1', 'real failed ROOT class')
require(type(failed['pid']) is int and failed['pid'] == 2427, 'real V2 failed child')
require(type(failed['exit_code']) is int and failed['exit_code'] == 1 and failed['status'] == 'FAIL', 'V2 failure retained')
require(failed['actual_execution'] is True and failed['completed'] is True and failed['operator_unchanged'] is True, 'actual failure complete')
require(failed['argv'] == ['/usr/bin/python3','-B',str(F/'close_source_adversary_v2.py')], 'literal failed argv')
require(digest(body(root/'prelaunch_operator.py')) == failed['operator_sha256'], 'actual failure operator full source')
for key in ['stdout','stderr']:
    raw = body(root/(key+'.bin'))
    require(type(failed[key]['bytes']) is int and len(raw) == failed[key]['bytes'] and digest(raw) == failed[key]['sha256'], 'actual failed full stream '+key)
require(body(root/'stdout.bin') == b'' and b"primary_cap['started_utc'] == q['observation_started_utc']" in body(root/'stderr.bin'), 'retained exact V2 clock assertion failure')
require(utc(failed['started_utc']) <= utc(failed['finished_utc']), 'failed root UTC clock interval')
pins = load(own(c['old_V2_payload_preservation']))
require(type(pins['original_payload_count']) is int and len(pins['files']) == pins['original_payload_count'] == 80, 'old V2 payload count')
require(digest(('\n'.join(ref['path'] for ref in pins['files'])+'\n').encode()) == '555d45acdd92a8fd001bcf2dc2a2cbd00f0553111df175bad5a118968340b006', 'old complete V2 paths')
for ref in pins['files']:
    own(ref)
old = load(body(F/'OWN_INPUT_READ_BINDINGS.json'))
live_rows = [ref for ref in old['external_bindings'] if ref['path'] != str(R/'unsolved_math_prioritization/QUEUE.md')]
require(len(live_rows) == 2610 and len({row['path'] for row in live_rows}) == 2610, 'exact remaining original live bindings')
for ref in live_rows:
    live(ref)
for ref in q['new_fixed_external_receipts']:
    live(ref)
require(not (F/'SELF_MANIFEST.json').exists(), 'no own closure launched')


def mutant(label, which, key, value, observation_change=None):
    cap,pre,child,observation = map(copy.deepcopy,[actual_cap,actual_pre,actual_child,q])
    target = {'cap':cap,'pre':pre,'child':child,'q':observation}[which]
    target[key] = value
    if observation_change is not None:
        observation[observation_change[0]] = observation_change[1]
    try:
        triple(cap,pre,child,observation)
    except (AssertionError,ValueError):
        rejected.append(label)
        return
    raise AssertionError('clock mutant accepted: '+label)


mutant('child start substituted with operator start','child','started_utc',actual_cap['started_utc'])
mutant('child finish substituted with operator finish','child','finished_utc',actual_cap['finished_utc'])
mutant('qualifier start substituted with operator start','q','observation_started_utc',actual_cap['started_utc'])
mutant('qualifier finish substituted with operator finish','q','observation_finished_utc',actual_cap['finished_utc'])
mutant('child and qualifier both replaced by another contained time','child','started_utc','2026-10-03T06:33:25.440122+00:00',('observation_started_utc','2026-10-03T06:33:25.440122+00:00'))
mutant('operator begins after actual child','cap','started_utc','2026-10-03T06:33:25.440122+00:00')
mutant('operator finishes before actual child','cap','finished_utc','2026-10-03T06:33:30.393866+00:00')
mutant('prelaunch follows operator start','pre','created_utc','2026-10-03T06:33:25.390726+00:00')
mutant('naive prelaunch time','pre','created_utc','2026-10-03T06:33:25.390324')
mutant('naive operator start','cap','started_utc','2026-10-03T06:33:25.390725')
mutant('naive child finish','child','finished_utc','2026-10-03T06:33:30.393867')
mutant('non-UTC child offset','child','started_utc','2026-10-02T23:33:25.440121-07:00')
mutant('future operator finish','cap','finished_utc','2999-10-03T06:33:30.420706+00:00')
mutant('child interval reversed','child','finished_utc','2026-10-03T06:33:25.440120+00:00')
mutant('boolean child PID','child','actual_pid',True)
mutant('wrong capture child PID','cap','child_pid',55087)
mutant('boolean operator PID','cap','operator_pid',True)
mutant('boolean success exit','cap','exit_code',False)
mutant('wrong prelaunch operator PID','pre','operator_pid',55088)
mutant('failed primary mislabeled completed evidence','cap','status','FAIL_UNEXPECTED_EXIT')
require(len(rejected) == len(set(rejected)) == 20, 'all clock mutants independently rejected')
result = {'schema':'pr46-source-adversary-actual-child-clock-controls/v3','status':'PASS_REAL_CHILD_OBSERVATION_CLOCK_CONTROLS',
          'actual_pid':os.getpid(),'started_utc':started,'finished_utc':datetime.now(timezone.utc).isoformat(),
          'assertions':count,'rejected_clock_mutants':rejected,'real_primary_actual_child':55086,'real_primary_actual_operator':55085,
          'real_aware_UTC_clock_chain':real_chain,'old_V2_operator_child_equality':old_equality,
          'old_V2_payload_bodies_preserved':80,'original_live_bindings_checked':2610,'prior_fixed_receipts_checked':6,'new_fixed_receipts_checked':4,
          'unique_full_body_read_paths':len(reads),'full_read_bytes_including_repeats':read_bytes,
          'clock_qualification_body_sha256':digest(c_raw),'dated_native_qualification_body_sha256':digest(q_raw),
          'production_imported_compiled_executed':False,'own_closure_launched':False,'fresh_native_authority':False,
          'future_acceptance_approved':False,'source_verdict_unchanged':'REJECT_MANDATORY_SOURCE_CORRECTION','mandatory_finding_unchanged':'S1',
          'new_substantive_attempts':0,'audit_turns':0}
with (F/'CLOSURE_CLOCK_CONTROL_RESULT_V3.json').open('x') as handle:
    handle.write(json.dumps(result,indent=2)+'\n')
print(json.dumps({key:result[key] for key in ['status','actual_pid','assertions','old_V2_payload_bodies_preserved','original_live_bindings_checked','real_aware_UTC_clock_chain','old_V2_operator_child_equality']},indent=2))
