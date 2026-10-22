from pathlib import Path
import importlib.util, json, subprocess, sys, tempfile, shutil
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('verify',ROOT/'verify_package.py');v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)

def require(ok,msg):
    if not ok: raise RuntimeError(msg)

results=[]
mutations=[('gap arithmetic','scripts/exact_gap_checks.py','mu * mu - D','mu * mu + D'),('matrix determinant','scripts/endpoint_decoder_check.py','(1, 0, 0, 1)','(2, 0, 0, 1)'),('symbolic matrix scaling','scripts/exact_audit.py','n(y * u)','n(2 * y * u)')]
for label,file,old,new in mutations:
    source=(ROOT/file).read_text();require(old in source,'mutation anchor missing')
    for flags in [[],['-O']]:
        with tempfile.TemporaryDirectory() as d:
            f=Path(d)/'mutant.py';f.write_text(source.replace(old,new,1))
            run=subprocess.run([sys.executable,*flags,str(f)],cwd=d,capture_output=True,text=True)
            # Run mutated mathematics directly, bypassing hash rejection.
            e=next(e for e in json.loads((ROOT/'AST_PROVENANCE.json').read_text()) if e['script']==file)
            output=Path(d)/Path(e['expected']).name
            differs=not output.exists() or output.read_bytes()!=(ROOT/e['expected']).read_bytes()
            require(run.returncode!=0 or differs,'mathematical mutation escaped')
            results.append(label+(' optimized' if flags else ' normal')+': rejected')
for kind in ['extra','missing','corrupt','nested_manifest','root_manifest_excluded']:
    with tempfile.TemporaryDirectory() as d:
        root=Path(d)/'package';shutil.copytree(ROOT,root)
        expected=v.inventory(root)
        if kind=='extra':(root/'extra.txt').write_text('extra')
        elif kind=='missing':(root/'REPORT.md').unlink()
        elif kind=='corrupt':(root/'REPORT.md').write_text('changed')
        elif kind=='nested_manifest':(root/'scripts/MANIFEST.json').write_text('{}')
        else:(root/'MANIFEST.json').write_text('changed root manifest')
        try: actual=v.inventory(root); rejected=actual!=expected
        except RuntimeError:rejected=True
        require(rejected==(kind!='root_manifest_excluded'),'inventory control failed: '+kind)
        results.append(kind+': PASS')
print(json.dumps(results,indent=2))
