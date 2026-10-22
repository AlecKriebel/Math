#!/usr/bin/env python3
"""Isolated actual proposed/frozen bodies and the unchanged synthetic pipeline."""
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
FROZEN=HERE/'pre_bibliographic_binding'
PROPOSED=HERE/'proposed'
PRESERVATION_FILE=HERE/'INPUT_PRESERVATION.json'
ROOT=AUDIT.parents[1]
SCRATCH=ROOT/'private/pr0280_bibliographic_context_repair'
SCRATCH.mkdir(parents=True,exist_ok=True)
ATTEMPTS=[]


def check(condition,message):
    if not condition:raise RuntimeError('CONTROL CHECK FAILED: '+message)
def forbidden(*args,**kwargs):
    ATTEMPTS.append(True);raise RuntimeError('ACTUAL PROVIDER ACCESS FORBIDDEN')
def write(path,value):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
def implementation(frozen=False):
    entries={e['path']:e for e in json.loads(PRESERVATION_FILE.read_text())['files']}
    for name in ['ops_binding','prepublication_check','publication_live_gates','verify_published_files','record_publication_ledger']:
        source=(FROZEN if frozen else PROPOSED)/(name+'.py')
        if frozen:check(hashlib.sha256(source.read_bytes()).hexdigest()==entries[name+'.py']['sha256'],'exact frozen390 source')
        module=types.ModuleType(name);module.__file__=str(AUDIT/(name+'.py'));sys.modules[name]=module
        exec(compile(source.read_bytes(),str(source),'exec'),module.__dict__)
    return tuple(sys.modules[n] for n in ['ops_binding','prepublication_check','publication_live_gates','verify_published_files','record_publication_ledger'])


source=FROZEN/'ops_doi_identity_repair_20261021/integrated_controls.py'
tree=ast.parse(source.read_text())
exec(compile(ast.Module(body=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='run_pipeline'],type_ignores=[]),str(source),'exec'),globals())
