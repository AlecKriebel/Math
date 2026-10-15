#!/usr/bin/env python3
"""Fresh independent exact checks; this is not the manuscript's omitted checker."""
from fractions import Fraction as Q
from itertools import product
from math import lcm
from pathlib import Path
import json,sys,datetime,hashlib
HERE=Path(__file__).resolve().parent

def demand(ok,msg):
    if not ok: raise RuntimeError(msg)

def build(w,delta=True):
    n=len(w);S=sum(w); a=[Q(z,24*S) for z in w]; eps=Q(1,24*S)
    E=[]; nodes=['s','t']
    for g,sgn in [('p',1),('m',-1)]:
        for i in range(n+1): nodes += [g+'s'+str(i),g+'t'+str(i)]
        E.append((g+'s0',g+'t0',1,eps/5 if delta else Q(0)))
        for i,v in enumerate(a,1):
            v*=sgn; cap=2**(i-1); cheap=v/2; dear=(2**i-1-v)/2
            E.extend([(g+'s'+str(i),g+'s'+str(i-1),cap,cheap),(g+'t'+str(i-1),g+'t'+str(i),cap,cheap),(g+'s'+str(i),g+'t'+str(i-1),cap,dear),(g+'s'+str(i-1),g+'t'+str(i),cap,dear)])
        E.extend([('s',g+'s'+str(n),2**n,Q(0)),(g+'t'+str(n),'t',2**n,Q(0))])
    E.append(('ps0','mt0',1,Q(0)))
    D=lcm(*(e[3].denominator for e in E)); rho=[Q(1,4*D*3**(i+1)) for i in range(len(E))]
    pert=[e[3]+r for e,r in zip(E,rho)]
    # independently derive a topological order rather than trusting its existence
    order=[];incoming={v:0 for v in nodes};adj={v:[] for v in nodes}
    for u,v,cap,c in E: incoming[v]+=1;adj[u].append(v)
    ready=sorted(v for v in nodes if incoming[v]==0)
    while ready:
        u=ready.pop(0);order.append(u)
        for v in adj[u]:
            incoming[v]-=1
            if incoming[v]==0: ready.append(v);ready.sort()
    demand(len(order)==len(nodes),'network cycle'); rank={v:i for i,v in enumerate(order)}
    H=1+max(map(abs,pert)); shifted=[c+H*(rank[v]-rank[u]) for (u,v,cap,z),c in zip(E,pert)]
    demand(all(z>0 for z in shifted),'positive potential');demand(len(E)==8*n+7 and len(nodes)==4*n+6,'size')
    return {'w':w,'n':n,'nodes':nodes,'E':E,'D':D,'rho':rho,'orig':[e[3] for e in E],'pert':pert,'shifted':shifted,'H':H,'rank':rank,'F':2**(n+1),'e':len(E)-1}

def residual(B,f,cost):
    R={v:[] for v in B['nodes']}
    for i,((u,v,cap,z),c) in enumerate(zip(B['E'],cost)):
        if f[i]<cap: R[u].append((v,i,1,c,Q(cap)-f[i]))
        if f[i]>0: R[v].append((u,i,-1,-c,f[i]))
    return R

def paths(B,f,cost):
    R=residual(B,f,cost);result=[]
    def visit(u,seen,edges,c):
        if u=='t':result.append((c,tuple(edges)));return
        for v,i,d,z,cap in R[u]:
            if v not in seen:visit(v,seen|{v},edges+[(i,d,cap)],c+z)
    visit('s',{'s'},[],Q(0));return result

def shortest(B,f,cost):
    P=paths(B,f,cost)
    if not P:return []
    z=min(c for c,p in P);return [p for c,p in P if c==z]

def augment(f,p,t=None):
    amt=min(z for i,d,z in p) if t is None else t;g=list(f)
    for i,d,z in p:g[i]+=d*amt
    return tuple(g),amt

def optimal_certificate(B,f,cost):
    # Super-source zero edges to every node: exact Bellman-Ford reduced-cost dual.
    R=residual(B,f,cost);dist={v:Q(0) for v in B['nodes']}
    for k in range(len(dist)):
        changed=False
        for u in R:
            for v,i,d,c,cap in R[u]:
                if dist[v]>dist[u]+c:dist[v]=dist[u]+c;changed=True
        if not changed:break
    demand(not changed,'negative residual cycle')
    for u in R:
        for v,i,d,c,cap in R[u]:demand(c+dist[u]-dist[v]>=0,'dual reduced cost')
    return dist

