#!/usr/bin/env python3
"""Exact finite probes of two rejected inverse-limit construction mechanisms.

No finite computation is a proof of the full21.122 dichotomy. The accompanying
notes supply the unrestricted proofs for the restricted model families.
"""
from itertools import permutations,product,combinations
from datetime import datetime,timezone
from pathlib import Path
from hashlib import sha256
import json

HERE=Path(__file__).resolve().parent

def mul(p,q): return tuple(p[q[i]] for i in range(len(p)))
def inv(p):
    q=[0]*len(p)
    for i,j in enumerate(p): q[j]=i
    return tuple(q)
def inverse_word(w): return [-a for a in w[::-1]]
def comm(a,b): return inverse_word(a)+inverse_word(b)+a+b
def evaluate(w,gs):
    identity=tuple(range(len(gs[0])))
    vals={i+1:g for i,g in enumerate(gs)}
    vals.update({-i-1:inv(g) for i,g in enumerate(gs)})
    v=identity
    for letter in w: v=mul(v,vals[letter])
    return v
def parity(p): return sum(p[i]>p[j] for i in range(len(p)) for j in range(i+1,len(p)))%2

def words():
    c=comm([1],[2]); cx=[-1]+c+[1]
    return {'x_fourth':[1]*4,
            'commutator_squared':c+c,
            'commutator_with_its_x_conjugate':comm(c,cx),
            'squared_commutator_of_squares':comm([1,1],[2,2])*2}

def union_power_count(sets,n):
    total=0
    for size in range(1,len(sets)+1):
        for ix in combinations(range(len(sets)),size):
            joint=set.intersection(*(sets[i] for i in ix))
            total+=(-1)**(size+1)*len(joint)**n
    return total

def finite_controller():
    group=list(permutations(range(4)))
    out={}
    for name,w in words().items():
        restricted={(a,b):set() for a,b in product(range(2),repeat=2)}
        for x,y in product(group,repeat=2):
            restricted[(parity(x),parity(y))].add(evaluate(w,(x,y)))
        sets=list(restricted.values())
        all_values=set.union(*sets)
        assert union_power_count(sets,1)==len(all_values)
        explicit_two=set.union(*(set(product(s,repeat=2)) for s in sets))
        assert union_power_count(sets,2)==len(explicit_two)
        out[name]={'fixed_word':w,'parity_fiber_counts':{str(k):len(v) for k,v in restricted.items()},
          'word_image_on_n_fold_fiber_product':{str(n):union_power_count(sets,n) for n in range(1,13)},
          'exact_n2_union_crosscheck':len(explicit_two),
          'interpretation':'If any parity fiber has at least2 values, the infinite fixed-C2 fiber product has continuum many values.'}
    return out

def tree_groups():
    groups=[[(0,)]]
    for depth in range(1,4):
        prev=groups[-1]; half=2**(depth-1)
        group=[]
        for a,b,swap in product(prev,prev,range(2)):
            left=tuple(x+swap*half for x in a)
            right=tuple(x+(1-swap)*half for x in b)
            group.append(left+right)
        assert len(set(group))==2**(2**depth-1)
        groups.append(group)
    out=[]
    for depth,group in enumerate(groups[1:],1):
        n=2**depth; half=n//2
        tau=tuple(range(half,n))+tuple(range(half))
        centralizers=sum(mul(g,tau)==mul(tau,g) for g in group)
        classes={mul(mul(inv(g),tau),g) for g in group}
        assert len(group)//centralizers==len(classes)==len(groups[depth-1])
        vals={}
        for name,w in words().items():
            vals[name]=len({evaluate(w,(x,y)) for x,y in product(group,repeat=2)})
        out.append({'depth':depth,'order':len(group),'root_flip_class_size':len(classes),
                    'root_flip_centralizer_order':centralizers,'word_image_sizes':vals})
    formula=[{'depth':d,'group_log2_order':2**d-1,'root_flip_class_log2_size':2**(d-1)-1} for d in range(1,13)]
    return {'exact_small_groups':out,'proved_wreath_recurrence':formula,
            'interpretation':'Root-flip conjugacy classes grow without bound; their inverse-limit class is infinite and hence at least continuum. General weak-branch exclusion is proved separately.'}

def main():
    root=HERE.parent
    inputs=('priority/sources/notebook21_fresh.txt','priority/sources/shumyatsky2401.15707v2.txt')
    result={'utc':datetime.now(timezone.utc).isoformat(),
            'status':'EXACT_RESTRICTED_MODEL_PROBES_ONLY',
            'input_sha256':{n:sha256((root/n).read_bytes()).hexdigest() for n in inputs},
            'finite_common_controller_S4_to_C2':finite_controller(),
            'binary_iterated_wreath':tree_groups()}
    (HERE/'finite_model_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
