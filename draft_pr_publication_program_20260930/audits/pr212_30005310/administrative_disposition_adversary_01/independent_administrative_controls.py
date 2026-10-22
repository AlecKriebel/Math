"""Independent offline PR212 administrative-disposition checks.
Reads retained immutable inputs only. Writes this folder's result only.
No network, Git, subprocess, reference, lock, PR or provider API exists.
"""
import base64
import copy
import datetime
import hashlib
import json
import math
import os
from pathlib import Path
import stat

OUT = Path(__file__).resolve().parent
CASE = OUT.parent
NATIVE = CASE / 'native_custody_01'
CAP = CASE / 'admin_status_confirmation_01'
GOAL = Path('/Users/alec/.codex/attachments/4df73d3d-641f-4907-b9ad-c47c468f2589/goal-objective.md')
HEAD = '99af7a27a711271bcd0b9e7ce90e374e4100ea6d'
ORIGINAL = 'c697b4a5cc62f3b8836d8c37d82b71a1d1c53fb7'
BLOB = '75dd3438de4cd64c023595f67b9331392278315f'
CHECKS = []
INPUTS = []

def need(ok, label):
    if type(ok) is not bool or not ok:
        raise ValueError(label)

def checked(label, fn):
    fn()
    CHECKS.append({'label': label, 'outcome': 'PASS'})

