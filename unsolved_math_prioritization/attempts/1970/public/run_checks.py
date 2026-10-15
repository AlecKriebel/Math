#!/usr/bin/env python3
"""Replay exact finite checks and semantic rejection controls in temporary copies."""
from pathlib import Path
import ast, hashlib, json, os, shutil, subprocess, sys, tempfile
ROOT=Path(__file__).resolve().parent
MODES=[('normal',[]),('O',['-O']),('OO',['-OO'])]
CHECKS=[('checks/exact/verify_exact.py','fixtures/verify_exact.json'),('checks/check_structure.py','fixtures/check_structure.json'),('checks/check_arithmetic.py','fixtures/check_arithmetic.json'),('checks/check_independently.py','fixtures/check_independently.json')]
CHECKS.append(('checks/check_crosslinks.py','fixtures/check_crosslinks.json'))
CHECKS += [('checks/check_single_defect.py','fixtures/check_single_defect.json'),('checks/check_tail.py','fixtures/check_tail.json'),('checks/check_local_independently.py','fixtures/check_local_independently.json')]
EXACT_CONTROLS=['wrong_tau','omit_vertex','wrong_X','wrong_count','wrong_delta','wrong_q0','wrong_q1','wrong_q0_witness','wrong_color','wrong_patch','truncate_prefix','historic_bytes_claim']
MUTATIONS=[
 ('structure_recurrence','checks/check_structure.py','1 + int(defect == (a, b)) - ar[-1][a] - ar[-1][a + 1]','2 + int(defect == (a, b)) - ar[-1][a] - ar[-1][a + 1]','Verification condition failed'),
 ('arithmetic_constant','checks/check_arithmetic.py','constant = 1 - correction / 21','constant = 1 - correction / 20','renormalized constant mismatch'),
 ('candidate_vector','checks/check_arithmetic.py','v[(2 * h) % 3] += 1','v[(2 * h) % 3] += 2','nine-breakpoint vector mismatch'),
 ('independent_tau','checks/check_independently.py','return costs[0],ways[0]','return costs[0]+1,ways[0]','vertex branching mismatch'),
 ('tail_endpoint','checks/check_tail.py','b = floor_log(x / 2 ** a, 3) + 1','b = floor_log(x / 2 ** a, 3)','strict-cutoff exponent mismatch'),
 ('local_convolution','checks/check_local_independently.py','value=(1-(-2)**b)//3','value=(1-(-2)**b)//3+1','exact stencil mismatch'),
]
if (ROOT/'checks/check_single_defect.py').is_file():
    MUTATIONS += [('one_defect_exception','checks/check_single_defect.py','delta>=-epsilon','delta>=0','suffix exceeds exceptional saving'),('one_defect_color','checks/check_single_defect.py','adjusted[(m+2)%3] -= 1','adjusted[(m+1)%3] -= 1','finite q1 mismatch')]

def require(ok,why):
    if not ok: raise RuntimeError(why)
def sha(b):return hashlib.sha256(b).hexdigest()
def snapshot():return {p.relative_to(ROOT).as_posix():sha(p.read_bytes()) for p in ROOT.rglob('*') if p.is_file()}
def invoke(flags,script,cwd,args=()):
    env=dict(os.environ);env.pop('PYTHONOPTIMIZE',None);env.pop('PYTHONPATH',None)
    return subprocess.run([sys.executable,'-I','-B',*flags,str(script),*args],cwd=cwd,env=env,capture_output=True,timeout=900)
class FailGuard(ast.NodeTransformer):
    def __init__(self):self.changed=False
    def visit_If(self,node):
        if not self.changed and node.body and isinstance(node.body[0],ast.Raise):
            self.changed=True;node.test=ast.Constant(True)
            node.body=[ast.Raise(exc=ast.Call(func=ast.Name(id='RuntimeError',ctx=ast.Load()),args=[ast.Constant('intentional explicit guard probe')],keywords=[]))]
            return node
        return self.generic_visit(node)
