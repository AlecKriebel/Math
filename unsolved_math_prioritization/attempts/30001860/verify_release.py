#!/usr/bin/env python3
"""Portable exact-byte and bounded-control replay; not a formal proof checker."""
from pathlib import Path, PurePosixPath
import argparse
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile

AUTHOR = set('ATTEMPTS.md MANIFEST.json PROOF.md README.md SOURCE_VERIFICATION.json STATUS.json VERIFICATION.md verification_results.json verify.py'.split())
AUDIT = set('AUDIT_MANIFEST.json AUDIT_REPORT.md AUDIT_RESULTS.json BINDING.json NEGATIVE_CONTROLS.md REPRODUCE.md SCOPE_CLARIFICATIONS.md authored_replay.log authored_replay_results.json independent_controls.log independent_controls.py independent_results.json'.split())
TOP = set('README.md RELEASE_STATUS.json verify_release.py REPLAY_RESULTS.json RELEASE_MANIFEST.json'.split())
EXPECTED = TOP | {'release/'+s for s in AUTHOR} | {'independent_audit/safe/'+s for s in AUDIT}
PINS = {
    'release/MANIFEST.json': (1582, 'f23f0fc8f7f634f9fab4a19077126435f6bc5796b979cea9bd5f68de338348ca'),
    'independent_audit/safe/AUDIT_MANIFEST.json': (None, '26c32df4164a696125048476f9b5a5227646f64f5468a22b47227966ab4c1747'),
    'independent_audit/safe/AUDIT_REPORT.md': (20889, '04e2b9f16653e67ef71a968434a5f3190c3f1d8af623d45ee5cc435f7aeebd5a'),
}

def require(ok, message):
    if not ok:
        raise ValueError(message)

def sha(b):
    return hashlib.sha256(b).hexdigest()

def read_json(path):
    return json.loads(path.read_bytes())

def checked_record(root, name, rec):
    path = PurePosixPath(name)
    require(not path.is_absolute() and '..' not in path.parts and str(path) == name, 'unsafe path: '+name)
    b = (root/name).read_bytes()
    require(len(b) == rec['bytes'] and sha(b) == rec['sha256'], 'byte binding: '+name)

def records(root, rows, expected):
    require(len(rows) == len(expected) and {r['path'] for r in rows} == expected, 'manifest inventory')
    for r in rows:
        checked_record(root, r['path'], r)

def verify(root, replay=True):
    found, dirs = set(), set()
    for p in root.rglob('*'):
        require(not p.is_symlink(), 'symlink')
        name = p.relative_to(root).as_posix()
        if p.is_file():
            found.add(name)
        else:
            require(p.is_dir(), 'special node')
            dirs.add(name)
    require(found == EXPECTED, 'exact file boundary')
    require(dirs == {'release','independent_audit','independent_audit/safe'}, 'exact directory boundary')
    m = read_json(root/'RELEASE_MANIFEST.json')
    require(m['schema'] == 1 and m['problem_id'] == '30001860', 'manifest identity')
    records(root, m['files'], EXPECTED-{'RELEASE_MANIFEST.json'})
    for name, (size, digest) in PINS.items():
        b = (root/name).read_bytes()
        require(sha(b) == digest and (size is None or len(b) == size), 'external pin: '+name)
    author = root/'release'; audit = root/'independent_audit/safe'
    am, im, binding = read_json(author/'MANIFEST.json'), read_json(audit/'AUDIT_MANIFEST.json'), read_json(audit/'BINDING.json')
    require(am['problem_id'] == im['problem_id'] == binding['problem_id'] == '30001860', 'frozen identities')
    records(author, am['files'], AUTHOR-{'MANIFEST.json'})
    records(audit, im['files'], AUDIT-{'AUDIT_MANIFEST.json'})
    records(author, binding['frozen_files'], AUTHOR-{'MANIFEST.json'})
    checked_record(author, 'MANIFEST.json', binding['frozen_manifest'])
    require(im['frozen_manifest_sha256'] == PINS['release/MANIFEST.json'][1], 'audit target')
    require(im['verdict'] == 'PASS_SCOPED_WITH_CONTROLLING_RANK_CLARIFICATION', 'audit verdict')
    status = read_json(root/'RELEASE_STATUS.json')
    require(status['problem_id'] == '30001860' and status['queue_status'] == 'unsolved' and status['turns'] == '5/5', 'disposition')
    require(status['full_resolution'] is False and status['controlling_rank_clarification_adopted'] is True, 'scope gate')
    require(status['GL_U_lower_bound_minimum_natural_dimension'] == 3 and status['LNP_lower_bound_minimum_semisimple_rank'] == 2, 'rank gate')
    require(status['SL_SU_extension'] == 'fixed_q_only', 'fixed-field gate')
    result = {'integrity':'PASS', 'package_files':len(EXPECTED), 'frozen_author_files':len(AUTHOR), 'frozen_audit_files':len(AUDIT),
              'qualification':'Exact-byte integrity and finite controls only; not a formal proof, novelty, or global-openness certificate.'}
    if replay:
        with tempfile.TemporaryDirectory(prefix='classical-replay-') as td:
            t = Path(td)
            cmd = [sys.executable, '-B']
            a = subprocess.run(cmd+[str(author/'verify.py'),'--sp4','--output',str(t/'author.json')],capture_output=True,check=True)
            require(not a.stderr and (t/'author.json').read_bytes() == (author/'verification_results.json').read_bytes(), 'author exact replay')
            b = subprocess.run(cmd+[str(audit/'independent_controls.py'),'--frozen',str(author),'--output',str(t/'independent.json')],capture_output=True,check=True)
            require(not b.stderr, 'independent stderr')
            got, expected = read_json(t/'independent.json'), read_json(audit/'independent_results.json')
            got.pop('elapsed_seconds'); expected.pop('elapsed_seconds')
            require(got == expected and got['all_passed'] is True, 'independent semantic replay')
            require(len(got['matrices']) == 5 and got['coefficients']['partition_matches'] == 198, 'control coverage')
            result['replay'] = {'author':'byte-identical','independent':'identical after excluding elapsed_seconds only',
                                'matrix_controls':5,'partition_matches':198,'mathematical_negative_controls':7,
                                'finite_controls_are_asymptotic_proof':False}
    return result

