#!/usr/bin/env python3
"""Independent exact audit of PR 1205; Python standard library only.

This program was written for this review. It never imports candidate code.
It reads certificate.json as inert data, independently constructs roots/quiver,
pulls back optimized monomials in a sparse Laurent polynomial ring over Z,
and verifies both separately generated certificate tables. No float or LP used.
"""
from collections import defaultdict, deque
from fractions import Fraction
from math import comb
from pathlib import Path
import ast
import hashlib
import json
import re
import sys

HERE = Path(__file__).resolve().parent
DATA = HERE / "certificate.json"
N = 12
WORD = (1, 2, 3, 2, 4, 2, 1, 2, 3, 2, 4, 2)
EDGES = {frozenset((1, 2)), frozenset((2, 3)), frozenset((2, 4))}
CARTAN = tuple(tuple(2 if i == j else -1 if frozenset((i+1,j+1)) in EDGES else 0 for j in range(4)) for i in range(4))
ZERO = (0,) * N

def require(condition, message):
    if not condition:
        raise ValueError(message)

def dot(a, b):
    return sum(x*y for x, y in zip(a, b))

def add(*ps):
    out = defaultdict(int)
    for p in ps:
        for e, c in p.items():
            out[e] += c
    return {e:c for e,c in out.items() if c}

def mul(p, q):
    out = defaultdict(int)
    for e, c in p.items():
        for f, d in q.items():
            out[tuple(x+y for x,y in zip(e,f))] += c*d
    return {e:c for e,c in out.items() if c}

def monomial(*positions):
    e = [0]*N
    for position in positions:
        e[position-1] += 1
    return {tuple(e):1}

ONE = {ZERO:1}
Y = [None] + [monomial(i) for i in range(1, N+1)]

def next_positions(word):
    return [next((l for l in range(k+1,len(word)) if word[l] == word[k]),len(word)) for k in range(len(word))]

def quiver(word):
    nxt = next_positions(word)
    frozen = {k for k in range(N) if nxt[k] == N}
    B = [[0]*N for _ in range(N)]
    def arrow(a,b):
        if not {a,b} <= frozen:
            B[a][b] += 1
            B[b][a] -= 1
    for k in range(N):
        if nxt[k] < N:
            arrow(k,nxt[k])
        for l in range(k+1,N):
            if l < nxt[k] < nxt[l] and frozenset((word[k],word[l])) in EDGES:
                arrow(l,k)
    return B,frozen

def mutate(B,k,frozen):
    require(k not in frozen, "frozen vertex mutation")
    out = [[0]*N for _ in range(N)]
    for a in range(N):
        for b in range(N):
            if a in frozen and b in frozen:
                continue
            if a == k or b == k:
                out[a][b] = -B[a][b]
            else:
                out[a][b] = B[a][b] + max(B[a][k],0)*max(B[k][b],0) - max(-B[a][k],0)*max(-B[k][b],0)
    return out

def divide_binomial(p,k,D):
    """Exact division by (1+y_k)^D in Z[y_1^+-1,...,y_N^+-1]."""
    if not D:
        return p
    groups = defaultdict(lambda:defaultdict(int))
    for e,c in p.items():
        key = list(e)
        key[k] = 0
        groups[tuple(key)][e[k]] += c
    out = defaultdict(int)
    for key,coeffs in groups.items():
        coeffs = {j:c for j,c in coeffs.items() if c}
        if not coeffs:
            continue
        minimum = min(coeffs)
        # Shift the Laurent polynomial to an ordinary polynomial first.
        remainder = {j-minimum:c for j,c in coeffs.items()}
        quotient = defaultdict(int)
        while remainder and max(remainder) >= D:
            degree = max(remainder)-D
            leading = remainder[degree+D]
            quotient[degree] += leading
            for i in range(D+1):
                j = degree+i
                remainder[j] = remainder.get(j,0)-leading*comb(D,i)
                if remainder[j] == 0:
                    del remainder[j]
        require(not remainder,"non-exact binomial division")
        for j,c in quotient.items():
            e = list(key)
            e[k] = j+minimum
            out[tuple(e)] += c
    return {e:c for e,c in out.items() if c}

def pullback(p,B,k):
    """Substitute a single reciprocal-X mutation, using PRE-mutation B."""
    pending = []
    for e,c in p.items():
        f = list(e)
        f[k] = -e[k] + sum(-B[a][k]*e[a] for a in range(N) if a != k and B[a][k] < 0)
        power = sum(B[a][k]*e[a] for a in range(N) if a != k)
        pending.append((tuple(f),c,power))
    D = max(0,-min(power for _,_,power in pending))
    numerator = defaultdict(int)
    for e,c,power in pending:
        for j in range(power+D+1):
            f = list(e)
            f[k] += j
            numerator[tuple(f)] += c*comb(power+D,j)
    return divide_binomial(dict(numerator),k,D)

