#!/usr/bin/env python3
"""Independent weighted-cycle, Boolean closure, period-deletion falsification.

No candidate or previous checker imported. This uses all fixed-total states and
Boolean matrix closure, rather than assuming the halting dichotomy or following
a selected trajectory. Cycle fluxes solve integer-image equations directly.
"""
import sys
sys.dont_write_bytecode=True
import argparse, itertools as it, json, math
from collections import Counter

def need(q,msg):
    if not q:raise ValueError(msg)
def comps(c,n):
    if n==1:yield(c,);return
    for k in range(c+1):
        for z in comps(c-k,n-1):yield(k,)+z
def endpoint(r,x,f):
    return tuple(x[v]-r[v]*f[v]+r[v-1]*f[v-1] for v in range(len(r)))
def fire(r,x,v):
    need(x[v]>=r[v],'illegal firing')
    f=tuple(int(w==v) for w in range(len(r)))
    return endpoint(r,x,f)
def closure(r,c):
    states=list(comps(c,len(r)));index={x:i for i,x in enumerate(states)}
    a=[]
    for x in states:
        row=0
        for v in range(len(r)):
            if x[v]>=r[v]:row|=1<<index[fire(r,x,v)]
        a.append(row)
    # Nonempty paths only: diagonal presence detects cycles/recurrent states.
    for k in range(len(states)):
        for j in range(len(states)):
            if a[j]>>k&1:a[j]|=a[k]
    return states,index,a
