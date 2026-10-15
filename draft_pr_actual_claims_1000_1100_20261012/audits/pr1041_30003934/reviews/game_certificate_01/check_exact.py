#!/usr/bin/env python3
"""Fresh standard-library exact tests, independent of submitted scripts.

No floating point and no imported submitted computations. Finite tests cannot
prove the source-flow interface for every PARTITION instance.
"""
from fractions import Fraction as Q
from math import lcm, factorial
from pathlib import Path
import itertools, json, datetime, hashlib

ROOT = Path(__file__).resolve().parent

def dot(a,b): return sum((x*y for x,y in zip(a,b)),Q(0))
def neg(a): return [-x for x in a]

def network(weights):
    n=len(weights); S=sum(weights); a=[Q(w,24*S) for w in weights]
    vertices=['s','t']; edges=[]
    def add(u,v,cap,c): edges.append([u,v,Q(cap),Q(c)])
    for sign in [1,-1]:
        for i in range(n+1): vertices += [(sign,'s',i),(sign,'t',i)]
        add((sign,'s',0),(sign,'t',0),1,Q(1,120*S))
        for i in range(1,n+1):
            vi=sign*a[i-1]; cap=2**(i-1)
            add((sign,'s',i),(sign,'s',i-1),cap,vi/2)
            add((sign,'t',i-1),(sign,'t',i),cap,vi/2)
            add((sign,'s',i),(sign,'t',i-1),cap,(2**i-1-vi)/2)
            add((sign,'s',i-1),(sign,'t',i),cap,(2**i-1-vi)/2)
        add('s',(sign,'s',n),2**n,0)
        add((sign,'t',n),'t',2**n,0)
    distinguished=len(edges); add((1,'s',0),(-1,'t',0),1,0)
    D=lcm(*(e[3].denominator for e in edges))
    for i,e in enumerate(edges,1): e[3]+=Q(1,4*D*3**i)
    order=[]; unseen=set(vertices)
    while unseen:
        ready=[v for v in vertices if v in unseen and not any(e[1]==v and e[0] in unseen for e in edges)]
        assert ready, 'not a DAG'
        for v in ready: order.append(v);unseen.remove(v)
    ranks={v:i for i,v in enumerate(order)}
    H=1+max(abs(e[3]) for e in edges)
    for e in edges: e[3]+=H*(ranks[e[1]]-ranks[e[0]]);assert e[3]>0
    return vertices,edges,distinguished,Q(2**(n+1))

def residual(edges,flow):
    r=[]
    for i,(u,v,cap,c) in enumerate(edges):
        if flow[i]<cap:r.append((u,v,c,i,1,cap-flow[i]))
        if flow[i]>0:r.append((v,u,-c,i,-1,flow[i]))
    return r

def shortest(vertices,res,source=None):
    dist={v: (Q(0) if source is None or v==source else None) for v in vertices};pred={}
    for iteration in range(len(vertices)):
        changed=False
        for u,v,c,i,sign,capacity in res:
            if dist[u] is not None and (dist[v] is None or dist[v]>dist[u]+c):
                dist[v]=dist[u]+c;pred[v]=(u,v,c,i,sign,capacity);changed=True
        if not changed:return dist,pred
    raise AssertionError('negative residual cycle')

def ssp(vertices,edges,e,F):
    f=[Q(0)]*len(edges);q=Q(0);segments=[]
    while True:
        dist,pred=shortest(vertices,residual(edges,f),'s')
        if dist['t'] is None:break
        path=[];v='t'
        while v!='s':
            step=pred[v];path.append(step);v=step[0]
            assert len(path)<len(vertices)
        amount=min(step[-1] for step in path)
        old=f[:]
        for u,v,c,i,sign,cap in path:f[i]+=sign*amount
        segments.append((q,amount,old,f[:]))
        q+=amount
        shortest(vertices,residual(edges,f))
    assert q==F and f[e]==0
    return segments

