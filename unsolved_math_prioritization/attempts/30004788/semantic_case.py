#!/usr/bin/env python3
"""Deterministic error-only entry point; mathematical checker bytes are unchanged."""
import sys
from pathlib import Path
if len(sys.argv)!=3 or sys.argv[1] not in ('check_exact.py','independent_exact.py'):
    raise SystemExit('REJECT: checker and mutation required')
script,mutation=sys.argv[1:]
raw=(Path(__file__).absolute().parent/script).read_bytes()
sys.argv=[script,'--mutate',mutation]
try:
    exec(compile(raw,'<'+script+'>','exec'),{'__name__':'__main__'})
except RuntimeError as error:
    print('SEMANTIC_REJECTION: '+str(error),file=sys.stderr)
    sys.exit(1)