def corruption_controls(root):
    cases = ['changed_author','changed_audit','changed_guide','missing','extra_hidden','nested_empty','symlink','unlisted_pdf',
             'manifest_traversal','manifest_omission','manifest_duplicate','coordinated_author','coordinated_audit',
             'wrong_status','wrong_rank','removed_clarification','uniform_SL_SU']
    for case in cases:
        with tempfile.TemporaryDirectory(prefix='classical-corruption-') as td:
            p = Path(td)/'packet'; shutil.copytree(root,p)
            outer = read_json(p/'RELEASE_MANIFEST.json')
            def rebind(name):
                b = (p/name).read_bytes()
                for row in outer['files']:
                    if row['path'] == name:
                        row.update(bytes=len(b),sha256=sha(b))
                        return
                raise ValueError('unlisted mutation')
            if case.startswith('changed_'):
                name = {'changed_author':'release/PROOF.md','changed_audit':'independent_audit/safe/AUDIT_REPORT.md','changed_guide':'README.md'}[case]
                b = bytearray((p/name).read_bytes()); b[0] ^= 1; (p/name).write_bytes(b)
            elif case == 'missing': (p/'README.md').unlink()
            elif case == 'extra_hidden': (p/'.extra').write_text('synthetic control')
            elif case == 'nested_empty': (p/'release/empty').mkdir()
            elif case == 'symlink': (p/'README.md').unlink(); (p/'README.md').symlink_to('release/README.md')
            elif case == 'unlisted_pdf': (p/'source.pdf').write_bytes(b'%PDF synthetic corruption control')
            elif case.startswith('manifest_'):
                if case == 'manifest_traversal': outer['files'][0]['path']='../README.md'
                elif case == 'manifest_omission': outer['files'].pop()
                else: outer['files'].append(dict(outer['files'][0]))
            elif case.startswith('coordinated_'):
                folder, name, manifest = ('release','PROOF.md','MANIFEST.json') if case.endswith('author') else ('independent_audit/safe','AUDIT_REPORT.md','AUDIT_MANIFEST.json')
                target = folder+'/'+name; ip = folder+'/'+manifest
                (p/target).write_bytes((p/target).read_bytes()+b'\nsynthetic change\n')
                inner = read_json(p/ip); b=(p/target).read_bytes()
                for row in inner['files']:
                    if row['path'] == name: row.update(bytes=len(b),sha256=sha(b))
                (p/ip).write_text(json.dumps(inner)); rebind(target); rebind(ip)
            else:
                s = read_json(p/'RELEASE_STATUS.json')
                key, value = {'wrong_status':('queue_status','claimed_solved'),'wrong_rank':('GL_U_lower_bound_minimum_natural_dimension',2),
                              'removed_clarification':('controlling_rank_clarification_adopted',False),'uniform_SL_SU':('SL_SU_extension','uniform_q')}[case]
                s[key]=value; (p/'RELEASE_STATUS.json').write_text(json.dumps(s)); rebind('RELEASE_STATUS.json')
            (p/'RELEASE_MANIFEST.json').write_text(json.dumps(outer))
            try:
                verify(p,replay=False)
            except (ValueError,KeyError,OSError):
                pass
            else:
                raise RuntimeError('accepted actual corruption: '+case)
    return cases

if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--integrity-only',action='store_true')
    parser.add_argument('--self-test',action='store_true')
    args=parser.parse_args()
    root=Path(__file__).resolve().parent
    result=verify(root,replay=not args.integrity_only)
    if args.self_test:
        result['actual_corruptions_rejected']=corruption_controls(root)
    print(json.dumps(result,indent=2,sort_keys=True))
