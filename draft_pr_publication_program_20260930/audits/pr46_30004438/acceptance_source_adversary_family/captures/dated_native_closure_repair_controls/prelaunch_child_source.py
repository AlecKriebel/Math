#!/usr/bin/env python3
"""Independent private controls of the one-path historical closure repair."""
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
assertions = 0
rejected = []
read_bytes = 0
reads = set()


def must(value, label):
    global assertions
    assertions += 1
    assert value, label


def typed(a, b):
    if type(a) is not type(b):
        return False
    if type(a) is dict:
        return a.keys() == b.keys() and all(typed(a[k], b[k]) for k in a)
    if type(a) is list:
        return len(a) == len(b) and all(typed(x, y) for x, y in zip(a, b))
    return a == b


def decode(raw):
    def unique(items):
        result = {}
        for key, value in items:
            must(key not in result, 'strict JSON duplicate key')
            result[key] = value
        return result
    def bad(value):
        raise ValueError('nonfinite JSON ' + value)
    def finite(value):
        number = float(value)
        must(math.isfinite(number), 'finite JSON float')
        return number
    return json.loads(raw, object_pairs_hook=unique, parse_constant=bad, parse_float=finite)


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def body(path):
    global read_bytes
    must(path.is_absolute() and path.resolve() == path, 'literal normalized absolute path')
    must(not path.is_symlink() and stat.S_ISREG(path.lstat().st_mode), 'regular body')
    must(all(not p.is_symlink() for p in path.parents), 'no symlink ancestor')
    raw = path.read_bytes()
    reads.add(str(path))
    read_bytes += len(raw)
    return raw


def own(ref):
    path = Path(ref['path'])
    if not path.is_absolute():
        must('..' not in path.parts, 'no own relative escape')
        path = F / path
    must(F in path.parents, 'own body scope')
    raw = body(path)
    must(type(ref['bytes']) is int and len(raw) == ref['bytes'], 'own full bytes')
    must(digest(raw) == ref['sha256'], 'own full SHA')
    return raw


def live(ref):
    raw = body(Path(ref['path']))
    must(type(ref['bytes']) is int and len(raw) == ref['bytes'], 'external full bytes')
    must(digest(raw) == ref['sha256'], 'external full SHA')
    must(type(ref['full_mode']) is int and stat.S_IMODE(Path(ref['path']).stat().st_mode) == ref['full_mode'], 'external full mode')
    return {k: ref[k] for k in ['path', 'bytes', 'sha256', 'full_mode']}


def time(value):
    stamp = datetime.fromisoformat(value)
    must(stamp.tzinfo is not None and stamp.utcoffset().total_seconds() == 0, 'aware UTC')
    must(stamp <= datetime.now(timezone.utc), 'no future evidence clock')
    return stamp


q_raw = body(F / 'DATED_NATIVE_CLOSURE_QUALIFICATION_V2.json')
q = decode(q_raw)
old_raw = body(F / 'OWN_INPUT_READ_BINDINGS.json')
old = decode(old_raw)
original = decode(body(F / 'PRIVATE_CONTROL_RESULT.json'))
row = next(r for r in old['external_bindings'] if r['path'] == str(R / 'unsolved_math_prioritization/QUEUE.md'))
before = next(r for r in original['native13_before'] if r['path'] == 'unsolved_math_prioritization/QUEUE.md')
after = next(r for r in original['native13_after'] if r['path'] == 'unsolved_math_prioritization/QUEUE.md')
git_body = own(q['captured_historical_body'])
caps = [decode(own(ref)) for ref in q['recovery_captures']]
tree_body = own(caps[1]['stdout'])
commit_body = own(caps[2]['stdout'])
extra = [live(ref) for ref in q['new_fixed_external_receipts']]
root_cap = decode(body(Path(extra[0]['path'])))
diagnosis = decode(body(Path(extra[4]['path'])))