def game(vertices,edges,e,F):
    V=len(vertices);p=len(edges);L=V-1;K=Q(1,2*L);eps=K/2;m=p+2
    h=[Q(0)]+[F]*(p+1);q=h[:];q[e+2]-=K*L*F
    c=[Q(0),Q(0)]+[L*F*arc[3] for arc in edges]
    R=[];r=[];s=[];labels=[]
    def constraint(row,rhs,parameter,label): R.append(row);r.append(Q(rhs));s.append(Q(parameter));labels.append(label)
    for i,arc in enumerate(edges):
        row=[Q(0)]*m;row[i+2]=L*F;constraint(row,arc[2],0,('cap',i))
    for v in vertices:
        d=int(v=='s')-int(v=='t');row=[-d*z for z in q]
        for i,arc in enumerate(edges):row[i+2]+=L*F*(int(arc[0]==v)-int(arc[1]==v))
        constraint(row,0,0,('cons+',v));constraint(neg(row),0,0,('cons-',v))
    parameter_index=len(R);constraint(q,0,1,('param+',));constraint(neg(q),0,-1,('param-',))
    # One common integer Q clears the dual constraint coefficients and RHS.
    clear=lcm(*(z.denominator for row in R for z in row),*(z.denominator for z in c))
    H0=max([1,clear]+[abs(int(z*clear)) for row in R for z in row]+[abs(int(z*clear)) for z in c])
    k=len(R);d0=k+1;C=k*factorial(d0)*H0**d0;M=C+1
    a=[-eps]+[F-eps]*(m-1);b=[Q(0)]+[-M*z for z in s]
    A=[[Q(0)]*(k+1) for _ in range(m)]
    for i in range(m):
        A[i][0]=-c[i]
        for j in range(k):A[i][j+1]=-c[i]-M*R[j][i]+M*r[j]
    B=[[-A[i][j]+a[i]*b[j] for j in range(k+1)] for i in range(m)]
    assert all(A[i][j]+B[i][j]==a[i]*b[j] for i in range(m) for j in range(k+1))
    assert any(a) and M in b and -M in b
    assert m==p+2 and len(b)==p+2*V+3
    return dict(V=V,p=p,L=L,K=K,eps=eps,F=F,e=e,h=h,q=q,c=c,R=R,r=r,s=s,labels=labels,M=M,a=a,b=b,A=A,B=B,diagnostic=parameter_index+1)

def simplex(g,flow,q):
    h=q+g['K']*flow[g['e']];LF=g['L']*g['F']
    x=[1-h/g['F'],h/g['F']-sum(flow)/LF]+[v/LF for v in flow]
    assert min(x)>=0 and sum(x)==1 and dot(g['q'],x)==q
    return x

def dual_opponent(g,vertices,edges,flow,q):
    # Exact network dual from residual shortest-path potentials, independently
    # checked after lifting into the actual simplex LP.
    potentials,_=shortest(vertices,residual(edges,flow))
    mu=[Q(0)]*len(g['R'])
    for i,(u,v,cap,c) in enumerate(edges):mu[i]=max(Q(0),-(c+potentials[u]-potentials[v]))
    offset=len(edges)
    for i,v in enumerate(vertices):
        mu[offset+2*i]=max(Q(0),potentials[v]);mu[offset+2*i+1]=max(Q(0),-potentials[v])
    beta=potentials['s']-potentials['t'];mu[-2]=max(Q(0),beta);mu[-1]=max(Q(0),-beta)
    x=simplex(g,flow,q)
    slack=[g['c'][i]+sum(mu[j]*g['R'][j][i] for j in range(len(mu))) for i in range(len(x))]
    assert min(slack)>=0 and dot(slack,x)==0
    violations=[dot(row,x)-rr-ss*q for row,rr,ss in zip(g['R'],g['r'],g['s'])]
    assert max(violations)<=0 and dot(mu,violations)==0
    assert dot(g['c'],x)==-sum(z*(rr+ss*q) for z,rr,ss in zip(mu,g['r'],g['s']))
    assert sum(mu)<g['M']
    return [1-sum(mu)/g['M']]+[z/g['M'] for z in mu]

def verify(A,B,x,y):
    assert min(x)>=0 and min(y)>=0 and sum(x)==sum(y)==1
    row=[dot(z,y) for z in A];col=[sum(x[i]*B[i][j] for i in range(len(x))) for j in range(len(y))]
    assert max(row)<=dot(x,row) and max(col)<=dot(y,col)
    return True

def rejected(operation):
    try:operation()
    except (AssertionError,ValueError,ZeroDivisionError):return True
    return False

