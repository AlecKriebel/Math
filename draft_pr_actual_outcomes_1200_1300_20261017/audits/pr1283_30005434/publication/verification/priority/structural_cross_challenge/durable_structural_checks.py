#!/usr/bin/env python3
"""Portable finite diagnostics. No files/private inputs are read or written.

The universal results are proved in CROSS_CHALLENGE.md. This program validates
named fixtures, the required equations, and explicit counterexamples. All checks
use explicit exceptions, including under Python -O/-OO. Output is deterministic
JSON on stdout. --inject-failure is a required negative control and exits 1.
"""
import argparse
import itertools
import json
import sys


class DiagnosticFailure(RuntimeError):
    pass


def require(predicate, message):
    if not predicate:
        raise DiagnosticFailure(message)


def all_tuples(elements, length):
    return itertools.product(elements, repeat=length)


def model_from_order(name, count, le, top):
    elements = tuple(range(count))
    table = []
    for x in elements:
        row = []
        for y in elements:
            lower = [z for z in elements if le(z, x) and le(z, y)]
            greatest = [z for z in lower if all(le(w, z) for w in lower)]
            require(len(greatest) == 1, name + ': pair lacks a unique meet')
            row.append(greatest[0])
        table.append(row)
    return name, elements, lambda x, y: table[x][y], top


def fixtures():
    chain = lambda n: model_from_order('chain' + str(n), n, lambda x,y:x<=y, n-1)
    boolean = lambda n: model_from_order('boolean' + str(2**n), 2**n, lambda x,y:(x&y)==x, 2**n-1)
    m3 = model_from_order('M3', 5, lambda x,y:x==y or x==0 or y==4, 4)
    n5 = model_from_order('N5', 5, lambda x,y:x==y or x==0 or y==4 or (x==1 and y==2), 4)
    return [chain(1), chain(4), boolean(2), boolean(3), m3, n5]


def properties(elements, meet, op, e):
    le = lambda x,y:meet(x,y)==x
    pairs = tuple(all_tuples(elements, 2))
    triples = tuple(all_tuples(elements, 3))
    return {
        'meet_idempotent': all(meet(x,x)==x for x in elements),
        'meet_commutative': all(meet(x,y)==meet(y,x) for x,y in pairs),
        'meet_associative': all(meet(meet(x,y),z)==meet(x,meet(y,z)) for x,y,z in triples),
        'greatest_e': all(le(x,e) for x in elements),
        'left_logical_unit': all(op(e,x)==x for x in elements),
        'right_absorption': all(op(x,e)==e for x in elements),
        'diagonal': all(op(x,x)==e for x in elements),
        'separation': all(x==y or op(x,y)!=e or op(y,x)!=e for x,y in pairs),
        'order_compatibility': all((op(x,y)==e)==le(x,y) for x,y in pairs),
        'cycloid': all(op(op(x,y),op(x,z))==op(op(y,x),op(y,z)) for x,y,z in triples),
        'meet_preservation': all(op(x,meet(y,z))==meet(op(x,y),op(x,z)) for x,y,z in triples),
        'mixed_identity': all(op(meet(x,y),z)==op(op(x,y),op(x,z)) for x,y,z in triples),
        'H4': all(op(x,meet(x,y))==op(x,y) for x,y in pairs),
        'hemiimplication': all(le(meet(x,op(x,y)),y) for x,y in pairs),
        'left_map_absorption': all(not le(u,x) or op(u,op(x,z))==op(u,z) for u,x,z in triples),
        'discrete': all(not le(x,y) or x==y or y==e for x,y in pairs),
    }


def partial_product_condition(elements, meet, op):
    le = lambda x,y:meet(x,y)==x
    products = {}
    for x,y in all_tuples(elements,2):
        candidates = [z for z in elements if le(z,y) and op(y,z)==x]
        require(len(candidates)<=1, 'L partial product is not unique')
        if candidates:
            products[x,y]=candidates[0]
    for y,z in all_tuples(elements,2):
        p=op(y,z)
        require((p,y) in products, 'Rump3.4 candidate product missing')
        require(products[p,y]==meet(y,z), 'Rump3.4 candidate product differs from supplied meet')
        suitable=[x for x in elements if (x,y) in products and le(products[x,y],z)]
        require(p in suitable and all(le(x,p) for x in suitable), 'Rump3.4 greatest-element condition failed')
    return True


