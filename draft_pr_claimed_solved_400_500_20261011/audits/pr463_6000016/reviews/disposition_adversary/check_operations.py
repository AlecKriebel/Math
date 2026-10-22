#!/usr/bin/env python3
"""Offline actual-entrypoint tests; no executable real API dispatch is retained."""
import argparse
import base64
import contextlib
import copy
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import sys
import tempfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
HELPER = HERE.parents[1] / 'operations_history/before_disposition_adversary1/repair_pr463_status.py'
REVIEWED_HELPER_SHA256 = '96431115586558f37922254c65753264871319f7b580d40685e1796e68cc5976'
ORIGINAL = '982fcf87d60c9f8d4ec853d5dd5f4ad6021a6649'
BRANCH = 'research/6000016-hessian-stability-audited'
QUEUE = 'unsolved_math_prioritization/QUEUE.md'
FAMILIES = ['source_topology', 'global_obstruction', 'reproduction', 'priority', 'candidate_adversary', 'disposition_adversary']

def require(condition, message):
    if not condition:
        raise RuntimeError(message)

def digest(data):
    return hashlib.sha256(data).hexdigest()

def fixture():
    row = (HERE.parents[1] / 'selected_queue_row.md').read_text().strip()
    header = '| Rank | ID / code | Problem | EV | Impact (/10) | Difficulty | Proposed | Status | Turns | Chat | Findings | DOI |'
    adjacent = '| 492 | 6000015 / OTHER | Adjacent | 1 | 2 | 3 | 1998 | unsolved | 5/5 | adjacent-chat | adjacent-finding | adjacent-doi |'
    queue = ('intro bytes\n' + header + '\n|---|---|---|---|---|---|---|---|---|---|---|---|\n' + adjacent + '\n' + row + '\ntrailer bytes\n').encode()
    reviews = [{'family': f, 'blocking_issues': 0, 'unresolved_disposition_issues': 0,
                'report_path': 'reviews/' + f + '/REPORT.md',
                'result_path': 'reviews/' + f + '/RESULT.json'} for f in FAMILIES]
    gate = {'verdict': 'ACCEPTED_PRIORITY_CLASSIFICATION', 'pr': 463,
            'problem_id': '6000016', 'original_head': ORIGINAL, 'recommended_status': 'already_solved',
            'root_read_entire_final_reports': True, 'helper_sha256': digest(HELPER.read_bytes()),
            'reviews': reviews, 'reviewed_files': [],
            'published_disposition_url': 'https://github.com/AlecKriebel/Math/blob/' + 'a'*40 + '/draft_pr_claimed_solved_400_500_20261011/audits/pr463_6000016/DISPOSITION_SYNTHESIS.md'}
    return queue, gate

class FakeAPI:
    def __init__(self, queue, config):
        self.queue = queue
        self.config = config
        self.calls = []
        self.ref = ORIGINAL
        self.new_bytes = None
        self.patch_count = 0
        self.ref_reads = 0

    def __call__(self, endpoint, payload=None, method='POST'):
        self.calls.append({'endpoint': endpoint, 'mutation': payload is not None, 'method': method})
        if endpoint == 'pulls/463':
            return {'state': self.config.get('state', 'open'), 'draft': self.config.get('draft', True),
                    'head': {'sha': self.config.get('head', ORIGINAL), 'ref': self.config.get('head_ref', BRANCH),
                             'repo': {'full_name': self.config.get('head_repo', 'AlecKriebel/Math')}},
                    'base': {'ref': self.config.get('base', 'main'), 'repo': {'full_name': 'AlecKriebel/Math'}}}
        if endpoint.startswith('git/ref/heads/'):
            self.ref_reads += 1
            if self.ref_reads == self.config.get('ref_changed_on_read'):
                self.ref = '0'*40
            return {'object': {'sha': self.config.get('ref', self.ref)}}
        if endpoint == 'git/commits/' + ORIGINAL:
            return {'tree': {'sha': 'root-tree'}}
        if endpoint == 'git/trees/root-tree':
            return {'tree': [{'path': 'unsolved_math_prioritization', 'sha': 'queue-tree', 'type': 'tree', 'mode': '040000'}]}
        if endpoint == 'git/trees/queue-tree':
            return {'tree': [{'path': 'QUEUE.md', 'sha': 'original-blob', 'type': 'blob', 'mode': '100644'}]}
        if endpoint == 'git/blobs/original-blob':
            return {'content': base64.b64encode(self.queue).decode()}
        if endpoint == 'git/blobs':
            self.new_bytes = base64.b64decode(payload['content'])
            return {'sha': 'new-blob'}
        if endpoint == 'git/trees':
            require(payload['base_tree'] == 'root-tree' and payload['tree'] == [{'path': QUEUE, 'mode': '100644', 'type': 'blob', 'sha': 'new-blob'}], 'Wrong tree patch')
            return {'sha': 'new-tree'}
        if endpoint == 'git/commits':
            require(payload['parents'] == [ORIGINAL] and payload['tree'] == 'new-tree', 'Wrong commit parent/tree')
            return {'sha': 'b'*40}
        if endpoint.startswith('compare/'):
            return {'files': [{'filename': self.config.get('compare_file', QUEUE)}]}
        if endpoint.startswith('git/refs/heads/'):
            require(payload == {'sha': 'b'*40, 'force': False}, 'Wrong branch update')
            self.patch_count += 1
            if self.config.get('patch_fails_no_update'):
                raise RuntimeError('Simulated uncertain ref update with unchanged readback')
            self.ref = 'b'*40
            if self.config.get('patch_uncertain_success'):
                raise RuntimeError('Simulated successful but uncertain response')
            return {'object': {'sha': self.ref}}
        if endpoint == 'git/blobs/new-blob':
            return {'content': base64.b64encode(self.new_bytes).decode()}
        raise RuntimeError('Unexpected fake API endpoint: ' + endpoint)

