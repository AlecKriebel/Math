#!/usr/bin/env python3
"""Independent exact controls; no sampled paths and no submitted solver imports."""
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path
import json
import sys

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parents[1] / "sources/published-source/universal_simultaneous_amplification/phase4_landmark_closure/paper_hybrid_threshold"
for wheel in ("mpmath-1.3.0-py3-none-any.whl", "sympy-1.14.0-py3-none-any.whl"):
    sys.path.insert(0, str(SOURCE / "vendor" / wheel))
import sympy as s

def need(ok, message):
    if not ok:
        raise RuntimeError(message)

def gaussian(a, b):
    a = [list(row) + [value] for row, value in zip(a,b)]
    n = len(a)
    for col in range(n):
        pivot = next(i for i in range(col,n) if a[i][col])
        a[col], a[pivot] = a[pivot], a[col]
        div = a[col][col]
        a[col] = [v / div for v in a[col]]
        for i in range(n):
            if i != col and a[i][col]:
                fac = a[i][col]
                a[i] = [u - fac*v for u,v in zip(a[i],a[col])]
    return [row[-1] for row in a]

def generic_rates(weights, mask, fitness, rule):
    n = len(weights)
    f = [fitness if mask >> i & 1 else F(1) for i in range(n)]
    # Continuous time: Bd multiply the event probabilities by global F;
    # dB multiply by n. Such positive statewise factors preserve committors.
    row = {}
    degree = [sum(v) for v in weights]
    for v in range(n):
        rate = F(0)
        for u in range(n):
            if bool(mask>>u & 1) != bool(mask>>v & 1):
                if rule == "Bd":
                    rate += f[u] * weights[u][v] / degree[u]
                else:
                    rate += f[u] * weights[u][v] / sum(f[j]*weights[j][v] for j in range(n))
        if rate:
            row[mask ^ (1<<v)] = rate
    return row

def center_graph(C,m):
    w = [[F(0) for _ in range(C+m)] for _ in range(C+m)]
    for i,j in combinations(range(C),2): w[i][j] = w[j][i] = F(1)
    for j in range(C,C+m): w[0][j] = w[j][0] = F(1)
    return w

def label(mask,C,m):
    return mask&1, sum(mask>>i&1 for i in range(1,C)), sum(mask>>i&1 for i in range(C,C+m))

def formula_rates(state,C,m,r,rule):
    h,i,l = state
    c,d = C-1,C-1+m
    out = {}
    def add(state,rate):
        if rate: out[state] = rate
    if rule == "Bd":
        add((h,i+1,l),r*(c-i)*(F(h,d)+F(i,c)))
        add((h,i-1,l),i*(F(1-h,d)+F(c-i,c)))
        if not h: add((1,i,l),r*(F(i,c)+l))
        if h: add((0,i,l),F(c-i,c)+m-l)
        add((h,i,l+1),F(r*h*(m-l),d))
        add((h,i,l-1),F((1-h)*l,d))
    else:
        if i<c: add((h,i+1,l),F((c-i)*r*(h+i),c+(r-1)*(h+i)))
        if i: add((h,i-1,l),F(i*(c-i+1-h),c+(r-1)*(i-1+h)))
        if not h: add((1,i,l),F(r*(i+l),d+(r-1)*(i+l)))
        if h: add((0,i,l),F(d-i-l,d+(r-1)*(i+l)))
        add((h,i,l+1),F(h*(m-l)))
        add((h,i,l-1),F((1-h)*l))
    return out

def center_table_controls():
    count=0
    for C,m in [(2,1),(3,2),(4,2)]:
        w = center_graph(C,m)
        for r in [F(3,2),F(2,3),F(1)]:
            for rule in ["Bd","dB"]:
                for mask in range(1 << (C+m)):
                    agg={}
                    for target,rate in generic_rates(w,mask,r,rule).items():
                        lab=label(target,C,m)
                        agg[lab]=agg.get(lab,F(0))+rate
                    need(agg==formula_rates(label(mask,C,m),C,m,r,rule),f"center mismatch {C,m,r,rule,mask}")
                    count+=1
    return count

def count_fixation(n,r,rule):
    # Direct up/down event sums on Kn, independently from any formula.
    w=center_graph(n,0)
    products=[F(1)]
    for k in range(1,n):
        mask=(1<<k)-1
        row=generic_rates(w,mask,r,rule)
        up=sum(v for state,v in row.items() if state.bit_count()==k+1)
        down=sum(v for state,v in row.items() if state.bit_count()==k-1)
        products.append(products[-1]*down/up)
    return 1/sum(products)

def baseline_controls():
    count=0
    for n in range(2,10):
        for r in [F(3,2),F(2,3),F(1)]:
            for rule in ["Bd","dB"]:
                actual=count_fixation(n,r,rule)
                if r==1: expected=F(1,n)
                elif rule=="Bd": expected=(1-1/r)/(1-r**(-n))
                else: expected=F(n-1,n)*(1-1/r)/(1-r**(-(n-1)))
                need(actual==expected,f"Kn mismatch {n,r,rule}")
                count+=1
    return count

