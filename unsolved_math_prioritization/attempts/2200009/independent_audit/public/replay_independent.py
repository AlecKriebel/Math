#!/usr/bin/env python3
"""Replay the independent diagnostic in a genuinely nonroot read-only copy."""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import hashlib
import json
import os
import subprocess
import sys
import tempfile


def main():
    if os.getuid() == 0 or os.geteuid() == 0:
        raise ValueError('genuinely nonroot execution required')
    original = Path(__file__).resolve().with_name('independent_checks.py').read_bytes()
    with tempfile.TemporaryDirectory(prefix='mesh-independent-') as td:
        root = Path(td)
        readonly = root/'readonly'
        readonly.mkdir()
        script = readonly/'independent_checks.py'
        script.write_bytes(original)
        script.chmod(0o444)
        readonly.chmod(0o555)
        denials = []
        try:
            for label, action in [('create', lambda:(readonly/'probe').write_text('no')),
                                  ('overwrite',lambda:script.open('wb'))]:
                try:
                    handle = action()
                except PermissionError:
                    denials.append(label)
                else:
                    if hasattr(handle,'close'):
                        handle.close()
                    raise ValueError('read-only probe succeeded')
            def run(mode):
                flags = [] if mode == 'normal' else [mode]
                p = subprocess.run([sys.executable,'-I','-S','-B',*flags,str(script)],
                                   cwd=root,capture_output=True,timeout=600)
                if p.returncode != 0:
                    raise ValueError(mode+': '+p.stderr.decode('utf-8','replace'))
                return p.stdout
            modes=['normal','-O','-OO']
            with ThreadPoolExecutor(max_workers=3) as pool:
                outputs=list(pool.map(run,modes))
            if any(output != outputs[0] for output in outputs):
                raise ValueError('mode-dependent independent output')
            if script.read_bytes()!=original or {p.name for p in readonly.iterdir()}!={'independent_checks.py'}:
                raise ValueError('read-only bytes or inventory changed')
            result=json.loads(outputs[0])
            if result['status']!='PASS':
                raise ValueError('failed independent result')
            return {'schema':'mesh-preserver-independent-replay-v1','status':'PASS',
                    'uid':os.getuid(),'euid':os.geteuid(),'modes':modes,
                    'read_only_write_denials':denials,'bytes_unchanged':True,
                    'script_sha256':hashlib.sha256(original).hexdigest(),
                    'output_sha256':hashlib.sha256(outputs[0]).hexdigest(),
                    'diagnostics':result}
        finally:
            readonly.chmod(0o755)
            script.chmod(0o644)


if __name__=='__main__':
    print(json.dumps(main(),sort_keys=True,indent=2))
