#!/usr/bin/env python3
"""Replay preserved158 control logic against repaired canonical helpers, new outputs only."""
import hashlib
from pathlib import Path
import sys
HERE=Path(__file__).resolve().parent
AUDIT=HERE.parent
source=AUDIT/'publication_operations_preparation/prior_review_02_full/publication_operations_preparation/offline_controls.py'
code=source.read_text()
if hashlib.sha256(source.read_bytes()).hexdigest() != next(
        e['sha256'] for e in __import__('json').loads((AUDIT/'publication_operations_preparation/MANIFEST.json').read_text())['files']
        if e['path']=='publication_operations_preparation/offline_controls.py'):
    raise RuntimeError('Historical158-control source binding differs')
output=HERE/('regression_optimized' if sys.flags.optimize else 'regression_normal')
output.mkdir(exist_ok=True)
old='HERE=Path(__file__).resolve().parent\nAUDIT=HERE.parent'
if code.count(old)!=1:raise RuntimeError('Unexpected old control entrypoint')
code=code.replace(old,'HERE=Path('+repr(str(output))+')\nAUDIT=Path('+repr(str(AUDIT))+')')
exec(compile(code,str(source),'exec'),{'__name__':'__main__','__file__':str(source)})