def cycles(B,f,cost):
    R=residual(B,f,cost);result=[];order={v:i for i,v in enumerate(B['nodes'])}
    for start in B['nodes']:
        def visit(u,seen,edges,c):
            for v,i,d,z,cap in R[u]:
                if v==start and edges:
                    sigma=[0]*len(B['E'])
                    for k,sgn in edges+[(i,d)]:sigma[k]+=sgn
                    result.append((c+z,sigma))
                elif v not in seen and order[v]>=order[start]:visit(v,seen|{v},edges+[(i,d)],c+z)
        visit(start,{start},[],Q(0))
    return result

def feasible(B,f,q):
    bal={v:Q(0) for v in B['nodes']}
    for z,(u,v,cap,c) in zip(f,B['E']):
        demand(0<=z<=cap,'capacity');bal[u]+=z;bal[v]-=z
    for v,z in bal.items():demand(z==(q if v=='s' else -q if v=='t' else 0),'conservation')
    L=len(B['nodes'])-1;demand(sum(f)<=L*q,'DAG bound')

def exact_run(B,check_cycles=False):
    f=(Q(0),)*len(B['E']);q=Q(0);history=[];halves=[];orig_ties=0;cyclecount=0
    while True:
        P=shortest(B,f,B['pert']); O=shortest(B,f,B['orig'])
        demand(len(P)<=1,'perturbed path not unique');orig_ties+=len(O)>1
        if not P:demand(not O,'different max flow state');break
        p=P[0];demand(p in O,'perturbed chooses original nonshortest')
        C=sum(B['pert'][i]*d for i,d,z in p);Cs=sum(B['shifted'][i]*d for i,d,z in p)
        demand(Cs-C==B['H']*(B['rank']['t']-B['rank']['s']),'path potential')
        half,_=augment(f,p,Q(1,2));feasible(B,half,q+Q(1,2));optimal_certificate(B,half,B['pert'])
        if check_cycles:
            for c,sigma in cycles(B,half,B['pert']):
                cyclecount+=1;demand(c!=0 or not any(sigma),'nontrivial zero cycle')
        if half[B['e']]==Q(1,2):
            L=len(B['nodes'])-1;K=Q(1,2*L);h=q+Q(1,2)+K/2
            demand(q+Q(1,2)<=B['F']-Q(3,2),'half range');demand(h<B['F'],'simplex h range')
            x=[1-h/B['F'],h/B['F']-sum(half)/(L*B['F'])]+[z/(L*B['F']) for z in half]
            demand(sum(x)==1 and all(z>=0 for z in x),'simplex embedding')
            demand(B['F']*(1-x[0])-K*(L*B['F']*x[2+B['e']])==q+Q(1,2),'simplex inverse q')
            halves.append(str(q+Q(1,2)))
        g,amt=augment(f,p);demand(amt==1,'not unit SSP'); q+=amt;feasible(B,g,q);optimal_certificate(B,g,B['pert']);history.append((f[B['e']],g[B['e']]));f=g
    demand(q==B['F'],'F max');demand(f[B['e']]==0,'final bridge');feasible(B,f,q)
    # Scale final zero-e max flow at additional rational values; only feasibility is claimed.
    for q0 in [Q(0),Q(1,7),Q(B['F'],3),Q(B['F'])]:
        feasible(B,[z*q0/B['F'] for z in f],q0)
    for i,(a,b) in enumerate(history):
        if a==0 and b==1:demand(i+1<len(history) and history[i+1]==(Q(1),Q(0)),'bridge not immediate reverse')
    yes=any(sum(w for k,w in enumerate(B['w']) if j>>k&1)*2==sum(B['w']) for j in range(2**B['n']))
    demand(bool(halves)==yes,'partition equivalence')
    demand(sum(B['rho'])<Q(1,8*B['D']),'rho sum')
    return {'weights':B['w'],'partition':yes,'iterations':len(history),'half_values':halves,'original_tie_states':orig_ties,'simple_cycles_checked':cyclecount,'D':B['D'],'cost_max_denominator_bits':max(z.denominator.bit_length() for z in B['shifted'])}

