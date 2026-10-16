#!/usr/bin/env python3
"""Save actual full-package replays in four outer optimization modes."""
import argparse
import json
import os
from pathlib import Path
import subprocess


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--python', type=Path, required=True)
    args = ap.parse_args()
    p = Path(__file__).resolve().parent
    pin = json.loads((p/'BUILD_RECEIPT.json').read_text())['manifest_sha256']
    for label, flags, optimize in [('normal', [], None), ('O', ['-O'], None),
                                   ('OO', ['-OO'], None), ('env2', [], '2')]:
        env = dict(os.environ)
        env.pop('PYTHONOPTIMIZE', None)
        if optimize is not None:
            env['PYTHONOPTIMIZE'] = optimize
        proc = subprocess.run([str(args.python), *flags, str(p/'tmp/bundle/verify_package.py'),
                '--expected-manifest', pin, '--pdf', str(p/'output/pdf/note.pdf'),
                '--workdir', str(p/'tmp/replay')], env=env, capture_output=True, text=True,
                timeout=1800)
        (p/('PACKAGE_REPLAY_'+label+'.stdout')).write_text(proc.stdout)
        (p/('PACKAGE_REPLAY_'+label+'.stderr')).write_text(proc.stderr)
        if proc.returncode != 0:
            raise RuntimeError(label+' replay failed:\n'+proc.stderr)
        result = json.loads(proc.stdout)
        (p/('PACKAGE_REPLAY_'+label+'.json')).write_text(json.dumps(result, indent=2)+'\n')
        print(label, {k: result[k] for k in ['status', 'fresh_exact_predicates',
                    'fresh_floating_diagnostics', 'worker_optimization']}, flush=True)
    same = len({(p/('PACKAGE_REPLAY_'+m+'.json')).read_bytes()
                for m in ['normal', 'O', 'OO', 'env2']}) == 1
    print('All four results identical:', same)


if __name__ == '__main__':
    main()
