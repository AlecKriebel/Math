#!/usr/bin/env python3
"""Independent finite controls for the pointed-object counterexample.

These are regression and mutation controls, not a proof of an infinite-category
claim or a formal proof certificate.  Only the Python standard library is used.
"""
import hashlib
import itertools as it
import json
from functools import lru_cache
from pathlib import Path

COUNTS = {}

def check(name, condition):
    if not condition:
        raise AssertionError(name)
    COUNTS[name] = COUNTS.get(name, 0) + 1

# An object is its actual cardinality; element 0 is its distinguished point.
def maps(s, t, injective=False):
    if injective:
        return [(0,) + p for p in it.permutations(range(1, t), s - 1)]
    return [(0,) + p for p in it.product(range(t), repeat=s - 1)]

def make_evaluator(max_size, injective=False, discrete=False, pointwise_all=False):
    arrows = {s: [(t, f) for t in range(1, max_size+1)
                  for f in maps(s,t,injective)] for s in range(1,max_size+1)}
    if discrete:
        arrows = {s: [(s,tuple(range(s)))] for s in arrows}
    @lru_cache(None)
    def force(phi, size, env=()):
        kind = phi[0]
        if kind == 'T': return True
        if kind == 'F': return False
        if kind == '=':
            value = lambda t: 0 if t == -1 else env[t]
            return value(phi[1]) == value(phi[2])
        if kind == '&': return all(force(p,size,env) for p in phi[1:])
        if kind == '|': return any(force(p,size,env) for p in phi[1:])
        if kind == 'E':
            return any(force(phi[1],size,env+(a,)) for a in range(size))
        if kind == '>':
            return all(not force(phi[1],t,tuple(f[a] for a in env)) or
                       force(phi[2],t,tuple(f[a] for a in env))
                       for t,f in arrows[size])
        if kind == 'A':
            successors = [(size,tuple(range(size)))] if pointwise_all else arrows[size]
            return all(force(phi[1],t,tuple(f[a] for a in env)+(b,))
                       for t,f in successors for b in range(t))
        raise ValueError(phi)
    return arrows, force

T,F = ('T',),('F',)
neg = lambda p: ('>',p,F)
eq = lambda a,b: ('=',a,b)
BETA = ('A',neg(neg(eq(0,-1))))
ALPHA = neg(BETA)
EXTRA = ('E',neg(eq(0,-1)))
SINGLETON = ('A',eq(0,-1))
DECIDABLE = ('A',('|',eq(0,-1),neg(eq(0,-1))))

# Independent pointwise interpretation for the positive fragment only.
def positive(phi,size,env):
    op=phi[0]
    if op=='T':return True
    if op=='F':return False
    if op=='=':
        vals=[0 if t==-1 else env[t] for t in phi[1:]]
        return vals[0]==vals[1]
    if op=='&':return all(positive(p,size,env) for p in phi[1:])
    if op=='|':return any(positive(p,size,env) for p in phi[1:])
    if op=='E':return any(positive(phi[1],size,env+(x,)) for x in range(size))
    raise ValueError(op)


def geometric_formulas():
    terms=(-1,0,1)
    base=[T,F]+[eq(a,b) for a in terms for b in terms]
    formulas=set(base)
    for p,q in it.product(base,repeat=2):
        formulas.update([('&',p,q),('|',p,q)])
    for a,b in it.product(terms,repeat=2):
        p=eq(2,a);q=eq(2,b)
        formulas.update([('E',('&',p,q)),('E',('|',p,q)),
                         ('E',('&',p,('E',('&',eq(3,2),eq(3,b))))),
                         ('|',F,('E',('&',p,q)),eq(0,1))])
    formulas.update([('|',),('&',),('E',F),('E',T),
                     ('&',('|',eq(0,-1),eq(0,1)),('E',eq(2,1)))])
    return sorted(formulas,key=repr)


def closure(n,E):
    # Floyd-Warshall closure, independent of the author's union-find.
    r=[[a==b for b in range(n)] for a in range(n)]
    for a,b in E:r[a][b]=r[b][a]=True
    for k in range(n):
        for a in range(n):
            for b in range(n):r[a][b] |= r[a][k] and r[k][b]
    reps=[min(b for b in range(n) if r[a][b]) for a in range(n)]
    roots=sorted(set(reps));q=tuple(roots.index(a) for a in reps)
    return r,q,roots

# A proof-producing verifier: witnesses are original context terms only.
def extract(phi,Erel,q,roots,term_env=(1,2)):
    def resolve(t):return 0 if t==-1 else term_env[t]
    kind=phi[0]
    if kind=='T':return ('truth',)
    if kind=='F':return None
    if kind=='=':
        a,b=map(resolve,phi[1:])
        return ('equality',a,b) if Erel[a][b] else None
    if kind=='&':
        pieces=[extract(p,Erel,q,roots,term_env) for p in phi[1:]]
        return None if any(p is None for p in pieces) else ('and',tuple(pieces))
    if kind=='|':
        for index,p in enumerate(phi[1:]):
            proof=extract(p,Erel,q,roots,term_env)
            if proof is not None:return ('or',index,proof)
        return None
    if kind=='E':
        for witness in roots:
            proof=extract(phi[1],Erel,q,roots,term_env+(witness,))
            if proof is not None:return ('exists',witness,proof)
        return None
    raise ValueError(kind)


