#!/usr/bin/env python3
"""Destructive negative controls on temporary copies only."""
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent

def main():
    if not __debug__ or sys.flags.optimize:
        raise RuntimeError('Assertions must remain enabled')
    sys.dont_write_bytecode = True
    spec = importlib.util.spec_from_file_location('contact_publication_verifier',ROOT/'verify_publication.py')
    verifier = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(verifier)
    verifier.integrity(ROOT)
    tests = {}
    with tempfile.TemporaryDirectory(prefix='contact-process-negative-') as t:
        for name in ('altered_file','extra_file','extra_directory','missing_file','symlink','corrupted_archive'):
            copy = Path(t)/name
            shutil.copytree(ROOT,copy)
            if name == 'altered_file':
                with (copy/'author/PROOF.md').open('ab') as f: f.write(b'\nTAMPER\n')
            elif name == 'extra_file': (copy/'extra.txt').write_text('unlisted')
            elif name == 'extra_directory': (copy/'extra').mkdir()
            elif name == 'missing_file': (copy/'audit/CORRECTIONS.md').unlink()
            elif name == 'symlink':
                (copy/'author/PROOF.md').unlink()
                (copy/'author/PROOF.md').symlink_to(ROOT/'author/PROOF.md')
            else:
                f = copy/'frozen_archives/contact_process_30004594_authored.zip.b64'
                f.write_bytes(b'A'+f.read_bytes()[1:])
            try:
                verifier.integrity(copy)
            except (AssertionError,ValueError,FileNotFoundError):
                tests[name] = 'REJECTED'
            else:
                raise AssertionError('Negative control accepted: '+name)
    env=dict(os.environ);env['PYTHONDONTWRITEBYTECODE']='1'
    proc=subprocess.run([sys.executable,'-O','-B',str(ROOT/'verify_publication.py')],env=env,capture_output=True,text=True)
    assert proc.returncode != 0 and 'Assertions must be enabled' in proc.stderr
    tests['optimized_python'] = 'REJECTED'
    verifier.integrity(ROOT)
    print(json.dumps({'status':'PASS','negative_controls':tests,'packet_unchanged':True},indent=2,sort_keys=True))

if __name__ == '__main__':
    main()
