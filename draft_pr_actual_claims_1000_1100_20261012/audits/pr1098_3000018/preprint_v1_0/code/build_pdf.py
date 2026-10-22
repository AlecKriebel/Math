"""Compile in a newly created external directory; every child output stays there."""
import sys
sys.dont_write_bytecode = True
import argparse
import json
import os
import shutil
import subprocess
from common import ROOT, archive_bytes, digest, fresh, regular

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--out-dir', required=True)
    a = p.parse_args()
    out = fresh(a.out_dir)
    archive_bytes()  # Authenticate all payload and bootstrap before authoring.
    source = regular(ROOT/'paper.tex').read_bytes()
    out.mkdir()  # A fresh directory prevents compiler overwrites of any prior file.
    (out/'paper.tex').write_bytes(source)
    cache = out/'cache'
    cache.mkdir()
    env = dict(os.environ)
    env['XDG_CACHE_HOME'] = str(cache)
    env['TMPDIR'] = str(out)
    env['SOURCE_DATE_EPOCH'] = '1792108800'
    env['FORCE_SOURCE_DATE'] = '1'
    # The local installed bundle cache is read; all created compiler files use out.
    command = ['tectonic', '--untrusted', '--outdir', str(out),
               '--keep-logs', '--keep-intermediates', str(out/'paper.tex')]
    completed = subprocess.run(command, cwd=out, env=env, capture_output=True)
    (out/'compiler.stdout').write_bytes(completed.stdout)
    (out/'compiler.stderr').write_bytes(completed.stderr)
    if completed.returncode:
        raise RuntimeError('Tectonic failed; inspect files in '+str(out))
    log = regular(out/'paper.log').read_text(errors='replace')
    if 'Overfull' in log or 'LaTeX Warning: Reference' in log or 'undefined' in log:
        raise ValueError('overfull box or undefined reference; inspect '+str(out))
    raw = regular(out/'paper.pdf').read_bytes()
    print(json.dumps({'bytes':len(raw),'sha256':digest(raw)}))
