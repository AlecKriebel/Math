#!/usr/bin/env python3
"""Independent exact adversarial controls; no packaged helper imports.
Written and first run before the published helper code was inspected.
These finite controls do not prove stochastic convergence or almost-sure claims.
"""
from fractions import Fraction as Q
from itertools import combinations
from math import cos,sin,pi,factorial
from pathlib import Path
import json,datetime,hashlib
checks=0
def need(ok,msg):
    global checks
    checks+=1
    if not ok:raise RuntimeError(msg)
def mm(A,B):return [[sum(x*y for x,y in zip(row,col)) for col in zip(*B)] for row in A]
def quad(M,w):return sum(w[i]*M[i][j]*w[j] for i in range(len(w)) for j in range(len(w)))
def determinant(A):
    A=[list(map(Q,row)) for row in A];d=Q(1)
    for i in range(len(A)):
        j=next((j for j in range(i,len(A)) if A[j][i]),None)
        if j is None:return Q(0)
        if j!=i:A[i],A[j]=A[j],A[i];d=-d
        v=A[i][i];d*=v
        for j in range(i+1,len(A)):
            t=A[j][i]/v
            for k in range(i,len(A)):A[j][k]-=t*A[i][k]
    return d

def equilibrium(edges,a,alpha,b):
    n=len(b);m=len(edges);incident=[[i for i,e in enumerate(edges) if v in e] for v in range(n)]
    S=[sum(a[e]**alpha for e in I) for I in incident]
    rates=[b[v]*S[v] for v in range(n)]
    for i,(u,v) in enumerate(edges):need(a[i]**(1-alpha)==b[u]+b[v],'equilibrium relation')
    F=[-a[i]+sum(rates[v]*a[i]**alpha/S[v] for v in edges[i]) for i in range(m)]
    need(F==[0]*m and sum(a)==sum(rates),'exact equilibrium and total rate')
    J=[[Q(-int(i==j))+sum(rates[v]*(alpha*a[i]**(alpha-1)*int(i==j)/S[v]-alpha*a[i]**alpha*a[j]**(alpha-1)/S[v]**2) for v in edges[i] if j in incident[v]) for j in range(m)] for i in range(m)]
    H=[[((alpha-1)*a[i]**(1-2*alpha)*int(i==j)-alpha*sum(rates[v]/S[v]**2 for v in edges[i] if j in incident[v]))/alpha**2 for j in range(m)] for i in range(m)]
    need(all(sum(J[i][j] for i in range(m))==-1 for j in range(m)),'no radial positive eigenvalue')
    HL=[[J[i][j]/a[i] for j in range(m)] for i in range(m)]
    need(HL==list(map(list,zip(*HL))),'positive diagonal similarity to symmetric matrix')
    need(all(HL[i][j]==alpha*a[i]**(alpha-1)*H[i][j]*alpha*a[j]**(alpha-1) for i in range(m) for j in range(m)),'Hessian congruence at equilibrium')
    return {'rates':rates,'S':S,'J':J,'H':H,'HL':HL}

# Fully explicit arbitrary-weight/rate equilibria: at alpha=2, a_uv=1/(b_u+b_v).
# Cycle perturbations are zero on chords and attachments.
cycle_results=[]
for m in range(3,12):
    for variant in range(5):
        edges=[tuple(sorted((i,(i+1)%m))) for i in range(m)]
        if variant>=1 and m>=4:edges.append((0,2))
        if variant>=2:edges.extend([(0,m),(m,m+1)])
        if variant>=3:edges.append((1,m+2))
        if variant>=4:edges.append((2,m+3))
        n=max(max(e) for e in edges)+1
        b=[Q((i*7+variant*3)%17+1,(i*5+3)%11+1) for i in range(n)]
        a=[1/(b[u]+b[v]) for u,v in edges]
        r=equilibrium(edges,a,2,b)
        D=sum(a[i]**-3 for i in range(m));C=sum(b[v]/r['S'][v] for v in range(m))
        need(D>=4*C,'weighted cycle inequality')
        candidates=[]
        if m%2==0:candidates=[[Q((-1)**i) if i<m else Q(0) for i in range(len(edges))]]
        else:
            theta=pi-pi/m
            for fn in (cos,sin):candidates.append([Q(fn(i*theta)).limit_denominator(1000000) if i<m else Q(0) for i in range(len(edges))])
        energies=[quad(r['H'],w) for w in candidates]
        need(max(energies)>0,'exact positive rational Hessian witness')
        j=max(range(len(energies)),key=lambda j:energies[j]);w=candidates[j]
        cycle_results.append({'cycle_length':m,'variant':variant,'edges':edges,'b':b,'a':a,'rates':r['rates'],'sum_D_minus_4sum_c':D-4*C,'witness':w,'exact_Hessian_energy':energies[j]})

