"""Mathematical, hardening-provenance, and fail-closed inventory controls."""
import ast,hashlib,importlib.util,json,os,stat,tempfile
from pathlib import Path
from unittest.mock import patch
ROOT=Path(__file__).parent

def require(ok,message):
    if not ok:raise RuntimeError(message)
def load(name):
    spec=importlib.util.spec_from_file_location(name,ROOT/(name+'.py'));m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m

def main():
    original=load('check_tricycles');independent=load('audit_independent');inv=load('verify_inventory');checks=[]
    cases=[('path_single_chip',[[1],[0,2],[1]],[1,0,0],True),('cycle_single_chip',[[1,2],[0,2],[0,1]],[1,0,0],False),('cycle_two_chips',[[1,2],[0,2],[0,1]],[1,1,0],True),('parallel_single_chip',[[1,1],[0,0]],[1,0],False),('parallel_two_chips',[[1,1],[0,0]],[1,1],True)]
    for name,adj,D,expected in cases:
        weighted=[{w:row.count(w) for w in row} for row in adj]
        a=all(original.reaches(weighted,D,q)[0] for q in range(len(adj)))
        b=all(independent.reaches(adj,D,q) for q in range(len(adj)))
        require(a==b==expected,name);checks.append({'test':name,'expected_rank_one':expected,'burning':a,'sandpile':b})
    # A deliberate mathematically wrong non-strict burning threshold must fail on a tree.
    code=(ROOT/'check_tricycles.py').read_text();require('incoming[v] > D[v]' in code,'mutation target')
    mutant={};exec(compile(code.replace('incoming[v] > D[v]','incoming[v] >= D[v]'),'<threshold-mutant>','exec'),mutant)
    require(not mutant['reaches']([{1:1},{0:1,2:1},{1:1}],[1,0,0],2)[0],'threshold mutation undetected')
    checks.append({'test':'non_strict_threshold_mutant','rejected_by_tree_control':True})
    class Harden(ast.NodeTransformer):
        def visit_Assert(self,node):
            return ast.copy_location(ast.If(test=ast.UnaryOp(op=ast.Not(),operand=node.test),body=[ast.Raise(exc=ast.Call(func=ast.Name(id='AssertionError',ctx=ast.Load()),args=[node.msg or ast.Constant(value='verification failed')],keywords=[]),cause=None)],orelse=[]),node)
    guards=0
    for n in ['check_tricycles.py','check_lengths.py','audit_independent.py']:
        old=(ROOT/'originals'/n).read_text();new=(ROOT/n).read_text();p=json.loads((ROOT/'provenance'/(n+'.json')).read_text())
        require(hashlib.sha256(old.encode()).hexdigest()==p['original_sha256'],'original hash')
        require(hashlib.sha256(new.encode()).hexdigest()==p['hardened_sha256'],'hardened hash')
        require(ast.dump(ast.parse(old),include_attributes=True)==p['original_full_ast'],'original full AST')
        stage=old
        for out in ['TRICYCLE_CHECKS.json','LENGTH_CHECKS.json']:
            stage=stage.replace("open('gonality_subdivisions_3000040/residual_attempt/"+out+"','w')","open(__import__('pathlib').Path(__file__).with_name('"+out+"'),'w')")
        require(ast.dump(ast.parse(stage),include_attributes=True)==p['path_adjusted_full_ast'],'path full AST')
        expected=ast.unparse(ast.fix_missing_locations(Harden().visit(ast.parse(stage))))+'\n'
        require(expected==new,'unauthorized source change')
        require(ast.dump(ast.parse(new),include_attributes=True)==p['hardened_full_ast'],'hardened full AST')
        require(not any(isinstance(x,ast.Assert) for x in ast.walk(ast.parse(new))),'remaining assert')
        for node in ast.walk(ast.parse(old)):
            if isinstance(node,ast.Assert):
                guard=Harden().visit(node);module=ast.fix_missing_locations(ast.Module(body=[guard],type_ignores=[]))
                good={'D':[0,1],'good':[[1]],'row':{'positive_rank_positions':[[1]],'candidates':4},'count':4,'actual':5,'expected':{'gonality':5,'witness_positions':[1]}}
                bad=dict(good,D=[-1],good=[],actual=6)
                exec(compile(module,'<positive-guard>','exec'),good)
                try:exec(compile(module,'<negative-guard>','exec'),bad)
                except AssertionError:guards+=1
                else:raise RuntimeError('guard accepted corruption')
    checks.append({'test':'all_source_AST_and_guard_controls','guards':guards,'passed':True})
    with tempfile.TemporaryDirectory() as td:
        td=Path(td);root=td/'root';root.mkdir();(root/'nested').mkdir();link=td/'rootlink';link.symlink_to(root,target_is_directory=True)
        def rejected(path):
            with patch.object(Path,'read_text',side_effect=RuntimeError('read before validation')),patch.object(Path,'read_bytes',side_effect=RuntimeError('read before validation')):
                try:inv.verify(path)
                except ValueError:return True
            raise RuntimeError('unsafe path accepted')
        require(rejected(link),'root symlink');checks.append({'test':'root_symlink_before_reads','passed':True})
        nested=root/'nested'/'bad';nested.symlink_to(root,target_is_directory=True);require(rejected(root),'nested symlink');nested.unlink();checks.append({'test':'nested_symlink_before_reads','passed':True})
        os.mkfifo(nested);require(rejected(root),'nested FIFO');require(rejected(nested),'root FIFO');nested.unlink();checks.append({'test':'root_and_nested_FIFO_before_reads','passed':True})
        class Entry:
            name='synthetic';path=str(root/'synthetic')
            def stat(self,follow_symlinks=False):return type('Mode',(),{'st_mode':mode})()
        for mode in [stat.S_IFSOCK,stat.S_IFCHR,stat.S_IFBLK]:
            with patch.object(inv.os,'scandir',return_value=[Entry()]):require(rejected(root),'synthetic special mode')
        checks.append({'test':'synthetic_socket_character_block_modes_no_socket_created','passed':True})
    print(json.dumps({'mode':'optimized' if not __debug__ else 'normal','controls':checks,'all_passed':True},separators=(',',':')))
if __name__=='__main__':main()
