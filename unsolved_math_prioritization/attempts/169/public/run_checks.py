#!/usr/bin/env python3
"""Replay finite mathematics and semantic negative controls in disposable copies."""
import ast,hashlib,json,os,shutil,subprocess,sys,tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parent
MODES=[('normal',[]),('O',['-O']),('OO',['-OO'])]
MUTANTS=[
 ('adaptive_flux_sign','check_adaptive_flux.py','rhs=-q*K*D/(1-q)','rhs=q*K*D/(1-q)','exchange moment identity'),
 ('cylinder_minimum','check_cylinders_products.py','minimum=F(m*(k-r),n-r)','minimum=F(m*(k-r+1),n-r)','conditioned minimum'),
 ('canonical_double_division','check_canonical_normalization.py','W[J]+=F(1,R);','W[J]+=F(1,R*R);','cap canonical normalized probability'),
 ('graph_component_rank','check_additive_graphs.py',"require(rank==v-h,'graph rank including isolated vertices')","require(rank==v-h+1,'graph rank including isolated vertices')",'graph rank including isolated vertices'),
 ('greedy_rounding_sign','check_residual_profiles.py','g.append(g[-1]-(k*g[-1]+p-i-1)//(p-i))','g.append(g[-1]+(k*g[-1]+p-i-1)//(p-i))','integer greedy sandwich'),
 ('joint_exchange_union','check_canonical_normalization.py','a=dx+dy-s;b=2*k-dx-dy-r+s','a=dx+dy+s;b=2*k-dx-dy-r+s','exact pair exchange probability'),
]
def require(ok,msg):
    if not ok:raise RuntimeError(msg)
def sha(b):return hashlib.sha256(b).hexdigest()
def snapshot():return {p.relative_to(ROOT).as_posix():sha(p.read_bytes()) for p in ROOT.rglob('*') if p.is_file()}
def invoke(flags,script,cwd):
    env=dict(os.environ);env.pop('PYTHONOPTIMIZE',None);env.pop('PYTHONPATH',None)
    return subprocess.run([sys.executable,'-I','-B',*flags,str(script)],cwd=cwd,env=env,capture_output=True,timeout=240)
class Guard(ast.NodeTransformer):
    def __init__(self):self.changed=False
    def visit_If(self,node):
        if not self.changed and node.body and isinstance(node.body[0],ast.Raise):
            self.changed=True;node.test=ast.Constant(True)
            node.body=[ast.Raise(exc=ast.Call(func=ast.Name(id='RuntimeError',ctx=ast.Load()),args=[ast.Constant('intentional finite guard probe')],keywords=[]))]
            return node
        return self.generic_visit(node)
def main():
    cp=invoke([],ROOT/'verify_package.py',ROOT);require(cp.returncode==0 and not cp.stderr,'initial integrity failure')
    before=snapshot();records=[];guards=[];mutants=[]
    with tempfile.TemporaryDirectory(prefix='random-cover-finite-') as tmp:
        base=Path(tmp)
        for script in sorted((ROOT/'checks').glob('*.py')):
            source=script.read_text();tree=ast.parse(source)
            require(not any(isinstance(n,ast.Assert) for n in ast.walk(tree)),'optimization-sensitive assert')
            trans=Guard();mutant=trans.visit(ast.parse(source));ast.fix_missing_locations(mutant)
            require(trans.changed,'missing explicit runtime guard')
            baseline=(ROOT/'fixtures'/(script.stem+'.json')).read_bytes()
            for mode,flags in MODES:
                work=base/(script.stem+'_'+mode);shutil.copytree(ROOT,work)
                cp=invoke(flags,work/'checks'/script.name,work)
                require(cp.returncode==0 and cp.stderr==b'','finite checker failed: '+script.name+' '+mode+' '+cp.stderr.decode())
                require(cp.stdout==baseline,'finite baseline mismatch: '+script.name+' '+mode)
                records.append({'script':'checks/'+script.name,'mode':mode,'output_bytes':len(baseline),'output_sha256':sha(baseline),'matches_baseline':True})
                (work/'checks'/script.name).write_text(ast.unparse(mutant)+'\n')
                cp=invoke(flags,work/'checks'/script.name,work)
                require(cp.returncode!=0 and b'intentional finite guard probe' in cp.stderr,'disabled finite guard')
                guards.append({'script':'checks/'+script.name,'mode':mode,'rejected':True})
        for name,filename,old,new,label in MUTANTS:
            source=(ROOT/'checks'/filename).read_text();require(source.count(old)==1,'nonunique mutation target '+name)
            work=base/name;shutil.copytree(ROOT,work);(work/'checks'/filename).write_text(source.replace(old,new))
            for mode,flags in MODES:
                cp=invoke(flags,work/'checks'/filename,work)
                require(cp.returncode!=0 and label.encode() in cp.stderr,'formula mutation accepted or wrong failure '+name+' '+cp.stderr.decode())
                mutants.append({'case':name,'mode':mode,'expected_guard':label,'rejected':True})
        work=base/'rational_fixture';shutil.copytree(ROOT,work)
        path=work/'fixtures/moment_4.json';data=json.loads(path.read_text());data['weights'][0][0]+=1;path.write_text(json.dumps(data))
        for mode,flags in MODES:
            cp=invoke(flags,work/'checks/check_moment_certificates.py',work)
            require(cp.returncode!=0 and b'positive normalized weights' in cp.stderr,'corrupt rational fixture accepted')
            mutants.append({'case':'rational_fixture_weight','mode':mode,'expected_guard':'positive normalized weights','rejected':True})
    require(snapshot()==before,'source package modified by replay')
    print(json.dumps({'status':'PASS','finite_checkers':9,'finite_executions':len(records),'guard_rejections':len(guards),'semantic_mutation_rejections':len(mutants),'modes':[m for m,_ in MODES],'source_tree_modified':False,'optimization_sensitive_assertions':False,'scope':'Finite exact formula and example replay only; no asymptotic probability conclusion.','checks':records,'guard_controls':guards,'semantic_controls':mutants},sort_keys=True,indent=2))
if __name__=='__main__':main()
