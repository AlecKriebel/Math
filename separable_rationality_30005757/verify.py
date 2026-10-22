"""Fail-closed publication inventory, AST provenance and complete symbolic replay."""
import ast
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent
EXPECTED = {'PACKAGE_AUDIT.md', 'search.py', 'all_length4_results.json', 'exact_4231_checks.json', 'DATASET_MAPPING.json', 'RESEARCH_REPORT.md', 'check_obstructions.py', 'singularity_obstructions.md', 'check.stdout.txt', 'pole_checks.json', 'MANIFEST.json', 'check_4231.py', 'check_4231.stdout.txt', 'verify.py', 'SOURCE_GATE.md', 'ACCEPTANCE_RECEIPT.json', 'PUBLICATION_PROVENANCE.json', 'check.py', 'exact_checks.json', 'PUBLIC_SOURCE_METADATA.json', 'search_summary.json', 'README.md', 'STATUS.json', 'INDEPENDENT_AUDIT.md', 'check_obstructions.stdout.txt'}

def require(ok, message):
    if not ok:
        raise RuntimeError(message)

def inventory(root):
    entries = list(root.rglob('*'))
    require(not any(p.is_symlink() or not p.is_file() for p in entries), 'Non-file or symlink in package')
    require({p.relative_to(root).as_posix() for p in entries} == EXPECTED, 'Strict inventory mismatch')
    m = json.loads((root / 'MANIFEST.json').read_text())
    require(set(m['files']) == EXPECTED - {'MANIFEST.json'}, 'Manifest key mismatch')
    for name, spec in m['files'].items():
        data = (root / name).read_bytes()
        require(spec == {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}, 'Hash/size mismatch: ' + name)

class Harden(ast.NodeTransformer):
    def __init__(self, name, source):
        self.name, self.source = name, source
    def visit_Assert(self, node):
        return ast.copy_location(ast.If(test=ast.UnaryOp(op=ast.Not(), operand=node.test), body=[ast.Raise(exc=ast.Call(func=ast.Name(id='RuntimeError', ctx=ast.Load()), args=[ast.Constant(value=f'{self.name}:{node.lineno}: ' + ast.get_source_segment(self.source, node.test))], keywords=[]), cause=None)], orelse=[]), node)

