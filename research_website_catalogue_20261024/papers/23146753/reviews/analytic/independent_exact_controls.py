"""Own rational diagnostics for the manuscript-first analytic derivation.

No release programme or third-party source is imported. Finite controls are
not the all-graph proof, which is in EARLY_RECONSTRUCTION.md and REPORT.md.
"""
from fractions import Fraction as Q
from itertools import product
from collections import Counter
from math import lcm
import json

def require(c,why):
    if not c: raise RuntimeError(why)

def cube(n):return tuple(product((0,1),repeat=n))
def power2(k):return Q(2**k) if k>=0 else Q(1,2**(-k))
def is_mtp(w):
    return all(w[tuple(min(a,b) for a,b in zip(x,y))]*
               w[tuple(max(a,b) for a,b in zip(x,y))]>=w[x]*w[y]
               for x in w for y in w)

def flow_control(h,interactions):
    """Sparse rational residual graph; DFS augmentation, independent cut scan."""
    n=len(h);src=n;snk=n+1;nodes=range(n+2)
    c={(u,v):Q(0) for u in nodes for v in nodes}
    b=[-Q(a) for a in h]
    old_edges=set()
    for u,v,J in interactions:
        J=Q(J);require(J>=0,'negative coupling supplied')
        c[u,v]+=J;b[u]-=J;old_edges.add(frozenset((u,v)))
    for i,bi in enumerate(b):
        if bi>=0:c[i,snk]+=bi
        else:c[src,i]-=bi
    r=dict(c);value=Q(0);augmentations=0
    while True:
        seen={src};stack=[(src,[])];path=None
        while stack:
            u,prefix=stack.pop()
            if u==snk:path=prefix;break
            for v in reversed(tuple(nodes)):
                if v not in seen and r[u,v]>0:
                    seen.add(v);stack.append((v,prefix+[(u,v)]))
        if path is None:break
        delta=min(r[e] for e in path);require(delta>0,'nonpositive augmentation')
        for u,v in path:r[u,v]-=delta;r[v,u]+=delta
        value+=delta;augmentations+=1
        require(augmentations<10000,'unexpected finite diagnostic complexity')
    energies={x:-sum(Q(a)*xi for a,xi in zip(h,x))-
              sum(Q(J)*x[u]*x[v] for u,v,J in interactions) for x in cube(n)}
    emin=min(energies.values());kappa=sum(-bi for bi in b if bi<0)
    residuals={}
    for x,E in energies.items():
        U={src}|{i for i,xi in enumerate(x) if xi}
        C=sum(c[u,v] for u in U for v in nodes if v not in U)
        R=sum(r[u,v] for u in U for v in nodes if v not in U)
        require(C==E+kappa,'cut/energy constant')
        require(R==C-value==E-emin,'exact all-cut residual identity')
        residuals[x]=R
    require(value==emin+kappa,'max flow/minimum cut value')
    require(all(q>=0 for q in r.values()),'negative residual')
    require(all(not r[u,v] or u>=n or v>=n or frozenset((u,v)) in old_edges
                for u in nodes for v in nodes),'new nonterminal adjacency')
    scale=lcm(*(z.denominator for z in residuals.values()))
    W={x:power2(-int(z*scale)) for x,z in residuals.items()}
    require(max(W.values())==1 and 1<=sum(W.values())<=2**n,'lost normalizer')
    require(is_mtp(W),'attractive law MTP failure')
    return {'vertices':n,'edges':len(interactions),'rational_flow_value':str(value),
            'augmentations':augmentations,'all_configuration_cut_identities':len(energies),
            'exact_power_of_two_weight_normalizer':str(sum(W.values())),
            'residual_nonterminal_edges_stay_original':True,'minimum_scaled_energy_weight':1}

def conditional_independent(w,A,B,C):
    # p(a,b,c)p(c)=p(a,c)p(b,c), including null conditioning events.
    for a,b,c in product(cube(len(A)),cube(len(B)),cube(len(C))):
        select=lambda x,I,y:tuple(x[i] for i in I)==y
        joint=sum(v for x,v in w.items() if select(x,A,a) and select(x,B,b) and select(x,C,c))
        pc=sum(v for x,v in w.items() if select(x,C,c))
        pac=sum(v for x,v in w.items() if select(x,A,a) and select(x,C,c))
        pbc=sum(v for x,v in w.items() if select(x,B,b) and select(x,C,c))
        if joint*pc!=pac*pbc:return False
    return True