def execute(name, config, expected_acceptance):
    queue, gate = fixture()
    if 'queue_status' in config:
        queue = queue.replace(b'| claimed_solved |', ('| '+config['queue_status']+' |').encode())
    if config.get('duplicate_target'):
        row = next(x for x in queue.splitlines() if b'6000016 /' in x)
        queue += row + b'\n'
    if config.get('crlf'):
        queue = queue.replace(b'\n', b'\r\n')
    for key, value in config.get('gate_updates', {}).items():
        gate[key] = value
    for key in config.get('gate_delete', []):
        gate.pop(key, None)
    if config.get('review_update'):
        gate['reviews'][0].update(config['review_update'])
    if config.get('missing_family'):
        gate['reviews'].pop()
    if config.get('duplicate_family'):
        gate['reviews'][-1] = copy.deepcopy(gate['reviews'][0])
    private = HERE / 'private_cases'
    private.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='case_', dir=private) as d:
        audit = Path(d).resolve()
        (audit/'pr_metadata.json').write_text(json.dumps({'headRefName': BRANCH}))
        (audit/'SOURCE_RECEIPT.json').write_text(json.dumps({'queue_sha256': digest(queue)}))
        if not config.get('missing_gate'):
            (audit/'PRIORITY_DISPOSITION_GATE.json').write_text(json.dumps(gate))
        if config.get('prior_operation'):
            (audit/'STATUS_REPAIR_OPERATION.json').write_text('{}')
        if config.get('output_attack'):
            target = audit/config.get('output_name','STATUS_REPAIR_RECEIPT.json')
            outside = audit/'sentinel.txt'; outside.write_text('sentinel')
            if config['output_attack'] == 'symlink':
                target.symlink_to(outside)
            elif config['output_attack'] == 'dangling':
                target.symlink_to(audit/'absent')
            elif config['output_attack'] == 'hardlink':
                os.link(outside, target)
            elif config['output_attack'] == 'directory':
                target.mkdir()
            elif config['output_attack'] == 'fifo':
                os.mkfifo(target)
        if config.get('evidence'):
            data = b'actual accepted bytes\n'
            (audit/'BOUND_REPORT.md').write_bytes(data)
            gate['reviewed_files'] = [{'path': 'BOUND_REPORT.md', 'sha256': digest(data) if config['evidence']=='matching' else '0'*64}]
            (audit/'PRIORITY_DISPOSITION_GATE.json').write_text(json.dumps(gate))
        spec = importlib.util.spec_from_file_location('repair_' + name, HELPER)
        m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
        m.AUDIT = audit
        api = FakeAPI(queue, config)
        m.api = api
        old = sys.argv
        sys.argv = [str(HELPER)] + (['--apply'] if config.get('apply') else [])
        error = None
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                m.main()
        except Exception as e:
            error = {'type': type(e).__name__, 'message': str(e)}
        finally:
            sys.argv = old
        accepted = error is None
        if accepted and config.get('apply'):
            before = queue.splitlines(keepends=True)
            after = api.new_bytes.splitlines(keepends=True)
            require(len(before)==len(after), 'Line count changed')
            changed = [i for i,(a,b) in enumerate(zip(before,after)) if a!=b]
            require(len(changed)==1, 'Multiple rows changed')
            a = before[changed[0]].decode().rstrip('\r\n').split('|')
            b = after[changed[0]].decode().rstrip('\r\n').split('|')
            require([i for i,(u,v) in enumerate(zip(a,b)) if u!=v]==[8,11], 'Adjacent cell changed')
            require(b[8].strip()=='already_solved' and b[9].strip()=='1/5' and b[12].strip()=='', 'Preserved cells changed')
            require(api.patch_count==1, 'Repeated branch mutation')
        if config.get('output_attack'):
            require((audit/'sentinel.txt').read_text()=='sentinel', 'Outside output overwritten')
        if config.get('patch_fails_no_update'):
            require(api.patch_count==1, 'Repeated uncertain branch update')
        require(accepted==expected_acceptance, name + ': unexpected acceptance')
        return {'case': name, 'accepted': accepted, 'expected_acceptance': expected_acceptance,
                'error': error, 'api_call_count': len(api.calls),
                'mutation_calls': [c for c in api.calls if c['mutation']], 'ref_patch_count': api.patch_count}