def all_original_executions(B):
    start=(Q(0),)*len(B['E']);front={(start,False):1};level=0;states=1;branches=0;terminal=set()
    while front:
        nxt={}
        for (f,used),count in front.items():
            P=shortest(B,f,B['orig']);branches+=max(0,len(P)-1)
            if not P:terminal.add(used);continue
            for p in P:
                g,amt=augment(f,p);demand(amt==1,'all-tie nonunit');nu=used or any(i==B['e'] and d==1 for i,d,z in p)
                if any(i==B['e'] and d==1 for i,d,z in p):
                    demand(f[B['e']]==0 and g[B['e']]==1,'forward range')
                    P2=shortest(B,g,B['orig']);demand(P2,'no reverse')
                    demand(all(any(i==B['e'] and d==-1 for i,d,z in p2) for p2 in P2),'tie does not reverse')
                nxt[(g,nu)]=nxt.get((g,nu),0)+count
        front=nxt;states+=len(front);level+=1;demand(level<=B['F']+1,'state growth')
    return {'weights':B['w'],'all_terminal_used_flags':sorted(terminal),'distinct_states':states,'tie_branches':branches}

def negative_controls():
    # Without delta, a yes instance admits an SSP sequence that never uses e.
    B=build([1,1],False);f=(Q(0),)*len(B['E']);used=False
    while True:
        P=shortest(B,f,B['orig'])
        if not P:break
        no=[p for p in P if all(i!=B['e'] for i,d,z in p)]
        demand(no,'delta=0 skip-bridge control failed');f,amt=augment(f,no[0])
    demand(f[B['e']]==0,'negative control bridge')
    # Zero cycle test must reject a true zero-cost cycle, but permit the formal 2-cycle.
    C={'nodes':['s','t'],'E':[('s','t',1,Q(0)),('s','t',1,Q(0))]};zcyc=cycles(C,(Q(1,2),Q(1,2)),[Q(0),Q(0)])
    demand(any(c==0 and any(sig) for c,sig in zcyc),'zero cycle control insensitive')
    demand(any(c==0 and not any(sig) for c,sig in zcyc),'formal zero cycle control insensitive')
    # Oversized perturbation can violate original shortest comparison.
    C={'nodes':['s','t'],'E':[('s','t',1,Q(0)),('s','t',1,Q(1))]};f=(Q(0),Q(0));P=shortest(C,f,[Q(2),Q(1)]);O=shortest(C,f,[Q(0),Q(1)])
    demand(P[0] not in O,'comparison control insensitive')
    return {'delta_zero_yes_sequence_skips_bridge':True,'nontrivial_zero_cycle_detected':True,'formal_zero_projection_cycle_detected':True,'oversized_perturbation_breaks_comparison':True}

def main():
    cases=[[1],[1,1],[1,2],[1,2,3],[1,2,4],[2,3,4,5],[1,1,1,1],[1,1,1],[3,5,7,11],[1,2,3,6],[2,4,8,16],[1,3,5,7]]
    cases+=list(map(list,product(range(1,4),repeat=3)))
    unique=[]
    for w in cases:
        if w not in unique:unique.append(w)
    checks=[exact_run(build(w),len(w)<=2) for w in unique]
    all_tie=[all_original_executions(build(w)) for w in [[1],[1,1],[1,2],[1,2,3],[1,2,4],[1,1,1,1]]]
    for z in all_tie:
        yes=any(sum(w for k,w in enumerate(z['weights']) if j>>k&1)*2==sum(z['weights']) for j in range(2**len(z['weights'])))
        demand(z['all_terminal_used_flags']==[yes],'all tie partition')
    report={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'mode':'python -O' if not __debug__ else 'python normal','exact_arithmetic':'fractions.Fraction; no floating-point optimization','checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'checks':checks,'all_original_tie_execution_checks':all_tie,'negative_controls':negative_controls(),'status':'PASS','limits':'Finite checks support quantified proof; not exhaustive n, not omitted historical executable, not a game/penalty/certificate check.'}
    dest=HERE/('CHECKS_OPTIMIZED.json' if not __debug__ else 'CHECKS_NORMAL.json');dest.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({'mode':report['mode'],'cases':len(checks),'total_augmentations':sum(x['iterations'] for x in checks),'tie_execution_cases':len(all_tie),'negative_controls':report['negative_controls'],'status':'PASS'},indent=2))
if __name__=='__main__':main()
