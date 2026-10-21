#!/usr/bin/env python3
"""Review02 extension checks; finite falsification attempts, not theorem verification.

Uses pinned copied mechanism constructors; separately checks real fractional
flow feasibility/duals and direct original/auxiliary payoff inequalities.
"""
from pathlib import Path
from fractions import Fraction as Q
import importlib.util, json, datetime

HERE=Path(__file__).resolve().parent
def imported(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod);return mod
flow=imported('flow02',HERE/'replay/flow_source_01/flow_check.py')
game=imported('game02',HERE/'replay/game_certificate_01/check_exact.py')
def need(condition,msg):
    if not condition: raise RuntimeError(msg)
def dot(a,b):return sum((x*y for x,y in zip(a,b)),Q(0))
def is_pair(A,B,x,y):
    if min(x)<0 or min(y)<0 or sum(x)!=1 or sum(y)!=1:return False
    rp=[dot(row,y) for row in A]
    cp=[sum(x[i]*B[i][j] for i in range(len(x))) for j in range(len(y))]
    return max(rp)==dot(x,rp) and max(cp)==dot(y,cp)

def expanded_flow(weights):
    B=flow.build(weights);f=(Q(0),)*len(B['E']);q=Q(0);checks=0;halves=[]
    while True:
        paths=flow.shortest(B,f,B['pert'])
        if not paths:break
        need(len(paths)==1,'perturbed simple path not unique')
        p=paths[0];need(p in flow.shortest(B,f,B['orig']),'same-state cost coupling')
        for t in [Q(1,7),Q(2,3),Q(999,1000)]:
            g,amt=flow.augment(f,p,t);q1=q+t
            bal={v:Q(0) for v in B['nodes']}
            for z,(u,v,cap,c) in zip(g,B['E']):
                need(0<=z<=cap,'fractional capacity');bal[u]+=z;bal[v]-=z
            need(all(z==(q1 if v=='s' else -q1 if v=='t' else 0) for v,z in bal.items()),'fractional conservation')
            L=len(B['nodes'])-1;need(sum(g)<=L*q1,'DAG bound')
            potentials=flow.optimal_certificate(B,g,B['pert'])
            for u,rows in flow.residual(B,g,B['shifted']).items():
                for v,i,sign,c,cap in rows:
                    adjusted_u=potentials[u]+B['H']*B['rank'][u]
                    adjusted_v=potentials[v]+B['H']*B['rank'][v]
                    need(c+adjusted_u-adjusted_v>=0,'potential invariant residual dual')
            checks+=1
        g,amt=flow.augment(f,p);need(amt==1,'unit augmentation');q+=amt;f=g
    need(q==B['F'] and f[B['e']]==0,'maximum endpoint')
    return {'weights':weights,'new_nonhalf_fraction_dual_checks':checks,'bits_D':B['D'].bit_length()}

