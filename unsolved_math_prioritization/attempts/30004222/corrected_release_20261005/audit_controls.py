#!/usr/bin/env python3
"""Independent finite diagnostics and witnesses; no imports from the frozen release.
The tests compare formulae, not directly computed all-rank web intersection forms.
"""
import argparse
from collections import Counter
from fractions import Fraction as F
from functools import lru_cache
from itertools import product
import json
from pathlib import Path


def partitions(length, bound):
    return [x for x in product(range(bound+1), repeat=length)
            if all(x[i] >= x[i+1] for i in range(length-1))]


def dominant(x):
    return tuple(sorted(x, reverse=True)) == tuple(x)


def pair_factors(old, new):
    ans = Counter()
    selected = []
    for i in range(len(old)):
        for j in range(i+1, len(old)):
            a = old[i]-old[j]+j-i
            b = new[i]-new[j]+j-i
            if a-b == 1:
                selected.append((i,j))
                ans[a] += 1
                ans[b] -= 1
    return compact(ans), selected


def compact(a):
    return {int(k): int(v) for k,v in sorted(a.items()) if v and k != 1}


@lru_cache(None)
def qinteger(m,q):
    assert m >= 1
    return sum(q**(m-1-2*i) for i in range(m))


def evaluate(a,q=F(1)):
    ans=F(1)
    for m,e in a.items():
        assert m >= 1
        ans *= qinteger(m,q)**e
    return ans


def conjugate(p,width):
    return tuple(sum(h >= j for h in p) for j in range(1,width+1))


def qbinomial_factors(top,bottom):
    assert 0 <= bottom <= top, (top,bottom)
    ans=Counter(range(top-bottom+1,top+1))
    ans.subtract(range(1,bottom+1))
    return ans


def lowering_norm_factors(tau,sigma):
    # Add a final blank row: sigma_s=0, hence a legal terminal label s.
    t=tuple(tau)+(0,)
    old=tuple(sigma)+(0,)
    s=len(t)
    N=[t[i]-old[i] for i in range(s)]
    ans=Counter()
    for i in range(s-1):
        for k in range(i+1,s):
            c=t[i]-t[k]+k-i
            ans.update(qbinomial_factors(c-1,N[i]))
            if k<s-1:
                ans.subtract(qbinomial_factors(c+N[k],N[i]))
    return compact(ans)


def row_factors(tau,sigma,include_last=True):
    t=tuple(tau)+(0,)
    ans=Counter()
    for i in range(len(tau)):
        N=t[i]-sigma[i]
        for k in range(i+1,len(tau)+int(include_last)):
            c=t[i]-t[k]+k-i
            for ell in range(1,sigma[k-1]-t[k]+1):
                assert c-ell-N > 0
                ans[c-ell]+=1
                ans[c-ell-N]-=1
    return compact(ans)


def full_dimension_ratio(old,new):
    a=F(1)
    for i in range(len(old)):
        for j in range(i+1,len(old)):
            a*=F(old[i]-old[j]+j-i,new[i]-new[j]+j-i)
    return a


