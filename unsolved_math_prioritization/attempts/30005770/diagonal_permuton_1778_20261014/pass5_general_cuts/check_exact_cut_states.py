#!/usr/bin/env python3
"""Finite regression of exact cut states, exposure histories and completion fibers.
The finite observed graph is not claimed to enumerate the complete all-size state set.
"""
from collections import Counter,defaultdict
from functools import lru_cache
from itertools import permutations,combinations
from pathlib import Path
import hashlib,json,sys,time

HERE=Path(__file__).resolve().parent
PROOF_SHA='01040a02521559ea6015e1928db860c7d6921f288b23cb356b8948ac0afa4fbc'

def require(ok,msg):
    if not ok:raise RuntimeError(msg)

def rank(seq):
    d={x:i+1 for i,x in enumerate(sorted(seq))}
    return tuple(d[x] for x in seq)

@lru_cache(None)
def perms(n):return tuple(permutations(range(1,n+1)))

@lru_cache(None)
def contains(p,q):
    comparisons=tuple((i,j,q[i]<q[j]) for i in range(len(q)) for j in range(i+1,len(q)))
    return any(all((p[ids[i]]<p[ids[j]])==v for i,j,v in comparisons)
               for ids in combinations(range(len(p)),len(q)))


def state_of(p,r,m):
    B=tuple((i,v) for i,v in enumerate(p,1) if i<=r<v)
    D=tuple(sorted(((i,v) for i,v in enumerate(p,1) if v<=r<i),key=lambda x:x[1]))
    F=tuple((i,v) for i,v in enumerate(p,1) if i<=r and v<=r)
    require(len(B)==len(D),('unequal boundary',p,r))
    b=rank(tuple(v for i,v in B));d=rank(tuple(i for i,v in D))
    profile={((),(),())}
    for h in range(1,min(m,len(F))+1):
        for selected in combinations(F,h):
            profile.add((rank(tuple(v for i,v in selected)),
                         tuple(sum(x<i for x,y in B) for i,v in selected),
                         tuple(sum(y<v for x,y in D) for i,v in selected)))
    state=(b,d,tuple(sorted(profile)))
    known=tuple(v for i,v in enumerate(p,1) if i<=r or v<=r)
    return state,(B,D,F),rank(known)


def exposure_choice(p,r):
    # New diagonal index is r+1; r is the previous cut.
    t=r+1;v=p[r];j=p.index(t)+1
    if v==t:return ('diagonal',)
    close_lower=v<=r;close_upper=j<=r
    Bvalues=[x for i,x in enumerate(p,1) if i<=r<x]
    Dpositions=[i for i,x in enumerate(p,1) if x<=r<i]
    if close_lower and close_upper:return ('both_close',)
    if close_upper:
        remain=[x for x in Bvalues if x!=t]
        return ('replace_upper',1+sum(x<v for x in remain))
    if close_lower:
        remain=[i for i in Dpositions if i!=t]
        return ('replace_lower',1+sum(i<j for i in remain))
    return ('both_open',1+sum(x<v for x in Bvalues),1+sum(i<j for i in Dpositions))


def decode(history):
    B=[];D=[];p=[0]*len(history)
    for t,ch in enumerate(history,1):
        kind=ch[0]
        if kind=='diagonal':p[t-1]=t
        elif kind=='both_open':B.insert(ch[1]-1,t);D.insert(ch[2]-1,t)
        elif kind=='both_close':p[B.pop(0)-1]=t;p[t-1]=D.pop(0)
        elif kind=='replace_upper':p[B.pop(0)-1]=t;B.insert(ch[1]-1,t)
        elif kind=='replace_lower':p[t-1]=D.pop(0);D.insert(ch[1]-1,t)
        else:raise RuntimeError(kind)
    require(not B and not D,'unclosed exposure history')
    return tuple(p)


