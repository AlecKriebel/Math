#!/usr/bin/env python3
"""Independent exact audit. Never edits the supplied packet.
Usage: python3 -B check_independent.py PACKET NEW_EXTERNAL_OUTPUT_DIRECTORY
The output directory must not exist and is created outside PACKET. Mutation
copies are test fixtures; only JSON receipts are intended for publication.
"""
import ast
from fractions import Fraction
from functools import lru_cache
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

sys.dont_write_bytecode=True

def need(ok,msg):
    if not ok: raise RuntimeError(msg)

def pin(p):
    b=p.read_bytes()
    return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}

def inventory(p):
    return {q.name:pin(q) for q in sorted(p.iterdir())}

def ident(n):
    return tuple(tuple(int(i==j) for j in range(n)) for i in range(n))

def mul(a,b):
    n=len(a)
    return tuple(tuple(sum(a[i][k]*b[k][j] for k in range(n)) for j in range(n)) for i in range(n))

def inv(a):
    n=len(a); eye=ident(n)
    v=tuple(tuple(a[i][j]-eye[i][j] for j in range(n)) for i in range(n))
    power=eye; result=[list(row) for row in eye]
    for k in range(1,n):
        power=mul(power,v)
        for i in range(n):
            for j in range(n): result[i][j]+=(-1)**k*power[i][j]
    ans=tuple(tuple(row) for row in result)
    need(mul(a,ans)==eye and mul(ans,a)==eye,'matrix inverse')
    return ans

def comm(a,b): return mul(mul(mul(a,b),inv(a)),inv(b))

@lru_cache(None)
def shapes(n):
    if n==1: return (None,)
    return tuple((a,b) for k in range(1,n) for a in shapes(k) for b in shapes(n-k))

def matrix_tree(shape,n,start=0,twist=False,depth=0):
    if shape is None:
        a=[list(row) for row in ident(n+1)]; a[start][start+1]=1
        value=tuple(tuple(row) for row in a);end=start+1;sign=1
    else:
        a,m,s=matrix_tree(shape[0],n,start,twist,depth+1)
        b,end,t=matrix_tree(shape[1],n,m,twist,depth+1)
        value=comm(a,b);sign=s*t
    if twist:
        g=[list(row) for row in ident(n+1)]
        for i in range(n): g[i][i+1]=i+1
        g=tuple(tuple(row) for row in g)
        value=mul(mul(g,value),inv(g))
        if (start+depth)%2: value=inv(value);sign=-sign
    return value,end,sign

def matrix_tests():
    records=[]
    for n in range(1,9):
        for shape in shapes(n):
            for twist in [False,True]:
                value,end,sign=matrix_tree(shape,n,twist=twist)
                goal=[list(row) for row in ident(n+1)];goal[0][n]+=sign
                need(value==tuple(tuple(row) for row in goal),'distinct-letter matrix detection')
                need(end==n,'leaf indexing')
        records.append({'leaves':n,'all_ordered_binary_shapes':len(shapes(n)), 'variants_per_shape':2})
    a,_,_=matrix_tree((None,None),2)
    need(comm(a,a)==ident(3),'repeated-word commutator must vanish')
    return {'method':'independent integral unipotent matrices; no packet algebra imported',
            'records':records,'total_shapes':sum(r['all_ordered_binary_shapes'] for r in records),
            'repeated_word_negative_control':True}

def topology_samples():
    def wave(x):
        r=x-x.numerator//x.denominator
        return 2*r if r<=Fraction(1,2) else 2-2*r
    rows=[]
    for m in [1,2,3,10,100,1000]:
        t=Fraction(2*m,2*m+1); x=Fraction(m)
        delta=t*wave(x/t)-wave(x)
        need(delta==t and t>=Fraction(2,3),'uniform-topology counterexample witness')
        rows.append({'m':m,'t':str(t),'displacement_difference':str(delta)})
    return {'joint_ambient_continuity_not_uniform_metric_continuity':rows,
            'meaning':'For f(x,y)=(x,y+triangle(x)), t approaches 1 while differences at x=m approach 1.'}

