#!/usr/bin/env python3
"""Exact finite adversarial controls. No assert and no stochastic-limit certification."""
from fractions import Fraction as F
from itertools import product, combinations
from collections import Counter
from pathlib import Path
import argparse, json, hashlib

class VerificationFailure(Exception):
    pass

counts=Counter();instances=0;witnesses=0

def need(value,label,detail=None):
    if not value:
        raise VerificationFailure(json.dumps({'failed_claim':label,'witness':detail},sort_keys=True))
    counts[label]+=1

def validate(n,edges,slow,fast,seeds,root):
    need(n>0 and len(edges)==len(slow)==len(fast),'input_dimensions')
    need(all(0<=a<n and 0<=b<n for a,b in edges),'vertex_range')
    need(all(x>=0 for x in (*slow,*fast)),'nonnegative_lengths')
    need(root not in seeds and all(0<=x<n for x in (*seeds,root)),'disjoint_initial_sets')

def metric(n,edges,weights,root):
    # Bellman-Ford relaxation; None is genuine infinity. Nonnegative loops are harmless.
    ds=[None]*n;ds[root]=F(0)
    for unused in range(n-1):
        changed=False
        for (a,b),length in zip(edges,weights):
            for u,v in ((a,b),(b,a)):
                if ds[u] is not None and (ds[v] is None or ds[u]+length<ds[v]):
                    ds[v]=ds[u]+length;changed=True
        if not changed:break
    return ds

def outside(distance,T,closed=True):
    return distance is None or (distance>T if closed else distance>=T)

def evolve(n,edges,slow,fast,seeds,root,fast_wins_ties=True):
    # Recompute the boundary from infection times, independently of an event heap/list.
    validate(n,edges,slow,fast,seeds,root)
    color=[0]*n;at=[None]*n
    for s in seeds:color[s]=1;at[s]=F(0)
    color[root]=2;at[root]=F(0)
    while True:
        boundary=[]
        for i,(a,b) in enumerate(edges):
            for u,v in ((a,b),(b,a)):
                if color[u] and not color[v]:
                    c=color[u];weight=slow[i] if c==1 else fast[i]
                    priority=(0 if c==2 else 1) if fast_wins_ties else (0 if c==1 else 1)
                    boundary.append((at[u]+weight,priority,v,c,i,u))
        if not boundary:break
        t,priority,v,c,i,u=min(boundary)
        color[v]=c;at[v]=t
    return color,at

def all_paths(n,edges,start):
    adj=[[] for _ in range(n)]
    for i,(a,b) in enumerate(edges):
        adj[a].append((b,i));adj[b].append((a,i))
    pending=[((start,),())]
    while pending:
        vertices,inds=pending.pop();yield vertices,inds
        for v,i in adj[vertices[-1]]:
            if v not in vertices:pending.append((vertices+(v,),inds+(i,)))

def protected_suite(n,edges,slow,fast):
    global instances,witnesses
    for root in range(n):
        others=[x for x in range(n) if x!=root]
        ds=metric(n,edges,fast,root)
        for mask in range(1,1<<len(others)):
            seeds={v for i,v in enumerate(others) if mask>>i&1}
            for tie in (True,False):
                color,at=evolve(n,edges,slow,fast,seeds,root,tie);instances+=1
                for v in range(n):
                    if color[v]==2:
                        need(ds[v] is not None and ds[v]<=at[v],'actual_strong_ball_domination')
                for s in seeds:
                    for vertices,inds in all_paths(n,edges,s):
                        T=sum((slow[i] for i in inds),F(0))
                        if all(outside(ds[x],T) for x in vertices):
                            witnesses+=1;v=vertices[-1]
                            need(color[v]==1 and at[v]<=T,'protected_path_closed_ball',{'vertices':vertices,'T':str(T),'tie_fast_first':tie})