def spec_check(spec, observed, pre, post, recovered, tree, commit, failed, diag):
    must(spec['schema'] == 'pr46-source-adversary-dated-native-closure-qualification/v2', 'exact qualification schema')
    for key, value in [('original_external_binding_count', 2611), ('original_live_binding_count', 2610),
                       ('dated_native_qualification_count', 1), ('observation_primary_actual_child', 55086),
                       ('actual_failed_ROOT_closure_child', 84831), ('actual_failed_ROOT_closure_exit', 1)]:
        must(type(spec[key]) is int and spec[key] == value, 'exact typed count ' + key)
    for key in ['production_imported_compiled_executed', 'fresh_native_authority', 'future_acceptance_approved', 'own_closure_launched']:
        must(spec[key] is False, 'no future authority ' + key)
    must(spec['all_other_original_bindings_remain_exact_live_body_and_full_mode'] is True, 'retain other live bindings')
    must(spec['source_verdict_unchanged'] == 'REJECT_MANDATORY_SOURCE_CORRECTION' and spec['mandatory_finding_unchanged'] == 'S1', 'adverse finding unchanged')
    must(typed(spec['original_native_observation'], observed), 'entire typed observed native row')
    normalized = {k: observed[k] for k in ['path', 'bytes', 'sha256', 'full_mode']}
    expected = {'path':str(R / 'unsolved_math_prioritization/QUEUE.md'), 'bytes':382073,
                'sha256':'a1210bbc36ebd6cd4ced6480edb0fe5e01d28bac59ebd2cf4910312853e396be', 'full_mode':0o644}
    must(typed(normalized, expected), 'exact historical typed preimage')
    must(spec['historical_commit'] == 'e491808c3544ff44e8526d9b24857b5c9ca64208', 'recorded actual main')
    must(spec['historical_git_path'] == 'unsolved_math_prioritization/QUEUE.md', 'only exact native path')
    must(spec['historical_git_mode'] == '100644', 'Git regular mode not chmod observation')
    must(spec['historical_blob_sha1'] == 'd60e9b1df63bebb7b49af7bbb6c6ed64c83681d0', 'exact historical blob')
    relative = dict(expected, path=spec['historical_git_path'])
    must(typed(pre, relative) and typed(post, relative), 'complete typed before and after observations')
    must(len(recovered) == expected['bytes'] and digest(recovered) == expected['sha256'], 'full recovered SHA256 body')
    must(hashlib.sha1(b'blob '+str(len(recovered)).encode()+b'\0'+recovered).hexdigest() == spec['historical_blob_sha1'], 'Git object digest')
    must(tree == ('100644 blob '+spec['historical_blob_sha1']+'\t'+spec['historical_git_path']+'\n').encode(), 'entire historical ls-tree body')
    must(hashlib.sha1(b'commit '+str(len(commit)).encode()+b'\0'+commit).hexdigest() == spec['historical_commit'], 'actual historical commit object digest')
    must(failed['schema'] == 'root-explicit-command-capture/v1', 'literal failed ROOT capture class')
    must(type(failed['pid']) is int and failed['pid'] == 84831, 'actual failed child')
    must(type(failed['exit_code']) is int and failed['exit_code'] == 1 and failed['status'] == 'FAIL', 'failure retained')
    must(failed['actual_execution'] is True and failed['completed'] is True and failed['operator_unchanged'] is True, 'actual completed failure')
    must(type(failed['expected_exit_code']) is int and failed['expected_exit_code'] == 0, 'failed expected success')
    must(diag['schema'] == 'pr46-root-adverse-closure-failed-input-diagnosis/v2', 'use correct diagnosis only')
    must(type(diag['total']) is int and diag['total'] == 2611 and len(diag['changed']) == 1, 'single declared drift')
    must(typed(diag['changed'][0]['old'], expected), 'full typed diagnosed original')
    must(diag['changed'][0]['now']['path'] == expected['path'], 'no additional waived native path')
    must(diag['family_closed'] is False and diag['future_acceptance_approved'] is False, 'dated failure is no authority')