def expanded_game(weights):
    vertices,edges,e,F=game.network(weights);segments=game.ssp(vertices,edges,e,F);g=game.game(vertices,edges,e,F)
    m,N=len(g['a']),len(g['b']);x0=[Q(1)]+[Q(0)]*(m-1);y0=[Q(0)]*N;y0[g['diagnostic']]=1
    need(is_pair(g['A'],g['B'],x0,y0),'default direct pair')
    need(all(g['A'][i][g['diagnostic']]<g['A'][0][g['diagnostic']] for i in range(1,m)),'strict row default')
    need(all(g['B'][0][j]<g['B'][0][g['diagnostic']] for j in range(N) if j!=g['diagnostic']),'strict column default')
    new_aux=0;crossings=0
    for q,amt,old,new in segments:
        for frac in [Q(1,7),Q(1,2),Q(2,3)]:
            lam=q+amt*frac;f=[u+(v-u)*frac for u,v in zip(old,new)]
            if lam+g['K']*f[e]>F:continue
            x=game.simplex(g,f,lam);y=game.dual_opponent(g,vertices,edges,f,lam)
            aux=[[g['A'][i][j]-lam*g['b'][j] for j in range(N)] for i in range(m)]
            need(is_pair(aux,[[-z for z in row] for row in aux],x,y),'direct auxiliary pair')
            direct=is_pair(g['A'],g['B'],x,y);consistent=dot(g['a'],x)==lam
            if consistent:need(direct and f[e]==Q(1,2),'half crossing direct pair');crossings+=1
            new_aux+=1
    yes=any(sum(w for i,w in enumerate(weights) if mask>>i&1)*2==sum(weights) for mask in range(1<<len(weights)))
    need(bool(crossings)==yes,'positive witness equivalence')
    # Independently check complete payoff shift identities at off-optimum mixed points.
    x=[Q(i+1,m*(m+1)//2) for i in range(m)];y=[Q(N-j,N*(N+1)//2) for j in range(N)];lam=dot(g['a'],x)
    aux=[[g['A'][i][j]-lam*g['b'][j] for j in range(N)] for i in range(m)]
    shift=lam*dot(g['b'],y)
    need(all(dot(g['A'][i],y)-dot(aux[i],y)==shift for i in range(m)),'complete row shift')
    need(all(sum(x[i]*g['B'][i][j] for i in range(m))==-sum(x[i]*aux[i][j] for i in range(m)) for j in range(N)),'complete column correspondence')
    need(is_pair(g['A'],g['B'],x,y)==is_pair(aux,[[-z for z in row] for row in aux],x,y),'off-optimum both-direction best-response equivalence')
    return {'weights':weights,'new_direct_auxiliary_pair_checks':new_aux,'crossing_pairs':crossings,'off_optimum_full_payoff_identity_checks':m+N,'default_strict':True}

def adversarial_controls():
    # Equal-length binary perturbations can cancel if not ordered geometrically;
    # the ternary leading-term condition is quantitatively indispensable.
    need(sum([Q(1,3),-Q(1,9),-Q(1,27),-Q(1,81)])>0,'finite ternary tail')
    need(Q(1,2)-Q(1,4)-Q(1,4)==0,'unordered perturbation zero-cycle control')
    # Strict M>C matters for all minimizers, not only objective value.
    lam=Q(1);infeasible=Q(3,4);feasible=Q(1,2)
    need(-infeasible+max(Q(0),infeasible-lam/2)==-feasible,'boundary-penalty false minimizer')
    need(-infeasible+2*max(Q(0),infeasible-lam/2)>-feasible,'strict penalty rejects false minimizer')
    # Positive-dimensional exact rank-one product cells: two rational vertices
    # certify multiplicity independently of initially irrational observations.
    need(is_pair([[Q(0),Q(0)]],[[Q(1),Q(1)]],[Q(1)],[Q(1),Q(0)]),'1x2 endpoint1')
    need(is_pair([[Q(0),Q(0)]],[[Q(1),Q(1)]],[Q(1)],[Q(0),Q(1)]),'1x2 endpoint2')
    need(not is_pair([[Q(0),Q(0)]],[[Q(1),Q(1)]],[Q(1)],[Q(1),Q(1)]),'nonunit certificate')
    # No-perturbation equal-cost parallel paths give a real-demand continuum.
    E={'nodes':['s','t'],'E':[('s','t',1,Q(0)),('s','t',1,Q(0))]}
    cs=flow.cycles(E,(Q(1,3),Q(2,3)),[Q(0),Q(0)])
    need(any(c==0 and any(v) for c,v in cs),'unisolated real demand continuum control')
    return {'nongeometric_tail_cancellation':True,'M_equals_dual_bound_infeasible_tie':True,'strict_M_eliminates_tie':True,'one_by_two_continuum_endpoints':True,'nonunit_certificate_rejected':True,'without_perturbation_nontrivial_real_demand_zero_cycle':True}

def main():
    result={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'expanded_flow':[expanded_flow(w) for w in [[1],[10**15+3],[10**15+3,10**15+3],[10**15+3,10**15+4],[1,1,2,2],[3,3,6],[2,4,8,16,32]]],'expanded_games':[expanded_game(w) for w in [[3,3],[3,4],[3,3,6],[2,2,2]]],'new_all_original_choice_attempts':[flow.all_original_executions(flow.build(w)) for w in [[2,2],[2,4],[3,3,6],[1,1,2,2]]],'controls':adversarial_controls(),'limits':'Finite extension tests, not exhaustive equilibrium enumeration or proof of every n/irrational parameter. Constructs with pinned family code but checks new fractional cases and direct payoff identities independently. No omitted historical script replay.'}
    (HERE/'MATH_ADVERSARIAL_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
