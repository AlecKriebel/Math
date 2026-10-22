"""Independent finite local convention checks; not a computation of CM K2 values."""
from fractions import Fraction as F
import json
from pathlib import Path


def mm(x, y):
    return tuple(tuple(sum(x[i][k]*y[k][j] for k in range(2)) for j in range(2)) for i in range(2))


def inv(x):
    a,b=x[0];c,d=x[1];z=a*d-b*c
    return ((d/z,-b/z),(-c/z,a/z))


def mat(a,b,c,d):
    return ((F(a),F(b)),(F(c),F(d)))


def check(v, message):
    if not v:
        raise RuntimeError(message)


counts={"transfer_equations":0,"principal_scalar_comparisons":0,"higher_level_conjugations":0,"omitted_branch_conjugations":0,"component_shift_checks":0}
for p in (2,3,5,7,11):
    beta=mat(p,0,0,1);g=inv(beta);alpha=mat(1,0,0,p)
    for A in (3,4,5,7):
        if A%p==0:
            continue
        for depth in (1,2,3):
            low=A*p**(depth-1);N=low*p
            for eps in (-1,1):
                for u,v,w in ((0,1,0),(1,2,-1),(-2,3,2),(3,-1,4)):
                    gamma=mm(mm(mm(mat(eps,0,0,1),mat(1,u,0,1)),mat(1,0,N*v,1)),mat(1,w,0,1))
                    dg=mm(mm(beta,gamma),g)
                    aa,bb=gamma[0];cc,dd=gamma[1]
                    permutations=[]
                    for t in range(p):
                        s=((int(cc/N)+int(dd)*t)*pow(int(aa),-1,p))%p
                        permutations.append(s)
                        kt=mat(1,0,low*t,1);ks=mat(1,0,low*s,1)
                        ht=mm(g,kt);hs=mm(g,ks)
                        tau=mm(mm(inv(hs),gamma),ht)
                        check(tau==mm(mm(inv(ks),dg),kt),"transfer conjugation")
                        check(tau[1][0].denominator==1 and int(tau[1][0])%N==0,"strict lower left")
                        check(tau[1][1].denominator==1 and (int(tau[1][1])-1)%N==0,"strict lower right")
                        counts["transfer_equations"]+=1
                        old_tau=mm(mm(inv(mm(alpha,ks)),gamma),mm(alpha,kt))
                        check(tau==old_tau,"rational central scalar must not change transfer")
                        counts["principal_scalar_comparisons"]+=1
                        if depth>=2:
                            check(mm(mm(beta,ht),g)==mm(g,mat(1,0,(low//p)*t,1)),"higher-level representative")
                            counts["higher_level_conjugations"]+=1
                    check(sorted(permutations)==list(range(p)),"branch permutation")
                    if depth==1:
                        a=p*pow(p,-1,A);b=(a-1)//A
                        weyl=mat(a,b,A,1)
                        delta=mm(mm(g,weyl),alpha)
                        omitted=mm(weyl,g)
                        check(mm(mm(inv(omitted),dg),omitted)==mm(mm(inv(delta),gamma),delta),"omitted branch")
                        check(delta[1][0]%A==0 and delta[1][1]==p,"omitted inverse central diamond")
                        counts["omitted_branch_conjugations"]+=1

# Additive class labels allow nonprincipal q of all tested orders.
for h in range(2,12):
    for q in range(h):
        for r in range(h):
            inverse=(r+q)%h
            opposite=(r-q)%h
            central_after_inverse=(inverse-2*q)%h
            check(opposite==central_after_inverse,"v=z y^-1 component law")
            check((inverse+q)%h==(r+2*q)%h,"two inverse/degeneracy shifts")
            counts["component_shift_checks"]+=1

result={"status":"PASS","counts":counts,"boundary":"Exact local rational-matrix and finite class-label checks only. They do not prove nonprincipal CM transport, ray-field identities, regularity, or K2 nonvanishing."}
out=Path(__file__).with_name("INDEPENDENT_CHECK_RESULTS.json")
out.write_text(json.dumps(result,indent=2)+"\n")
print(json.dumps(result,indent=2))