def ladder_controls():
    count=0
    # Rates are multiples k or q-k of A,D,B,E. Preserve adverse reversals.
    for q in range(1,8):
        for A,D,B,E in [(F(2),F(3),F(5),F(7)),(F(7),F(3),F(5),F(1,100))]:
            states=[(h,k) for h in range(2) for k in range(q+1)]
            transient=[z for z in states if z not in [(0,0),(1,q)]]
            index={z:i for i,z in enumerate(transient)}
            matrix=[[F(0) for _ in transient] for _ in transient]
            rhs=[F(0) for _ in transient]
            for z,i in index.items():
                h,k=z
                row={(1,k):k*A,(0,k-1):k*D} if h==0 else {(1,k+1):(q-k)*B,(0,k):(q-k)*E}
                for target,rate in row.items():
                    if not rate: continue
                    matrix[i][i]+=rate
                    if target in index: matrix[i][index[target]]-=rate
                    elif target==(1,q): rhs[i]+=rate
            sol=gaussian(matrix,rhs)
            x=D*(B+E)/(B*(A+D))
            H=1/(1+(E/B)*sum(x**j for j in range(q)))
            P=(A/(A+D))*(1+E/B)*H
            need(sol[index[(1,0)]]==H,"exact ladder H")
            need(sol[index[(0,1)]]==P,"exact ladder P")
            need(1-H<=q*E/(B+E),"first-reversal sweep bound")
            count+=1
    return count

def symbolic_controls():
    r,sg,lam,eta=s.symbols("r sigma lambda eta", positive=True)
    p=1-1/r
    # Four entry rates are reconstructed directly from degrees, K2 committors,
    # and core limit p. E is negligible after reciprocal control.
    pair_B=s.factor((r/(r+1))*(2*sg*r*p)/(2*sg*r*p+2/(r+1)))
    pair_D=s.factor(s.Rational(1,2)*(2*r*p)/(2*r*p+sg/r))
    # Trace = [center starts + pair starts] / [C+m+2q], setting C=1 in
    # normalized population ratios and m/C=lambda eta, q/C=eta.
    trace_B=(p+lam*eta+2*eta*pair_B)/(1+(lam+2)*eta)
    trace_D=(p+2*eta*pair_D)/(1+(lam+2)*eta)
    B=s.factor(s.diff(trace_B/p,eta).subs(eta,0))
    D=s.factor(s.diff(trace_D/p,eta).subs(eta,0))
    need(s.factor(B-(2*(sg-1)/(1+sg*(r*r-1))+lam/(r-1)))==0,"response Bd")
    need(s.factor(D-(2*(r*(2-r)-sg)/(sg+2*r*(r-1))-lam))==0,"response dB")
    lower=s.solve(B,lam)[0]
    upper=s.solve(D,lam)[0]
    gap=s.factor(upper-lower)
    Q=(r-1)*sg**2+(r**3-4*r**2+3*r+1)*sg+r*(2*r-3)
    need(s.factor(gap+2*r*Q/((1+sg*(r*r-1))*(sg+2*r*(r-1))))==0,"feasibility")
    phase=s.expand(s.discriminant(Q,sg))
    need(phase==r**6-8*r**5+22*r**4-30*r**3+21*r**2-6*r+1,"sextic")
    sturm=s.sturm(phase,r)
    def signs(x):
        vals=[s.sign(z.subs(r,x)) for z in sturm]
        vals=[v for v in vals if v]
        return sum(a!=b for a,b in zip(vals,vals[1:]))
    roots=[signs(a)-signs(b) for a,b in [(s.Integer(1),s.Rational(3,2)),(s.Rational(3,2),s.Rational(151,100))]]
    need(roots==[0,1],"Sturm counts")
    # Rational margins provide an exact crossing of 3/2, independent of
    # the algebraic tangency parameters.
    margins=[s.factor(z.subs({r:s.Rational(3,2),sg:s.Rational(19,137),lam:s.Rational(20,27)})) for z in [B,D]]
    need(margins==[s.Rational(232,17361),s.Rational(65,12123)],"rational crossing")
    return {"Bd_response":str(B),"dB_response":str(D),"phase":str(phase),"Sturm_counts":roots,"rational_margins":[str(x) for x in margins]}

if __name__=="__main__":
    need(sys.flags.optimize==0,"optimized execution rejected")
    results={"python":sys.version,"sympy":s.__version__,"center_labelled_rows":center_table_controls(),"exact_complete_graph_controls":baseline_controls(),"exact_ladder_controls":ladder_controls(),"symbolic":symbolic_controls()}
    print(json.dumps(results,indent=2))
    print("PASS independent exact transition, baseline, macro-chain, and algebra controls")
