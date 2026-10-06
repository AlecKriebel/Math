#!/usr/bin/env python3
"""Independent signed-matching dynamic program versus the reviewed formula.
Requires a pinned payload; no representation-theoretic existence assertion.
"""
import sys
if not (sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode):
    raise SystemExit('Use python -I -S -B')
from functools import lru_cache
from itertools import combinations_with_replacement, product
import hashlib
import importlib.util
import json
from pathlib import Path

PIN = '1f1dae9e6a5123d86febe4d485dc5b29e7a43d1ff484a0915816acb4f18f0032'
def need(ok, message):
    if not ok: raise ValueError(message)

def load_checked(path, name):
    spec=importlib.util.spec_from_file_location(name,path)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module

def signed_counts(labels):
    """Coefficient p counts compatible matchings with p positive signature slots.
    An unpaired tau-fixed label may be positive or negative. A compatible pair
    consumes one slot of each sign, with no orientation factor. This avoids
    generating involution permutations or using factorial/binomial formulas.
    """
    n=len(labels)
    @lru_cache(None)
    def visit(mask):
        if not mask: return (1,)
        bit=mask & -mask; i=bit.bit_length()-1;rest=mask ^ bit
        out=[0]*(mask.bit_count()+1)
        def add(poly,shift):
            for degree,value in enumerate(poly):out[degree+shift]+=value
        if labels[i][0]==0:
            poly=visit(rest);add(poly,0);add(poly,1)
        choices=rest
        while choices:
            other=choices & -choices;choices^=other;j=other.bit_length()-1
            if labels[j]==(-labels[i][0],labels[i][1]):
                add(visit(rest ^ other),1)
        return tuple(out)
    return visit((1<<n)-1)

def main():
    root=Path(sys.argv[1]);pin=sys.argv[2]
    bootstrap=Path(__file__).with_name('isolated_bootstrap.py')
    need(hashlib.sha256(bootstrap.read_bytes()).hexdigest()==PIN,'Bootstrap source pin')
    loader=load_checked(bootstrap,'reviewed_bootstrap');data=loader.snapshot(root,pin)
    # Compile the validated bytes rather than reopening mutable payload source.
    namespace={'__name__':'independent_checked_formula'}
    exec(compile(data['math_checks.py'],'<validated math_checks.py>','exec'),namespace)
    formula=namespace['formula'];patterns=signatures=0
    for a0,a1,b0,b1 in product(range(9),repeat=4):
        n=a0+a1+2*(b0+b1)
        if 1<=n<=8:
            labels=[(0,0)]*a0+[(0,1)]*a1+[(1,0)]*b0+[(-1,0)]*b0+[(2,1)]*b1+[(-2,1)]*b1
            result=signed_counts(tuple(labels));patterns+=1
            for p in range(n+1):need(result[p]==formula(labels,p,n-p),'Author-universe mismatch');signatures+=1
    need((patterns,signatures)==(174,1266),'Author-universe count mismatch')
    alphabet=((0,3+4j),(0,5+6j),(1,3+4j),(-1,3+4j),(2,5+6j),(-2,5+6j))
    expanded=cases=unstable=0
    for n in range(1,9):
        for ix in combinations_with_replacement(range(len(alphabet)),n):
            labels=tuple(alphabet[i] for i in ix);vals=signed_counts(labels);expanded+=1
            stable=all(labels.count(x)==labels.count((-x[0],x[1])) for x in labels)
            unstable+=not stable
            for p,v in enumerate(vals):
                need(v==formula(labels,p,n-p),'Expanded-universe mismatch')
                need(v==formula(labels[::-1],p,n-p),'Reordering mismatch');cases+=1
            if not stable:need(not any(vals),'Unstable pattern has a matching')
    # More distinct blocks than the author's two-fixed/two-pair universe.
    extras=[((0,j) for j in range(8)),((0,0),(0,0),(0,1),(0,1),(0,2),(0,2)),((1,0),(-1,0),(2,1),(-2,1),(3,2),(-3,2))]
    for values in extras:
        labels=tuple(values);vals=signed_counts(labels)
        for p,v in enumerate(vals):need(v==formula(labels,p,len(labels)-p),'Additional block mismatch')
    print(json.dumps({'status':'pass','author_universe_patterns':patterns,'author_universe_signatures':signatures,'expanded_multisets':expanded,'expanded_signature_cases':cases,'expanded_unstable_multisets':unstable,'extra_block_examples':len(extras),'maximum_n':8,'method':'bitmask signed-matching coefficient recurrence, independent of labelled involution enumeration and closed formula','scope':'Finite regression only; not distinction or general-converse verification'},sort_keys=True))
if __name__=='__main__':main()
