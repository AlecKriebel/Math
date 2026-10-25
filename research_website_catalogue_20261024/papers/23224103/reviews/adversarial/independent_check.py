#!/usr/bin/env python3
"""Independent pre-support attack: exact global-clock finite cycle and controls.

No submitted source or checker was read before this file and its output were
sealed. Finite-cycle tests are diagnostics, never a Brownian convergence proof.
"""
from fractions import Fraction as Q
from itertools import product, permutations
from functools import lru_cache
from pathlib import Path
import json, math

checks=[]
def check(ok,label):
    if not ok: raise RuntimeError(label)
    checks.append(label)

def solve(A,b):
    """Gauss-Jordan over Q; no floating point or numerical tolerances."""
    n=len(b);M=[list(map(Q,row))+[Q(v)] for row,v in zip(A,b)]
    for j in range(n):
        k=next(k for k in range(j,n) if M[k][j])
        M[j],M[k]=M[k],M[j]
        scale=M[j][j];M[j]=[v/scale for v in M[j]]
        for i in range(n):
            if i!=j and M[i][j]:
                f=M[i][j];M[i]=[v-f*w for v,w in zip(M[i],M[j])]
    return [row[-1] for row in M]

def owner_probability(n,seeds,queries,labels):
    """Global Poisson clocks: each +/- walker jump has rate 1/2.

    States remember current positions and which query ownerships remain unset.
    A wrong first arrival is killed, a correct one removes the target. Embedded
    jump probabilities are 1/(2k). This preserves physical chronological order.
    """
    k=len(seeds);m=len(queries)
    @lru_cache(None)
    def stage(mask):
        targets={queries[j]:j for j in range(m) if mask>>j&1}
        allowed=[x for x in range(n) if x not in targets]
        states=list(product(allowed,repeat=k));idx={p:i for i,p in enumerate(states)}
        A=[[Q(int(i==j)) for j in range(len(states))] for i in range(len(states))]
        b=[Q(0) for _ in states]
        for pos in states:
            row=idx[pos]
            for who in range(k):
                for step in [-1,1]:
                    nxt=list(pos);nxt[who]=(nxt[who]+step)%n;nxt=tuple(nxt)
                    weight=Q(1,2*k)
                    if nxt[who] in targets:
                        j=targets[nxt[who]]
                        if labels[j]==who:
                            newmask=mask^(1<<j)
                            b[row]+=weight*(stage(newmask)[nxt] if newmask else 1)
                    else:
                        A[row][idx[nxt]]-=weight
        return dict(zip(states,solve(A,b)))
    return stage((1<<m)-1)[tuple(seeds)] if m else Q(1)

def order_probability(n,seed,queries,order):
    z=seed;remaining=set(queries);out=Q(1)
    for j in order:
        target=queries[j]
        distances=[((q-z)%n,q) for q in remaining]
        right,qright=min(distances)
        left,qleft=min(((z-q)%n,q) for q in remaining)
        ell=left+right
        p=(Q(right,ell) if target==qleft else 0)+(Q(left,ell) if target==qright else 0)
        out*=p;z=target;remaining.remove(target)
    return out

def discounted_interval(n,alpha,s):
    h=Q(1,n)
    A=[[Q(0) for j in range(n-1)] for i in range(n-1)]
    b=[Q(0) for i in range(n-1)]
    for i in range(n-1):
        A[i][i]=1+s*h*h
        if i:A[i][i-1]=-Q(1,2)
        else:b[i]+=Q(1,2)
        if i+1<n-1:A[i][i+1]=-Q(1,2)
    return solve(A,b)[int(alpha*n)-1]

