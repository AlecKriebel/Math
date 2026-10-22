#!/usr/bin/env python3
"""Capture the full mathematical JSON under the actual current adapters."""
import ast, hashlib, importlib.util, json, shutil, sys
from pathlib import Path
sys.dont_write_bytecode=True
W=Path(__file__).resolve().parent; K=W/'scratch/clean_check/verification_kit'
spec=importlib.util.spec_from_file_location('archive_wording_fullmath',K/'run_checks.py'); mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
results=[]
for kind,(relative,expected_hash) in mod.PROGRAMS.items():
    source=K/relative
    if hashlib.sha256(source.read_bytes()).hexdigest()!=expected_hash:raise RuntimeError('Pinned adapter source differs')
    work=W/'scratch'/('full-'+kind+('-O' if sys.flags.optimize else ''));work.mkdir();copied=work/source.name;shutil.copyfile(source,copied)
    if kind=='surface':
        d=work/'inputs/git';d.mkdir(parents=True)
        for p in (K/'originals/submitted').iterdir():shutil.copyfile(p,d/p.name)
    ns={'__name__':'archive_wording_fullmath_capture','__file__':str(copied)}
    exec(compile(mod.adapt(kind,source.read_text(),None),str(copied),'exec'),ns)
    if kind in ['word','priority']:local=ns['main']()
    if kind=='priority':
        tree=ast.parse(source.read_text());main=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='main')
        expr=next(n.value for n in main.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='result' for t in n.targets))
        actual=eval(compile(ast.Expression(expr),str(copied),'eval'),ns,dict(local,verified=[]));expected=json.loads((source.parent/'CONTROL_RESULTS.json').read_text());exclusions=['frozen_inputs_reverified']
    else:
        name='WORD_CONTROL_RESULTS.json' if kind=='word' else 'SANITY_RESULTS.json'
        actual=json.loads((work/name).read_text());expected=json.loads((source.parent/name).read_text());exclusions=['timestamp'] if kind=='surface' else []
    for key in exclusions:actual.pop(key,None);expected.pop(key,None)
    actual=json.loads(json.dumps(actual))
    if actual!=expected:raise RuntimeError('Full mathematics differs '+kind)
    results.append({'kind':kind,'source_sha256':expected_hash,'excluded_fields':exclusions,'full_mathematical_output':actual,'matches_preserved':True})
filename='FULL_MATHEMATICAL_OUTPUT_COMPARISON'+('_O' if sys.flags.optimize else '')+'.json'
prior=W.parents[1]/'newreviews/package_04'/filename
if results!=json.loads(prior.read_text()):raise RuntimeError('Full mathematical JSON differs from adopted whole04')
(W/filename).write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps({'status':'PASS','full_mathematical_fields_match_preserved_and_adopted_whole03':True,'optimized':bool(sys.flags.optimize)}))