spec_check(q, row, before, after, git_body, tree_body, commit_body, root_cap, diagnosis)
must(original['actual_pid'] == 55086 and original['main_before'] == original['main_after'] == q['historical_commit'], 'primary actual identity and main')
must(typed(original['native13_before'], original['native13_after']) and len(original['native13_before']) == 13, 'original entire native thirteen typed preservation')
must(type(old['normalized_external_count']) is int and len(old['external_bindings']) == old['normalized_external_count'] == 2611, 'entire original binding count')
must(len({r['path'] for r in old['external_bindings']}) == 2611, 'no duplicate or omitted binding')
live_rows = [live(ref) for ref in old['external_bindings'] if ref['path'] != row['path']]
must(len(live_rows) == 2610, 'all other original live bindings read and checked')
must(len(extra) == 6 and len({r['path'] for r in extra}) == 6, 'six new distinct fixed receipts')
for cap in caps:
    pre = decode(body(Path(cap['prelaunch']['path'])))
    folder = Path(cap['prelaunch']['path']).parent
    must(typed(cap['argv'], pre['argv']) and cap['cwd'] == pre['cwd'] == str(R), 'actual recovery command identity')
    must(type(cap['child_pid']) is int and cap['child_pid'] > 0 and type(cap['exit_code']) is int and cap['exit_code'] == 0, 'actual recovery success')
    must(cap['child_source'] is None and pre['child_source'] is None and pre['source_copied_before_launch'] is False, 'Git has no fabricated Python child source')
    must({p.name for p in folder.iterdir()} == {'CAPTURE.json','PRELAUNCH.json','prelaunch_operator.py','stdout.bin','stderr.bin'}, 'exact recovery capture topology')
    for key in ['operator','prelaunch','stdout','stderr']:
        own(cap[key])
    must(body(folder/'prelaunch_operator.py') == own(cap['operator']), 'prelaunch actual operator body')
    must(own(cap['stderr']) == b'', 'full empty actual Git stderr')
    clocks = [time(pre['created_utc']),time(cap['started_utc']),time(cap['finished_utc'])]
    must(clocks == sorted(clocks), 'actual recovery clock sequence')
must(typed([cap['argv'] for cap in caps], [
    ['/usr/bin/git','show',q['historical_commit']+':unsolved_math_prioritization/QUEUE.md'],
    ['/usr/bin/git','ls-tree',q['historical_commit'],'--','unsolved_math_prioritization/QUEUE.md'],
    ['/usr/bin/git','cat-file','commit',q['historical_commit']]]), 'all literal Git argv')
must(own(caps[0]['stdout']) == git_body, 'captured full Git body equality')
must(body(Path(extra[5]['path'])) == body(F/'close_source_adversary.py'), 'preserve identical ROOT archived original closer')
root_folder = Path(extra[0]['path']).parent
must({p.name for p in root_folder.iterdir()} == {'CAPTURE.json','prelaunch_operator.py','stdout.bin','stderr.bin'}, 'literal ROOT four-member failure class')
must(digest(body(Path(extra[1]['path']))) == root_cap['operator_sha256'], 'actual ROOT operator bound')
for key, index in [('stdout',2),('stderr',3)]:
    actual = body(Path(extra[index]['path']))
    must(type(root_cap[key]['bytes']) is int and len(actual) == root_cap[key]['bytes'] and digest(actual) == root_cap[key]['sha256'], 'full ROOT split stream '+key)
must(body(Path(extra[2]['path'])) == b'' and b'AssertionError' in body(Path(extra[3]['path'])), 'genuine failed full streams')
must(time(root_cap['started_utc']) <= time(root_cap['finished_utc']), 'failed ROOT actual clock')
pins_raw = own(q['original_payload_body_pins'])
pins = decode(pins_raw)
must(len(pins['files']) == pins['original_payload_count'] == 51, 'original full payload pin count')
must(digest(('\n'.join(ref['path'] for ref in pins['files'])+'\n').encode()) == pins['original_paths_sha256'] == '6784ff56af6f874984f1836eb6d49b691f3974172ae4a39aa2d84d29a7e49b7b', 'original exact51 names')
for ref in pins['files']:
    own(ref)
must(not (F/'SELF_MANIFEST.json').exists(), 'no own closure launched')


def reject(label, invoke):
    try:
        invoke()
    except (AssertionError, ValueError, KeyError):
        rejected.append(label)
        return
    raise AssertionError('mutant accepted: '+label)


def q_mutant(label, key, value):
    mutant = copy.deepcopy(q)
    mutant[key] = value
    reject(label, lambda:spec_check(mutant,row,before,after,git_body,tree_body,commit_body,root_cap,diagnosis))


for key,value in [('dated_native_qualification_count',2),('original_live_binding_count',2609),
                  ('original_external_binding_count',True),('fresh_native_authority',True),
                  ('future_acceptance_approved',True),('own_closure_launched',True),
                  ('production_imported_compiled_executed',True),('historical_commit','0'*40),
                  ('historical_git_path','unsolved_math_prioritization/state.json'),
                  ('historical_git_mode','100755'),('historical_blob_sha1','0'*40),
                  ('source_verdict_unchanged','PASS'),('all_other_original_bindings_remain_exact_live_body_and_full_mode',False)]:
    q_mutant('qualification '+key,key,value)
