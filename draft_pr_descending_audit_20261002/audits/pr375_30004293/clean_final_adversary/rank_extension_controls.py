#!/usr/bin/env python3
"""Postseal new rank-compression and entire rank-two reinsertion controls."""
from mathematical_controls import canonical,inside,quotient,hist,prod
from fractions import Fraction as F
from collections import defaultdict
from itertools import combinations,product
import json,datetime

def restrictions():
    examples=0;fibers=0;rankbounds=0
    G=tuple(range(2,10))
    for include in product((0,1),repeat=len(G)):
        B=tuple(x for x,b in zip(G,include) if b)
        groups=defaultdict(list)
        for bits in product((0,1),repeat=len(B)):
            groups[sum(x*b for x,b in zip(B,bits))].append(bits)
        for family in groups.values():
            k=len(family)
            if k<2:continue
            columns=[tuple(row[j] for row in family) for j in range(len(B))]
            one=(1,)*k;basis=canonical((one,));selected=[]
            for v in columns:
                if not inside(v,basis):selected.append(v);basis=canonical((*basis,v))
            R=len(selected)
            assert k<=2**R;rankbounds+=1
            for r in range(1,min(R,4)+1):
                rows=[(1,)+tuple(v[i] for v in selected[:r]) for i in range(k)]
                chosen=[];rowbasis=()
                for i,row in enumerate(rows):
                    new=canonical((*rowbasis,row))
                    if len(new)>len(rowbasis):rowbasis=new;chosen.append(i)
                    if len(chosen)==r+1:break
                assert len(chosen)==r+1
                reduced=[family[i] for i in chosen]
                assert len(set(reduced))==r+1
                assert len({sum(x*b for x,b in zip(B,row)) for row in reduced})==1
                newcolumns=[tuple(row[j] for row in reduced) for j in range(len(B))]
                assert len(canonical(((1,)*(r+1),*newcolumns)))==r+1
                examples+=1
            fibers+=1
    return {'all_selected_sets':2**len(G),'nontrivial_entire_fibers':fibers,'rank_bound_checks':rankbounds,'independent_row_restrictions':examples}

def full_rank2_kernel():
    G=tuple(range(2,7));laws={}
    for bits in product((0,1),repeat=len(G)):
        B=frozenset(x for x,b in zip(G,bits) if b)
        laws[B]=prod(F(1,x) if x in B else F(x-1,x) for x in G)
    cube=tuple(product((0,1),repeat=3))
    classes=tuple(sorted({quotient(v) for v in cube}))
    bases=[(v,w) for v in classes for w in classes if len(canonical((v,w)))==2]
    events={B for B in laws if max(hist(B).values())>=3}
    covered=set();kernel=F(0);ghosts=0;valid=0;offtarget=0
    # Numerical reconstruction is audited for every affine target. Zero alone
    # contributes to the full-rank equal-sum event union.
    affine_targets=((0,0),(1,0),(0,-2),(3,3))
    for B,p in laws.items():
        entries=tuple(sorted(B))
        for v,w in bases:
            det=v[0]*w[1]-v[1]*w[0]
            for patterns in product(classes,repeat=len(entries)):
                ghosts+=1
                sum0=sum(a*q[0] for a,q in zip(entries,patterns));sum1=sum(a*q[1] for a,q in zip(entries,patterns))
                for target in affine_targets:
                    z0=target[0]-sum0;z1=target[1]-sum1
                    x=F(z0*w[1]-z1*w[0],det);y=F(v[0]*z1-v[1]*z0,det)
                    assert x*v[0]+y*w[0]+sum0==target[0]
                    assert x*v[1]+y*w[1]+sum1==target[1]
                    if target!=(0,0):offtarget+=1;continue
                    if x.denominator!=1 or y.denominator!=1:continue
                    x,y=int(x),int(y)
                    if not (x>y and x in G and y in G and x not in B and y not in B):continue
                    if any(a>x and q!=(0,0) for a,q in zip(entries,patterns)):continue
                    if any(y<a<x and len(canonical((v,q)))>1 for a,q in zip(entries,patterns)):continue
                    S=B|{x,y};assert S in events
                    assert laws[S]==p/F((x-1)*(y-1))
                    covered.add(S);kernel+=p/F((x-1)*(y-1));valid+=1
    assert covered==events
    actual=sum((laws[B] for B in events),F(0))
    assert actual<=kernel
    return {'ground':G,'entire_law_configurations':len(laws),'all_ordered_independent_quotient_bases':len(bases),'ghost_free_assignments':ghosts,'arbitrary_affine_target_identities':offtarget,'valid_distinct_root_reinsertions':valid,'all_rank2_collision_configurations':len(events),'covered':len(covered),'exact_event_probability':str(actual),'exact_union_weight':str(kernel)}

def coefficient_certificate():
    z=F(2,5);terms=30
    lower=2*sum((z**(2*i+1)/F(2*i+1) for i in range(terms)),F(0))
    upper=lower+2*z**(2*terms+1)/((2*terms+1)*(1-z*z))
    assert F(21,20)*upper<1
    return {'log_7_over_3_upper':str(upper),'certified_21_over_20_log_7_over_3_below_one':True}
if __name__=='__main__':
    print(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'rank_compression':restrictions(),'full_reinsertion_kernel':full_rank2_kernel(),'strict_coefficient':coefficient_certificate(),'meaning':'postseal finite falsifiers of the distinct stronger audit derivation; universal proof separately recorded'},indent=2))