def main():
    cp=invoke([],ROOT/'verify_package.py',ROOT)
    require(cp.returncode==0 and not cp.stderr,'initial package integrity failure: '+cp.stderr.decode())
    before=snapshot();positive=[];negative=[];guard=[]
    with tempfile.TemporaryDirectory(prefix='ep168-replay-') as td:
        tmp=Path(td)
        for rel,fixture in CHECKS:
            source=(ROOT/rel).read_text();require(not any(isinstance(n,ast.Assert) for n in ast.walk(ast.parse(source))),'optimization-sensitive assertion')
            transform=FailGuard();mutant=transform.visit(ast.parse(source));ast.fix_missing_locations(mutant)
            # The exact verifier imports its explicit guard from finite_solver.
            guard_rel=rel
            if not transform.changed:
                require(rel=='checks/exact/verify_exact.py','missing explicit guard')
                guard_rel='checks/exact/finite_solver.py';transform=FailGuard();mutant=transform.visit(ast.parse((ROOT/guard_rel).read_text()));ast.fix_missing_locations(mutant)
            require(transform.changed,'missing explicit guard')
            baseline=(ROOT/fixture).read_bytes()
            for mode,flags in MODES:
                work=tmp/(Path(rel).stem+'_'+mode);shutil.copytree(ROOT,work)
                cp=invoke(flags,work/rel,work)
                require(cp.returncode==0 and not cp.stderr,'checker failed: '+rel+' '+mode+' '+cp.stderr.decode())
                require(cp.stdout==baseline,'output differs from exact fixture: '+rel+' '+mode)
                positive.append({'script':rel,'mode':mode,'output_sha256':sha(cp.stdout),'output_bytes':len(cp.stdout),'matches_fixture':True})
                (work/guard_rel).write_text(ast.unparse(mutant)+'\n')
                cp=invoke(flags,work/rel,work)
                require(cp.returncode!=0 and b'intentional explicit guard probe' in cp.stderr,'explicit guard disabled: '+rel+' '+mode)
                guard.append({'script':rel,'mode':mode,'rejected':True})
        for mode,flags in MODES:
            for name in EXACT_CONTROLS:
                cp=invoke(flags,ROOT/'checks/exact/verify_exact.py',tmp,('--inject',name))
                require(cp.returncode==2 and cp.stderr.startswith(b'VERIFICATION FAILED:') and b'negative control was not rejected' not in cp.stderr,'finite semantic control failed: '+name)
                negative.append({'case':name,'mode':mode,'rejected':True})
        for mode,flags in MODES:
            for name,label in [('independent_count','independent optimal_count comparison mismatch'),('base_q1','overlapping q1 minimum mismatch'),('missing_witness','witness cardinality/domain mismatch'),('missing_row','prefix length mismatch')]:
                cp=invoke(flags,ROOT/'checks/check_crosslinks.py',tmp,('--inject',name))
                require(cp.returncode!=0 and label.encode() in cp.stderr and b'cross-link mutation was not rejected' not in cp.stderr,'cross-link control failed: '+name+' '+cp.stderr.decode())
                negative.append({'case':'crosslink_'+name,'mode':mode,'rejected':True})
        for name,rel,old,new,label in MUTATIONS:
            source=(ROOT/rel).read_text();require(source.count(old)==1,'nonunique mutation target: '+name)
            work=tmp/name;shutil.copytree(ROOT,work);(work/rel).write_text(source.replace(old,new))
            for mode,flags in MODES:
                cp=invoke(flags,work/rel,work)
                require(cp.returncode!=0 and label.encode() in cp.stderr,'semantic mutation escaped or wrong failure: '+name+' '+cp.stderr.decode())
                negative.append({'case':name,'mode':mode,'rejected':True})
        # This control changes the actual shared input, not an in-memory option.
        work=tmp/'numeric_fixture';shutil.copytree(ROOT,work)
        target=work/'fixtures/exact/tau_through_X192.json';data=json.loads(target.read_text());data[-1]['tau']+=1;target.write_text(json.dumps(data))
        for mode,flags in MODES:
            cp=invoke(flags,work/'checks/check_arithmetic.py',work)
            require(cp.returncode!=0 and b'tau reconstruction changed' in cp.stderr,'numeric input corruption accepted')
            negative.append({'case':'numeric_fixture','mode':mode,'rejected':True})
    require(snapshot()==before,'public package changed during replay')
    print(json.dumps({'status':'PASS','finite_checkers':len(CHECKS),'positive_executions':len(positive),'guard_rejections':len(guard),'semantic_rejections':len(negative),'modes':[m for m,_ in MODES],'source_tree_modified':False,'resolution_claimed':False,'checks':positive,'guard_controls':guard,'semantic_controls':negative,'scope':'Exact finite optimization and algebra; all-scale mathematics relies on the included proofs.'},indent=2,sort_keys=True))
if __name__=='__main__':main()
