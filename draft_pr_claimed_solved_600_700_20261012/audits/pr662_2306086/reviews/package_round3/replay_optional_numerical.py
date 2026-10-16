#!/usr/bin/env python3
"""Replay the exact published archive in review-local temporary copies only."""
import datetime
import hashlib
import json
import os
from pathlib import Path
import tempfile
import types
import zipfile

HERE = Path(__file__).absolute().parent
A = HERE.parents[1]
data = (A / 'publication/real_schlicht_verification.zip').read_bytes()
if hashlib.sha256(data).hexdigest() != '945c5e52a136bd0187d51661140b617965c064c880628bdbeff3324516b9bc04':
    raise ValueError('archive drift')
with tempfile.TemporaryDirectory(prefix='optional-numerical-', dir=HERE / 'tmp') as temporary:
    root = Path(temporary)
    # Paths were strictly checked by publication_inputs/archive_binding and
    # are checked again by the extracted verifier before any code execution.
    with zipfile.ZipFile(A / 'publication/real_schlicht_verification.zip') as archive:
        archive.extractall(root)
    module = types.ModuleType('_round3_verifier')
    module.__file__ = str(root / 'verify_package.py')
    exec(compile((root / 'verify_package.py').read_bytes(), module.__file__, 'exec'), module.__dict__)
    before = module.verify(root)
    result = module.replay(root, numerical=True)
    if module.verify(root) != before:
        raise ValueError('packet changed')
output = {'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
          'status': 'PASS', 'archive_sha256': hashlib.sha256(data).hexdigest(),
          'numerical_certification': False, 'optimizer_rerun': False,
          'temporary_copies_only': True, 'result': result}
(HERE / 'OPTIONAL_NUMERICAL_REPLAY.json').write_text(json.dumps(output, indent=2) + '\n')
print(json.dumps({'status': 'PASS', 'numerical_certification': False, 'optimizer_rerun': False}))