def rank_one(A,B):
    C=[[x+y for x,y in zip(ar,br)] for ar,br in zip(A,B)]
    pivot=next(((i,j) for i,row in enumerate(C) for j,z in enumerate(row) if z),None)
    if pivot is None:return False
    i0,j0=pivot
    return all(C[i][j]*C[i0][j0]==C[i][j0]*C[i0][j] for i in range(len(C)) for j in range(len(C[0])))

def certify_nonunique(A,B,pair1,pair2):
    assert rank_one(A,B)
    verify(A,B,*pair1);verify(A,B,*pair2)
    assert pair1!=pair2
    return True

def phi(g,x,lam,M=None):
    M=g['M'] if M is None else M
    return dot(g['c'],x)+M*max([Q(0)]+[dot(row,x)-rr-ss*lam for row,rr,ss in zip(g['R'],g['r'],g['s'])])

def whole_case(weights):
    vertices,edges,e,F=network(weights);segments=ssp(vertices,edges,e,F);g=game(vertices,edges,e,F)
    m=len(g['a']);N=len(g['b']);x0=[Q(1)]+[Q(0)]*(m-1);y0=[Q(0)]*N;y0[g['diagnostic']]=1
    assert verify(g['A'],g['B'],x0,y0)
    rd=g['diagnostic'];assert all(g['A'][i][rd]<g['A'][0][rd] for i in range(1,m))
    assert all(g['B'][0][j]<g['B'][0][rd] for j in range(N) if j!=rd)
    negative_checks=0
    for lam in [-2*g['eps'],-g['eps'],-g['eps']/2]:
        assert phi(g,x0,lam)==-g['M']*lam
        for i in range(1,m):
            x=[Q(0)]*m;x[i]=1;assert phi(g,x,lam)>phi(g,x0,lam);negative_checks+=1
        penalties=[dot(row,x0)-rr-ss*lam for row,rr,ss in zip(g['R'],g['r'],g['s'])]
        assert penalties.count(max(penalties))==1
    positive=[];certified_optima=0;half_candidates=[]
    for q,amount,old,new in segments:
        for fraction in [Q(0),Q(1,2),Q(1)]:
            lam=q+amount*fraction;flow=[u+(v-u)*fraction for u,v in zip(old,new)]
            if lam+g['K']*flow[e]>F:continue
            x=simplex(g,flow,lam);y=dual_opponent(g,vertices,edges,flow,lam)
            auxiliary=[[g['A'][i][j]-lam*g['b'][j] for j in range(N)] for i in range(m)]
            assert verify(auxiliary,[[ -z for z in row] for row in auxiliary],x,y);certified_optima+=1
            assert phi(g,x,lam)==dot(g['c'],x)
            if flow[e]==Q(1,2):
                assert dot(g['a'],x)==lam and lam<=F-g['eps']
                assert verify(g['A'],g['B'],x,y)
                positive.append((lam,x,y));half_candidates.append(str(lam))
    brute=any(sum(subset)*2==sum(weights) for mask in range(1<<len(weights)) for subset in [[weights[i] for i in range(len(weights)) if mask>>i&1]])
    assert bool(positive)==brute
    # Deliberate sign failure must fail the original-game equilibrium verifier.
    neg_wrong_sign=False
    if positive:
        lam,x,y=positive[0];badB=[[ -g['A'][i][j]-g['a'][i]*g['b'][j] for j in range(N)] for i in range(m)]
        neg_wrong_sign=rejected(lambda:verify(g['A'],badB,x,y));assert neg_wrong_sign
    assert rejected(lambda:verify(g['A'],g['B'],x0,[Q(1)]+[Q(0)]*(N-1)))
    # Too-small penalty: at lambda=F the zero flow is cheaper than a feasible
    # max flow when M=0, and is infeasible. This is a real control for exactness.
    final_flow=segments[-1][3];xf=simplex(g,final_flow,F)
    assert phi(g,x0,F,M=0)<phi(g,xf,F,M=0)
    assert max(dot(row,x0)-rr-ss*F for row,rr,ss in zip(g['R'],g['r'],g['s']))>0
    return {'weights':weights,'partition_yes':brute,'dimensions':[m,N],'M_bits':g['M'].bit_length(),'ssp_segments':len(segments),'exact_auxiliary_optimum_checks':certified_optima,'negative_vertex_checks':negative_checks,'additional_pair_parameters':sorted(set(half_candidates)),'wrong_B_sign_rejected':neg_wrong_sign if positive else 'not_applicable','wrong_default_column_rejected':True,'M_zero_infeasible_improvement':True}