def counterexamples():
    # Endpoint/Voronoi comparison omits the blocked middle vertex a=1.
    edges=((0,1),(1,2),(3,1),(3,2))
    slow=(F(4),F(1),F(100),F(100));fast=(F(100),F(100),F(1),F(10))
    color,at=evolve(4,edges,slow,fast,{0},3)
    d1=metric(4,edges,slow,0);d2=metric(4,edges,fast,3)
    need(d1[2]==5 and d2[2]==10 and color[2]==2,'endpoint_and_voronoi_counterexample')
    endpoint={'n':4,'edges':edges,'weak_lengths':list(map(str,slow)),'strong_lengths':list(map(str,fast)),'weak_seeds':[0],'strong_root':3,'path':[0,1,2],'T':5,'weak_unopposed_distance_v':str(d1[2]),'strong_unopposed_distance_v':str(d2[2]),'actual_color_v':color[2],'actual_time_v':str(at[2])}
    # Closed ball boundary is necessary for arbitrary ties.
    edges2=((0,1),(2,1));slow2=(F(1),F(100));fast2=(F(100),F(1))
    c2,a2=evolve(3,edges2,slow2,fast2,{0},2,True);ds2=metric(3,edges2,fast2,2)
    need(ds2[1]==1 and c2[1]==2 and all(outside(ds2[v],F(1),False) for v in (0,1)),'open_ball_tie_counterexample')
    tie={'n':3,'edges':edges2,'weak_lengths':['1','100'],'strong_lengths':['100','1'],'weak_seeds':[0],'strong_root':2,'path':[0,1],'T':1,'actual_color_v':c2[1],'strong_wins_equal_time':True}
    # Separate parallel channels are necessary.
    pe=((0,1),(0,1),(2,1));ps=(F(10),F(1),F(100));pf=(F(100),F(100),F(3))
    cp,ap=evolve(3,pe,ps,pf,{0},2);cf,af=evolve(3,(pe[0],pe[2]),(ps[0],ps[2]),(pf[0],pf[2]),{0},2)
    need(cp[1]==1 and ap[1]==1 and cf[1]==2,'parallel_edge_collapse_counterexample')
    cl,al=evolve(3,((0,0),(1,1)),(F(0),F(0)),(F(0),F(0)),{0},1)
    need(cl==[1,2,0] and al[2] is None,'loops_do_not_infect_new_vertex')
    return {'endpoint_only':endpoint,'voronoi':endpoint,'open_ball':tie,'parallel_collapse':{'edges':pe,'true_color':cp[1],'collapsed_color':cf[1]}}

def resource_controls():
    # Repair at any chosen vertex; exact threshold crossing, count and second moment.
    for n in range(1,6):
        for degrees in product((2,3,5),repeat=n):
            for k in range(3,8):
                mass=sum(d for d in degrees if d>=k);number=sum(d>=k for d in degrees)
                inc=[]
                for i,d in enumerate(degrees):
                    repaired=list(degrees);repaired[i]+=1
                    delta=sum(x for x in repaired if x>=k)-mass;inc.append(delta)
                    need(0<=delta<=d+1,'repair_degree_mass_bound')
                    need(sum(x>=k for x in repaired)-number in (0,1),'repair_count_bound')
                    need(sum(x*x for x in repaired)-sum(x*x for x in degrees)==2*d+1,'repair_second_moment_identity')
                need(F(sum(inc),n)<=F(sum(degrees),n)+1,'uniform_repair_mass_expectation')
    need(sum(d for d in (4,2) if d>=4)-sum(d for d in (3,2) if d>=4)==4,'repair_not_just_one_half_edge')
    for j in range(2,21):
        for p in (F(1),F(1,2),F(1,7),F(1,100),F(2,5)):
            R=(j*j*p.denominator+p.numerator-1)//p.numerator
            need(R*p>=j*j,'ray_budget')
            need((1-p)**R<=F(1,1+R*p)<=F(1,j*j),'geometric_budget')
            for rate in (F(1,10),F(2,3),F(5)):
                T=F(j*j*R)/rate
                need(F(R)/(rate*T)==F(1,j*j),'time_budget_retains_rate')
        mean=4*j*j
        need(F(4,mean)<=F(1,j*j) and F(mean,2)>=j,'diverging_count_floor')
        need(F(3,j*j)/F(1,j)==F(3,j),'markov_fraction_transfer')
    # Sparse-spike finite-variance degree law P(D=2**m)=7/8**m, m>=1.
    need(F(7)*F(1,8)/(1-F(1,8))==1,'sparse_spike_mass')
    need(F(7)*F(1,4)/(1-F(1,4))==F(7,3),'sparse_spike_mean')
    need(F(7)*F(1,2)/(1-F(1,2))==7,'sparse_spike_second_moment')
    stages=[];last_B=0
    for j in range(2,11):
        q=F(1,8**(j-1));p=F(1,4**(j-1));R=j*j*4**(j-1);T=10*j*j*R
        resource=4*j*j*8**(j-1)
        B=max(2*j*T,resource.bit_length(),last_B+1);last_B=B
        # N=2**B symbolically. log2>=1/2 implies log N>=jT.
        need(R*p==j*j and B>=2*j*T,'thin_tail_symbolic_log_schedule')
        need(B>=resource.bit_length(),'thin_tail_symbolic_seed_floor')
        need(F(T,B)*2<=F(1,j),'thin_tail_o_log_bound')
        stages.append({'j':j,'threshold':2**j,'q':str(q),'p':str(p),'R':R,'T':T,'N_symbolic':'2**'+str(B),'local_all_n_bound_still_required':True})
    return stages

