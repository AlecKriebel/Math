#!/usr/bin/env python3
"""Pre-candidate exact rational controls. No author code imported or read.
Inputs: built-in explicit matrices and full 3-state denominator-2 family.
Output: complete JSON, including every scan matrix and all distinct witnesses.
These computations check finite ingredients, not the infinite-tail theorem.
"""
from fractions import Fraction as F
from itertools import product
from math import gcd, lcm
import json

def matmul(a,b):
    return [[sum((a[i][k]*b[k][j] for k in range(len(b))),F(0)) for j in range(len(b[0]))] for i in range(len(a))]
def power(a,k):
    ans=[[F(i==j) for j in range(len(a))] for i in range(len(a))]
    for _ in range(k): ans=matmul(ans,a)
    return ans

def classes(p):
    n=len(p); reach=[[p[i][j]>0 or i==j for j in range(n)] for i in range(n)]
    for k in range(n):
        for i in range(n):
            for j in range(n): reach[i][j] |= reach[i][k] and reach[k][j]
    parts=[]; used=set()
    for i in range(n):
        if i in used: continue
        c=[j for j in range(n) if reach[i][j] and reach[j][i]]; used.update(c)
        if all(p[s][t]==0 for s in c for t in range(n) if t not in c): parts.append(c)
    result=[]
    for c in parts:
        dist={c[0]:0}; todo=[c[0]]
        for s in todo:
            for t in c:
                if p[s][t]>0 and t not in dist: dist[t]=dist[s]+1; todo.append(t)
        d=0
        for s in c:
            for t in c:
                if p[s][t]>0: d=gcd(d,abs(dist[s]+1-dist[t]))
        assert d>0
        phase=[[s for s in c if dist[s]%d==r] for r in range(d)]
        assert all(phase)
        assert all(p[s][t]==0 or (dist[t]-dist[s]-1)%d==0 for s in c for t in c)
        result.append({'states':c,'period':d,'phases':phase})
    return result

def stationary_class(p,c):
    m=len(c)
    a=[[p[c[j]][c[i]]-F(i==j) for j in range(m)]+[F(0)] for i in range(m-1)]
    a.append([F(1)]*m+[F(1)])
    for j in range(m):
        pivot=next(i for i in range(j,m) if a[i][j])
        a[j],a[pivot]=a[pivot],a[j]; div=a[j][j]; a[j]=[v/div for v in a[j]]
        for i in range(m):
            if i!=j:
                r=a[i][j]; a[i]=[v-r*w for v,w in zip(a[i],a[j])]
    out=[F(0)]*len(p)
    for j,s in enumerate(c): out[s]=a[j][-1]
    assert all(out[s]>0 for s in c)
    assert sum(out)==1 and matmul([out],p)[0]==out
    return out

def stationary(p):
    cs=classes(p); v=[F(0)]*len(p)
    for c in cs:
        q=stationary_class(p,c['states'])
        v=[x+y/len(cs) for x,y in zip(v,q)]
    assert matmul([v],p)[0]==v
    return v

def finite_chain(p,pi=None):
    n=len(p); pi=stationary(p) if pi is None else pi
    assert all(x>=0 for row in p for x in row) and all(sum(row)==1 for row in p)
    assert sum(pi)==1 and matmul([pi],p)[0]==pi
    pos=[i for i in range(n) if pi[i]>0]; null=[i for i in range(n) if pi[i]==0]
    assert all(p[i][j]==0 for i in pos for j in null)
    cs=classes(p)
    labels=[]; positive_witness=[]
    for c in cs:
        if not any(pi[s]>0 for s in c['states']): continue
        for ph in c['phases']:
            labels.append(ph)
            a=power(p,c['period'])
            witness=None
            for k in range(1,n*n+1):
                b=power(a,k)
                if all(b[s][t]>0 for s in ph for t in ph):
                    witness={'phase':ph,'period':c['period'],'skeleton_positive_power':k,'min_entry':min(b[s][t] for s in ph for t in ph)};break
            assert witness is not None
            positive_witness.append(witness)
    rev=[[pi[t]*p[t][s]/pi[s] for t in pos] for s in pos]
    revcs=classes(rev)
    translated=[sorted(pos[s] for s in ph) for c in revcs for ph in c['phases']]
    assert sorted(map(tuple,map(sorted,labels)))==sorted(map(tuple,translated))
    assert all(sum(row)==1 for row in rev)
    return {'P':p,'stationary':pi,'positive_support':pos,'null_support':null,'closed_classes':cs,'positive_labels':labels,'reverse_kernel_on_positive_support':rev,'reverse_labels':translated,'positive_skeleton_witnesses':positive_witness}

def mv(p,v):return [sum((x*y for x,y in zip(row,v)),F(0)) for row in p]

def word(p,e,w):
    v=[F(1)]*len(p)
    for a in reversed(w):v=[e[i][a]*x for i,x in enumerate(mv(p,v))]
    return v

def new_basis(basis,v):
    v=v[:]
    for pivot,b in basis:
        coef=v[pivot];v=[x-coef*y for x,y in zip(v,b)]
    if not any(v):return False
    j=next(i for i,x in enumerate(v) if x);v=[x/v[j] for x in v]
    basis.append((j,v));basis.sort(key=lambda z:z[0]);return True