def certificate_controls():
    A=[[Q(1),Q(6)],[Q(0),Q(9)]];B=[[Q(1),Q(0)],[Q(6),Q(9)]]
    witnesses=[([Q(1),Q(0)],[Q(1),Q(0)]),([Q(0),Q(1)],[Q(0),Q(1)]),([Q(3,4),Q(1,4)],[Q(3,4),Q(1,4)])]
    for x,y in witnesses:assert verify(A,B,x,y)
    assert certify_nonunique(A,B,witnesses[0],witnesses[1])
    assert rejected(lambda:certify_nonunique(A,B,witnesses[0],witnesses[0]))
    assert rejected(lambda:verify(A,B,[Q(1,2)]*2,[Q(1,2)]*2))
    assert rejected(lambda:verify(A,B,[Q(1),Q(1)],[Q(1),Q(0)]))
    assert rejected(lambda:verify(A,B,[Q(-1),Q(2)],[Q(1),Q(0)]))
    # Rank-one continuum: any two rational boundary pairs certify two distinct
    # pairs even when the originally observed witness has irrational entries.
    zero=[[Q(0)]*2 for _ in range(2)];ones=[[Q(1)]*2 for _ in range(2)]
    assert verify(zero,ones,*witnesses[0]) and verify(zero,ones,*witnesses[1])
    assert certify_nonunique(zero,ones,witnesses[0],witnesses[1])
    assert not rank_one(zero,zero)
    assert not rank_one([[Q(1),Q(0)],[Q(0),Q(1)]],zero)
    # One player has only one pure action, the other has a continuum.
    assert verify([[Q(0),Q(0)]],[[Q(1),Q(1)]],[Q(1)],[Q(1),Q(0)])
    assert verify([[Q(0),Q(0)]],[[Q(1),Q(1)]],[Q(1)],[Q(0),Q(1)])
    return {'three_equilibrium_example':True,'two_pair_certificate_accepted':True,'duplicate_pair_certificate_rejected':True,'rank_zero_and_rank_two_invalid_recognized':True,'non_equilibrium_midpoint_rejected':True,'non_unit_and_negative_vectors_rejected':True,'degenerate_rank_one_continuum_boundary_witnesses':True,'one_by_two_continuum':True}

def toy_penalty():
    # x=(1-t,t), Rx=t<=lambda/2, c=-t; exact mu=1 works uniformly
    # for all real lambda in [0,2]. M>1 is necessary to exclude all infeasible
    # minimizers: M=1 makes the objective flat on the entire infeasible interval.
    checks=0
    for lam in [Q(0),Q(1,3),Q(1),Q(2)]:
        optimum=-lam/2
        for t in [Q(0),Q(1,7),Q(1,2),Q(5,7),Q(1),lam/2]:
            val=-t+2*max(Q(0),t-lam/2)
            assert val>=optimum
            if t>lam/2:assert val>optimum
            checks+=1
    lam=Q(1);t=Q(3,4)
    assert -t+max(Q(0),t-lam/2)==-lam/2 and t>lam/2
    return {'exact_checks':checks,'M_equals_dual_norm_infeasible_tie':True}

def main():
    data={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'arithmetic':'fractions.Fraction; integer determinants bound; exact residual shortest paths and direct best-response checks','source_code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'whole_games':[whole_case(w) for w in [[1],[1,1],[1,2],[1,2,3],[1,2,4],[2,2,2]]],'certificates':certificate_controls(),'toy_penalty':toy_penalty(),'limits':'Finite game checks certify each displayed pair and auxiliary optimum by exact inequalities. They do not prove complete equilibrium enumeration or the source-flow interface for arbitrary instances. Submitted old six-game and 39-network checks were not accessed or replayed.'}
    (ROOT/'EXACT_RESULTS.json').write_text(json.dumps(data,indent=2)+'\n');print(json.dumps(data,indent=2))

if __name__=='__main__':main()