def run():
    counts=Counter()
    per_n={}
    for n in range(2,7):
        valid=invalid=0
        for old in partitions(n,4):
            for mu in product((0,1),repeat=n):
                if not 0<sum(mu)<n:
                    continue
                new=tuple(x+y for x,y in zip(old,mu))
                ff,pairs=pair_factors(old,new)
                coordinate_pairs=[(i,j) for i in range(n) for j in range(i+1,n)
                                  if mu[i]==0 and mu[j]==1]
                assert pairs==coordinate_pairs
                assert sum(new)-sum(old)==sum(mu)
                has_zero=any(old[i]-old[j]+j-i-1==0 for i,j in pairs)
                assert dominant(new)==(not has_zero)
                if has_zero:
                    invalid+=1
                    continue
                valid+=1
                counts['central_shifts']+=1
                shifted=tuple(x-9 for x in old)
                shifted_new=tuple(x+y for x,y in zip(shifted,mu))
                assert pair_factors(shifted,shifted_new)[0]==ff
                value=evaluate(ff)
                assert value>=1
                for q in (F(2),F(3,2)):
                    positive=evaluate(ff,q)
                    negative=evaluate(ff,-q)
                    assert negative==(-1)**len(pairs)*positive
                    counts['q_sign_parity_evaluations']+=1
                # For n=2 the sl2 summands have the tensor product's parity.
                if n==2:
                    m=old[0]-old[1]
                    high=new[0]-new[1]
                    assert (high-m-1)%2==0
                    if mu==(0,1):
                        assert m>=1 and value==F(m+1,m)
                    else:
                        assert value==1
                    counts['rank_one_weight_parity_checks']+=1
        counts['admissible_vertical_strips']+=valid
        counts['inadmissible_vertical_strips']+=invalid
        per_n[str(n)]={'valid':valid,'invalid':invalid}

    per_rows={}
    # Independent horizontal-strip selection uses all partition pairs and an
    # explicit new-box-column test, not interlacing ranges.
    for r in range(1,6):
        universe=partitions(r,6)
        subtotal=0
        for tau in universe:
            for sigma in universe:
                if any(a>b for a,b in zip(sigma,tau)):
                    continue
                columns=[col for row in range(r)
                         for col in range(sigma[row]+1,tau[row]+1)]
                if len(columns)!=len(set(columns)):
                    continue
                alpha=conjugate(sigma,tau[0])
                beta=conjugate(tau,tau[0])
                root,_=pair_factors(alpha,beta)
                row=row_factors(tau,sigma)
                lowering=lowering_norm_factors(tau,sigma)
                assert root==row==lowering, (tau,sigma,root,row,lowering)
                for q in (F(1),F(2),F(3,2)):
                    assert evaluate(root,q)==evaluate(lowering,q)
                    counts['horizontal_q_rational_evaluations']+=1
                subtotal+=1
        per_rows[str(r)]=subtotal
        counts['horizontal_strips']+=subtotal
        counts['lowering_inverse_square_matches']+=subtotal

    old=(3,1,0);mu=(0,1,0);new=(3,2,0)
    correct=evaluate(pair_factors(old,new)[0])
    wrong=F(1)
    for i in range(3):
        for j in range(i+1,3):
            if mu[i]==1 and mu[j]==0:
                d=old[i]-old[j]+j-i
                wrong*=F(d,d-1)
    assert (correct,full_dimension_ratio(old,new),wrong)==(F(3,2),F(1),F(2))
    bottom=evaluate(row_factors((2,),(1,)))
    omitted=evaluate(row_factors((2,),(1,),False))
    assert (bottom,omitted)==(F(2),F(1))
    assert 3**2*correct==F(27,2)
    assert correct*correct!=correct  # positive square root cannot equal kappa
    bad_old=(0,0);bad_new=(0,1)
    assert not dominant(bad_new) and 0 in pair_factors(bad_old,bad_new)[0]

    # Minimal source-normalization witness from Eqs. (5.10)-(5.16).
    witness_norm=lowering_norm_factors((2,),(1,))
    assert witness_norm=={2:1}
    q1=evaluate(witness_norm,F(1));q2=evaluate(witness_norm,F(2))
    assert (q1,1/q1,q2,1/q2)==(F(2),F(1,2),F(5,2),F(2,5))
    # Scalar quantum-sl2 check: <fv,fv>=<v,efv>=[2]<v,v>.
    assert qinteger(2,F(2))==q2

    # The all-j product in printed Eq. (5.38) is not a single-step norm.
    previous=evaluate(lowering_norm_factors((2,),(1,)))
    terminal=evaluate(lowering_norm_factors((3,),(2,)))
    assert (previous,terminal,previous*terminal)==(F(2),F(3),F(6))

    # Eq. (2.15) as printed selects no roots. Repairing only the condition
    # while retaining outer-shape distances still gives an undefined [1]/[0].
    inner=(1,0);outer=(1,1)
    literal=[(i,j) for i in range(2) for j in range(i+1,2)
             if inner[i]==outer[i] and inner[j]==outer[j]+1]
    assert literal==[]
    assert inner[0]-inner[1]+1==2
    assert outer[0]-outer[1]+1-1==0

    # Source Conjecture 1 direction inconsistency under the usual left action.
    mu3=(0,1,1)
    # w sends mu3 to (1,1,0): e1->e3, e2->e1, e3->e2.
    w=(2,0,1);winv=tuple(w.index(i) for i in range(3))
    intended=[(i+1,j+1) for i in range(3) for j in range(i+1,3)
              if mu3[i]==0 and mu3[j]==1]
    printed=[(i+1,j+1) for i in range(3) for j in range(i+1,3)
             if winv[i]>winv[j]]
    assert intended==[(1,2),(1,3)] and printed==[(1,3),(2,3)]

    return {
        'status':'PASS',
        'scope':'Exact bounded formula diagnostics, not independent computation of all web intersection forms.',
        'counts':dict(counts),'vertical_by_dimension':per_n,'horizontal_by_rows':per_rows,
        'frozen_six_negatives':{
            'all_positive_roots':{'right':str(correct),'wrong':str(full_dimension_ratio(old,new)),'rejected':True},
            'reverse_root_orientation':{'right':str(correct),'wrong':str(wrong),'rejected':True},
            'rescale_basis':{'right':str(correct),'rescaled':str(9*correct),'rejected':True},
            'omit_bottom_row':{'right':str(bottom),'wrong':str(omitted),'rejected':True},
            'omit_dominance':{'old':[0,0],'new':[0,1],'denominator':0,'rejected':True},
            'norm_vs_square':{'square':'3/2','square_root_is_not_square':True,'rejected':True}},
        'source_normalization_reciprocal_witness':{
            'tableau_rows':[[1,2]],'parent_rows':[[1]],'s':2,
            'tau':[2,0],'sigma':[1,0],'N_1_2':1,'c_1_2':3,
            'old_gl_weight':[1,0],'mu':[0,1],'new_gl_weight':[1,1],
            'B_q':'[2]','N_prime_squared_q':'1/[2]','kappa_q':'[2]',
            'at_q1':{'B':str(q1),'N_prime_squared':str(1/q1),'kappa':str(q1)},
            'at_q2':{'B':str(q2),'N_prime_squared':str(1/q2),'kappa':str(q2)},
            'frozen_claim_rejected':True},
        'source_all_j_product_witness':{'tableau_rows':[[1,2,3]],'parent_rows':[[1,2]],
            'at_q1':{'B_step':str(terminal),'N_prime_step_squared':str(1/terminal),
                       'all_j_product':str(previous*terminal),'parent_all_j_product':str(previous)}},
        'source_partition_restatement_witness':{'old':[1,0],'new':[1,1],
            'literal_product':'1','condition_only_repair_denominator':0,'correct_kappa':'[2]'},
        'source_permutation_direction_witness':{'mu':mu3,'w_original_to_sorted':[3,1,2],
            'correct_pairs':intended,'printed_inverse_pairs':printed},
        'root_of_unity_boundary':{'old':[2,0],'mu':[0,1],'formula':'[3]/[2]',
            'q':'i','numerator':-1,'denominator':0,'unrestricted_specialization_rejected':True},
        'q_integer_q1_checks':{'range':[1,40], 'passed':all(qinteger(m,F(1))==m for m in range(1,41))}
    }

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--output');args=ap.parse_args()
    result=json.dumps(run(),indent=2,sort_keys=True)+'\n'
    if args.output:Path(args.output).write_text(result)
    print(result,end='')