def main():
    output={}
    # Interlaced target orders expose increment/physical-time confusion directly.
    orders=[(0,1),(1,0)];increments=[[Q(2),Q(2)],[Q(3),Q(1,2)]]
    physical=[[sum(increments[i][:orders[i].index(j)+1]) for j in range(2)] for i in range(2)]
    true=[min(range(2),key=lambda i:physical[i][j]) for j in range(2)]
    wrong=[min(range(2),key=lambda i:increments[i][orders[i].index(j)]) for j in range(2)]
    check(true==[0,1] and wrong==[1,0],'noncumulative_clock_control_reverses_both_owners')
    output['clock_control']={'orders':orders,'increments':[[str(v) for v in a] for a in increments],
                             'physical':[[str(v) for v in a] for a in physical],
                             'correct_owners':true,'increment_only_wrong_owners':wrong}
    # Independent finite-chain query laws, normalized through exact global clocks.
    laws=[]
    for n,seeds,queries in [(4,(0,2),(1,3)),(5,(0,2),(1,3,4)),(6,(0,3),(1,2,4))]:
        law={a:owner_probability(n,seeds,queries,a) for a in product(range(2),repeat=len(queries))}
        check(sum(law.values())==1,f'global_clock_law_normalized_n{n}')
        check(all(0<=v<=1 for v in law.values()),f'global_clock_law_nonnegative_n{n}')
        for j,x in enumerate(queries):
            marginal=sum(v for a,v in law.items() if a[j]==0)
            direct=owner_probability(n,seeds,(x,),(0,))
            check(marginal==direct,f'query_marginal_matches_direct_n{n}_j{j}')
        laws.append({'n':n,'seeds':seeds,'queries':queries,'law':{','.join(map(str,a)):str(v) for a,v in law.items()}})
    output['global_clock_query_laws']=laws
    # Repeated removal and normalization for all single-walker circular orders.
    order_cases=[]
    for n,queries in [(5,(1,2,3,4)),(7,(1,3,4,6))]:
        probs=[order_probability(n,0,queries,o) for o in permutations(range(len(queries)))]
        check(sum(probs)==1,f'ordered_exit_total_mass_n{n}')
        check(any(v==0 for v in probs),f'impossible_orders_have_zero_mass_n{n}')
        order_cases.append({'n':n,'total_orders':len(probs),'nonzero_orders':sum(v>0 for v in probs),'total_mass':str(sum(probs))})
    check(order_probability(5,0,(2,),(0,))==1,'singleton_identified_endpoints_sum_to_one')
    output['single_walker_orders']=order_cases
    # Complete finite-cell moments vs an independent discrete query expansion.
    n=5;seeds=(0,2);queries=(1,3,4)
    law={a:owner_probability(n,seeds,queries,a) for a in product(range(2),repeat=len(queries))}
    owner_vectors={a:(0,a[0],1,a[1],a[2]) for a in law}
    theta=[Q(1,3),Q(7,4)];moments=[]
    for m in range(7):
        moment=sum(prob*(sum(theta[i] for i in owner_vectors[a])/n)**m for a,prob in law.items())
        # Discrete Fubini sum includes duplicate queries and seeds, handled literally.
        query_expansion=sum(sum(prob*math.prod(theta[owner_vectors[a][x]] for x in xs) for a,prob in law.items()) for xs in product(range(n),repeat=m))/n**m
        check(moment==query_expansion,f'compact_volume_moment_matches_joint_queries_m{m}')
        check(0<=moment<=max(theta)**m,f'moment_bound_m{m}')
        equal=sum(prob*Q(5,3)**m for prob in law.values())
        check(equal==Q(5,3)**m,f'equal_laplace_variables_m{m}')
        moments.append(str(moment))
    transform=sum(float(prob)*math.exp(-float(sum(theta[i] for i in owner_vectors[a])/n)) for a,prob in law.items())
    for N in range(7):
        partial=sum((-1)**m*float(Q(moments[m]))/math.factorial(m) for m in range(N+1))
        bound=float(max(theta)**(N+1)/math.factorial(N+1))
        check(abs(transform-partial)<=bound+1e-14,f'outer_factorial_bound_finite_model_N{N}')
    output['finite_cell_moments']={'theta':[str(v) for v in theta],'moments':moments,'transform_float':transform}
    # Generator factor check by discounted gambler's ruin, a separate interface.
    values=[];errors=[]
    alpha=Q(1,4);s=Q(3,2)
    exact_brownian=math.sinh(float((1-alpha))*math.sqrt(2*float(s)))/math.sinh(math.sqrt(2*float(s)))
    wrong_generator=math.sinh(float((1-alpha))*math.sqrt(float(s)))/math.sinh(math.sqrt(float(s)))
    for nn in [4,8,16,32]:
        v=discounted_interval(nn,alpha,s);error=abs(float(v)-exact_brownian);errors.append(error)
        values.append({'n':nn,'exact_discrete':str(v),'error_to_generator_half':error})
    check(all(errors[j+1]<errors[j] for j in range(3)),'discounted_chain_converges_toward_half_generator_formula')
    check(errors[-1]<abs(float(Q(values[-1]['exact_discrete']))-wrong_generator)/100,'wrong_generator_factor_rejected')
    output['discounted_exit']={'alpha':str(alpha),'s':str(s),'brownian_half_generator':exact_brownian,'wrong_full_generator':wrong_generator,'discrete_values':values}
    # An anti-control for extending the nonnegative-theta bound to arbitrary signs.
    z=-2.0
    check(abs(math.exp(-z)-1)>abs(z),'nonnegative_theta_remainder_not_valid_for_negative_theta')
    output['status']='PASS independent controls; finite chains are not a Brownian limit proof'
    output['assertions_passed']=len(checks);output['checks']=checks
    path=Path(__file__).with_name('independent-check-results.json');path.write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps({k:v for k,v in output.items() if k!='checks'},indent=2))
if __name__=='__main__':main()