def output_quotient(p,e,pi=None):
    detail=finite_chain(p,pi); pi=detail['stationary'];n=len(p)
    labels=detail['positive_labels'];initials=[]
    for ph in labels:
        mass=sum(pi[s] for s in ph);initials.append([pi[s]/mass if s in ph else F(0) for s in range(n)])
    words=[w for k in range(n) for w in product(range(len(e[0])),repeat=k)]
    vectors=[word(p,e,w) for w in words]
    signature=[[sum((x*y for x,y in zip(alpha,v)),F(0)) for v in vectors] for alpha in initials]
    groups=[]
    for i,sig in enumerate(signature):
        found=next((g for g in groups if signature[g[0]]==sig),None)
        if found is None:groups.append([i])
        else:found.append(i)
    basis=[];generation=[]
    for k in range(n+1):
        for w in product(range(len(e[0])),repeat=k):new_basis(basis,word(p,e,w))
        generation.append({'word_length':k,'dimension':len(basis)})
    assert generation[n]['dimension']==generation[n-1]['dimension']
    for a in range(len(e[0])):
        for _,v in basis[:]: assert not new_basis(basis,[e[i][a]*x for i,x in enumerate(mv(p,v))])
    witnesses=[]
    for i in range(len(labels)):
        for j in range(i+1,len(labels)):
            idx=next((k for k in range(len(words)) if signature[i][k]!=signature[j][k]),None)
            witnesses.append({'labels':[i,j],'equal_full_output_laws':idx is None,'first_distinguishing_word':None if idx is None else list(words[idx]),'probabilities':None if idx is None else [signature[i][idx],signature[j][idx]]})
    detail.update({'emissions':e,'conditional_initial_distributions':initials,'word_space_dimensions':generation,'observable_quotient_by_label_indices':groups,'pairwise_witnesses':witnesses})
    return detail

def fractions(matrix):return [[F(v) for v in row] for row in matrix]

def run():
    tests=[]
    cases=[
        ('one_state_zero_emission_symbol',[[1]],[[1,0]],None,[[0]]),
        ('period2_revealed',[[0,1],[1,0]],[[1,0],[0,1]],None,[[0],[1]]),
        ('period2_erased',[[0,1],[1,0]],[[1,0],[1,0]],None,[[0,1]]),
        ('nonergodic_classes_erased',[[1,0],[0,1]],[[F(1,2),F(1,2)]]*2,None,[[0,1]]),
        ('nonergodic_classes_revealed',[[1,0],[0,1]],[[1,0],[0,1]],None,[[0],[1]]),
        ('zero_mass_closed_class_and_transient',[[1,0,0],[0,1,0],[F(1,2),0,F(1,2)]],[[1,0],[0,1],[0,1]],[1,0,0],[[0]]),
        ('period2_vs_period3_erased',[[0,1,0,0,0],[1,0,0,0,0],[0,0,0,1,0],[0,0,0,0,1],[0,0,1,0,0]],[[F(1,2),F(1,2)]]*5,None,[[0,1,2,3,4]]),
        ('first_marginal_equal_word2_separates',[[0,0,1,0],[0,0,0,1],[F(1,2),F(1,2),0,0],[F(1,2),F(1,2),0,0]],[[1,0],[0,1],[1,0],[0,1]],None,[[0],[1]]),
        ('nonreversible_aperiodic',[[F(1,2),F(1,2),0],[0,F(1,2),F(1,2)],[F(1,2),0,F(1,2)]],[[1,0],[0,1],[F(1,2),F(1,2)]],None,[[0]])]
    for name,p,e,pi,expected in cases:
        d=output_quotient(fractions(p),fractions(e),None if pi is None else [F(v) for v in pi]);assert d['observable_quotient_by_label_indices']==expected
        if name=='first_marginal_equal_word2_separates':
            w=d['pairwise_witnesses'][0]; assert len(w['first_distinguishing_word'])==2 and w['probabilities']==[F(1,2),F(1,4)]
        tests.append({'name':name,'data':d,'assertions_passed':True})
    sharp=[]
    for n in range(2,8):
        p=[[F(j==min(i+1,n-1)) for j in range(n)] for i in range(n)];e=[[F(i!=n-1),F(i==n-1)] for i in range(n)]
        delta=[F(1),F(-1)]+[F(0)]*(n-2);found=None
        for k in range(n):
            for w in product(range(2),repeat=k):
                v=word(p,e,w); val=sum((x*y for x,y in zip(delta,v)),F(0))
                if val:
                    found={'P':p,'emissions':e,'initial_difference':delta,'N':n,'first_distinguishing_word':list(w),'length':k,'probability_difference':val};break
            if found:break
        assert found is not None and found['length']==n-1;sharp.append(found)
    rows=[[F(a,2),F(b,2),F(c,2)] for a in range(3) for b in range(3) for c in range(3) if a+b+c==2]
    scan=[]
    for p in product(rows,repeat=3):scan.append(finite_chain([row[:] for row in p]))
    return {'scope':'Finite structural/linear ingredients only; universal probability proof is a separate artifact.','targeted_models':tests,'word_bound_sharpness_general_initial_distributions':sharp,'complete_three_state_denominator_two_scan':scan,'all_assertions_passed':True}

if __name__=='__main__':
    print(json.dumps(run(),indent=2,default=lambda x:str(x) if isinstance(x,F) else x))
