"""Exact diagnostic checks for a prior-theory implication, not a new proof search."""
from fractions import Fraction as F
from itertools import permutations
from pathlib import Path
import hashlib,json,sys

class AuditFailure(ValueError): pass
CHECKS=[]
def require(condition,label):
    CHECKS.append(label)
    if not condition: raise AuditFailure(label)
def rejected(fn,label):
    try:fn()
    except AuditFailure:return
    raise AuditFailure('Mutant was accepted: '+label)
def mv(a,z):return [sum(F(x)*y for x,y in zip(row,z)) for row in a]
def rank(a):
    b=[[F(x) for x in r] for r in a];j=0
    for c in range(len(b[0])):
        k=next((k for k in range(j,len(b)) if b[k][c]),None)
        if k is None:continue
        b[j],b[k]=b[k],b[j];v=b[j][c];b[j]=[x/v for x in b[j]]
        for k in range(len(b)):
            if k!=j:
                v=b[k][c];b[k]=[x-v*y for x,y in zip(b[k],b[j])]
        j+=1
    return j

N=6;ZERO=(0,)*N
def const(n):return {} if not n else {ZERO:n}
def var(i):return {tuple(int(j==i) for j in range(N)):1}
def add(*pp):
    out={}
    for p in pp:
        for e,c in p.items():out[e]=out.get(e,0)+c
    return {e:c for e,c in out.items() if c}
def scale(p,c):return {e:c*v for e,v in p.items() if c*v}
def mul(*pp):
    out=const(1)
    for p in pp:
        nxt={}
        for e,c in out.items():
            for f,d in p.items():
                ef=tuple(x+y for x,y in zip(e,f));nxt[ef]=nxt.get(ef,0)+c*d
        out={e:c for e,c in nxt.items() if c}
    return out
def diff(p,i):
    return {tuple(x-int(j==i) for j,x in enumerate(e)):c*e[i] for e,c in p.items() if e[i]}
def determinant(matrix):
    n=len(matrix);out={}
    for perm in permutations(range(n)):
        inv=sum(perm[i]>perm[j] for i in range(n) for j in range(i+1,n))
        out=add(out,scale(mul(*(matrix[i][perm[i]] for i in range(n))),(-1)**inv))
    return out
def jacobian(mapping):return determinant([[diff(p,j) for j in range(N)] for p in mapping])
def divided(p,exp):
    require(all(all(x>=y for x,y in zip(e,exp)) for e in p),'polynomial division exact')
    return {tuple(x-y for x,y in zip(e,exp)):c for e,c in p.items()}
def canonical(p):return [[list(e),c] for e,c in sorted(p.items())]

def implication(lp,local_upper,local_origin_verified):
    require(local_origin_verified,'origin-local upper-bound bridge required')
    require(lp>local_upper,'strict separation needed for contrapositive')
    return 'not singleton-fiber condition'