# Exact triangle stability and endpoint: J=-I+alpha/4 times triangle Laplacian.
triangle=[]
for alpha in (Q(5,4),Q(4,3),Q(17,12),Q(17,4)):
    J=[[alpha/2-1 if i==j else -alpha/4 for j in range(3)] for i in range(3)]
    for w,e in [([1,1,1],Q(-1)),([1,-1,0],3*alpha/4-1),([1,1,-2],3*alpha/4-1)]:
        need([sum(J[i][j]*w[j] for j in range(3)) for i in range(3)]==[e*x for x in w],'triangle eigenvalues exact')
    triangle.append({'alpha':alpha,'radial':-1,'transverse':3*alpha/4-1})
need(triangle[0]['transverse']<0 and triangle[1]['transverse']==0 and triangle[2]['transverse']>0,'critical endpoint not strictly stable/unstable')

# Unequal-rate scope control: an exactly stable 4-edge path at alpha=5.
# This refutes an unrequested unequal-rate whisker extension, NOT the paper.
alpha=5;edges=[(i,i+1) for i in range(4)];a=list(map(Q,[1,10,100,1000]))
b=[Q(0)]*5;b[3]=Q(1,2*1000**4);b[4]=b[3]
for i in (2,1,0):b[i]=a[i]**(1-alpha)-b[i+1]
need(min(b)>0,'positive countercontrol rates')
r=equilibrium(edges,a,alpha,b)
minors=[determinant([[-r['HL'][i][j] for j in range(k)] for i in range(k)]) for k in range(1,5)]
need(all(x>0 for x in minors),'Sylvester exact negative-definite Hessian on length4 path')
unequal={'alpha':alpha,'edges':edges,'a':a,'b':b,'rates':r['rates'],'negative_Hessian_leading_principal_minors':minors,'conclusion':'Strictly stable non-whisker equilibrium at unequal positive rates. Scope control only; equal-rate theorem not contradicted.'}

# Exact whisker interval certificate reconstructed from endpoints and rational caps.
intervals=[(Q(17,4),Q(13,3),Q(29,5)),(Q(13,3),Q(9,2),Q(25,4)),(Q(9,2),Q(5),Q(243,32)),(Q(5),Q(6),Q(729,64)),(Q(6),Q(7),Q(2187,128))]
rows=[]
def f(a,s):return (s*s+(a-s)**2)/a
for A,B,T in intervals:
    need(T**B.denominator>=Q(3,2)**B.numerator,'rational power cap')
    S=T/(1+T);margin=1-1/A-f(Q(3,2),S)
    need(S>=Q(3,4) and margin>0,'closed interval strict endpoint margin')
    rows.append({'A':A,'B':B,'T':T,'S':S,'f':f(Q(3,2),S),'margin':margin})
