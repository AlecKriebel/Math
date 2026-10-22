#!/usr/bin/env python3
"""Independent exact arithmetic audit. Python standard library, no assert statements.
The geometric identification is a mathematical argument in AUDIT.md, not a test.
"""
import argparse
from fractions import Fraction as Q
from itertools import combinations, product
from math import gcd, lcm
import json

CHECKS=0

def require(value,label):
    global CHECKS
    if not value:
        raise ValueError('AUDIT FAILURE: '+label)
    CHECKS+=1

def eye(n):return [[int(i==j) for j in range(n)] for i in range(n)]
def transpose(a):return [list(r) for r in zip(*a)]
def mm(a,b):return [[sum(x*y for x,y in zip(r,c)) for c in zip(*b)] for r in a]
def det(a):
    # Fraction-free Bareiss elimination with row pivoting.
    a=[r[:] for r in a];n=len(a);last=1;sign=1
    if not n:return 1
    for k in range(n-1):
        z=next((j for j in range(k,n) if a[j][k]),None)
        if z is None:return 0
        if z!=k:a[k],a[z]=a[z],a[k];sign=-sign
        pivot=a[k][k]
        for i in range(k+1,n):
            for j in range(k+1,n):
                v=a[i][j]*pivot-a[i][k]*a[k][j]
                if v%last:raise ArithmeticError('nonexact Bareiss division')
                a[i][j]=v//last
            a[i][k]=0
        last=pivot
    return sign*a[-1][-1]

def inverse(a):
    n=len(a);b=[[Q(x) for x in r]+[Q(x) for x in eye(n)[i]] for i,r in enumerate(a)]
    for col in range(n):
        pivot=next(i for i in range(col,n) if b[i][col]);b[col],b[pivot]=b[pivot],b[col]
        c=b[col][col];b[col]=[x/c for x in b[col]]
        for i in range(n):
            if i!=col:
                c=b[i][col];b[i]=[x-c*y for x,y in zip(b[i],b[col])]
    return [r[n:] for r in b]

def poly(coeff,t):
    v=0
    for c in reversed(coeff):v=v*t+c
    return v

