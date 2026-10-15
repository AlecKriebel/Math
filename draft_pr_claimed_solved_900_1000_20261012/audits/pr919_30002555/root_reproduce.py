"""Read-only root replay of the externally pinned original completed candidate."""
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import subprocess

A = Path(__file__).resolve().parent
ROOT = A.parents[2]
O = A / 'original/unsolved_math_prioritization/attempts/30002555'
PYTHON = ROOT / 'draft_pr_claimed_solved_900_1000_20261012/audits/pr906_30006419/reviews/computation_family/tmp/venv/bin/python'
MANIFEST = 'a7f24f30d76ca7e53da932dfc1f19deac67f13a675742175274e30ca767832f8'
VERIFIER = '07ed9f87820a8cbaa10deec92fbf14b68a61e969e8bf849d8c5484eac4aa5374'


def require(value, label):
    if not value:
        raise RuntimeError(label)


def main():
    tmp = A / 'tmp'
    tmp.mkdir(exist_ok=True)
    env = dict(os.environ, TMPDIR=str(tmp))
    snap = json.loads((A / 'ORIGINAL_SNAPSHOT.json').read_text())
    for name, pin in snap['files'].items():
        require(hashlib.sha256((A / 'original' / name).read_bytes()).hexdigest() == pin,
                'Original snapshot drift')
    require(hashlib.sha256((O / 'VERIFY_PUBLICATION.py').read_bytes()).hexdigest() == VERIFIER,
            'External verifier anchor mismatch')
    require(hashlib.sha256((O / 'PUBLICATION_MANIFEST.json').read_bytes()).hexdigest() == MANIFEST,
            'External manifest anchor mismatch')
    modes = [('normal', [], None), ('O', ['-O'], None), ('OO', ['-OO'], None),
             ('env2', [], '2')]
    receipts = []
    outputs = []
    for name, flags, poison in modes:
        current_env = dict(env)
        if poison:
            current_env['PYTHONOPTIMIZE'] = poison
        command = [str(PYTHON), '-B', *flags, str(O / 'VERIFY_PUBLICATION.py'),
                   '--expected-manifest', MANIFEST]
        result = subprocess.run(command, env=current_env, capture_output=True, timeout=180)
        require(result.returncode == 0, 'Original full replay failed: ' + result.stderr.decode(errors='replace'))
        parsed = json.loads(result.stdout)
        require(parsed['status'] == 'PASS' and len(parsed['replays']) == 15,
                'Wrong full replay scope')
        outputs.append(result.stdout)
        (tmp / ('root_replay_' + name + '.json')).write_bytes(result.stdout)
        receipts.append({'mode': name, 'status': 'PASS',
                         'output_sha256': hashlib.sha256(result.stdout).hexdigest(),
                         'nested_replays': len(parsed['replays'])})
    require(len(set(outputs)) == 1, 'Original outputs differ among four modes')
    mutation = subprocess.run([str(PYTHON), '-I', '-B', str(O / 'TEST_MUTATIONS.py'),
                               '--expected-manifest', MANIFEST, '--expected-verifier', VERIFIER],
                              env=env, capture_output=True, timeout=180)
    require(mutation.returncode == 0, 'Original mutation suite failed')
    require(mutation.stdout == (O / 'MUTATION_RESULTS.json').read_bytes(),
            'Original mutation receipt differs')
    controls = json.loads(mutation.stdout)
    for name, pin in snap['files'].items():
        require(hashlib.sha256((A / 'original' / name).read_bytes()).hexdigest() == pin,
                'Original snapshot changed after replay')
    out = {'utc': datetime.now(timezone.utc).isoformat(), 'status': 'PASS',
           'original_head': snap['head'], 'original_files_unchanged': 27,
           'manifest_sha256': MANIFEST, 'verifier_sha256': VERIFIER,
           'runtime': subprocess.run([str(PYTHON), '--version'], capture_output=True, text=True, check=True).stdout.strip(),
           'four_full_modes': receipts, 'four_outputs_identical': True,
           'mutation_classes': controls['mutation_classes'], 'mutation_rejections': controls['rejections'],
           'positive_baselines': controls['positive_baselines'],
           'environment_controls': controls['ordinary_child_environment_controls'],
           'mutation_frozen_receipt_byte_identical': True,
           'limits': 'Finite arithmetic and fixed original-byte integrity; not a mathematical proof, sandbox, human review or priority certificate.'}
    (A / 'ROOT_ORIGINAL_REPRODUCTION.json').write_text(json.dumps(out, indent=2) + '\n')
    print(json.dumps(out, indent=2))


if __name__ == '__main__':
    main()