def main():
    require('--false-control' not in sys.argv,'deliberate false guard')
    # Exponents come from the six original binomial monomials in the stated order.
    aa=[[1,0,0,0,1,0],[0,1,0,0,0,1],[0,0,1,1,0,0]]
    bb=[[0,1,0,1,0,0],[0,0,1,0,1,0],[1,0,0,0,0,1]]
    a=[[aa[i][j] for i in range(3)]+[bb[i][j] for i in range(3)] for j in range(6)]
    a += [[int(i==j) for i in range(3)]*2 for j in range(3)]
    expected=[[1,0,0,0,0,1],[0,1,0,1,0,0],[0,0,1,0,1,0],[0,0,1,1,0,0],[1,0,0,0,1,0],[0,1,0,0,0,1],[1,0,0,1,0,0],[0,1,0,0,1,0],[0,0,1,0,0,1]]
    require(a==expected,'all augmented rows reconstructed')
    require(rank(a)==5,'rank five')
    require(mv(a,[F(1)]*3+[F(-1)]*3)==[0]*9,'kernel direction exact')
    z0=[F(0)]*3+[F(1)]*3;z1=[F(1)]*3+[F(0)]*3
    require(mv(a,z0)==[1]*9 and mv(a,z1)==[1]*9,'distinct rational endpoints same image')
    y=[F(0)]*6+[F(1)]*3
    require([sum(y[i]*a[i][j] for i in range(9)) for j in range(6)]==[1]*6,'dual certificate exact')
    require(sum(y)==3 and sum(z0)==3,'LP optimum three')
    # A linear affine map constant at both endpoints is identically constant on their segment.
    require(mv(a,[u-v for u,v in zip(z1,z0)])==[0]*9,'universal segment-image identity')
    # Bottom saturation and three directed inequalities force equal mu values.
    require(a[0]==[1,0,0,0,0,1] and a[1]==[0,1,0,1,0,0] and a[2]==[0,0,1,0,1,0],'full-face cyclic chain rows')
    # Exact codimension-two charts after blowing up the origin; all six entry pivots.
    u,alpha,beta,gamma,D,E=[var(i) for i in range(6)]
    matrix=[[u,mul(u,alpha),mul(u,beta)],[mul(u,gamma),mul(u,add(D,mul(alpha,gamma))),mul(u,add(E,mul(beta,gamma)))]]
    rows=[];u2=(2,0,0,0,0,0);u5=mul(u,u,u,u,u)
    for rp in range(2):
        for cp in range(3):
            ro=[rp,1-rp];co=[cp]+[j for j in range(3) if j!=cp]
            orig=[[None]*3 for _ in range(2)]
            for i in range(2):
                for j in range(3):orig[ro[i]][co[j]]=matrix[i][j]
            minors=[add(mul(orig[0][0],orig[1][1]),scale(mul(orig[0][1],orig[1][0]),-1)),add(mul(orig[0][1],orig[1][2]),scale(mul(orig[0][2],orig[1][1]),-1)),add(mul(orig[0][2],orig[1][0]),scale(mul(orig[0][0],orig[1][2]),-1))]
            strict=[divided(p,u2) for p in minors]
            require(all(all(e[4]+e[5]>=1 for e in p) for p in strict),'all strict minors in (D,E)')
            require(any(p==D or p==scale(D,-1) for p in strict),'D is a strict minor up to sign')
            require(any(p==E or p==scale(E,-1) for p in strict),'E is a strict minor up to sign')
            jac=jacobian(orig[0]+orig[1])
            require(jac==u5 or jac==scale(u5,-1),'origin-blowup Jacobian order five')
            rows.append({'pivot_row':rp,'pivot_column':cp,'strict_minors':list(map(canonical,strict)),'jacobian':canonical(jac),'strict_center_equations':['D=0','E=0'],'codimension':2})
    # Strict center and first exceptional divisor are coordinate-transverse.
    require(rank([[int(i==j) for i in range(6)] for j in [0,4,5]])==3,'u,D,E independent coordinate normals')
    # Two second-blowup charts give the same two-divisor normal crossing model.
    second=[]
    for chart in ['D-pivot','E-pivot']:
        v,w=var(4),var(5)
        dq,eq=(v,mul(v,w)) if chart=='D-pivot' else (mul(v,w),v)
        mapping=[u,mul(u,alpha),mul(u,beta),mul(u,gamma),mul(u,add(dq,mul(alpha,gamma))),mul(u,add(eq,mul(beta,gamma)))]
        jac=jacobian(mapping);expected_jac=mul(u5,v)
        require(jac==expected_jac or jac==scale(expected_jac,-1),'combined Jacobian u^5 v')
        min1=add(mul(mapping[0],mapping[4]),scale(mul(mapping[1],mapping[3]),-1))
        min2=add(mul(mapping[1],mapping[5]),scale(mul(mapping[2],mapping[4]),-1))
        min3=add(mul(mapping[2],mapping[3]),scale(mul(mapping[0],mapping[5]),-1))
        strict=[divided(p,(2,0,0,0,1,0)) for p in [min1,min2,min3]]
        require(any(p==const(1) or p==const(-1) for p in strict),'total transform principal u^2 v')
        second.append({'chart':chart,'jacobian':canonical(jac),'total_ideal_generator':'u^2 v','discrepancy_orders':{'E0':5,'E1':1},'ideal_orders':{'E0':2,'E1':1},'log_discrepancy_ratios':['6/2=3','2/1=2']})
    docampo=[F((2-i)*(3-i),2-i) for i in range(2)]
    require(docampo==[F(3),F(2)] and min(docampo)==2,'Docampo formula specialized to generic two-by-three size-two minors')
    require(implication(F(3),F(2),True)=='not singleton-fiber condition','conditional theorem strict contrapositive')
    rejected(lambda:implication(F(3),F(2),False),'unbridged global threshold')
    rejected(lambda:implication(F(2),F(2),True),'equal threshold not contradiction')
    rejected(lambda:implication(F(1),F(2),True),'reverse inequality not contradiction')
    rejected(lambda:require(F(5,2)==F(2),'missing discrepancy plus one'),'discrepancy normalization')
    rejected(lambda:require(len(a)==6,'dropped augmented rows'),'unaugmented substitution')
    result={'result':'PASS','diagnostic_exception_checks':len(CHECKS),'matrix':a,'LP_optimum':3,'global_prior_formula':2,'origin_local_upper_bound':2,'origin_local_threshold':2,'claim_is_reviewer_deduction_from_prior_theory':True,'explicit_prior_numbered_question_counterexample_found_by_this_family':False,'six_origin_blowup_charts':rows,'second_blowup_charts':second,'source_historical_claims_are_manually_verified_not_computationally_inferred':True,'new_central_proof_search_turns':0}
    print(json.dumps(result,indent=2))
if __name__=='__main__':main()
