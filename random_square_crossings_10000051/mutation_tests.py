"""Fail-closed controls. Supply the same externally trusted publication pin.
Runs normal, -O and -OO entry points; all mutations occur in temporary copies.
"""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


def need(value, reason):
    if not value:
        raise ValueError(reason)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--manifest-sha256', required=True)
    p.add_argument('--verifier-sha256', required=True)
    a = p.parse_args()
    root = Path(__file__).resolve().parent
    need(digest((root/'PUBLIC_MANIFEST.json').read_bytes()) == a.manifest_sha256,
         'untrusted original manifest')
    # Use the unchanged wrapper outside the mutated trees, avoiding execution of mutated code.
    wrapper = root/'verify_publication.py'
    def call(packet, flags=(), pin=a.manifest_sha256, script=wrapper):
        need(not script.is_symlink() and digest(script.read_bytes()) == a.verifier_sha256,
             'external verifier bootstrap pin mismatch')
        return subprocess.run([sys.executable, '-I', '-B', *flags, str(script),
                               '--packet', str(packet), '--manifest-sha256', pin],
                              capture_output=True, text=True, timeout=180)
    records = []
    for flags in [(), ('-O',), ('-OO',)]:
        r = call(root, flags)
        need(r.returncode == 0, 'valid baseline rejected: '+r.stderr)
        for case in ['original_byte', 'audit_byte', 'corrected_byte', 'missing_file',
                     'unexpected_file', 'symlink', 'manifest_byte', 'manifest_refreeze',
                     'incorrect_external_pin', 'empty_directory', 'root_symlink',
                     'duplicate_manifest_key', 'verifier_bootstrap']:
            with tempfile.TemporaryDirectory(prefix='square-crossing-mutation-') as td:
                dest = Path(td)/'packet'; shutil.copytree(root, dest)
                if case in ['original_byte', 'audit_byte', 'corrected_byte']:
                    path = {'original_byte': 'original/CANDIDATE.md',
                            'audit_byte': 'audit/AUDIT.md',
                            'corrected_byte': 'corrected/checks/verify_rational.py'}[case]
                    with (dest/path).open('ab') as f: f.write(b'\n')
                elif case == 'missing_file':
                    (dest/'corrected/checks/example_tiling.json').unlink()
                elif case == 'unexpected_file':
                    (dest/'unexpected.txt').write_text('unmanifested control\n')
                elif case == 'symlink':
                    target = dest/'corrected/checks/example_tiling.json'
                    target.unlink(); target.symlink_to('../../original/checks/example_tiling.json')
                elif case == 'manifest_byte':
                    with (dest/'PUBLIC_MANIFEST.json').open('ab') as f: f.write(b' ')
                elif case == 'manifest_refreeze':
                    target = dest/'corrected/CANDIDATE.md'
                    with target.open('ab') as f: f.write(b'\n')
                    mp = dest/'PUBLIC_MANIFEST.json'; m = json.loads(mp.read_bytes())
                    for e in m['files']:
                        if e['path'] == 'corrected/CANDIDATE.md':
                            e['bytes'] = len(target.read_bytes()); e['sha256'] = digest(target.read_bytes())
                    mp.write_text(json.dumps(m, indent=2)+'\n')
                if case == 'empty_directory':
                    (dest/'unexpected_empty_directory').mkdir()
                elif case == 'root_symlink':
                    link = Path(td)/'root_link'; link.symlink_to(dest, target_is_directory=True)
                    dest = link
                elif case == 'duplicate_manifest_key':
                    mp = dest/'PUBLIC_MANIFEST.json'
                    mp.write_bytes(mp.read_bytes().replace(b'{', b'{"problem_id": 10000051,', 1))
                elif case == 'verifier_bootstrap':
                    malicious = Path(td)/'altered_verifier.py'
                    malicious.write_text("raise SystemExit('MUTATED VERIFIER MUST NOT RUN')\n")
                    try:
                        call(dest, flags, script=malicious)
                    except ValueError as e:
                        need(str(e) == 'external verifier bootstrap pin mismatch', 'wrong bootstrap rejection')
                    else:
                        raise ValueError('mutated verifier executed')
                    records.append({'case': case, 'mode': flags[0] if flags else 'normal', 'rejected': True})
                    continue
                pin = ('0'*64 if case == 'incorrect_external_pin' else
                       digest((dest/'PUBLIC_MANIFEST.json').read_bytes()) if case == 'duplicate_manifest_key'
                       else a.manifest_sha256)
                r = call(dest, flags, pin)
                need(r.returncode != 0, 'mutation accepted: '+case)
                records.append({'case': case, 'mode': flags[0] if flags else 'normal', 'rejected': True})
    print(json.dumps({'status': 'PASS', 'baseline_modes': 3, 'negative_controls': records}, indent=2))


if __name__ == '__main__':
    main()
