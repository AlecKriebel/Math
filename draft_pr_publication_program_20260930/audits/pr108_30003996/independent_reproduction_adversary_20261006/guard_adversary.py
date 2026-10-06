#!/usr/bin/env python3
"""Load the exact definitions, then adversarially exercise their real predicates.
AST trimming omits top-level finite suites and receipt writes only. No originals modified.
"""
import ast,hashlib,json,sys
from pathlib import Path
family,script,attack=sys.argv[1:4]
p=Path(script).resolve();source=p.read_text();module=ast.parse(source)
# Keep the unchanged declarations before the first top-level census loop.
first_loop=next(i for i,n in enumerate(module.body) if isinstance(n,ast.For))
module.body=module.body[:first_loop]
if attack=='known_false':
    changed=0
    for n in ast.walk(module):
        if family=='author' and isinstance(n,ast.Assert) and isinstance(n.test,ast.Compare) and isinstance(n.test.left,ast.Name) and n.test.left.id=='feasible':
            n.test=ast.Constant(False);changed+=1
        elif family=='author' and isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id=='require' and n.args and isinstance(n.args[0],ast.Compare) and isinstance(n.args[0].left,ast.Name) and n.args[0].left.id=='feasible':
            n.args[0]=ast.Constant(False);changed+=1
    if family=='author' and changed!=1:raise RuntimeError('did not locate unique final guard')
if family=='author' and attack=='corrupt_cost':
    run=next(n for n in module.body if isinstance(n,ast.FunctionDef) and n.name=='run')
    location=next(i for i,n in enumerate(run.body) if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='sats' for t in n.targets))
    run.body[location:location]=ast.parse('cost[0][0,1]=cost[0][1,0]=7').body
ast.fix_missing_locations(module)
print(json.dumps({'family':family,'script_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'attack':attack,'optimization':sys.flags.optimize,'definition_load':'exact AST definitions; top-level census omitted; mutation explicitly described'},sort_keys=True),flush=True)
ns={'__file__':str(p),'__name__':'isolated_verifier_definitions'}
exec(compile(module,str(p),'exec'),ns)
if family=='author':
    if attack in ['known_false','corrupt_cost']:
        ns['run'](1,((1,),))
    elif attack=='cycles':
        for N,E in [(4,((0,1),(1,2),(0,2))),(3,((0,1),(0,1))), (3,((0,1),(1,2),(0,2)))]:
            ts=ns['alltrees'](N,E)
            if N==4 or len(set(E))<2:
                if ts:raise RuntimeError('cycle/disconnected graph returned a tree')
            elif len(ts)!=3:raise RuntimeError('three actual triangle trees missing')
    else:raise RuntimeError('unknown attack')
else:
    if attack=='known_false':ns['ck'](False,'known-false sentinel')
    elif attack=='corrupt_cost':
        construct=ns['construct']
        def corrupt(n,cl):
            N,E,C,K=construct(n,cl)
            C[0][0][1]=C[0][1][0]=7
            return N,E,C,K
        ns['construct']=corrupt
        ns['test'](1,((1,),))
    elif attack=='cycles':
        if ns['allowed_trees'](4,((0,1),(1,2),(0,2))):raise RuntimeError('cycle/disconnected graph returned a tree')
        if len(ns['allowed_trees'](3,((0,1),(1,2),(0,2))))!=3:raise RuntimeError('three actual triangle trees missing')
    else:raise RuntimeError('unknown attack')
print(json.dumps({'completed':True,'outcome':'valid_tree_enumeration_control_passed' if attack=='cycles' else 'false_or_corrupted_control_accepted','optimization':sys.flags.optimize},sort_keys=True))