def reflect(root,i):
    out = list(root)
    out[i] -= dot(CARTAN[i],root)
    return tuple(out)

def weyl_roots(word):
    columns = [tuple(int(i == j) for i in range(4)) for j in range(4)]
    inversions=[]
    for letter in word:
        i = letter-1
        inversions.append(columns[i])
        columns = [tuple(columns[j][a]-CARTAN[i][j]*columns[i][a] for a in range(4)) for j in range(4)]
    return inversions,columns

def root_closure():
    found = {tuple(int(i == j) for i in range(4)) for j in range(4)}
    todo = deque(found)
    while todo:
        r=todo.popleft()
        for i in range(4):
            s=reflect(r,i)
            if s not in found:
                found.add(s)
                todo.append(s)
    return found

def rank(rows):
    a = [list(map(Fraction,r)) for r in rows]
    pivot=0
    for column in range(len(a[0])):
        hit=next((i for i in range(pivot,len(a)) if a[i][column]),None)
        if hit is None:
            continue
        a[pivot],a[hit]=a[hit],a[pivot]
        d=a[pivot][column]
        a[pivot]=[x/d for x in a[pivot]]
        for i in range(len(a)):
            if i != pivot:
                d=a[i][column]
                a[i]=[x-d*y for x,y in zip(a[i],a[pivot])]
        pivot+=1
        if pivot==len(a):
            break
    return pivot

def proof_data(text):
    rows=[]; zs=[]
    for _,digits,v in re.findall(r"\|(\d+)\|([012]{12})\|(\([^|]+\))\|",text):
        rows.append(tuple(map(int,digits)))
        zs.append(ast.literal_eval(v))
    require(len(rows)==22 and len(zs)==22,"PROOF table parse")
    return rows,zs

def audit_data(text):
    rows=[]; vs=[]
    for line in text.splitlines():
        m = re.fullmatch(r"\| (\d+) \| W_[1-4] \| (.*?) \|",line)
        if m:
            e=[0]*N
            for position,exponent in re.findall(r"y_(\d+)(?:\^(\d+))?",m.group(2)):
                e[int(position)-1] += int(exponent or 1)
            rows.append(tuple(e))
        m = re.fullmatch(r"\| (\d+) \| (\([^|]+\)) \|",line)
        if m:
            vs.append(ast.literal_eval(m.group(2)))
    require(len(rows)==22 and len(vs)==22,"AUDIT table parse")
    return rows,vs

def separators_valid(rows,zs):
    return len(rows)==len(zs) and all(len(z)==N and dot(a,z)==(-1 if i==j else max(0,dot(a,z))) for j,z in enumerate(zs) for i,a in enumerate(rows))

def polynomial_matches(actual,rows):
    return actual == {r:1 for r in rows} and len(rows)==len(set(rows))

def reconstruct_frozen(B,frozen,f,route):
    matrices=[B]
    for k in route:
        matrices.append(mutate(matrices[-1],k-1,frozen))
    require(all(matrices[-1][f-1][a]<=0 for a in range(N) if a not in frozen),"not optimized")
    p=Y[f]; sizes=[]
    for j in reversed(range(len(route))):
        p=pullback(p,matrices[j],route[j]-1)
        require(all(c>0 and min(e)>=0 for e,c in p.items()),"not positive polynomial after pullback")
        sizes.append(len(p))
    return p,matrices,sizes

def mutate_values(values,B,k):
    out=list(values)
    out[k]=1/values[k]
    for a in range(N):
        if a == k:
            continue
        b=B[a][k]
        out[a]=values[a]*(1+values[k])**b if b>=0 else values[a]*values[k]**(-b)*(1+values[k])**b
    return out

def evaluate(p,values):
    out=Fraction(0)
    for e,c in p.items():
        term=Fraction(c)
        for power,value in zip(e,values):
            term*=value**power
        out+=term
    return out