for key,value in [('path',str(R/'unsolved_math_prioritization/state.json')),('bytes',True),('full_mode',False),('sha256','0'*64),('literal_observations',[])]:
    mutant = copy.deepcopy(q)
    mutant['original_native_observation'][key] = value
    reject('entire old row '+key,lambda m=mutant:spec_check(m,row,before,after,git_body,tree_body,commit_body,root_cap,diagnosis))
for name,mutant in [('before',dict(before,bytes=True)),('after',dict(after,extra='unapproved'))]:
    args = (mutant,after) if name == 'before' else (before,mutant)
    reject('typed original '+name,lambda a=args:spec_check(q,row,a[0],a[1],git_body,tree_body,commit_body,root_cap,diagnosis))
reject('changed recovered byte',lambda:spec_check(q,row,before,after,b'X'+git_body[1:],tree_body,commit_body,root_cap,diagnosis))
reject('changed tree mode',lambda:spec_check(q,row,before,after,git_body,tree_body.replace(b'100644',b'100755'),commit_body,root_cap,diagnosis))
reject('changed commit body',lambda:spec_check(q,row,before,after,git_body,tree_body,commit_body+b'X',root_cap,diagnosis))
for key,value in [('status','PASS'),('exit_code',False),('actual_execution',False),('pid',True)]:
    mutant = dict(root_cap,**{key:value})
    reject('failed capture '+key,lambda m=mutant:spec_check(q,row,before,after,git_body,tree_body,commit_body,m,diagnosis))
mutant = copy.deepcopy(diagnosis)
mutant['changed'].append(copy.deepcopy(mutant['changed'][0]))
reject('additional native exception',lambda:spec_check(q,row,before,after,git_body,tree_body,commit_body,root_cap,mutant))
for raw in [b'{"x":1,"x":2}',b'{"x":NaN}',b'{"x":1e999}',b'{} {}']:
    reject('strict JSON '+raw.decode(),lambda r=raw:decode(r))
must(not typed(False,0) and not typed(None,{}) and not typed(1,1.0), 'typed null/bool/numeric distinctions')
must(len(rejected) == 32, 'all expected independent mutant rejections')
current_queue = body(R / 'unsolved_math_prioritization/QUEUE.md')
result = {'schema':'pr46-source-adversary-dated-native-repair-controls/v1','status':'PASS_DATED_NATIVE_REPAIR_CONTROLS',
          'actual_pid':os.getpid(),'started_utc':started,'finished_utc':datetime.now(timezone.utc).isoformat(),
          'assertions':assertions,'rejected_mutants':rejected,'original_live_bindings_checked':2610,
          'dated_native_observations_checked':1,'additional_fixed_external_receipts_checked':6,
          'original_payload_bodies_preserved':51,'unique_full_body_read_paths':len(reads),'full_read_bytes_including_repeats':read_bytes,
          'original_bindings_body_sha256':digest(old_raw),'qualification_body_sha256':digest(q_raw),
          'original_payload_pins_body_sha256':digest(pins_raw),
          'full_verified_live_refs_digest':digest(json.dumps(live_rows,sort_keys=True,separators=(',',':')).encode()),
          'historical_full_body_bytes':len(git_body),'historical_full_body_sha256':digest(git_body),
          'historical_commit':q['historical_commit'],'historical_blob_sha1':q['historical_blob_sha1'],
          'dated_current_queue_observation_only':{'path':str(R/'unsolved_math_prioritization/QUEUE.md'),
              'bytes':len(current_queue),'sha256':digest(current_queue),'full_mode':stat.S_IMODE((R/'unsolved_math_prioritization/QUEUE.md').stat().st_mode)},
          'production_imported_compiled_executed':False,'own_closure_launched':False,'fresh_native_authority':False,
          'future_acceptance_approved':False,'source_verdict_unchanged':'REJECT_MANDATORY_SOURCE_CORRECTION',
          'mandatory_finding_unchanged':'S1','new_substantive_attempts':0,'audit_turns':0}
with (F/'CLOSURE_REPAIR_CONTROL_RESULT.json').open('x') as handle:
    handle.write(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:result[k] for k in ['status','actual_pid','assertions','original_live_bindings_checked','dated_native_observations_checked','additional_fixed_external_receipts_checked','original_payload_bodies_preserved']},indent=2))