def main():
    need(len(sys.argv)==3,'supply packet and new output directory')
    packet=Path(sys.argv[1]).resolve();out=Path(sys.argv[2]).resolve()
    need(packet not in out.parents and packet!=out,'output must be external')
    need(not out.exists(),'output directory already exists')
    need(os.geteuid()==1000,'this audit requires actual UID 1000')
    out.mkdir(parents=True);fixtures=out/'fixtures';fixtures.mkdir()
    before=inventory(packet)
    records=[];env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1')
    def run(label,target,flags=(),arguments=(),expected=0,error=None):
        command=[sys.executable,'-B',*flags,str(target/'check_claims.py'),*map(str,arguments)]
        r=subprocess.run(command,env=env,capture_output=True,text=True)
        need(r.returncode==expected,label+' return code: '+r.stderr)
        if error: need(error in r.stderr,label+' rejection reason: '+r.stderr)
        # Canonical command contains no execution-local paths; output is unmodified.
        canonical=['python3','-B',*flags,'PACKET/check_claims.py']
        canonical += ['EXTERNAL_OUTPUT' if str(x)==str(out/'external.json') else
                      'PACKET/must_not_exist.json' if str(x)==str(packet/'must_not_exist.json') else str(x)
                      for x in arguments]
        row={'name':label,'command':canonical,'returncode':r.returncode,'stdout':r.stdout,'stderr':r.stderr}
        records.append(row);return r
    for flags,label in [((),'normal'),(('-O',),'O'),(('-OO',),'OO')]:
        r=run('frozen_'+label,packet,flags,('--require-readonly',))
        data=json.loads(r.stdout)
        need(data['uid']==1000 and data['readonly']['directory_create_denied'] and
             data['readonly']['existing_file_write_open_denials']==len(before),'actual permissions')
    run('inside_output_rejected',packet,('-OO',),('--require-readonly','--output',packet/'must_not_exist.json'),1,'output must be external')
    need(not (packet/'must_not_exist.json').exists(),'forbidden output appeared')
    r=run('external_output_succeeds',packet,(),('--require-readonly','--output',out/'external.json'))
    need(not r.stdout and json.loads((out/'external.json').read_text())['status']=='passed','external output')
    def clone(label):
        target=fixtures/label;shutil.copytree(packet,target)
        target.chmod(0o755)
        for p in target.iterdir():p.chmod(0o644)
        return target
    target=clone('writable')
    run('writable_tree_rejected',target,('-O',),('--require-readonly',),1,'packet directory is writable')
    target=clone('report_byte_mutation')
    with (target/'REPORT.md').open('a') as f:f.write('\nIndependent mutation control.\n')
    run('report_mutation_rejected',target,('-OO',),(),1,'pinned byte count mismatch: REPORT.md')
    changes=[
      ('dilation_wrong_argument','t*pl_value(points,x/t)','t*pl_value(points,t*x)','track diameter bound failed'),
      ('interval_target_on_C','u=l+F(2,5)*L; v=l+F(3,5)*L','u=l; v=l+L/10','target gap meets next Cantor stage'),
      ('magnus_wrong_inverse','return u+v+inverse_word(u)+inverse_word(v)','return u+v+inverse_word(v)+inverse_word(u)','full Magnus leading term failed'),
      ('duality_drop_infinity','if degree==0:return N  # reduced H^0','if degree==0:return 0  # reduced H^0','H2 dimension boundary failed'),
      ('radial_expands','a=multiplier*r','a=r/multiplier','PL strict monotonicity required')]
    mutations=[]
    for label,old,new,reason in changes:
        target=clone(label);script=target/'check_claims.py';s=script.read_text()
        need(s.count(old)==1,'mutation must have one exact target')
        script.write_text(s.replace(old,new))
        pins=json.loads((target/'PAYLOAD_PINS.json').read_text())
        for p in pins['files']:
            if p['path']=='check_claims.py':p.update(pin(script))
        (target/'PAYLOAD_PINS.json').write_text(json.dumps(pins,indent=2)+'\n')
        r=run(label,target,('-OO',),(),1,reason)
        need('pinned ' not in r.stderr,'semantic mutation was caught only by a pin')
        mutations.append({'name':label,'checker':pin(script),'pin_file':pin(target/'PAYLOAD_PINS.json'),
                          'rejection':reason,'checker_pin_updated_before_run':True})
    matrices=matrix_tests();topology=topology_samples()
    need(before==inventory(packet),'original packet bytes changed')
    need(not any(isinstance(n,ast.Assert) for n in ast.walk(ast.parse(Path(__file__).read_text()))),'audit relies on assert')
    receipt={'status':'passed','uid':os.geteuid(),'python_optimization':sys.flags.optimize,
             'original_packet_unchanged':True,'packet_inventory':before,'runs':records,
             'external_output_contents':json.loads((out/'external.json').read_text()),
             'semantic_mutations':mutations,'independent_matrices':matrices,'topology_examples':topology,
             'limits':'Finite checks support the authored audit; they do not prove the imported topological theorems.'}
    (out/'INDEPENDENT_RUNS.json').write_text(json.dumps(receipt,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'passed','checker_executions':len(records),'semantic_mutations':len(mutations),
                      'independent_shapes':matrices['total_shapes'],'original_packet_unchanged':True}))

if __name__=='__main__':main()
