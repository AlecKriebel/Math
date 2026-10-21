"""Reproducibility and integrity checks; not a general mathematical proof."""
import ast
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent

def require(condition, message):
    if not condition:
        raise RuntimeError(message)

def sha(data):
    return hashlib.sha256(data).hexdigest()

def inventory(root):
    manifest = json.loads((root / 'manifest.json').read_text())
    require(set(manifest) == {'schema', 'files'}, 'manifest schema')
    expected = manifest['files']
    require(isinstance(expected, dict), 'file inventory type')
    for name, item in expected.items():
        p = PurePosixPath(name)
        require(not p.is_absolute() and p.as_posix() == name and all(v not in ('', '.', '..') for v in name.split('/')) and '\\' not in name, 'unsafe inventory path')
        require(name != 'manifest.json' and not (len(p.parts)>1 and 'manifest' in p.name.lower()), 'nested or self manifest')
        require(set(item) == {'bytes', 'sha256'}, 'inventory entry schema')
    found = set()
    for base, dirs, files in os.walk(root, followlinks=False):
        for name in dirs + files:
            p = Path(base) / name
            require(not p.is_symlink(), 'symlink rejected')
            rel = p.relative_to(root).as_posix()
            require('\\' not in rel and all(v not in ('', '.', '..') for v in rel.split('/')), 'unsafe filesystem path')
        for name in files:
            p = Path(base) / name
            rel = p.relative_to(root).as_posix()
            if rel == 'manifest.json':
                continue
            require(not ('/' in rel and 'manifest' in name.lower()), 'nested manifest rejected')
            found.add(rel)
            require(rel in expected, 'unlisted file: ' + rel)
            data = p.read_bytes()
            require(expected[rel] == {'bytes': len(data), 'sha256': sha(data)}, 'hash/size mismatch: ' + rel)
    require(found == set(expected), 'missing inventory files')
    # Empty unlisted directories also cannot hide later payloads.
    for base, dirs, _ in os.walk(root):
        for name in dirs:
            rel = (Path(base)/name).relative_to(root).as_posix()
            require(any(v.startswith(rel+'/') for v in expected), 'unlisted directory')

def provenance():
    prov = json.loads((ROOT/'guard_conversion_provenance.json').read_text())
    data = (ROOT/'exact_checks.py').read_bytes()
    require(sha(data)==prov['converted_sha256'], 'converted source provenance')
    tree = ast.parse(data)
    require(not any(isinstance(n, ast.Assert) for n in ast.walk(tree)), 'optimized-away assertion')
    require(ast.dump(tree, include_attributes=False)==prov['converted_ast'], 'full converted AST')
    class Restore(ast.NodeTransformer):
        count = 0
        def visit_FunctionDef(self, node):
            if node.name == 'record':
                guard=node.body[0]
                require(isinstance(guard,ast.If) and isinstance(guard.test,ast.UnaryOp) and isinstance(guard.test.op,ast.Not) and not guard.orelse, 'guard form')
                require(len(guard.body)==1 and isinstance(guard.body[0],ast.Raise), 'guard raise')
                exc=guard.body[0].exc
                require(isinstance(exc,ast.Call) and isinstance(exc.func,ast.Name) and exc.func.id=='RuntimeError' and len(exc.args)==1 and not exc.keywords, 'guard exception')
                node.body[0]=ast.Assert(test=guard.test.operand,msg=exc.args[0]); self.count+=1
            return self.generic_visit(node)
    restore=Restore(); original=restore.visit(tree)
    require(restore.count==1 and ast.dump(original,include_attributes=False)==prov['original_ast'], 'full original AST restoration')

def run_script(code, flags):
    with tempfile.TemporaryDirectory() as tmp:
        p=Path(tmp)/'exact_checks.py'; p.write_text(code)
        result=subprocess.run([sys.executable,'-B',*flags,str(p)],capture_output=True,text=True)
        artifact=Path(tmp)/'exact_check_results.json'
        return result, artifact.read_text() if artifact.exists() else None

def replay():
    code=(ROOT/'exact_checks.py').read_text()
    expected=(ROOT/'exact_check_results.json').read_text()
    controls=[
        ('model_normalization', '(1 - a) * (1 - b)]', '(1 - a) * (2 - b)]', 'score_b'),
        ('zero_total_stratum', 'G = s.groebner([z * D - 1], a, b, z, domain=s.QQ)', 'G = s.groebner([a, z * D - 1], a, b, z, domain=s.QQ)', 'allzero not empty'),
        ('saturation_localization', 'G = s.groebner([a, b - s.Rational(1, 2), z * D - 1]', 'G = s.groebner([a, b - s.Rational(1, 2)]', 'specialize_then_saturate_is_unit'),
        ('rank_one_determinant', 'N - r - c + t]])', 'N - r - c + 2 * t]])', 'expected determinant Nt-rc'),
    ]
    results=[]
    for label, flags in [('normal', []), ('optimized', ['-O'])]:
        result, artifact=run_script(code, flags)
        require(result.returncode==0 and result.stderr=='', label+' direct run')
        require(result.stdout==expected and artifact==expected and result.stdout==(ROOT/(label+'_stdout.json')).read_text(), label+' complete stdout/JSON replay')
        obj=json.loads(artifact)
        require(obj['count']==22 and len(obj['checks'])==22 and set(obj['checks'].values())=={'PASS'}, 'complete 22 checks')
        for name, old, new, failure in controls:
            require(code.count(old)==1, 'unique mutation anchor '+name)
            result, artifact=run_script(code.replace(old,new),flags)
            require(result.returncode!=0 and ('RuntimeError: '+failure) in result.stderr and artifact is None, 'algebraic mutation escaped '+name+' '+label)
            results.append(name+' '+label+' rejected')
    return results

def inventory_controls():
    results=[]
    for name in ['nested_manifest','symlink','unlisted_file','unsafe_manifest_path','missing_file','changed_file']:
        with tempfile.TemporaryDirectory() as tmp:
            copy=Path(tmp)/'package'; shutil.copytree(ROOT,copy)
            if name=='nested_manifest':
                (copy/'nested').mkdir(); (copy/'nested/manifest.json').write_text('{}')
            elif name=='symlink': (copy/'alias').symlink_to('report.md')
            elif name=='unlisted_file': (copy/'unlisted.txt').write_text('unexpected')
            elif name=='unsafe_manifest_path':
                m=json.loads((copy/'manifest.json').read_text()); m['files']['../escape']={'bytes':0,'sha256':sha(b'')}; (copy/'manifest.json').write_text(json.dumps(m))
            elif name=='missing_file': (copy/'report.md').unlink()
            else: (copy/'report.md').write_text('altered')
            try: inventory(copy)
            except RuntimeError: results.append(name+' rejected')
            else: raise RuntimeError('inventory control escaped '+name)
    return results

if __name__=='__main__':
    inventory(ROOT)
    provenance()
    result={'status':'PASS','check_count':22,'full_stdout_json_replay':['normal','optimized'],'algebraic_controls':replay(),'inventory_controls':inventory_controls(),'limitations':'Finite checks supplement the authored proofs; no general classification or novelty claim.'}
    print(json.dumps(result,indent=2))
