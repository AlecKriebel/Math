#!/usr/bin/env python3
"""Acceptance controls on temporary copies; no changes to the reviewed package."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


def main():
    source = Path(__file__).absolute().parent
    records = []
    cases = ['baseline','relocation','source','proof','result','missing','extra','cache',
             'symlink','fifo','schema','repinned_false_result']
    with tempfile.TemporaryDirectory(prefix='young-tops-second-controls-') as temporary:
        root = Path(temporary)
        for optimized in (False,True):
            for case in cases:
                target = root / str(optimized) / case / 'path with spaces'
                shutil.copytree(source, target)
                if case in ('source','proof','result'):
                    name = {'source':'weight_graph_check.py','proof':'SECOND_REVIEW.md',
                            'result':'weight_graph_results.json'}[case]
                    file = target / name
                    file.write_bytes(file.read_bytes() + b' ')
                elif case == 'missing':
                    (target/'weight_graph_results.json').unlink()
                elif case == 'extra':
                    (target/'extra').write_bytes(b'')
                elif case == 'cache':
                    (target/'__pycache__').mkdir()
                elif case in ('symlink','fifo'):
                    file = target/'weight_graph_results.json'
                    file.unlink()
                    if case == 'symlink':
                        file.symlink_to('README.md')
                    else:
                        os.mkfifo(file)
                elif case == 'schema':
                    file = target/'manifest.json'
                    data = json.loads(file.read_text()); data['schema'] = 'wrong'
                    file.write_text(json.dumps(data))
                elif case == 'repinned_false_result':
                    file = target/'weight_graph_results.json'
                    data = json.loads(file.read_text()); data['family'][0]['socle_dimension'] = 3
                    file.write_text(json.dumps(data))
                    manifest_file = target/'manifest.json'
                    manifest = json.loads(manifest_file.read_text())
                    raw = file.read_bytes()
                    manifest['files'][file.name] = {'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}
                    manifest_file.write_text(json.dumps(manifest))
                command = [sys.executable,'-B'] + (['-O'] if optimized else [])
                completed = subprocess.run(command + [str(target/'verify_second_review.py')],
                                           cwd=root,text=True,capture_output=True,timeout=30)
                positive = case in ('baseline','relocation')
                passed = completed.returncode == 0 if positive else (completed.returncode != 0 and 'REJECT:' in completed.stderr)
                if not passed:
                    raise RuntimeError(case + ': ' + completed.stdout + completed.stderr)
                row = {'case':case,'optimized':optimized,'passed':True,'returncode':completed.returncode}
                if not positive:
                    row['rejection'] = completed.stderr.strip()
                records.append(row)
    print(json.dumps({'status':'PASS','checks':records},sort_keys=True,indent=2))


if __name__ == '__main__':
    main()