need(all(intervals[i][1]==intervals[i+1][0] for i in range(4)),'closed interval cover without gaps')
need(1-Q(1,4)-f(Q(3,2),Q(29,34))<0,'false extension of first certificate to alpha4 rejected')
R=lambda a:2*a**7-3*a**6+2
need(R(Q(9,7))==Q(52763,823543)>0,'global polynomial minimum')
# Unbounded tail certificate, with exact rational exponential upper bounds.
sum4=sum(Q(8,5)**k/factorial(k) for k in range(5))
tail5=Q(8,5)**5/factorial(5)/(1-Q(4,15))
need(sum4==Q(9067,1875) and tail5==Q(4096,34375),'exponential exact series/tail')
need(sum4+tail5==Q(510973,103125)<6,'strict exponential bound')
prior=sum(Q(9,4)**k/factorial(k) for k in range(13))+Q(9,4)**13/factorial(13)/(1-Q(9,56))
need(prior==Q(191714244173193067,20206532637491200)<Q(19,2),'prior alpha24 arithmetic')
need(Q(9,4)*(prior+1)<Q(189,8)<24,'prior rate threshold')
# Arithmetic in Q(sqrt2), pairs x+y sqrt2; C=3-sqrt2.
def sq_add(a,b):return (a[0]+b[0],a[1]+b[1])
def sq_mul(a,b):return (a[0]*b[0]+2*a[1]*b[1],a[0]*b[1]+a[1]*b[0])
C=(Q(3),Q(-1));C2=sq_mul(C,C)
need(sq_add(C2,C)==(Q(14),Q(-7)),'C^2+C=7(C-1)')
need(Q(7,5)**2<2<Q(3,2)**2,'1<C<8/5 exact radical bracket')
for A in [Q(7),Q(8),Q(100),Q(10**9)]:
    need((6-A)/4<0 and Q(8,5)/A<Q(1,2),'tail half-endpoint and C/alpha interior')
    h=sq_add(sq_add((C2[0]/A,C2[1]/A),(-(A-1)*C[0]/A,-(A-1)*C[1]/A)),(Q(1),Q(0)))
    expected=(-(C[0]-1)*(1-7/A),-C[1]*(1-7/A))
    need(h==expected,'exact tail quadratic identity')

# Graph-only endpoint: exhaustive labelled simple graphs through six vertices.
# If internal edges form a matching, every nontrivial component is a tree of diameter<=3.
graph_counts={}
for n in range(1,7):
    possible=list(combinations(range(n),2));accepted=0
    for mask in range(1<<len(possible)):
        edges=[e for i,e in enumerate(possible) if (mask>>i)&1]
        adj=[set() for _ in range(n)]
        for u,v in edges:adj[u].add(v);adj[v].add(u)
        internal=[e for e in edges if len(adj[e[0]])>1 and len(adj[e[1]])>1]
        used=[v for e in internal for v in e]
        if len(used)!=len(set(used)):continue
        accepted+=1;seen=set()
        for root in range(n):
            if root in seen:continue
            comp={root};q=[root]
            while q:
                u=q.pop()
                for v in adj[u]-comp:comp.add(v);q.append(v)
            seen|=comp
            need(sum(len(adj[u]) for u in comp)==2*(len(comp)-1),'matching internal edges imply no cycle')
            for u in comp:
                dist={u:0};q=[u]
                for v in q:
                    for w in adj[v]-dist.keys():dist[w]=dist[v]+1;q.append(w)
                need(max(dist.values())<=3,'matching internal edges imply whisker diameter')
    graph_counts[n]=accepted

# Finite prefix reachability control; no stochastic simulation.
edges=[(0,1),(1,2),(0,2)];rates=[Q(1,3),Q(5,7),Q(2)];N=[1,1,1];target=[3,2,4];prob=Q(1)
for e,goal in enumerate(target):
    while N[e]<goal:
        v=edges[e][0];den=sum(N[j]**2 for j,x in enumerate(edges) if v in x)
        prob*=rates[v]/sum(rates)*Q(N[e]**2,den);N[e]+=1
need(N==target and prob>0,'positive unit-to-integer-count path')
result={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS','checks':checks,'independence':'Authored and run before packaged helpers; no stochastic simulations.','weighted_cycle_equilibria':cycle_results,'triangle_endpoints':triangle,'unequal_rate_scope_control':unequal,'closed_interval_rows':rows,'tail_exponential_upper_bound':sum4+tail5,'prior_exponential_upper_bound':prior,'internal_matching_graph_counts':graph_counts,'integer_initialization_path':{'target':target,'exact_probability':prob},'coverage_limits':['Finite exact controls do not prove stochastic convergence, support equality or attainment.','Universal cycle/whisker proofs separately reconstructed from the manuscript.','No equality-case result at alpha=4/3; no sharp whisker result.']}
def encode(x):
    if isinstance(x,Q):return str(x)
    raise TypeError(type(x))
print(json.dumps(result,default=encode,indent=2))