VARIANTS=('endpoint_only','open_ball','voronoi','parallel_collapse','parity_plus_one','budget_without_rate','seed_divergence_without_floor','uniform_identity_without_uniform_root','log_bound_replaced_by_size')

def reject_false_variant(variant,examples):
    if variant in ('endpoint_only','voronoi'):
        w=examples[variant];need(w['actual_color_v']==1,'false_'+variant,w)
    elif variant=='open_ball':
        w=examples[variant];need(w['actual_color_v']==1,'false_open_ball',w)
    elif variant=='parallel_collapse':
        w=examples[variant];need(w['true_color']==w['collapsed_color'],'false_parallel_collapse',w)
    elif variant=='parity_plus_one':
        need(4<=1,'false_parity_plus_one',{'original_degrees':[3,2],'repaired':[4,2],'k':4,'seed_mass_increment':4})
    elif variant=='budget_without_rate':
        j=3;R=9;rate=F(1,10);T=j*j*R
        need(F(R)/(rate*T)<=F(1,j*j),'false_budget_without_rate',{'j':j,'R':R,'rate':str(rate),'T':T,'Markov_bound':str(F(R)/(rate*T))})
    elif variant=='seed_divergence_without_floor':
        # E count=1/n tends to zero for q_n=1/n²; Markov P(count>=1)<=1/n.
        need(F(1,100)>=1,'false_seed_divergence_without_floor',{'n':100,'q_n':'1/10000','expected_count':'1/100','upper_bound_nonempty':'1/100'})
    elif variant=='uniform_identity_without_uniform_root':
        need(F(1,10)==0,'false_uniform_identity_without_uniform_root',{'weak_vertices':9,'all_vertices':10,'unweak_fraction':'1/10','root_always_weak':'0 missed probability'})
    elif variant=='log_bound_replaced_by_size':
        # n_j=2**j >= j² for j>=4, t_j=j², but t/log n=j/log2>j.
        j=10;need(j<=F(1,j),'false_log_bound_replaced_by_size',{'j':j,'n_j':2**j,'t_j':j*j,'ratio_lower_bound':j})
    else:raise VerificationFailure('Unknown semantic variant')

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--variant',choices=('true',*VARIANTS),default='true');args=parser.parse_args()
    examples=counterexamples()
    if args.variant!='true':reject_false_variant(args.variant,examples)
    # Exhaustive 3-vertex multigraph-free topology includes empty/disconnected graphs and zero/ties.
    base=list(combinations(range(3),2))
    for mask in range(8):
        edges=[e for i,e in enumerate(base) if mask>>i&1];m=len(edges)
        for ws in product((F(0),F(1),F(2)),repeat=2*m):protected_suite(3,edges,ws[:m],ws[m:])
    # Undirected multigraph edge cases, fractional lengths, all disjoint source choices, both tie conventions.
    for edges in [((0,1),(0,1),(1,2),(2,3),(3,0),(2,2)),((0,1),(1,1),(2,3)),((0,1),(1,2),(2,3))]:
        m=len(edges)
        for case in range(12):
            slow=tuple(F((case+2*i)%4,2) for i in range(m));fast=tuple(F((2*case+i*i)%5,3) for i in range(m))
            protected_suite(4,edges,slow,fast)
    stages=resource_controls()
    # Correlated vertex indicators still satisfy the exact uniform-root identity and Markov.
    for n in range(1,20):
        for unweak in range(n+1):
            need(sum((F(1,n) for v in range(n) if v<unweak),F(0))==F(unweak,n),'uniform_root_fraction_identity')
    rejected=[]
    for variant in VARIANTS:
        try:reject_false_variant(variant,examples)
        except VerificationFailure as e:rejected.append({'variant':variant,'explicit_exception':str(e)})
        else:raise VerificationFailure('Semantic false variant was not rejected: '+variant)
    need(len(rejected)==len(VARIANTS),'all_false_variants_rejected')
    print(json.dumps({'status':'PASS','scope':'Exact finite controls and arithmetic. Does not certify the stochastic local limit or novelty.','source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'finite_competition_instances':instances,'protected_path_witnesses':witnesses,'checks':sum(counts.values()),'categories':dict(counts),'semantic_false_variants':rejected,'thin_tail_stages':stages},indent=2,sort_keys=True))

if __name__=='__main__':main()