def n5_scope_diagnostics(elements, meet, e):
    le=lambda x,y:meet(x,y)==x
    def join(x,y):
        upper=[u for u in elements if le(x,u) and le(y,u)]
        least=[u for u in upper if all(le(u,v) for v in upper)]
        require(len(least)==1, 'N5 join not unique')
        return least[0]
    def covers(upper,lower):
        return upper!=lower and le(lower,upper) and not any(z!=lower and z!=upper and le(lower,z) and le(z,upper) for z in elements)
    # N5 labels 0=0,a=1,b=2,c=3,e=4, with 0<a<b<e and 0<c<e.
    require(join(2,3)==e and covers(e,3), 'N5 lower-semimodular premise missing')
    require(meet(2,3)==0 and not covers(2,0), 'N5 lower-semimodular failure missing')
    def closure(subset):
        inf=e
        for x in subset:
            inf=meet(inf,x)
        return {u for u in elements if u!=e and le(inf,u)}
    A=closure({2})
    B=closure({1})
    D=closure({2,3})
    require(A < B < D, 'N5 closure interval is not a strict intermediate interval')
    return {
        'labels':['0','a','b','c','e'],
        'lower_semimodularity_counterexample':{'x':'b','y':'c','join':'e','join_covers_y':True,'x_meet_y':'0','x_covers_meet':False},
        'closure_exchange_counterexample':{'A':[2],'B':[1],'added_x':3,'closure_A':sorted(A),'closure_B':sorted(B),'closure_A_plus_x':sorted(D)},
    }


def run_checks(inject_failure):
    if inject_failure:
        require(False, 'injected false predicate')
    results={}
    for name,elements,meet,e in fixtures():
        op=lambda x,y: e if meet(x,y)==x else meet(x,y)
        p=properties(elements,meet,op,e)
        for key,value in p.items():
            if key!='discrete':
                require(value, name+': '+key+' failed')
        p['Rump3_4_partial_product_condition']=partial_product_condition(elements,meet,op)
        if name=='N5':
            require(not p['discrete'], 'N5 unexpectedly discrete')
            p['scope_diagnostics']=n5_scope_diagnostics(elements,meet,e)
        results[name]=p
    # The four workshop equations hold for right projection at each point.
    e_set=tuple(range(4))
    for point in e_set:
        p=properties(e_set,min,lambda x,y:y,point)
        for key in ['left_logical_unit','right_absorption','cycloid','meet_preservation','mixed_identity']:
            require(p[key], 'Right projection at point '+str(point)+': '+key+' failed')
        require(not p['diagonal'], 'Nontrivial right projection unexpectedly satisfies the L diagonal')
    results['right_projection']={'chain4_all_four_prescribed_points':True,'not_L_on_chain4':True}
    # Different old order implication: failure on Boolean four at distinct atoms.
    meet=lambda x,y:x&y
    old=lambda x,y:3 if meet(x,y)==x else y
    left=old(1,meet(1,2)); right=meet(old(1,1),old(1,2))
    require(left==0 and right==2 and left!=right, 'Old order implication negative witness failed')
    results['old_order_implication_counterexample']={'x':1,'y':1,'z':2,'lhs':left,'rhs':right}
    # hIS4 + all logical unit/order laws + meet preservation need not be cycloid.
    table=[[3,3,3,3],[0,3,3,3],[0,0,3,3],[0,1,2,3]]
    op=lambda x,y:table[x][y]
    p=properties(e_set,min,op,3)
    for key in ['H4','hemiimplication','left_logical_unit','right_absorption','diagonal','separation','order_compatibility','meet_preservation']:
        require(p[key], 'hIS4 counterexample missing '+key)
    left=op(op(1,2),op(1,0)); right=op(op(2,1),op(2,0))
    require(left==0 and right==3 and not p['cycloid'] and not p['mixed_identity'], 'hIS4 cycloid/mixed negative witness failed')
    results['hIS4_counterexample']={'table':table,'cycloid_witness':{'x':1,'y':2,'z':0,'lhs':left,'rhs':right},'meet_preservation':True,'mixed_identity':False}
    return {'status':'passed','scope':'Named finite diagnostics only; universal and canonical-closure arguments are mathematical proofs in CROSS_CHALLENGE.md.','results':results}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--inject-failure',action='store_true',help='Deliberately fail an explicit false predicate; required negative control')
    args=parser.parse_args()
    try:
        result=run_checks(args.inject_failure)
    except DiagnosticFailure as error:
        print(json.dumps({'status':'failed','failure':str(error)},sort_keys=True,indent=2))
        return 1
    print(json.dumps(result,sort_keys=True,indent=2))
    return 0


if __name__=='__main__':
    sys.exit(main())
