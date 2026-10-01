#!/usr/bin/env python3
"""Independent finite semantic controls. These are not KPU or definability tests."""
from itertools import product
from collections import Counter
from pathlib import Path
import hashlib,json
counts=Counter()
def check(ok,kind):
    if not ok:raise AssertionError(kind)
    counts[kind]+=1

def powerset(n):
    return [frozenset(i for i in range(n) if m>>i&1) for m in range(1<<n)]

# Exhaust all small surjections, all target bounds, all unary truth predicates,
# and all exact cover subsets. This uses uneven as well as duplicate fibers.
surjections=0
for bsize in range(1,4):
    B=range(bsize)
    for asize in range(bsize,5):
        for nu in product(B,repeat=asize):
            if set(nu)!=set(B):continue
            surjections+=1
            A=range(asize); cover_candidates=powerset(asize)
            for bound in powerset(bsize):
                family=[c for c in cover_candidates if {nu[x] for x in c}==bound]
                check(bool(family),'total_exact_cover_family')
                for truth in powerset(bsize):
                    expected_ex=bool(bound&truth);expected_all=bound<=truth
                    results=[]
                    for c in family:
                        ex=any(nu[x] in truth for x in c)
                        univ=all(nu[x] in truth for x in c)
                        check((ex,univ)==(expected_ex,expected_all),'both_bounded_quantifiers')
                        results.append((ex,univ))
                    check(any(x[0] for x in results)==expected_ex and any(x[1] for x in results)==expected_all,'existential_nonfunctional_cover_choice')
            for x,y in product(A,repeat=2):
                eq=nu[x]==nu[y]
                check(eq==(any(nu[x]==b==nu[y] for b in B)),'quotient_equality')

# A small AST interpreter independently checks nesting, Boolean operations,
# an unbounded existential, sort predicates, equality and parameter choices.
# Covers here are external subsets for diagnostics only, not internal A-sets.
forms=[
 ('all','x','y',('some','z','x',('P','z'))),
 ('some','x','y',('all','z','x',('notP','z'))),
 ('all','x','y',('exists','z',('and',('eq','z','x'),('or',('P','z'),('notP','x'))))),
 ('some','x','y',('or',('eq','x','p'),('notP','p'))),
 ('all','x','y',('or',('notSet','x'),('all','z','x',('neq','z','p')))),
 ('exists','x',('and',('eq','x','p'),('all','z','x',('P','z')))),
 ('and',('all','x','y',('P','x')),('some','x','y',('neq','x','p'))),
 ('or',('all','x','p',('notP','x')),('some','x','y',('Set','x'))),
]

def eval_formula(form,env,nu,members,sorts,truth,families,translated):
    op=form[0]
    image=lambda variable:nu[env[variable]] if translated else env[variable]
    if op in ('P','notP','Set','notSet'):
        val=image(form[1]) in (truth if 'P' in op else sorts)
        return not val if op.startswith('not') else val
    if op in ('eq','neq'):
        val=image(form[1])==image(form[2])
        return val if op=='eq' else not val
    if op in ('and','or'):
        a=eval_formula(form[1],env,nu,members,sorts,truth,families,translated)
        b=eval_formula(form[2],env,nu,members,sorts,truth,families,translated)
        return a and b if op=='and' else a or b
    if op=='exists':
        _,v,body=form
        domain=range(len(nu)) if translated else range(len(members))
        return any(eval_formula(body,dict(env,**{v:x}),nu,members,sorts,truth,families,translated) for x in domain)
    _,v,bound,body=form
    q=all if op=='all' else any
    ranges=families[image(bound)] if translated else [members[image(bound)]]
    return any(q(eval_formula(body,dict(env,**{v:x}),nu,members,sorts,truth,families,translated) for x in cover) for cover in ranges)

nu=(2,0,1,2,0)
possible_edges=((0,1),(0,2),(1,2))
for edge_bits in range(8):
    members={y:frozenset(x for k,(x,z) in enumerate(possible_edges) if y==z and edge_bits>>k&1) for y in range(3)}
    covers=powerset(len(nu))
    families={y:[c for c in covers if {nu[x] for x in c}==members[y]] for y in range(3)}
    # Both an empty set and a distinct urelement are tested where possible.
    for sorts in powerset(3):
        if any(members[y] and y not in sorts for y in range(3)):continue
        for truth in powerset(3):
            for y,p in product(range(len(nu)),repeat=2):
                for form in forms:
                    actual=eval_formula(form,{'y':y,'p':p},nu,members,sorts,truth,families,True)
                    expected=eval_formula(form,{'y':nu[y],'p':nu[p]},nu,members,sorts,truth,families,False)
                    check(actual==expected,'nested_ast_with_parameters_sorts_and_exists')

# Finite analogue of collection's logical equivalence, not a KPU axiom check.
for bound in powerset(3):
    for relation in range(512):
        R=lambda z,u:bool(relation>>(3*z+u)&1)
        lhs=all(any(R(z,u) for u in range(3)) for z in bound)
        rhs=any(all(any(R(z,u) for u in d) for z in bound) for d in powerset(3))
        check(lhs==rhs,'finite_collection_equivalence')

# Explicit falsification controls for each indispensable semantic hypothesis.
check(all(x!=1 for x in [0])!=all(x!=1 for x in [0,1]),'reject_undercoverage')
check(any(x==1 for x in [0,1])!=any(x==1 for x in [0]),'reject_overcoverage')
check(any(all([]) for c in [])!=all([]),'reject_nontotal_cover_family')
check((0==1)!=((0//2)==(1//2)),'reject_literal_representative_equality')

root=Path(__file__).resolve().parent
print(json.dumps({'status':'PASS','assertions':sum(counts.values()),'surjections_tested':surjections,'categories':dict(counts),
 'author_receipt_expected_count_from_loop_sizes':2*30+340+3*4680+1384+2*36864+4,
 'proof_sha256':'16039e2409de331bead57262612c12e3ac08359669df4de7075804fd2917a002',
 'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
 'limitations':['Finite relational semantics only','Not KPU model validation','Not internal cover existence or Sigma definability','Not a proof of the original converse']},indent=2))