def audit_pattern(alpha,N=7):
    m=len(alpha);tau=tuple(x+1 for x in alpha)+(1,)
    transitions={};valid_edges=defaultdict(dict)
    actual=defaultdict(Counter);fixed_fibers=defaultdict(lambda:defaultdict(set))
    paths_checked=0;valid_prefix_edges=0
    for n in range(N+1):
        for p in perms(n):
            history=tuple(exposure_choice(p,r) for r in range(n))
            require(decode(history)==p,('history inverse',alpha,p))
            paths_checked+=1
            records=[state_of(p,r,m) for r in range(n+1)]
            W=max(len(s[0]) for s,_,_ in records)
            good=not contains(p,tau)
            if good:actual[n][W]+=1
            for r,((s,(B,D,F),known),ch) in enumerate(zip(records,history)):
                if contains(known,tau):continue
                valid_prefix_edges+=1
                sp,_,knownp=records[r+1]
                valid=not contains(knownp,tau)
                key=(s,ch);value=(sp,valid)
                require(key not in transitions or transitions[key]==value,
                        ('profile transition is not sufficient',alpha,n,p,r,ch))
                transitions[key]=value
                if valid:valid_edges[s][ch]=sp
            # Fixed-coordinate profile equivalence, including zero-completion interiors.
            if n<=6:
                for r,(s,(B,D,F),known) in enumerate(records):
                    if contains(known,tau):continue
                    key=(n,r,B,D,s[2])
                    language=fixed_fibers[key][F]
                    if good:
                        NE=tuple(v for i,v in enumerate(p,1) if i>r and v>r)
                        language.add(rank(NE))
    fibers_compared=0;nontrivial_profiles=0
    for key,interiors in fixed_fibers.items():
        languages=list(interiors.values())
        require(all(x==languages[0] for x in languages),('completion profile languages differ',alpha,key))
        if len(interiors)>1:
            nontrivial_profiles+=1;fibers_compared+=len(interiors)
    empty=((),(),(((),(),()),))
    transfer_rows=[]
    for K in range(N//2+1):
        dp={empty:1}
        row=[]
        for n in range(N+1):
            got=sum(v for s,v in dp.items() if not s[0])
            expected=sum(v for w,v in actual[n].items() if w<=K)
            require(got==expected,('finite transfer count',alpha,K,n,got,expected))
            row.append(got)
            nxt=Counter()
            for s,v in dp.items():
                for ch,sp in valid_edges.get(s,{}).items():
                    if len(sp[0])<=K:nxt[sp]+=v
            dp=nxt
        transfer_rows.append({'K':K,'coefficients_through_N':row})
    return {'alpha':list(alpha),'tau':list(tau),'N':N,'raw_histories_checked':paths_checked,
            'valid_prefix_edge_observations':valid_prefix_edges,
            'distinct_state_choice_pairs':len(transitions),
            'distinct_profile_fiber_groups':len(fixed_fibers),
            'multiple_interior_profile_groups':nontrivial_profiles,
            'interiors_in_multiple_groups':fibers_compared,
            'bounded_width_transfer_rows':transfer_rows,
            'full_class_counts':[sum(actual[n].values()) for n in range(N+1)]}


def completion_obstruction():
    alpha=(2,1,4,3);tau=(3,2,5,4,1);rows=[]
    for N in range(8):
        n=N+4;plus=minus=expected=0
        for sigma in perms(N):
            p=(n,2,3)+tuple(x+3 for x in sigma)+(1,)
            q=(n,3,2)+tuple(x+3 for x in sigma)+(1,)
            a=not contains(p,tau);b=not contains(q,tau)
            require(a==(not contains(sigma,alpha)),('positive completion language',N,sigma))
            require(b==(sigma==tuple(range(1,N+1))),('negative completion language',N,sigma))
            sp,coords1,_=state_of(p,3,4);sm,coords2,_=state_of(q,3,4)
            require(coords1[:2]==coords2[:2] and sp[:2]==sm[:2],('boundary mismatch',N,sigma))
            require(sp[2]!=sm[2],('profile failed to distinguish',N))
            plus+=a;minus+=b;expected+=not contains(sigma,alpha)
        require(plus==expected and minus==1,('fiber count',N))
        if N:require(plus>=2**(N-1),('exponential lower bound',N))
        rows.append({'N':N,'positive_fiber':plus,'restricted_fiber':minus})
    return rows


def extra_blocks_and_packing():
    blocks=0;packings=0;histories=0
    for m in (2,3,4):
        for alpha in perms(m):
            tau=tuple(x+1 for x in alpha)+(1,)
            for K in range(5):
                k=K+1
                gamma=tuple(range(2*k,0,-1)) if alpha==tuple(range(1,m+1)) else tuple(range(k+1,2*k+1))+tuple(range(1,k+1))
                require(not contains(gamma,tau),('extra block forbidden pattern',alpha,K))
                require(all(set(gamma[:i])!=set(range(1,i+1)) for i in range(1,len(gamma))),('extra block decomposable',alpha,K))
                W=max(sum(x>r for x in gamma[:r]) for r in range(len(gamma)+1))
                require(W==K+1,('extra block width',alpha,K,W));blocks+=1
            for k in (1,2):
                if alpha==tuple(range(1,m+1)):
                    p=tuple(range(1,(m-1)*k+1))+tuple(range(m*k,(m-1)*k,-1))
                else:
                    prefix=tuple(j*m+x for j in range(k) for x in alpha)
                    Q=tuple((x-1)*k+r for x in alpha for r in range(1,k+1))
                    p=prefix+tuple(x+m*k for x in Q)
                require(not contains(p,tau),('perfect packing example forbidden',alpha,k))
                history=tuple(exposure_choice(p,r) for r in range(len(p)))
                require(decode(history)==p,('perfect-packing history inverse',alpha,k))
                for r in range(len(p)+1):
                    state,_,known=state_of(p,r,m)
                    require(not contains(known,tau),('perfect-packing partial forbidden',alpha,k,r))
                    if state[0]:require(not contains(state[0],alpha),('upper crossing not alpha-free',alpha,k,r))
                packings+=1;histories+=len(p)
    return {'extra_sum_indecomposable_blocks':blocks,'perfect_packing_examples':packings,
            'perfect_packing_exposure_steps':histories}


def main():
    start=time.time()
    require(hashlib.sha256((HERE/'EXACT_CUT_STATES_AND_CONTEXT_OBSTRUCTION.md').read_bytes()).hexdigest()==PROOF_SHA,'Frozen proof changed')
    configs=[(1,2),(2,1)]+list(perms(3))+[(2,1,4,3)]
    audits=[]
    for alpha in configs:
        row=audit_pattern(alpha,7);audits.append(row)
        print('Exact cut-state checks passed for alpha='+''.join(map(str,alpha)),flush=True)
    fibers=completion_obstruction();stress=extra_blocks_and_packing()
    out={'status':'PASS','scope':'Finite state/projection/completion regressions; not a full all-size state enumeration or asymptotic proof.',
         'proof_sha256':PROOF_SHA,'python':sys.version,'optimization_level':sys.flags.optimize,
         'pattern_audits':audits,'width_one_completion_fibers':fibers,'stress_checks':stress,
         'elapsed_seconds':round(time.time()-start,3)}
    path=HERE/f'CHECK_OPTIMIZATION_{sys.flags.optimize}.json'
    path.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'status':'PASS','output':str(path),'elapsed_seconds':out['elapsed_seconds']}))

if __name__=='__main__':main()
