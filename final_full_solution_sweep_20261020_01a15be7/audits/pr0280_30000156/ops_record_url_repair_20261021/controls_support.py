#!/usr/bin/env python3
"""Actual frozen/current helper loading; scratch-only full pipeline fixture."""
import ast
import copy
from contextlib import ExitStack
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import types
from unittest.mock import patch
HERE=Path(__file__).resolve().parent
AUDIT=HERE.parent
FROZEN=HERE/'pre_record_url_binding'
ATTEMPTS=[]


def check(value,message):
    if not value:raise RuntimeError('CONTROL CHECK FAILED: '+message)


def forbidden(*args,**kwargs):
    ATTEMPTS.append(True)
    raise RuntimeError('ACTUAL PROVIDER ACCESS FORBIDDEN')


def write(path,value):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')


def implementation(frozen):
    entries={e['path']:e for e in json.loads((HERE/'INPUT_PRESERVATION.json').read_text())['files']}
    for name in ['ops_binding','prepublication_check','publication_live_gates','verify_published_files','record_publication_ledger']:
        path=(FROZEN if frozen else AUDIT)/(name+'.py')
        if frozen:check(hashlib.sha256(path.read_bytes()).hexdigest()==entries[name+'.py']['sha256'],'frozen exact code')
        module=types.ModuleType(name);module.__file__=str(AUDIT/(name+'.py'));sys.modules[name]=module
        exec(compile(path.read_bytes(),str(path),'exec'),module.__dict__)
    return tuple(sys.modules[n] for n in ['ops_binding','prepublication_check','publication_live_gates','verify_published_files','record_publication_ledger'])

# Reuse the full fixture with actual gather/account_search/reconcile/append
# bodies. Only test fixture functions are extracted; no old main or outputs run.
source=FROZEN/'ops_doi_identity_repair_20261021/integrated_controls.py'
tree=ast.parse(source.read_text())
exec(compile(ast.Module(body=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='run_pipeline'],type_ignores=[]),str(source),'exec'),globals())