def charpoly(a):
    # Newton identities from all traces through dimension n.
    n=len(a);power=eye(n);traces=[];descending=[1]
    for k in range(1,n+1):
        power=mm(power,a);traces.append(sum(power[i][i] for i in range(n)))
        numerator=-sum(descending[k-i]*traces[i-1] for i in range(1,k+1))
        if numerator%k:raise ArithmeticError('Newton division')
        descending.append(numerator//k)
    return descending[::-1],traces

def burau_determinant(w,t):
    m=eye(2)
    for letter in w:m=mm(m,[[-t,1],[0,1]] if letter==1 else [[1,0],[t,-t]])
    return (1-m[0][0])*(1-m[1][1])-m[0][1]*m[1][0]

def word(exponents):return sum(([letter]*p for letter,p in zip((1,2,1,2),exponents)),[])
def cycles(w):
    p=list(range(3))
    for l in w:p[l-1],p[l]=p[l],p[l-1]
    unseen=set(range(3));answer=[]
    while unseen:
        x=min(unseen);c=[]
        while x in unseen:unseen.remove(x);c.append(x+1);x=p[x]
        answer.append(c)
    return answer

def geometric_matrix(w):
    # Chronological basis, constructed directly from consecutive band endpoints.
    occurrences={letter:[i for i,l in enumerate(w) if l==letter] for letter in (1,2)}
    curves=sorted((a,b,l) for l,positions in occurrences.items() for a,b in zip(positions,positions[1:]))
    n=len(curves);v=[[-int(i==j) for j in range(n)] for i in range(n)];rules=[]
    for i,(a,b,l) in enumerate(curves):
        for j,(c,d,m) in enumerate(curves):
            if i>=j:continue
            if b==c:
                require(l==m,'shared endpoint belongs to one column')
                v[j][i]=1;rules.append([i,j,'shared positive band'])
            elif a<c<b<d:
                require(abs(l-m)==1,'interleaving adjacent columns')
                if l<m:v[i][j]=1
                else:v[j][i]=-1
                rules.append([i,j,'interleaving'])
    # Reindex only after constructing every linking entry.
    order=sorted(range(n),key=lambda i:(curves[i][2],curves[i][0]))
    return [[v[i][j] for j in order] for i in order],[[curves[i][2],curves[i][0]+1,curves[i][1]+1] for i in order],rules

def vec(n,i):return [int(j==i) for j in range(n)]
def mulvec(q,v):return [sum(x*y for x,y in zip(r,v)) for r in q]
def pairing(q,a,b):return sum(x*y for x,y in zip(a,mulvec(q,b)))
def order(q,a):return lcm(*(x.denominator for x in mulvec(q,a)))

def smith(a):
    # Integer elementary row/column Euclidean reduction, independently of inverse.
    a=[r[:] for r in a];n=len(a)
    for k in range(n):
        at=next(((i,j) for i in range(k,n) for j in range(k,n) if a[i][j]),None)
        if at is None:break
        i,j=at;a[k],a[i]=a[i],a[k]
        for r in a:r[k],r[j]=r[j],r[k]
        while True:
            changed=False
            for i in range(k+1,n):
                if a[i][k]:
                    quotient=a[i][k]//a[k][k]
                    a[i]=[x-quotient*y for x,y in zip(a[i],a[k])]
                    if a[i][k]:a[i],a[k]=a[k],a[i]
                    changed=True;break
            if changed:continue
            for j in range(k+1,n):
                if a[k][j]:
                    quotient=a[k][j]//a[k][k]
                    for r in a:r[j]-=quotient*r[k]
                    if a[k][j]:
                        for r in a:r[j],r[k]=r[k],r[j]
                    changed=True;break
            if changed:continue
            bad=next(((i,j) for i in range(k+1,n) for j in range(k+1,n) if a[i][j]%a[k][k]),None)
            if bad is None:break
            i,j=bad;a[k]=[x+y for x,y in zip(a[k],a[i])]
        if a[k][k]<0:a[k]=[-x for x in a[k]]
    require(all(not a[i][j] for i in range(n) for j in range(n) if i!=j),'Smith diagonal')
    d=[a[i][i] for i in range(n)]
    require(all(d[i+1]%d[i]==0 for i in range(n-1) if d[i]),'Smith divisibility')
    return d

def lcs(a,b):
    last=[0]*(len(b)+1)
    for c in a:
        current=[0]
        for j,d in enumerate(b):current.append(last[j]+1 if c==d else max(last[j+1],current[-1]))
        last=current
    return last[-1]

def variants(w):return {tuple(w[i:]+w[:i]) for i in range(len(w))}|{tuple(3-x for x in w[i:]+w[:i]) for i in range(len(w))}

def run(tamper=None):
    global CHECKS
    CHECKS=0
    coefficients=[1,-1,-1,6,-13,21,-29,35,-37,35,-29,21,-13,6,-1,-1,1]
    if tamper=='polynomial':coefficients[8]+=1
    target_cp=[1,0,-29,0,172,0,-393,0,443,0,-269,0,89,0,-15,0,1]
    exponents={'K':[3,3,6,6],'J':[3,5,3,7]}
    if tamper=='word':exponents['J']=[3,5,3,5]
    answers={}
    for label,e in exponents.items():
        w=word(e);v,curves,local_rules=geometric_matrix(w);n=len(v)
        require(len(w)==18 and len(cycles(w))==1,'18-letter knot input '+label)
        require(n==16,'rank 16 surface basis')
        if tamper=='edge' and label=='K':v[2][10]=0
        s=[[-v[i][j]-v[j][i] for j in range(n)] for i in range(n)]
        adjacency=[[2*int(i==j)-s[i][j] for j in range(n)] for i in range(n)]
        require(all(adjacency[i][j] in (0,1) for i in range(n) for j in range(n)),'unsigned adjacency')
        edges=[(i,j) for i in range(n) for j in range(i+1,n) if adjacency[i][j]]
        seen={0}
        while True:
            expanded=seen|{j for i in seen for j in range(n) if adjacency[i][j]}
            if expanded==seen:break
            seen=expanded
        require(len(edges)==n-1 and len(seen)==n,'linking graph is a tree')
        cp,traces=charpoly(adjacency);require(cp==target_cp,'exact adjacency characteristic polynomial')
        # All subsets of 15 edges, not the author's recursive matching algorithm.
        matchings=[0]*9
        for mask in range(1<<len(edges)):
            occupied=0;size=0;valid=True
            for i,(a,b) in enumerate(edges):
                if (mask>>i)&1:
                    new=(1<<a)|(1<<b)
                    if occupied&new:valid=False;break
                    occupied|=new;size+=1
            if valid:matchings[size]+=1
        require(matchings==[1,15,89,269,443,393,172,29,1],'enumerated matchings')
        require(cp==[(-1)**((n-i)//2)*matchings[(n-i)//2] if (n-i)%2==0 else 0 for i in range(n+1)],'matching identity')
        for t in range(-9,10):
            require(burau_determinant(w,t)==(1+t+t*t)*poly(coefficients,t),'Burau polynomial identity at '+str(t))
        for t in range(-8,9):
            require(det([[v[i][j]-t*v[j][i] for j in range(n)] for i in range(n)])==poly(coefficients,t),'Seifert polynomial identity at '+str(t))
        require(det(s)==-243,'symmetrized determinant')
        require(det([[v[i][j]-v[j][i] for j in range(n)] for i in range(n)])==1,'unimodular intersection form')
        # Leading-principal-minor criterion, independent of author LDL algorithm.
        leading=[1]+[det([r[:k] for r in s[:k]]) for k in range(1,n+1)]
        require(all(leading),'nonzero leading principal minors')
        signs=[1 if leading[i]*leading[i+1]>0 else -1 for i in range(n)]
        require(signs.count(1)==15 and signs.count(-1)==1,'ordinary inertia')
        snf=smith(s);expected=[1]*14+([9,27] if label=='K' else [3,81])
        require(snf==expected,'Smith normal form '+label)
        q=inverse(s);require(mm(s,q)==eye(n),'rational inverse')
        x=vec(n,0);y=vec(n,8 if label=='K' else 3);y[0]-=20 if label=='K' else 29
        orders=[order(q,z) for z in (x,y)]
        expect_orders=[27,9] if label=='K' else [81,3]
        require(orders==expect_orders,'cyclic coordinate orders')
        gram=[[pairing(q,a,b)%1 for b in (x,y)] for a in (x,y)]
        expect_gram=[[Q(16,27),Q(0)],[Q(0),Q(5,9)]] if label=='K' else [[Q(50,81),Q(0)],[Q(0),Q(1,3)]]
        require(gram==expect_gram,'cyclic coordinate linking pairing')
        classes={tuple(t%1 for t in mulvec(q,[a*x[i]+b*y[i] for i in range(n)])) for a in range(orders[0]) for b in range(orders[1])}
        require(len(classes)==243,'full cyclic group generation')
        answers[label]={'exponents':e,'word':w,'basis_column_start_end_one_based':curves,'seifert_matrix':v,'linking_edges_zero_based':edges,'characteristic_coefficients_ascending':cp,'power_traces':traces,'matching_counts':matchings,'alexander_coefficients_ascending':coefficients,'smith_diagonal':snf,'leading_principal_minors':leading,'inertia_S':[15,1,0],'signature':-14,'cyclic_orders':orders,'pairing_mod_1':[[str(x) for x in r] for r in gram],'genus':8,'tau':8,'s':16,'upsilon_at_1':-7}
    orders=(27,9,81,3);diagonal=(Q(16,27),Q(5,9),Q(-50,81),Q(-1,3))
    generators=[(3,0,0,1),(0,3,0,0),(0,0,9,0)]
    if tamper=='metabolizer':generators[0]=(1,0,0,1)
    pairing4=lambda a,b:sum(c*x*y for c,x,y in zip(diagonal,a,b))
    for a in generators:
        for b in generators:require(pairing4(a,b).denominator==1,'isotropic generators')
    subgroup={tuple(sum(c*g[i] for c,g in zip(coeffs,generators))%orders[i] for i in range(4)) for coeffs in product(range(9),range(3),range(9))}
    # Enumerate the entire 59049-element difference group with integer residues.
    numerators=[int(c*81) for c in diagonal]
    orthogonal={a for a in product(*(range(n) for n in orders)) if all(sum(c*x*y for c,x,y in zip(numerators,a,g))%81==0 for g in generators)}
    require(len(subgroup)==243 and subgroup==orthogonal,'explicit M equals full M-perp')
    stages=[[3,3,6,6],[3,3,5,6],[3,3,4,6],[3,3,3,6],[3,4,3,6],[3,5,3,6],[3,5,3,7]]
    if tamper=='movie':stages[2]=[3,3,3,6]
    moves=[]
    for a,b in zip(stages,stages[1:]):
        wa,wb=word(a),word(b);longer,shorter=(wa,wb) if len(wa)>len(wb) else (wb,wa)
        deletions=[i for i in range(len(longer)) if longer[:i]+longer[i+1:]==shorter]
        require(abs(len(wa)-len(wb))==1 and bool(deletions),'single-letter saddle transition')
        moves.append({'direction':'delete' if len(wa)>len(wb) else 'insert','position_one_based':deletions[0]+1,'letter':longer[deletions[0]]})
    component_counts=[len(cycles(word(e))) for e in stages]
    require(component_counts==[1,2,1,2,3,2,1],'movie component counts')
    require(word(stages[0])==answers['K']['word'] and word(stages[-1])==answers['J']['word'],'movie endpoints')
    maximum=max(lcs(a,b) for a in variants(answers['K']['word']) for b in variants(answers['J']['word']))
    require(maximum==15,'restricted common subword optimization')
    # Positive trefoil is the 3-braid 1112, a Markov stabilization of 111.
    tv,_,_=geometric_matrix([1,1,1,2]);require(tv==[[-1,0],[1,-1]],'positive trefoil sign calibration')
    require(det(tv)==1 and det([[tv[i][j]+tv[j][i] for j in range(2)] for i in range(2)])==3,'trefoil matrix')
    require(burau_determinant([1,1,1,2],2)==7*3,'trefoil Burau calibration')
    require(poly(coefficients,-1)==-243 and poly(coefficients,1)==1,'normalizations')
    require(8+(-7)+1==2,'minimal block-pair corollary')
    return {'audit_disposition':'scoped_mathematics_verified_original_question_unsolved','checks':CHECKS,'K':answers['K'],'J':answers['J'],'metabolizer':{'generators':generators,'order':len(subgroup),'orthogonal_complement_order':len(orthogonal),'equal_to_orthogonal_complement':True},'movie':{'stages':stages,'moves':moves,'component_counts':component_counts,'genus':3,'restricted_common_subword_maximum':maximum},'whole_signature_argument':'geometric matrix identification plus exact cospectrality plus tree gauge; see AUDIT.md','not_computed':['full Upsilon','full knot Floer complex','algebraic concordance class','smooth concordance answer']}

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--tamper',choices=['polynomial','word','edge','metabolizer','movie']);args=parser.parse_args()
    print(json.dumps(run(args.tamper),sort_keys=True,indent=2))