def reduced(r,x,y,p):
    # Flux q_v=r_v*f_v obeys q_v=q_(v-1)-delta_v.
    # Enumerate one common flux modulo lcm; exact finite test only.
    l=math.lcm(*r)
    for flux in range(l):
        q=[flux]
        for v in range(1,len(r)):q.append(q[-1]-(y[v]-x[v]))
        if any(q[v]%r[v] for v in range(len(r))):continue
        h=tuple(q[v]//r[v] for v in range(len(r)))
        if endpoint(r,x,h)!=y:continue
        k=min(h[v]//p[v] for v in range(len(r)))
        return tuple(h[v]-k*p[v] for v in range(len(r)))
    return None
def obstruct(r,x,g,u):
    z=endpoint(r,x,u)
    return u!=g and all(0<=u[v]<=g[v] for v in range(len(r))) and all(z[v]<r[v] for v in range(len(r)) if u[v]<g[v])
def run():
    cov=Counter();badlast=None;transpose=None;nonlegal=None
    families=list(it.product((1,2,3),repeat=3))+[(1,2,3,5),(3,1,2,1)]
    for r in families:
        n=len(r);l=math.lcm(*r);p=tuple(l//v for v in r)
        need(endpoint(r,(0,)*n,p)==(0,)*n,'cycle period flux')
        # Transpose convention gives a constant vector for weighted cycle and fails Lp=0.
        if len(set(r))>1 and transpose is None:
            q=(1,)*n;need(endpoint(r,(0,)*n,q)!=(0,)*n,'transposed-period mutation detected')
            transpose={'rates':r,'wrong_period':q,'L_times_wrong_period':endpoint(r,(0,)*n,q)}
        for c in range(5):
            states,index,a=closure(r,c);cov['complete_state_spaces']+=1;cov['all_states']+=len(states)
            for x in states:
                i=index[x];reachable=a[i]|(1<<i)
                cyclic=any((reachable>>j&1) and (a[j]>>j&1) for j in range(len(states)))
                stable=any((reachable>>j&1) and all(z<d for z,d in zip(y,r)) for j,y in enumerate(states))
                need(cyclic!=stable,'independent complete closure dichotomy')
                N=(c+1)**n
                frontier={x}
                # Stop on a repeated entire frontier, accelerating exact length N Boolean paths.
                seen={};t=0
                while t<N and frontier:
                    key=frozenset(frontier)
                    if key in seen:
                        period=t-seen[key];jump=(N-t)//period
                        if jump:t+=jump*period;continue
                    else:seen[key]=t
                    frontier={fire(r,z,v) for z in frontier for v in range(n) if z[v]>=r[v]};t+=1
                need(bool(frontier)==cyclic,'cutoff exact-length Boolean frontier')
                cov['cutoff_controls']+=1
                for j,y in enumerate(states):
                    g=reduced(r,x,y,p);yes=bool(reachable>>j&1);cov['reachability_pairs']+=1
                    if g is None:need(not yes,'integer nonimage reachable');cov['nonimage']+=1;continue
                    witnesses=[]
                    for u in it.product(*(range(v+1) for v in g)):
                        cov['bounded_vectors']+=1
                        if obstruct(r,x,g,u):witnesses.append(u)
                    need(bool(witnesses)==(not yes),'first-excess certificate closure comparison')
                    if witnesses:cov['negative_pairs']+=1
                    if nonlegal is None:
                        for u in witnesses:
                            z=endpoint(r,x,u)
                            if z not in index or not (reachable>>index[z]&1):nonlegal={'rates':r,'x':x,'y':y,'g':g,'u':u,'state':z};break
                # New mutation mechanism: deleting LAST rather than FIRST period occurrences.
                words=[(x,())]
                for _ in range(10):
                    nxt=[]
                    for z,w in words:
                        if all(w.count(v)>=p[v] for v in range(n)):
                            left=list(p);ret=[]
                            for v in reversed(w):
                                if left[v]:left[v]-=1
                                else:ret.append(v)
                            ret=tuple(reversed(ret));s=x;legal=True
                            for v in ret:
                                if s[v]<r[v]:legal=False;break
                                s=fire(r,s,v)
                            if not legal and badlast is None:badlast={'rates':r,'x':x,'word':w,'period':p,'last_deleted_word':ret}
                            # Correct first deletion must always remain legal.
                            left=list(p);s=x
                            for v in w:
                                if left[v]:left[v]-=1
                                else:s=fire(r,s,v)
                            need(s==z,'correct first-deletion endpoint')
                            cov['first_deletion_controls']+=1
                        if len(nxt)<1000:
                            for v in range(n):
                                if z[v]>=r[v]:nxt.append((fire(r,z,v),w+(v,)))
                    words=nxt
    # No counterexample found to uniform last deletion in this finite cycle family.
    # A deliberately mixed deletion rule does fail: first occurrence at vertex0,
    # last occurrence at vertex1, although removed counts equal a period.
    mixed={'rates':(1,1),'x':(1,0),'legal_word':(0,1,0,1,0),'removed_positions':(0,3),'retained_word':(1,0,0)}
    s=(1,0)
    for v in mixed['legal_word']:s=fire((1,1),s,v)
    need(mixed['x'][1]<1,'mixed-deletion first retained move must be illegal')
    need(endpoint((1,1),(1,0),(2,1))==s,'removed vector is exact full period')
    need(transpose is not None,'transpose mutation escaped')
    need(nonlegal is not None,'nonlegal u witness missing')
    # Local exact prefix inequality independently checks every boundary state,
    # including combinations that need not arise from an actual legal history.
    for N in range(1,31):
        M=N+1
        for d in range(1,12):
            for z,tv in it.product(range(d+2),range(N)):
                h=M*z+N-tv
                need((h>=M*d+1)==(z>=d),'local prefix threshold equivalence')
                cov['all_local_threshold_boundaries']+=1
    return {'status':'PASS','coverage':dict(cov),'distinct_faults_detected':{'mixed_period_occurrence_deletion':mixed,'uniform_last_deletion_counterexample_found_in_test_family':badlast,'transposed_period_convention':transpose},'nonrealizable_negative_certificate':nonlegal,'scope':'Finite exact controls; no general proof or historical program replay','imports_candidate_or_prior_checker':False}
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--inject-failure',action='store_true');a=p.parse_args()
    need(not a.inject_failure,'new unconditional failure control')
    print(json.dumps(run(),sort_keys=True,indent=2))
