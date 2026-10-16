"""Reproduce two output-path attacks on disposable copies, never frozen input.

The currently reviewed builder accepts both and changes its closed input. A
repaired builder should reject both before writing and preserve its input.
"""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import shutil
import subprocess
import sys
import zipfile

ROOT = Path(__file__).resolve().parent
PACKAGE = ROOT.parent / 'preprint'


def inventory(p):
    return {x.relative_to(p).as_posix(): hashlib.sha256(x.read_bytes()).hexdigest()
            for x in p.rglob('*') if x.is_file() and not x.is_symlink()}


def main():
    scratch = ROOT / 'tmp' / 'output_path_attacks'
    scratch.mkdir(parents=True, exist_ok=False)
    results = []
    try:
        for case in ['output_parent_symlink', 'receipt_symlink']:
            work = scratch / case
            source = work / 'input'
            out = work / 'out'
            with zipfile.ZipFile(PACKAGE / 'source-and-verification.zip') as z:
                for name in z.namelist():
                    if Path(name).is_absolute() or '..' in Path(name).parts:
                        raise ValueError('Unsafe source ZIP path')
                z.extractall(source)
            out.mkdir()
            before = inventory(source)
            if case == 'output_parent_symlink':
                (out / 'output').mkdir()
                (out / 'output' / 'pdf').symlink_to(source, target_is_directory=True)
            else:
                (out / 'PACKAGE_INVENTORY.json').symlink_to(source / 'paper.tex')
            cmd = [sys.executable, '-O', '-B', str(source / 'build_package.py'),
                   '--output-dir', str(out), '--pdf', str(PACKAGE / 'output/pdf/paper.pdf')]
            run = subprocess.run(cmd, cwd='/', capture_output=True, text=True, timeout=60)
            after = inventory(source)
            results.append({'case': case, 'cmd': cmd, 'returncode': run.returncode,
                            'closed_input_unchanged': before == after,
                            'added_paths': sorted(set(after) - set(before)),
                            'changed_paths': sorted(n for n in before if n in after and before[n] != after[n]),
                            'stderr': run.stderr})
            shutil.rmtree(work)
    finally:
        shutil.rmtree(scratch)
    receipt = {'checked_at_utc': datetime.now(timezone.utc).isoformat(),
               'status': 'PASS_REJECTION_AND_PRESERVATION' if all(r['closed_input_unchanged'] and r['returncode'] != 0 for r in results) else 'FAIL_CLOSED_INPUT_PRESERVATION',
               'cases': results,
               'scope': 'Two physical attacks exclusively on this review disposable copies; no frozen publication byte modified.'}
    (ROOT / 'OUTPUT_SYMLINK_ATTACK.json').write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps(receipt, indent=2))


if __name__ == '__main__':
    main()
