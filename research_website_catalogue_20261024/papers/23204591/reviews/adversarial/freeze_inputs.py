#!/usr/bin/env python3
"""Opaque read-only intake of original source and qualified existing core.
Only owned inputs/blobs and the owned manifest are written. No source helper,
programme, results or opinion is executed or interpreted here.
"""
from pathlib import Path
import datetime
import hashlib
import json

E=Path(__file__).resolve().parent
P=E.parents[3]
S=P/'papers/23204591/sources'
if (E/'PROTECTED_INPUTS.json').exists():raise ValueError('refuse intake overwrite')
source_files=[];source_dirs=[]
for p in sorted(S.rglob('*')):
    if p.is_symlink():raise ValueError('source symlink')
    if p.is_file():source_files.append(p)
    elif p.is_dir():source_dirs.append(p.relative_to(S).as_posix())
    else:raise ValueError('nonregular source')
core=sorted((P/'scripts').glob('*.py'))+[P/'verification/final-content-check.py']
if len(core)!=18:raise ValueError('qualified existing core must be17original plus authorized405b helper')
rows=[]
for p in source_files+core:
    b=p.read_bytes();h=hashlib.sha256(b).hexdigest();copy=E/'inputs/blobs'/h
    if copy.exists():
        if copy.read_bytes()!=b:raise ValueError('blob collision')
    else:copy.write_bytes(b)
    rows.append({'path':str(p),'copy':copy.relative_to(E).as_posix(),'bytes':len(b),'SHA256':h})
manifest={'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'files':rows,'source_namespace':{'path':str(S),
 'files':[p.relative_to(S).as_posix() for p in source_files],'directories':source_dirs},
 'core_files':[str(p) for p in core],
 'core_qualification':'17original plus sole separately root-authorized405b checkpoint helper',
 'opaque_copy_only_no_semantic_code_results_or_opinion_exposure':True,
 'raw_inputs_ignored_before_creation':True,'source_or_native_programmes_executed':False}
(E/'PROTECTED_INPUTS.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'source_files':len(source_files),'source_directories':len(source_dirs),
 'qualified_core':len(core),'protected_paths':len(rows)},indent=2))