def main():
    runs=[flow_control([],[]),flow_control([Q(-2)],[]),
          flow_control([Q(1,2),Q(-2,3),Q(4,5)],[(2,0,Q(3,7)),(0,1,Q(5,4))]),
          flow_control([Q(-3,2),Q(2,3),0,Q(5,4),Q(-3,5)],
                       [(1,0,Q(5,3)),(1,2,Q(2,5)),(3,2,Q(7,4)),(4,0,Q(2,7)),(4,3,Q(1,2))]),
          flow_control([2,-3,1,0,-1,4],[(0,1,3),(2,1,2),(3,2,0),(4,3,5)]),
          flow_control([Q((i*i)%7-3,3) for i in range(7)],
                       [(0,1,Q(2,3)),(2,1,Q(7,5)),(2,3,Q(1,2)),(4,3,Q(5,7)),(4,5,Q(9,4)),(6,5,Q(2,9)),(6,0,Q(3,2))])]
    X=cube(4);law={x:Q((2 if all(x) else 1) if x[2]==x[3] else 0,9) for x in X}
    require(sum(law.values())==1 and is_mtp(law),'published counterexample law')
    require(conditional_independent(law,(0,),(2,),(1,3)) and
            conditional_independent(law,(1,),(3,),(0,2)),'zero-event Markov control')
    bits=lambda texts:[tuple(map(int,x)) for x in texts.split()]
    left=bits('0000 0111 1011 1100');right=bits('0011 0100 1000 1111')
    for edge in [(0,1),(1,2),(2,3),(0,3)]:
        require(Counter(tuple(x[i] for i in edge) for x in left)==
                Counter(tuple(x[i] for i in edge) for x in right),'division-free edge-cell balance')
    lp=Q(1);rp=Q(1)
    for x in left:lp*=law[x]
    for x in right:rp*=law[x]
    require(lp==Q(1,9**4) and rp==Q(2,9**4),'nonfactorization products')
    # Tied equalities aggregate the two supplied cross interactions -2 and +3.
    target={x:(power2(-2*x[0]*x[2]+3*x[1]*x[3]) if x[0]==x[1] and x[2]==x[3] else Q(0)) for x in X}
    z=sum(target.values());target={x:w/z for x,w in target.items()}
    require(is_mtp(target),'aggregate positive law')
    errors=[]
    for k in [0,1,2,4,8,16]:
        W={x:power2(x[0]*x[2]-k*(int(x[0]!=x[1])+int(x[2]!=x[3]))) for x in X};Z=sum(W.values())
        pk={x:w/Z for x,w in W.items()}
        require(is_mtp(pk),'penalty attractive approximation')
        error=sum(abs(pk[x]-target[x]) for x in X)
        require(error<=Q(6)*power2(-k),'universal finite-sum error estimate instantiated')
        errors.append({'penalty_base2':k,'L1_exact':str(error)})
    require(all(Q(a['L1_exact'])>Q(b['L1_exact']) for a,b in zip(errors,errors[1:])),'density convergence control')
    # Pointwise factor flooring can lose MTP2 despite the original law being MTP2.
    eps=Q(1,10);bad={x:(Q(1) if not x[0] else eps)*(eps if x==(1,1) else 1) for x in cube(2)}
    require(not is_mtp(bad) and bad[0,0]*bad[1,1]-bad[0,1]*bad[1,0]==Q(-9,100),'invalid smoothing control')
    print(json.dumps({'method':'Own stdlib exact Fraction arithmetic, no archived source import/execution',
      'residual_controls':runs,'residual_configuration_checks':sum(r['all_configuration_cut_identities'] for r in runs),
      'C4':{'all256_MTP_pairs':True,'both_minimal_separator_conditional_independences':True,
            'balanced_edge_cells_all4_edges':True,'quartic_products':[str(lp),str(rp)],'not_finite_edge_factorizable':True},
      'aggregate_control':{'negative_supplied_cross_coefficient':-2,'positive_supplied_cross_coefficient':3,
                           'quotient_aggregate':1,'target_MTP':True,'density_errors':errors},
      'failure_control_naive_zero_factor_flooring':{'epsilon':'1/10','MTP_determinant':'-9/100','rejected':True},
      'normalizer_failure_control':'Without a gauge one can multiply factors by epsilon and keep the normalized uniform law while every limiting raw factor is zero. Residual gauge imposes max W=1 and prevents this loss.',
      'limits':'The tested graphs/parameters are finite corroborating/falsifying controls. The all-finite-graph proof is the support-poset and max-flow compactness derivation, not this census.'},indent=2))

if __name__=='__main__':main()
