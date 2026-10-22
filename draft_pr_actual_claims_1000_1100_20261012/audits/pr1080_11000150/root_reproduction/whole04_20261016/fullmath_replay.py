"""Capture every mathematical field from the actual portable AST adapters."""
from pathlib import Path
import ast, contextlib, hashlib, importlib.util, io, json, shutil, sys, tempfile
sys.dont_write_bytecode=True
HERE=Path('/Users/alec/Documents/Math/draft_pr_actual_claims_1000_1100_20261012/audits/pr1080_11000150/root_reproduction/whole04_20261016')
KIT=Path('/Users/alec/Documents/Math/draft_pr_actual_claims_1000_1100_20261012/audits/pr1080_11000150/preprint_v1_0/verification_kit')
spec=importlib.util.spec_from_file_location('review04_adapters',KIT/'run_checks.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
def need(x,s):
    if not x:raise RuntimeError(s)
rows=[]
with tempfile.TemporaryDirectory(prefix='whole04-fullmath-') as tmp:
    for kind,(relative,pinned) in m.PROGRAMS.items():
        original=KIT/relative
        need(hashlib.sha256(original.read_bytes()).hexdigest()==pinned,'source pin')
        work=Path(tmp)/kind;work.mkdir();copy=work/original.name;shutil.copyfile(original,copy)
        if kind=='surface':shutil.copytree(KIT/'originals/submitted',work/'inputs/git')
        namespace={'__name__':'whole04_capture','__file__':str(copy)}
        buffer=io.StringIO()
        with contextlib.redirect_stdout(buffer):
            tree=m.adapt(kind,original.read_text(),None)
            need(not any(isinstance(n,ast.Assert) for n in ast.walk(tree)),'assert remains')
            exec(compile(tree,str(copy),'exec'),namespace)
            if kind in ('word','priority'):local=namespace['main']()
        if kind=='priority':
            raw=ast.parse(original.read_text());main=next(n for n in raw.body if isinstance(n,ast.FunctionDef) and n.name=='main')
            expr=next(n.value for n in main.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='result' for t in n.targets))
            actual=eval(compile(ast.Expression(expr),str(copy),'eval'),namespace,dict(local,verified=[]))
            expected=json.loads((original.parent/'CONTROL_RESULTS.json').read_text());excluded=['frozen_inputs_reverified']
            # Verify exactly one cut, after every mathematical assertion and before historical custody.
            cut=next(i for i,n in enumerate(main.body) if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='b' for t in n.targets))
            need(all(not isinstance(n,ast.Assert) for n in main.body[cut:]),'unexpected math in omitted tail')
        else:
            name='WORD_CONTROL_RESULTS.json' if kind=='word' else 'SANITY_RESULTS.json'
            actual=json.loads((work/name).read_text());expected=json.loads((original.parent/name).read_text());excluded=['timestamp'] if kind=='surface' else []
        for field in excluded:actual.pop(field);expected.pop(field)
        actual=json.loads(json.dumps(actual))
        need(actual==expected,'full math mismatch: '+kind)
        rows.append({'kind':kind,'source_sha256':pinned,'excluded_fields':excluded,'full_mathematical_output':actual,'matches_preserved':True})
destination=HERE/('FULL_MATHEMATICAL_OUTPUT_COMPARISON_O.json' if sys.flags.optimize else 'FULL_MATHEMATICAL_OUTPUT_COMPARISON.json')
destination.write_text(json.dumps(rows,indent=2)+'\n')
print(json.dumps({'status':'PASS','optimized':bool(sys.flags.optimize),'all_mathematical_fields_compared':True,'historical_52_input_tail_replayed':False,'output':str(destination)}))
