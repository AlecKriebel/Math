#!/usr/bin/env python3
"""Independent standard-library algebra audit; stdout only; no geometric decision."""
import json
from fractions import Fraction
from itertools import combinations


def check(value, message):
    if not value:
        raise RuntimeError(message)


def mm(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]


def inv2(a):
    check(a[0][0]*a[1][1]-a[0][1]*a[1][0] == 1, 'SL2 determinant')
    return [[a[1][1], -a[0][1]], [-a[1][0], a[0][0]]]


def braid(word):
    a, b = [[1,1],[0,1]], [[1,0],[-1,1]]
    matrices = {1:a, 2:b, -1:inv2(a), -2:inv2(b)}
    out = [[1,0],[0,1]]
    for letter in word:
        out = mm(out, matrices[letter])
    return out, sum(1 if x > 0 else -1 for x in word)


def inverse(w):
    return [-x for x in w[::-1]]


def conj(g,w):
    return g+w+inverse(g)


# Polynomials are ascending integer coefficient tuples, normalized uniquely.
def norm(p):
    p = list(p)
    while len(p)>1 and p[-1]==0:
        p.pop()
    return tuple(p)


def add(p,q):
    return norm([(p[i] if i<len(p) else 0)+(q[i] if i<len(q) else 0) for i in range(max(len(p),len(q)))])


def scale(p,a):
    return norm([a*x for x in p])


def mul(p,q):
    out=[0]*(len(p)+len(q)-1)
    for i,x in enumerate(p):
        for j,y in enumerate(q):
            out[i+j]+=x*y
    return norm(out)


def rowadd(m,target,source,multiplier):
    m[target]=[add(x,scale(y,multiplier)) for x,y in zip(m[target],m[source])]


def wedge_square(form):
    # Independent full exterior-algebra expansion, not a hardcoded Pfaffian formula.
    total=(0,)
    for ij,p in form.items():
        for kl,q in form.items():
            seq=ij+kl
            if len(set(seq)) != 4:
                continue
            inversions=sum(seq[i]>seq[j] for i in range(4) for j in range(i+1,4))
            total=add(total,scale(mul(p,q),(-1)**inversions))
    return total


def main():
    a,b=[1],[2]
    g=[1,-2,-1]
    p=[a,conj([1,2,2],a)]
    q=[conj([1,1],b),b]
    beta=[1,1,2,2]*2+inverse([1,2]*3)
    check(braid([1,2,1])==braid([2,1,2]),'braid relation')
    check(braid(p[0]+p[1])==braid(q[0]+q[1])==braid(beta),'common product')
    for i in range(2):
        check(braid(conj(g,p[i]))==braid(q[i]),'global conjugacy')
    check(braid(conj(g,beta))==braid(beta),'centralizer')
    check(braid([1,2]*3)==([[-1,0],[0,-1]],6),'central element')
    cp=mm(braid([1,2,2])[0],[[1],[0]])
    cq=mm(braid([1,1])[0],[[0],[1]])
    check(cp==[[-1],[-2]] and cq==[[2],[1]],'vanishing cycles')

    # Universal row/column reduction over Z[n]. Each move is unimodular over Z
    # after every integer substitution, including n=0 and negative parameters.
    z,o,t,n=(0,),(1,),(2,),(0,1)
    m=[[o,t,o],[z,z,o],[(-1,),(-2,),o],[z,scale(n,-1),o]]
    rowadd(m,0,1,-1)
    rowadd(m,2,0,1)
    rowadd(m,2,1,-1)
    rowadd(m,3,1,-1)
    for row in m:
        row[1]=add(row[1],scale(row[0],-2))
    m[2],m[3]=m[3],m[2]
    for row in m:
        row[1],row[2]=row[2],row[1]
    m[2]=[scale(x,-1) for x in m[2]]
    check(m==[[o,z,z],[z,o,z],[z,z,n],[z,z,z]],'universal Smith reduction')

    f={(0,1):(1,), (0,2):(0,2), (0,3):(0,), (1,2):(0,), (1,3):(0,-2), (2,3):(1,-4)}
    square=wedge_square(f)
    check(square==(2,-8,8),'universal exterior-square identity')
    check(sum(Fraction(c)*Fraction(1,2)**i for i,c in enumerate(square))==0,'midpoint degeneration')
    # At the midpoint the form factors as (dx1+dx4) wedge (dx2+dx3).
    rank2={(0,1):1,(0,2):1,(0,3):0,(1,2):0,(1,3):-1,(2,3):-1}
    for ij,poly in f.items():
        check(sum(Fraction(c)*Fraction(1,2)**i for i,c in enumerate(poly))==rank2[ij],'rank two factorization')

    # Polynomial identity for every degree, separately from numerical samples.
    chi_closed=(0,3,-1)   # 3d-d^2
    chi_filling=add(chi_closed,(0,-1))
    check(chi_filling==(0,2,-1),'universal Euler identity')
    check(add(chi_closed,(-2,))!=chi_closed,'handle obstruction')
    samples=[]
    for d in (1,2,3,4,17,18,50,100):
        genus=(d*d-3*d+2)//2
        check(2-2*genus==3*d-d*d,'adjunction sample')
        samples.append({'d':d,'g':genus,'chi_filling':2-2*genus-d})
    out={'status':'PASS','method':'Independent SL2(Z)+exponent braid check, polynomial unimodular reduction, exterior algebra, polynomial adjunction',
         'braid':{'common_matrix':braid(beta)[0],'exponent':braid(beta)[1],'g_matrix':braid(g)[0],'P2_cycle':cp,'Q1_cycle':cq},
         'universal_relation_diagonal':m,'twice_pfaffian_polynomial':square,'chi_filling_polynomial':chi_filling,'degree_samples':samples,
         'scope':'Algebraic corroboration only. The report and audit give exact mathematical arguments; no isotopy decision is encoded.'}
    print(json.dumps(out,sort_keys=True,indent=2))


if __name__=='__main__':
    main()