def pin(raw):
    return {'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}

def native(kind, body):
    return hashlib.sha1(kind.encode() + b' ' + str(len(body)).encode() + b'\0' + body).hexdigest()

def regular(path, immutable=True):
    need(path.is_absolute() and path.resolve() == path, 'canonical input')
    f = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
    try:
        s = os.fstat(f)
        need(stat.S_ISREG(s.st_mode) and s.st_size < 16_000_000, 'bounded ordinary input')
        if immutable:
            need(stat.S_IMODE(s.st_mode) == 0o444, 'immutable input mode')
        raw = os.read(f, 16_000_000)
        t = os.fstat(f)
        need((s.st_dev,s.st_ino,s.st_size,s.st_mtime_ns,s.st_ctime_ns) ==
             (t.st_dev,t.st_ino,t.st_size,t.st_mtime_ns,t.st_ctime_ns), 'stable descriptor')
        need(len(raw) == s.st_size, 'complete input')
        return raw
    finally:
        os.close(f)

def strict(raw):
    def pairs(rows):
        v = {}
        for k, x in rows:
            need(k not in v, 'duplicate JSON key')
            v[k] = x
        return v
    def finite(v):
        x = float(v)
        need(math.isfinite(x), 'nonfinite JSON number')
        return x
    return json.loads(raw, object_pairs_hook=pairs, parse_float=finite,
                      parse_constant=lambda _: need(False, 'nonfinite JSON constant'))

def read_pin(path, size, sha, immutable=True):
    raw = regular(path, immutable)
    need(pin(raw) == {'bytes': size, 'sha256': sha}, 'input pin ' + str(path))
    INPUTS.append({'path': str(path), **pin(raw)})
    return raw

def same(a, b):
    if type(a) is not type(b):
        return False
    if type(a) is dict:
        return set(a) == set(b) and all(same(a[k], b[k]) for k in a)
    if type(a) is list:
        return len(a) == len(b) and all(same(x,y) for x,y in zip(a,b))
    return a == b

def row(raw):
    rows = []
    for line in raw.splitlines(keepends=True):
        cells = line.decode().split('|')
        if len(cells) == 14 and cells[2].strip().split(' / ')[0] == '30005310':
            rows.append((line, cells))
    need(len(rows) == 1, 'one exact target row')
    return rows[0]

def pr_guard(pr):
    need(type(pr['number']) is int and pr['number'] == 212, 'correct PR')
    need(pr['state'] == 'open' and pr['draft'] is True and pr['merged'] is False,
         'open draft unmerged')
    need(pr['head']['sha'] == HEAD and pr['head']['ref'] == 'math/30005310-colored-threshold-wip',
         'exact head branch')
    need(pr['base']['ref'] == 'main' and pr['base']['repo']['full_name'] == 'AlecKriebel/Math',
         'base identity')
    need(pr['title'] == '30005310: Credited prior counterexamples to literal numerical scenarios',
         'exact title')
    need(type(pr['commits']) is int and pr['commits'] == 3, 'three commits')

def policy_guard(p):
    exact = {
      'PR': 212, 'problem_id': '30005310', 'accepted': True,
      'original_eligible_status': 'claimed_solved', 'original_head': ORIGINAL,
      'current_corrected_status': 'already_solved', 'current_head': HEAD,
      'current_PR_open_draft_unmerged': True,
      'original_eligibility_rewritten_or_erased': False,
      'accepted_original_eligible_audit_evidence_preserved': True,
      'completed_eligible_workflow': False, 'publication_workflow_completed': False,
      'publication_ready': False, 'goal_complete': False,
      'administrative_checkpoint_complete': False,
      'Root_native_checkpoint_or_local_five_execution_by_this_gate': False,
      'numeric_advance_authorized_by_this_file': False,
      'actual_numeric_cursor_still': 212, 'conditional_target_numeric_cursor': 213,
      'actual_completed_count_retained': 53, 'actual_published_count_retained': 37,
      'last_completed_eligible_PR_retained': 211,
      'completed_and_published_membership_lists_must_remain_exactly_baseline': True,
      'new_paper_DOI_tracker_row_merge_close_comment_release_or_attempt_QUEUE_edit_authorized': False,
      'disposition': 'ADMINISTRATIVE_ADVANCE_CORRECTED_NONCLAIMED_DRAFT_UNTOUCHED',
      'evidence_scope': 'ACTUAL_ROOT_DISPOSITION_ONLY_NOT_NATIVE_OR_NUMERIC_ADVANCEMENT'
    }
    for k, v in exact.items():
        need(k in p and same(p[k], v), 'policy semantics ' + k)
    need('AFTER' not in p['archive_commit_if_later_authorized'] or
         'one-parent' in p['archive_commit_if_later_authorized'], 'no PR merge parent')
    need('one-parent' in p['archive_commit_if_later_authorized'] and
         'never a PR212HEAD merge parent' in p['archive_commit_if_later_authorized'],
         'ordinary Main parent required')
    need('separate actual administrative terminal' in p['next_gate'],
         'separate actual terminal required')

def main():
    pins = [
      ('ROOT_ADMINISTRATIVE_DISPOSITION_01.json',4606,'6e2f3b82c2a6a23ec4e33d51a92d3a4d91e9a702b8896c0c2e90703d6beeb824'),
      ('ROOT_MATHEMATICAL_ACCEPTANCE_01.json',7885,'790b6482fcc2ef5fe39ebb7fc12850213b67133de0221861ee6cb5eb122e4512'),
      ('ROOT_PRIORITY_ACCEPTANCE_01.json',6441,'1ad1506d4a21c4d1b4cef16a3db059ad3609fab1a33e1834c7b813356b9a73d2'),
      ('ROOT_NATIVE_CUSTODY_ACCEPTANCE_01.json',6525,'c240a9b71efee22f0699f42d1437d5731b5542024704c2ca7ceb129badbe3529'),
      ('ROOT_PRIORITY_QUALIFICATIONS_01.md',4342,'2ca7ab006830cb5038b98ca61707f21ff49d22572ccfd1b61ead510fa81ccd91'),
      ('admin_status_confirmation_01/capture_status.py',5719,'63af0ac1b2a78a95e5194d21ddfb8d66f631a2c709214b7ee5450e13a822cbf5'),
      ('admin_status_confirmation_01/FACTUAL_STATUS_CONFIRMATION.json',3225,'6476b124ad3565070a195436071d65cf2d087f48aab50f4181d7cdf36b1846f9'),
      ('admin_status_confirmation_01/ROOT_ACTUAL_EXECUTION.json',395,'c3e2a7e0d5ee16533b718c511e42f07256f2c4e5ebcd1ed22f5e1f5de0f03c16'),
      ('native_custody_01/get_primitives.py',3794,'808149b347a61809e37a0b71fc4dc602ec17e63e38e985d99123827268286e09'),
      ('native_custody_01/AUTHENTICATED_NATIVE_TREES.json',39395,'7b6f7a543d9964171b329c60442dc85295d88b80e3dde123cef1d5b0d116a36c'),
      ('native_custody_01/FACTUAL_CUSTODY_SUMMARY.json',13128,'d687b53177fd7897a0fdb1144ac437e62063057b133261f0da539fe7f32b5325'),
      ('native_custody_01/ACTUAL_TRANSPORT_INDEX.json',41188,'30c4e925c6158e126f0bfe09b37b6ac766c208c4d04f48c27377ebd0b3aed569')]
    raw_inputs = {p: read_pin(CASE / p,n,h) for p,n,h in pins}
    goal = read_pin(GOAL,4544,'1e29852cafce156dbc3b745f9d1b7bf973b6d07e4a3c924b901ad27754128d04',False)
    previous = strict(read_pin(CASE.parent/'pr211_5100063/ROOT_ACTUAL_COMPLETION_VERIFICATION_01.json',
             9799,'8acd4bb99e504f4fe59b9c28a91b8fdcfc5a71502b3b0f54cb98070a29467477'))
    need(previous['completed'] is True and previous['fully_completed_count'] == 53 and
         previous['published_count'] == 37 and previous['last_completed_PR'] == 211 and
         previous['next_numeric_intake_cursor'] == 212 and previous['goal_complete'] is False,
         'actual baseline counts')
    CHECKS.append({'label':'13 source/gate pins and actual prior baseline','outcome':'PASS'})
    policy = strict(raw_inputs['ROOT_ADMINISTRATIVE_DISPOSITION_01.json'])
    checked('policy separates original eligibility, current skip, counts and conditional advancement',
            lambda: policy_guard(policy))
    need(b'Skip every PR' in goal and b'anything other than `claimed_solved`' in goal,
         'actual goal strict status gate')
    for name in ['ROOT_MATHEMATICAL_ACCEPTANCE_01.json','ROOT_PRIORITY_ACCEPTANCE_01.json']:
        g = strict(raw_inputs[name])
        need(g['accepted'] is True and g['publication_ready'] is False and g['completed'] is False,
             'scientific gate not publication/completion')
    priority = strict(raw_inputs['ROOT_PRIORITY_ACCEPTANCE_01.json'])
    need(priority['bare_Boolean_conjecture_resolved'] is False and
         priority['current_status_classification_accepted'] == 'already_solved' and
         priority['unchanged_current_PR_publication_clearance'] is False and
         priority['firstness_or_causal_independence_established'] is False,
         'qualified priority scope')
    CHECKS.append({'label':'goal/gate semantic agreement and chronology not cleared','outcome':'PASS'})
    cap = strict(raw_inputs['admin_status_confirmation_01/FACTUAL_STATUS_CONFIRMATION.json'])
    need(len(cap['actual_GETs']) == 3 and cap['mutation_actions'] == 0 and
         cap['Root_disposition_or_checkpoint_acceptance'] is False and
         cap['perpetual_PR_or_Main_lease'] is False, 'factual capture only')
    responses=[]
    routes=['pulls/212','git/blobs/'+BLOB,'pulls/212']
    for index, rec in enumerate(cap['actual_GETs']):
        need(rec['route'] == routes[index], 'exact bounded route order')
        fetched={}
        for name in ['intent','response','stderr','receipt']:
            v=rec[name]
            need('/' not in v['path'], 'capture child path')
            fetched[name]=read_pin(CAP/v['path'],v['bytes'],v['sha256'])
        intent=strict(fetched['intent']);receipt=strict(fetched['receipt'])
        need(intent['argv'] == ['/opt/homebrew/Cellar/gh/2.85.0/bin/gh','api','--hostname',
             'github.com','--method','GET','repos/AlecKriebel/Math/'+routes[index]] and
             type(intent['retries']) is int and intent['retries']==0, 'actual GET-only exact intent')
        need(type(receipt['exit_code']) is int and receipt['exit_code']==0 and
             receipt['route']==routes[index] and receipt['method']=='GET' and
             same(receipt['intent'],rec['intent']) and
             same(receipt['stdout'],rec['response']) and same(receipt['stderr'],rec['stderr']) and
             fetched['stderr']==b'', 'actual successful raw trace association')
        responses.append(strict(fetched['response']))
    for pr in [responses[0],responses[2]]:
        pr_guard(pr)
    keys=('number','title','state','draft','merged','commits','body','created_at',
          'updated_at','merged_at','merge_commit_sha')
    need(all(same(responses[0].get(k),responses[2].get(k)) for k in keys),
         'dated start/end identity')
    blob=responses[1]
    need(blob['sha']==BLOB and blob['encoding']=='base64' and
         type(blob['size']) is int and blob['size']==371408,'blob exact envelope')
    body=base64.b64decode(''.join(blob['content'].split()),validate=True)
    need(native('blob',body)==BLOB and pin(body)=={'bytes':371408,'sha256':
         '3370b842e51760df443f3d08f26951cb9915e9946f2f3e0a200c5d75d07a552e'},'fresh body native OID')
    target,cells=row(body)
    need(cells[8].strip()=='already_solved' and cells[9].strip()=='1/5' and
         pin(target)==cap['QUEUE_row_pin'],'fresh exact corrected row')
    CHECKS.append({'label':'three full retained GET traces and fresh native corrected row','outcome':'PASS'})
    trees=strict(raw_inputs['native_custody_01/AUTHENTICATED_NATIVE_TREES.json'])
    for oid, entries in trees.items():
        raw=bytearray()
        for name, tup in sorted(entries.items(),key=lambda item:
                (item[0]+('/' if item[1][1]=='tree' else '')).encode()):
            mode, kind, child=tup
            need('/' not in name and kind in ('tree','blob'),'immediate finite tree')
            raw.extend(mode.lstrip('0').encode()+b' '+name.encode()+b'\0'+bytes.fromhex(child))
        need(native('tree',bytes(raw))==oid,'canonical tree '+oid)
    summary=strict(raw_inputs['native_custody_01/FACTUAL_CUSTODY_SUMMARY.json'])
    for role,expected_head,status in [('current',HEAD,'already_solved'),
                                     ('original',ORIGINAL,'claimed_solved')]:
        entry=summary[role]
        commit=regular(NATIVE/entry['raw_commit']['path'])
        need(pin(commit)=={k:entry['raw_commit'][k] for k in ('bytes','sha256')} and
             native('commit',commit)==expected_head,'canonical commit '+role)
        root=commit.split(b'\n',1)[0].decode().removeprefix('tree ')
        need(root==entry['tree'],'commit root '+role)
        mode,kind,subtree=trees[root]['unsolved_math_prioritization']
        need(mode=='040000' and kind=='tree','queue ancestor')
        qtuple=trees[subtree]['QUEUE.md'];q=summary['QUEUE'][role]
        need(qtuple==['100644','blob',q['sha']],'canonical queue path '+role)
        qbody=regular(NATIVE/q['private_QUEUE'])
        need(native('blob',qbody)==q['sha'] and pin(qbody)=={'bytes':q['bytes'],'sha256':q['sha256']},
             'retained original/current queue body')
        _,qc=row(qbody)
        need(qc[8].strip()==status,'distinct eligible/current statuses')
        if role=='current':
            need(qbody==body,'fresh body equals immutable current path body')
    need(commit.count(b'\nparent ')==1,'original one-parent relation retained')
    CHECKS.append({'label':'canonical nine trees, original/current commits and immutable QUEUE association','outcome':'PASS'})
    bad_fields={
      'original_eligible_status':'already_solved','current_corrected_status':'claimed_solved',
      'original_head':HEAD,'current_head':ORIGINAL,'current_PR_open_draft_unmerged':False,
      'original_eligibility_rewritten_or_erased':True,
      'accepted_original_eligible_audit_evidence_preserved':False,
      'completed_eligible_workflow':True,'publication_workflow_completed':True,
      'publication_ready':True,'goal_complete':True,'administrative_checkpoint_complete':True,
      'Root_native_checkpoint_or_local_five_execution_by_this_gate':True,
      'numeric_advance_authorized_by_this_file':True,'actual_numeric_cursor_still':213,
      'conditional_target_numeric_cursor':214,'actual_completed_count_retained':54,
      'actual_published_count_retained':38,'last_completed_eligible_PR_retained':212,
      'completed_and_published_membership_lists_must_remain_exactly_baseline':False,
      'new_paper_DOI_tracker_row_merge_close_comment_release_or_attempt_QUEUE_edit_authorized':True,
      'disposition':'MERGE_CURRENT_PR','evidence_scope':'ACTUAL_ROOT_COMPLETION'}
    for field,value in bad_fields.items():
        trial=copy.deepcopy(policy);trial[field]=value
        try:
            policy_guard(trial)
        except ValueError:
            CHECKS.append({'label':'negative policy '+field,'outcome':'EXPECTED_REFUSAL'})
        else:
            raise ValueError('policy negative accepted '+field)
    for field,value in [('number',True),('draft',False),('merged',True),('state','closed'),('commits',True)]:
        trial=copy.deepcopy(responses[0]);trial[field]=value
        try:
            pr_guard(trial)
        except ValueError:
            CHECKS.append({'label':'negative PR '+field,'outcome':'EXPECTED_REFUSAL'})
        else:
            raise ValueError('PR negative accepted '+field)
    for malformed in [b'{"a":1,"a":2}',b'{"a":NaN}',b'{"a":1e999}']:
        try:
            strict(malformed)
        except ValueError:
            CHECKS.append({'label':'strict JSON rejects '+malformed.decode(),'outcome':'EXPECTED_REFUSAL'})
        else:
            raise ValueError('malformed JSON accepted')
    result={'schema':'pr212-independent-administrative-offline-controls-v1',
      'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),
      'source_sha256':hashlib.sha256(regular(Path(__file__).resolve())).hexdigest(),
      'actual_execution':True,'checks':CHECKS,'input_pins':INPUTS,
      'mandatory_findings':[],'review_percent':100,
      'production_execution_or_advance_authorized':False,
      'no_network_Git_PR_provider_ref_lock_globalfive_or_other_chat_actions':True,
      'limitation':'Dated retained GET proof and policy review only; future packet/native/all-five execution requires separate review and actual Root terminal.'}
    data=(json.dumps(result,sort_keys=True,indent=2)+'\n').encode()
    f=os.open(OUT/'CONTROL_RESULT.json',os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o444)
    try:
        need(os.write(f,data)==len(data),'full result output');os.fsync(f)
    finally:
        os.close(f)
    print(json.dumps({'checks':len(CHECKS),'positive':sum(x['outcome']=='PASS' for x in CHECKS),
          'expected_refusals':sum(x['outcome']=='EXPECTED_REFUSAL' for x in CHECKS),
          'mandatory_findings':0,'result':pin(data)}))

if __name__ == '__main__':
    main()