def main():
    data=json.loads(DATA.read_text())
    require(data["word"] == list(WORD), "certificate word metadata differs")
    rows=[tuple(r["a"]) for r in data["certificate_rows"]]
    zs=[tuple(r["z"]) for r in data["certificate_rows"]]
    audit_rows=[tuple(r["a"]) for r in data["independent_certificate_rows"]]
    vs=[tuple(r["v"]) for r in data["independent_certificate_rows"]]
    B,frozen=quiver(WORD)
    arrows=[(a+1,b+1) for a in range(N) for b in range(N) if B[a][b]>0]
    expected_arrows=((1,7),(2,4),(3,2),(3,9),(4,6),(5,4),(5,11),(6,1),(6,8),(7,6),(8,3),(8,10),(9,8),(10,5),(10,12),(11,10))
    require(set(arrows)==set(expected_arrows),"quiver arrows")
    require(frozen=={6,8,10,11},"frozen vertices")
    inversions,columns=weyl_roots(WORD)
    roots=root_closure()
    positive={r for r in roots if all(x>=0 for x in r)}
    require(len(roots)==24 and len(positive)==12,"D4 root closure")
    require(len(set(inversions))==12 and set(inversions)==positive,"inversion roots")
    require(columns==[tuple(-int(i==j) for i in range(4)) for j in range(4)],"longest matrix is not -I")
    # Closed form is assembled independently as a polynomial dictionary.
    A=add(ONE,Y[3],mul(Y[2],Y[3]))
    BB=mul(mul(Y[2],Y[3]),mul(Y[4],Y[5]))
    F7=add(ONE,Y[6],mul(mul(Y[6],Y[8]),A),mul(mul(mul(Y[6],Y[8]),Y[10]),add(mul(add(ONE,Y[5]),A),mul(BB,add(ONE,Y[6],mul(Y[1],Y[6]))))))
    F9=add(ONE,Y[8],mul(mul(Y[8],Y[10]),add(ONE,Y[5],mul(Y[4],Y[5]))))
    expected=add(mul(Y[7],F7),mul(Y[9],F9),mul(Y[11],add(ONE,Y[10])),Y[12])
    routes={7:(2,6,1,3,4,8,5,10),9:(4,8,5,10),11:(10,),12:()}
    summands={}; routes_report={}
    for f,route in routes.items():
        p,matrices,sizes=reconstruct_frozen(B,frozen,f,route)
        for shift in (1,2,5):
            original=[Fraction(a+shift,a+shift+1) for a in range(N)]
            values=original
            for j,k in enumerate(route):
                values=mutate_values(values,matrices[j],k-1)
            require(values[f-1]==evaluate(p,original),"forward rational evaluation differs from reverse polynomial pullback")
        summands[f]=p
        routes_report[f]={"route":list(route),"optimized_frozen_row":matrices[-1][f-1],"reverse_pullback_term_counts":sizes}
    actual=add(*summands.values())
    require(actual==expected,"optimized pullback differs from closed formula")
    require(polynomial_matches(actual,rows),"PROOF support differs")
    require(polynomial_matches(actual,audit_rows),"AUDIT support differs")
    require(separators_valid(rows,zs),"PROOF separation failed")
    require(separators_valid(audit_rows,[tuple(-x for x in v) for v in vs]),"AUDIT sign/table separation failed")
    require(len(actual)==22 and all(c==1 for c in actual.values()),"coefficient claim")
    squared=[j+1 for j,e in enumerate(rows) if e[5]==2]
    require(squared==[21,22],"squared terms")
    K=[]
    nxt=next_positions(WORD)
    for k in range(N):
        K.append([1 if l==k or l==nxt[k] else CARTAN[WORD[k]-1][WORD[l]-1] if k<l<nxt[k] else 0 for l in range(N)])
    transformed=[tuple(sum(a[k]*K[k][l] for k in range(N)) for l in range(N)) for a in rows]
    require(all(abs(x)<=1 for a in transformed for x in a),"pullback exponent bound")
    require(transformed[20]==(0,1,0,1,0,1,-1,0,0,0,0,0),"row21 chamber map")
    require(transformed[21]==(1,0,0,0,0,0,0,0,0,0,0,0),"row22 chamber map")
    require(rank(rows)==12 and rank(transformed)==12,"rank and lineality")
    u=tuple(int(i in frozen) for i in range(N))
    require(all(dot(a,u)==1 for a in rows),"special interior vector")
    facet_points=[tuple(z[i]+u[i] for i in range(N)) for z in zs]
    require(all(dot(a,p)==0 if i==j else dot(a,p)>=1 for j,p in enumerate(facet_points) for i,a in enumerate(rows)),"facet-interior certificates")
    # Each unit tangent e_l - a_l/a_p e_p lies on a_j^perp.
    # The following independent rational check verifies 11-dimensional tangent spaces.
    for a in rows:
        pivot=next(i for i,x in enumerate(a) if x)
        tangents=[]
        for l in range(N):
            if l != pivot:
                t=[Fraction(0)]*N
                t[l]=1
                t[pivot]=-Fraction(a[l],a[pivot])
                tangents.append(t)
        require(rank(tangents)==11 and all(dot(a,t)==0 for t in tangents),"facet tangent rank")
    controls=[]
    def reject(label,condition):
        require(not condition,"negative control accepted: "+label)
        controls.append(label)
    changed=dict(actual); changed[rows[20]]=2
    reject("coefficient 2 instead of 1",polynomial_matches(changed,rows))
    dropped=dict(actual); dropped.pop(rows[20])
    reject("drop squared term",polynomial_matches(dropped,rows))
    clamped=[tuple(min(x,1) for x in a) for a in rows]
    reject("clamp exponent 2 to 1",polynomial_matches(actual,clamped))
    reject("wrong exponent-row signs",separators_valid([tuple(-x for x in a) for a in rows],zs))
    for j in range(22):
        bad=list(zs); bad[j]=ZERO
        reject("zero separator "+str(j+1),separators_valid(rows,bad))
    Bwrong=[r[:] for r in B]; Bwrong[0][6]*=-1; Bwrong[6][0]*=-1
    try:
        wrong_polynomial,_,_=reconstruct_frozen(Bwrong,frozen,7,routes[7])
        wrong_accepted=wrong_polynomial==summands[7]
    except ValueError:
        wrong_accepted=False
    reject("reverse horizontal arrow 1->7",wrong_accepted)
    try:
        wrong_polynomial,_,_=reconstruct_frozen(B,frozen,7,routes[7][:-1])
        wrong_accepted=wrong_polynomial==summands[7]
    except ValueError:
        wrong_accepted=False
    reject("omit final optimizing mutation for frozen 7",wrong_accepted)
    require(WORD[:-1]+(4,) != WORD,"control precondition")
    badroots,badcolumns=weyl_roots(WORD[:-1]+(4,))
    reject("wrong final word letter",len(set(badroots))==12 and set(badroots)==positive and badcolumns==columns)
    # Sampled exact-rational smoke checks of the independent mutation formula.
    # These are controls only; the identities proving this candidate are the
    # complete sparse-polynomial reconstruction above, not sampled evaluations.
    for k in range(N):
        if k in frozen:
            continue
        Bp=mutate(B,k,frozen)
        require(mutate(Bp,k,frozen)==B,"matrix mutation involution")
        for shift in (1,2,5):
            values=[Fraction(a+shift,a+shift+1) for a in range(N)]
            require(mutate_values(mutate_values(values,B,k),Bp,k)==values,"sampled rational mutation involution")
    # Exact division fixtures exercise both cancellation and its failure case.
    fixture=mul(monomial(2),mul(add(ONE,Y[6]),add(ONE,Y[6])))
    require(divide_binomial(fixture,5,2)==monomial(2),"binomial division fixture")
    try:
        divide_binomial(ONE,5,1)
        division_rejected=False
    except ValueError:
        division_rejected=True
    reject("accept a non-Laurent 1/(1+y6) quotient",not division_rejected)
    report={
        "status":"PASS",
        "independence":"Standard-library canonical reconstruction; two certificate tables loaded as inert JSON comparison data; no source-author code or historical computation is executed.",
        "word":WORD,"positive_roots":inversions,"weyl_columns":columns,
        "arrows":arrows,"frozen_positions":[i+1 for i in sorted(frozen)],
        "routes":routes_report,"combined_terms":len(actual),
        "summand_terms":{f:len(p) for f,p in summands.items()},
        "support_and_coefficients":[{"exponent":a,"coefficient":actual[a]} for a in rows],
        "proof_dot_products":[[dot(a,z) for a in rows] for z in zs],
        "audit_dot_products":[[dot(a,tuple(-x for x in v)) for a in audit_rows] for v in vs],
        "interior_point":u,"facet_relative_interior_points":facet_points,
        "support_rank":rank(rows),"cone_dimension":12,"lineality_dimension":0,"facet_dimension":11,
        "chamber_K":K,"transformed_support":transformed,"squared_rows":squared,
        "negative_controls_rejected":controls,
        "certificate_sha256":hashlib.sha256(DATA.read_bytes()).hexdigest(),
    }
    target=HERE/"results.json"
    target.write_text(json.dumps(report,indent=2)+"\n")
    print(json.dumps({"status":"PASS","terms":22,"separation_checks":968,"rank":12,"facets":22,"controls_rejected":len(controls),"result":str(target)},sort_keys=True))

if __name__ == "__main__":
    main()
