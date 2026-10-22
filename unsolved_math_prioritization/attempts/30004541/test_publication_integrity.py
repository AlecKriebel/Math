#!/usr/bin/env python3
"""Reject altered, missing, unexpected, and symlinked packet members."""
from pathlib import Path
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
ROOT = Path(__file__).resolve().parent

def invoke(root):
    return subprocess.run([sys.executable, str(root/'verify_publication.py')],
                          text=True, capture_output=True, cwd='/tmp')

def rehash(root, name):
    path = root/'PUBLICATION_MANIFEST.json'
    m = json.loads(path.read_text())
    data = (root/name).read_bytes()
    m['files'][name] = {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}
    path.write_text(json.dumps(m, indent=2)+'\n')

with tempfile.TemporaryDirectory(prefix='derrida-negative-controls-') as temp:
    dest = Path(temp)/'relocated packet'
    shutil.copytree(ROOT, dest)
    positive = invoke(dest)
    assert positive.returncode == 0, positive.stderr
    cases = ['changed-proof', 'missing-proof', 'unexpected-file', 'unexpected-empty-dir',
             'symlink', 'changed-freeze-with-rehashed-outer-manifest', 'changed-audit-with-rehashed-outer-manifest']
    for name in cases:
        shutil.rmtree(dest)
        shutil.copytree(ROOT, dest)
        proof = dest/'author/PROOFS.md'
        if name == 'changed-proof': proof.write_bytes(proof.read_bytes()+b'changed\n')
        elif name == 'missing-proof': proof.unlink()
        elif name == 'unexpected-file': (dest/'unexpected.txt').write_text('unexpected')
        elif name == 'unexpected-empty-dir': (dest/'unexpected-dir').mkdir()
        elif name == 'symlink':
            proof.unlink(); proof.symlink_to(ROOT/'author/PROOFS.md')
        elif name == 'changed-freeze-with-rehashed-outer-manifest':
            fn = 'frozen_archives/DERRIDA_30004541_AUTHOR_SAFE_FREEZE.zip.b64'
            p = dest/fn; b = p.read_bytes(); p.write_bytes(b'A'+b[1:]); rehash(dest, fn)
        else:
            fn = 'audit/AUDIT_REPORT.md'; p = dest/fn; p.write_bytes(p.read_bytes()+b'changed\n'); rehash(dest, fn)
        result = invoke(dest)
        assert result.returncode != 0, f'Failed to reject {name}'
    print(json.dumps({'status': 'PASS', 'relocated_positive_replay': json.loads(positive.stdout),
                      'negative_controls_rejected': cases}, indent=2))