def verify_proof(phi,proof,Erel,term_env=(1,2)):
    if proof is None:return False
    kind=phi[0]
    if kind=='T':return proof==('truth',)
    if kind=='F':return False
    if kind=='=':
        a,b=[0 if t==-1 else term_env[t] for t in phi[1:]]
        return proof==('equality',a,b) and Erel[a][b]
    if kind=='&':return proof[0]=='and' and len(proof[1])==len(phi)-1 and all(
        verify_proof(p,d,Erel,term_env) for p,d in zip(phi[1:],proof[1]))
    if kind=='|':return proof[0]=='or' and 0<=proof[1]<len(phi)-1 and verify_proof(
        phi[1+proof[1]],proof[2],Erel,term_env)
    if kind=='E':return proof[0]=='exists' and 0<=proof[1]<len(Erel) and verify_proof(
        phi[1],proof[2],Erel,term_env+(proof[1],))
    return False


def main():
    category_rows=[]
    for bound in range(1,6):
        for inj in [False,True]:
            arrows,force=make_evaluator(bound,inj)
            rows=[]
            for size in range(1,bound+1):
                # Bound 1 is a mandatory negative control: no growth exists.
                expected_beta=(not inj) or bound==1
                check('forcing_beta',force(BETA,size)==expected_beta)
                check('forcing_alpha',force(ALPHA,size)==(not expected_beta))
                check('forcing_extra',force(EXTRA,size)==(inj and size>1))
                check('forcing_decidable',force(DECIDABLE,size)==(inj or bound==1))
                for a in range(size):
                    check('element_double_negation',force(neg(neg(eq(0,-1))),size,(a,))==
                          (not inj or a==0))
                rows.append({'size':size,'beta':force(BETA,size),'alpha':force(ALPHA,size),
                             'exists_nonpoint':force(EXTRA,size)})
            category_rows.append({'max_size':bound,'injective':inj,
                                  'maps':sum(map(len,arrows.values())),'rows':rows})

    C,cforce=make_evaluator(4,False)
    D,dforce=make_evaluator(4,True)
    formulas=geometric_formulas()
    for size in range(1,5):
        for env in it.product(range(size),repeat=2):
            for phi in formulas:
                p=positive(phi,size,env)
                check('geometric_pointwise_and_restriction',p==cforce(phi,size,env)==dforce(phi,size,env))
                if p:
                    for target,f in C[size]:
                        check('positive_homomorphism_preservation',positive(phi,target,tuple(f[a] for a in env)))

    pairs=list(it.combinations(range(3),2))
    for mask in it.product([0,1],repeat=len(pairs)):
        E=[p for use,p in zip(mask,pairs) if use]
        relation,q,roots=closure(3,E)
        for phi in formulas:
            holds=positive(phi,len(roots),q[1:])
            proof=extract(phi,relation,q,roots)
            check('quotient_witness_extraction',holds==(proof is not None))
            if holds:check('extracted_proof_verification',verify_proof(phi,proof,relation))
            # Exhaust all finite pointed valuations on up to 4 carrier elements.
            semantically_entailed=True
            for size in range(1,5):
                for env in it.product(range(size),repeat=2):
                    v=(0,)+env
                    if all(v[a]==v[b] for a,b in E):
                        if not positive(phi,size,env):semantically_entailed=False
            check('quotient_all_geometric_consequences',holds==semantically_entailed)

    # Antecedent false/empty joins never produce an artificial quotient branch.
    for size in range(1,5):
        for env in it.product(range(size),repeat=2):
            check('false_antecedent',not positive(('|',),size,env))
            check('inconsistent_positive_branch',not positive(('&',eq(0,1),F),size,env))
            check('empty_conjunction',positive(('&',),size,env))

    # Each named mutation below is demonstrably incompatible with the theorem.
    mutations={}
    _,wrong_all=make_evaluator(4,True,pointwise_all=True)
    mutations['pointwise_universal_at_singleton']=wrong_all(BETA,1) and not dforce(BETA,1)
    mutations['replace_alpha_by_existential']=dforce(ALPHA,1) and not dforce(EXTRA,1)
    mutations['drop_double_negation']=cforce(BETA,1) and not cforce(SINGLETON,1)
    _,discrete=make_evaluator(4,False,discrete=True)
    mutations['remove_all_proper_transition_maps']=discrete(BETA,1) and not discrete(ALPHA,1)
    mutations['use_injections_for_generic']=dforce(ALPHA,1) and not cforce(ALPHA,1)
    _,singleton_only=make_evaluator(1,True)
    mutations['omit_growth_entirely']=not singleton_only(ALPHA,1)
    mutations['claim_alpha_classically_valid']=not discrete(ALPHA,1) and discrete(ALPHA,2)
    for label,killed in mutations.items():check('mutation_rejected_'+label,killed)

    result={'status':'PASS','purpose':'independent finite regression controls only',
            'assertions':sum(COUNTS.values()),'counts':COUNTS,
            'geometric_formulas':len(formulas),'equality_premise_sets':8,
            'category_rows':category_rows,'negative_controls_rejected':len(mutations),
            'mutations':mutations}
    path=Path(__file__).with_name('audit_controls.json')
    path.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':'PASS','assertions':result['assertions'],
                      'geometric_formulas':len(formulas),'negative_controls_rejected':len(mutations)},indent=2))

if __name__=='__main__':main()