def main():
    require(digest(HELPER.read_bytes())==REVIEWED_HELPER_SHA256, 'Historical helper changed')
    cases = [
        ('positive_preflight', {}, True), ('positive_apply', {'apply': True}, True),
        ('positive_crlf_apply', {'apply': True, 'crlf': True}, True),
        ('empty_evidence_gate', {'apply': True}, True),
        ('disconnected_matching_evidence', {'apply': True,'evidence':'matching'}, True),
        ('mutable_main_disposition_link', {'apply': True,'gate_updates':{'published_disposition_url':'https://github.com/AlecKriebel/Math/blob/main/DISPOSITION_SYNTHESIS.md'}}, True),
        ('unqualified_wrong_path_link', {'apply':True,'gate_updates':{'published_disposition_url':'https://github.com/AlecKriebel/Math/blob/'+'a'*40+'/other/DISPOSITION_SYNTHESIS.md?bad=1'}}, True),
        ('missing_gate', {'missing_gate':True}, False),
        ('wrong_helper_bytes', {'gate_updates':{'helper_sha256':'0'*64}}, False),
        ('root_acceptance_false', {'gate_updates':{'root_read_entire_final_reports':False}}, False),
        ('wrong_head_gate', {'gate_updates':{'original_head':'0'*40}}, False),
        ('wrong_status_gate', {'gate_updates':{'recommended_status':'claimed_solved'}}, False),
        ('missing_family', {'missing_family':True}, False), ('duplicate_family', {'duplicate_family':True}, False),
        ('count_bool', {'review_update':{'blocking_issues':False}}, False),
        ('count_float', {'review_update':{'blocking_issues':0.0}}, False),
        ('count_nonzero', {'review_update':{'blocking_issues':1}}, False),
        ('disposition_count_bool', {'review_update':{'unresolved_disposition_issues':False}}, False),
        ('evidence_hash_mismatch', {'evidence':'mismatch'}, False),
        ('excluded_already_solved', {'queue_status':'already_solved','apply':True}, False),
        ('excluded_unsolved', {'queue_status':'unsolved','apply':True}, False),
        ('excluded_empty', {'queue_status':'','apply':True}, False),
        ('head_changed', {'head':'0'*40,'apply':True}, False),
        ('ref_changed', {'ref':'0'*40,'apply':True}, False),
        ('head_ref_changed', {'head_ref':'other','apply':True}, False),
        ('head_repository_changed', {'head_repo':'Other/Repo','apply':True}, False),
        ('base_changed', {'base':'other','apply':True}, False),
        ('draft_false', {'draft':False,'apply':True}, False),
        ('state_closed', {'state':'closed','apply':True}, False),
        ('duplicate_target_row', {'duplicate_target':True,'apply':True}, False),
        ('prior_operation', {'prior_operation':True,'apply':True}, False),
        ('compare_unrelated_path', {'compare_file':'other.txt','apply':True}, False),
        ('uncertain_successful_patch', {'patch_uncertain_success':True,'apply':True}, True),
        ('uncertain_failed_patch', {'patch_fails_no_update':True,'apply':True}, False),
        ('ref_changed_before_commit', {'ref_changed_on_read':2,'apply':True}, False),
        ('ref_changed_before_patch', {'ref_changed_on_read':3,'apply':True}, False),
    ]
    cases += [('output_'+name+'_'+k, {'output_attack':k,'output_name':name,'apply':True}, False)
              for name in ['STATUS_REPAIR_PREFLIGHT.json','STATUS_REPAIR_OPERATION.json','STATUS_REPAIR_RECEIPT.json']
              for k in ['symlink','dangling','hardlink','directory','fifo']]
    results = [execute(*c) for c in cases]
    print(json.dumps({'status':'PASS','helper_sha256':digest(HELPER.read_bytes()),'test_count':len(results),
                      'all_api_dispatches':'mocked in process; no genuine network dispatch', 'results':results},indent=2))

if __name__=='__main__':
    main()
