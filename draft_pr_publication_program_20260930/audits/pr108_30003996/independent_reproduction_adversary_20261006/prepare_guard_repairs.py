#!/usr/bin/env python3
"""Create separate minimal explicit-guard suggestions. Originals are read-only."""
import ast,datetime,difflib,hashlib,json,shutil
from pathlib import Path
HERE=Path(__file__).resolve().parent
ORIG=HERE.parent/'original_source_authentication_20261006/original_attempt'
GUARD="def require(value, message='verification predicate failed'):\n if not value: raise AssertionError(message)\n"

def repair(text):
    nodes=[n for n in ast.walk(ast.parse(text)) if isinstance(n,ast.Assert)]
    lines=text.splitlines(keepends=True)
    offsets=[];total=0
    for line in lines:offsets.append(total);total+=len(line)
    edits=[]
    for n in nodes:
        start=offsets[n.lineno-1]+n.col_offset;end=offsets[n.end_lineno-1]+n.end_col_offset
        test=ast.get_source_segment(text,n.test)
        message=', '+ast.get_source_segment(text,n.msg) if n.msg else ''
        edits.append((start,end,'require('+test+message+')'))
    for a,b,s in sorted(edits,reverse=True):text=text[:a]+s+text[b:]
    # Place definition after imports, before the first executable data binding/guard.
    if 'checks=0;tree_cases=0;formula_count=0' in text:
        text=text.replace('checks=0;tree_cases=0;formula_count=0',GUARD+'checks=0;tree_cases=0;formula_count=0',1)
    else:
        text=text.replace('root=Path(__file__).resolve().parent',GUARD+'root=Path(__file__).resolve().parent',1)
    text=text.replace("'all_pass':True,", "'all_pass':True,'guard_mode':'explicit_require_survives_python_optimization','verifier_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),",1)
    return text,len(nodes)

manifest=[]
for family,rel,file in [('author','verify.py','verify.py'),('old_review','independent_review/independent_checks.py','independent_checks.py')]:
    original=(ORIG/rel).read_text();fixed,count=repair(original)
    for mode in ['normal','optimized']:
        dst=HERE/'suggested_guard_repairs'/f'{family}_{mode}';dst.mkdir(parents=True,exist_ok=True)
        (dst/file).write_text(fixed)
        if family=='author':shutil.copyfile(ORIG/'PROOF.md',dst/'PROOF.md')
        else:
            (dst/'author_replay').mkdir(exist_ok=True)
            shutil.copyfile(ORIG/'independent_review/author_replay/PROOF.md',dst/'author_replay/PROOF.md')
    diff=''.join(difflib.unified_diff(original.splitlines(keepends=True),fixed.splitlines(keepends=True),fromfile='original/'+rel,tofile='suggested/'+rel))
    (HERE/'suggested_guard_repairs'/f'{family}.diff').write_text(diff)
    manifest.append({'family':family,'replaced_assert_nodes':count,'original_sha256':hashlib.sha256(original.encode()).hexdigest(),'suggested_sha256':hashlib.sha256(fixed.encode()).hexdigest(),'receipt_changes':['guard_mode','verifier_sha256'],'proof_unchanged':True})
(HERE/'suggested_guard_repairs'/'repair_manifest.json').write_text(json.dumps({'time_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'repairs':manifest,'purpose':'Verifier hardening only; no mathematical proof change; original files and receipts untouched.'},indent=2)+'\n')
print(json.dumps(manifest,indent=2))
