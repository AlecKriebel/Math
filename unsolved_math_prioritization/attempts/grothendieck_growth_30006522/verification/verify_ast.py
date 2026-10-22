"""Verify every research module, including imports, helpers, checks and main body."""
import ast,hashlib,json,pathlib,sys
ROOT=pathlib.Path(__file__).resolve().parents[1]
class Normalize(ast.NodeTransformer):
    def visit_Constant(self,node):
        if isinstance(node.value,str):
            node.value=node.value.replace('recovery_grothendieck_1873_20261021/research/','').replace('/tmp/groth_supports','groth_supports')
        return node

def main():
    records=json.loads((ROOT/'verification'/'AST_PROVENANCE.json').read_text())
    if {r['file'] for r in records}!={p.name for p in (ROOT/'research').glob('*.py')}:raise RuntimeError('Module inventory mismatch')
    for r in records:
        data=(ROOT/'research'/r['file']).read_bytes()
        if hashlib.sha256(data).hexdigest()!=r['packaged_sha256']:raise RuntimeError('Packaged byte mismatch')
        tree=ast.dump(ast.parse(data),include_attributes=False)
        if hashlib.sha256(tree.encode()).hexdigest()!=r['whole_module_normalized_ast_sha256']:raise RuntimeError('Whole module AST mismatch')
        if len(sys.argv)>1:
            original=(pathlib.Path(sys.argv[1])/r['file']).read_bytes()
            if hashlib.sha256(original).hexdigest()!=r['original_sha256']:raise RuntimeError('Original byte mismatch')
            if ast.dump(Normalize().visit(ast.parse(original)),include_attributes=False)!=tree:raise RuntimeError('Unexpected source transformation')
    print('PASS: all four whole-module ASTs and byte hashes'+('; originals independently compared' if len(sys.argv)>1 else ''))
if __name__=='__main__':main()
