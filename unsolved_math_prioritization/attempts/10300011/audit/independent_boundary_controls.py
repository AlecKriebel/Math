#!/usr/bin/env python3
"""Exercise an externally authenticated bootstrap on isolated mutated copies."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

MANIFEST = '93febcc968a3b244c9cdee7af00fb1ce24519ef03582039cd6b68c2733aab3ae'
BOOTSTRAP = '7ad7d12073e58e60d33966770689af7dbe7193adfcb5cde38b63f41bc30133c5'


def need(ok, message):
    if not ok:
        raise ValueError(message)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def inventory(root):
    return {p.relative_to(root).as_posix(): (p.stat().st_size, sha(p)) for p in sorted(root.rglob('*')) if p.is_file()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--subject', required=True, type=Path)
    args = parser.parse_args()
    root = args.subject.resolve()
    need(sha(root/'MANIFEST.json') == MANIFEST and sha(root/'bootstrap.py') == BOOTSTRAP, 'external author pins failed')
    before = inventory(root)
    script = root/'bootstrap.py'
    mutations = [
        'proof_one_byte', 'verifier_marker', 'bootstrap_change', 'manifest_duplicate',
        'manifest_path_escape', 'manifest_boolean_size', 'coordinated_forgery',
        'missing_claims', 'added_file', 'added_directory', 'payload_symlink',
        'directory_symlink', 'root_symlink', 'fifo', 'truncated_manifest',
    ]
    accepted = rejected = 0
    outcomes = []
    with tempfile.TemporaryDirectory(prefix='independent-boundary-') as temp:
        temp = Path(temp)
        for flags in ([], ['-O'], ['-OO']):
            for case in ['exact_copy'] + mutations:
                candidate = temp/('candidate-' + str(accepted + rejected))
                shutil.copytree(root, candidate)
                marker = temp/'UNEXPECTED_EXECUTION'
                subject = candidate
                if case == 'proof_one_byte':
                    p = candidate/'author/PROOF.md'; p.write_bytes(p.read_bytes() + b'\n')
                elif case == 'verifier_marker':
                    (candidate/'author/verify.py').write_text('from pathlib import Path\nPath('+repr(str(marker))+').write_text("executed")\n')
                elif case == 'bootstrap_change':
                    p = candidate/'bootstrap.py'; p.write_bytes(p.read_bytes()+b'\n')
                elif case == 'manifest_duplicate':
                    p = candidate/'MANIFEST.json'; p.write_text(p.read_text().rstrip()[:-1]+',"problem_id":10300011}\n')
                elif case in ('manifest_path_escape', 'manifest_boolean_size', 'coordinated_forgery'):
                    p = candidate/'MANIFEST.json'; obj = json.loads(p.read_text())
                    if case == 'manifest_path_escape':
                        obj['files']['author/../../outside'] = {'bytes':0,'sha256':'0'*64}
                    elif case == 'manifest_boolean_size':
                        obj['files']['author/CLAIMS.json']['bytes'] = True
                    else:
                        claim = candidate/'author/CLAIMS.json'; c = json.loads(claim.read_text()); c['status']='solved'; claim.write_text(json.dumps(c))
                        obj['files']['author/CLAIMS.json'] = {'bytes':claim.stat().st_size,'sha256':sha(claim)}
                    p.write_text(json.dumps(obj))
                elif case == 'missing_claims':
                    (candidate/'author/CLAIMS.json').unlink()
                elif case == 'added_file':
                    (candidate/'surprise.txt').write_text('unexpected')
                elif case == 'added_directory':
                    (candidate/'empty').mkdir()
                elif case == 'payload_symlink':
                    p = candidate/'author/CLAIMS.json'; p.unlink(); p.symlink_to(root/'author/CLAIMS.json')
                elif case == 'directory_symlink':
                    (candidate/'linked').symlink_to(root/'author', target_is_directory=True)
                elif case == 'root_symlink':
                    subject = temp/('root-link-' + str(accepted+rejected)); subject.symlink_to(candidate, target_is_directory=True)
                elif case == 'fifo':
                    os.mkfifo(candidate/'unexpected_fifo')
                elif case == 'truncated_manifest':
                    (candidate/'MANIFEST.json').write_bytes(b'{')
                result = subprocess.run([sys.executable,'-I','-S','-B',*flags,str(script),'--root',str(subject)],capture_output=True,text=True,timeout=90)
                if case == 'exact_copy':
                    need(result.returncode == 0 and not result.stderr, 'relocated exact copy failed')
                    need(json.loads(result.stdout)['status'] == 'PASS_AUTHENTICATED_AUTHOR_BOUNDARY', 'unexpected positive output')
                    accepted += 1
                else:
                    need(result.returncode != 0 and not result.stdout and result.stderr, 'mutation accepted: '+case)
                    rejected += 1
                need(not marker.exists(), 'untrusted verifier executed before authentication')
                outcomes.append({'mode':' '.join(flags) or 'normal','case':case,'accepted':case=='exact_copy'})
    need(inventory(root) == before, 'original author bytes changed')
    print(json.dumps({'status':'PASS_INDEPENDENT_BOUNDARY_CONTROLS','accepted_exact_copies':accepted,
                      'rejected_mutated_copies':rejected,'untrusted_marker_executed':False,
                      'original_unchanged':True,'cases':outcomes},sort_keys=True))


if __name__ == '__main__':
    try:
        main()
    except (ValueError, OSError, KeyError, TypeError, subprocess.SubprocessError) as exc:
        print('FAIL: '+str(exc),file=sys.stderr)
        sys.exit(2)