def provenance():
    data = json.loads((ROOT / 'PUBLICATION_PROVENANCE.json').read_text())
    require(sorted(item['file'] for item in data['assert_hardening']) == ['check.py', 'check_4231.py'], 'Exact provenance coverage mismatch')
    for item in data['assert_hardening']:
        source = item['original_source']
        raw = source.encode()
        require(item['original'] == {'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}, 'Original source provenance hash mismatch')
        records = []
        def walk(node, ancestors):
            if isinstance(node, ast.Assert):
                records.append({'line': node.lineno, 'column': node.col_offset, 'condition': ast.get_source_segment(source, node.test), 'condition_ast': ast.dump(node.test, include_attributes=False), 'control_flow': [{'kind': type(a).__name__, 'line': a.lineno, 'header': ast.unparse(a.test) if isinstance(a, ast.If) else ast.unparse(a.target) + ' in ' + ast.unparse(a.iter)} for a in ancestors]})
            for child in ast.iter_child_nodes(node):
                walk(child, ancestors + ([node] if isinstance(node, (ast.For, ast.If)) else []))
        original = ast.parse(source)
        walk(original, [])
        require(records == item['assertions'], 'Exact assertion/control-flow provenance mismatch')
        expected = ast.fix_missing_locations(Harden(item['file'], source).visit(original))
        actual = ast.parse((ROOT / item['file']).read_text())
        require(ast.dump(expected, include_attributes=False) == ast.dump(actual, include_attributes=False), 'Hardened AST differs beyond assertion replacement')
        require(not any(isinstance(n, ast.Assert) for n in ast.walk(actual)), 'Residual assert')

def run(path, optimized):
    return subprocess.run([sys.executable, '-B'] + (['-O'] if optimized else []) + [str(path)], text=True, capture_output=True, timeout=600, env={**os.environ, 'PYTHONDONTWRITEBYTECODE': '1'})

def main():
    inventory(ROOT)
    if '--inventory-only' in sys.argv:
        print('inventory PASS')
        return
    provenance()
    import itertools
    rows=json.loads((ROOT/'all_length4_results.json').read_text())
    patterns=['1342','2314','2341','2431','3241','3412','3421','4231']
    expected_bases={tuple(b) for n in range(1,9) for b in itertools.combinations(patterns,n)}
    require(len(rows)==255 and {tuple(r['basis']) for r in rows}==expected_bases, 'Exact 255-basis coverage mismatch')
    require(all(len(r['coefficients'])==81 for r in rows), 'Coefficient range mismatch')
    require(sorted({r['modular_recurrence_order'] for r in rows})==[40,41], 'Recurrence screen summary mismatch')
    import shutil
    replay=[]
    controls=[]
    with tempfile.TemporaryDirectory() as temporary:
        tmp=Path(temporary)
        copied=tmp/'copy'
        shutil.copytree(ROOT,copied)
        for script, output, result in [('check.py','check.stdout.txt','exact_checks.json'),('check_4231.py','check_4231.stdout.txt','exact_4231_checks.json'),('check_obstructions.py','check_obstructions.stdout.txt',None)]:
            for optimized in (False,True):
                process=run(copied/script,optimized)
                require(process.returncode==0,process.stderr)
                require(process.stdout==(ROOT/output).read_text(),'Complete stdout mismatch: '+script)
                if result:
                    require((copied/result).read_bytes()==(ROOT/result).read_bytes(),'Complete JSON mismatch: '+result)
                replay.append({'script':script,'optimized':optimized,'full_output_match':True})
        rows=json.loads((ROOT/'all_length4_results.json').read_text())
        for label,field in [('count','coefficients'),('state','states')]:
            altered=json.loads(json.dumps(rows))
            if field=='coefficients':altered[0][field][4]+=1
            else:altered[0][field]+=1
            (copied/'all_length4_results.json').write_text(json.dumps(altered))
            for optimized in (False,True):
                process=run(copied/'check.py',optimized)
                require(process.returncode!=0 and 'RuntimeError: check.py:' in process.stderr,'Mathematical corruption escaped: '+label)
                controls.append({'mutation':label,'optimized':optimized,'rejected':True,'failure':process.stderr.strip().splitlines()[-1]})
        shutil.copy(ROOT/'all_length4_results.json',copied/'all_length4_results.json')
        script=(ROOT/'check_4231.py').read_text()
        require(script.count('4 * x ** 3 - 9 * x * x + 6 * x - 1')==1,'Algebra mutation target missing')
        (copied/'check_4231.py').write_text(script.replace('4 * x ** 3 - 9 * x * x + 6 * x - 1','4 * x ** 3 - 8 * x * x + 6 * x - 1'))
        for optimized in (False,True):
            process=run(copied/'check_4231.py',optimized)
            require(process.returncode!=0 and 'RuntimeError: check_4231.py:' in process.stderr,'Algebra corruption escaped')
            controls.append({'mutation':'quadratic coefficient','optimized':optimized,'rejected':True,'failure':process.stderr.strip().splitlines()[-1]})
        # Missing provenance coverage must fail even with refreshed file metadata.
        coverage=tmp/'coverage';shutil.copytree(ROOT,coverage)
        data=json.loads((coverage/'PUBLICATION_PROVENANCE.json').read_text());data['assert_hardening']=[]
        (coverage/'PUBLICATION_PROVENANCE.json').write_text(json.dumps(data))
        command="import sys;sys.path.insert(0,sys.argv[1]);import verify;verify.provenance()"
        process=subprocess.run([sys.executable,'-B','-O','-c',command,str(coverage)],text=True,capture_output=True)
        require(process.returncode!=0 and 'Exact provenance coverage mismatch' in process.stderr,'Missing AST coverage accepted')
        # Separate unaltered copy: exercise strict recursive inventory.
        clean=tmp/'inventory';shutil.copytree(ROOT,clean)
        for name in ['unexpected.txt','nested/MANIFEST.json']:
            target=clean/name;target.parent.mkdir(parents=True,exist_ok=True);target.write_text('{}')
            try:inventory(clean)
            except RuntimeError:pass
            else:raise RuntimeError('Unexpected inventory entry accepted: '+name)
            target.unlink()
            if target.parent!=clean:target.parent.rmdir()
        manifest=json.loads((clean/'MANIFEST.json').read_text());manifest['files']['MANIFEST.json']={'bytes':0,'sha256':'0'*64};(clean/'MANIFEST.json').write_text(json.dumps(manifest))
        try:inventory(clean)
        except RuntimeError:pass
        else:raise RuntimeError('Manifest self-entry accepted')
    print(json.dumps({'replay':replay,'corruption_controls':controls,'nested_manifest_rejected':True,'unexpected_file_rejected':True,'manifest_self_entry_rejected':True,'missing_provenance_rejected':True,'ast_provenance':'PASS','inventory':'PASS'},indent=2))

if __name__=='__main__':main()
