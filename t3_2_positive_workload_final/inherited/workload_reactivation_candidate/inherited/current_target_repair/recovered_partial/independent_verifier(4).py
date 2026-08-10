#!/usr/bin/env python3
"""Dependency-free independent replay of certified partial T3-2 repair claims."""
from __future__ import annotations
import hashlib,itertools,json,math,subprocess,sys
from fractions import Fraction
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

def falling(n,k):
    if n<k:return 0
    z=1
    for j in range(k):z*=n-j
    return z

def prop(x,y):
    z=1
    for a,b in zip(x,y):z*=falling(a,b)
    return z

def probs(x):
    # two-linkage regression channel order A->2A,2A->A,0->AB,AB->B,B->0
    sources=((1,0),(2,0),(0,0),(1,1),(0,1))
    a=[prop(x,s) for s in sources];d=sum(a)
    return [Fraction(v,d) for v in a]

def V(x,t):return sum(math.lgamma(x[i]-t[i]+1) for i in range(2))

def fire(x,s,u):return tuple(x[i]-s[i]+u[i] for i in range(2))

def actual_episode(x,t,path):
    sources=((1,0),(2,0),(0,0),(1,1),(0,1));targets=((2,0),(1,0),(1,1),(0,1),(0,0))
    memo={}
    def rec(x,t,k):
        key=(x,t,k)
        if key in memo:return memo[key]
        p=probs(x);base=V(x,t);z=0.0
        for i,(s,u) in enumerate(zip(sources,targets)):
            if not prop(x,s):continue
            y=fire(x,s,u);inc=V(y,u)-base
            if k<len(path) and i==path[k]:z+=float(p[i])*(inc+rec(y,u,k+1))
            elif k==len(path):z+=float(p[i])*inc
            else:z+=float(p[i])*inc
        memo[key]=z;return z
    return rec(x,t,0)

def activation_pair(n):
    # current target 2A, condition on 0->AB, append AB->B->0 episode.
    x=(n,0);activation=math.log(prop(x,(2,0)))
    return activation+actual_episode((n+1,1),(1,1),(3,4))

def honest(n):return actual_episode((n,0),(2,0),(1,))

def graph_audit():
    # Exhaust strong directed graphs through three nodes and workloads 0..2.
    total=0
    for n in (2,3):
        nodes=range(n);E=[e for e in itertools.permutations(nodes,2)]
        for mask in range(1<<len(E)):
            edges=[E[i] for i in range(len(E)) if mask>>i&1]
            def reach(reverse=False):
                adj={i:[] for i in nodes}
                for a,b in edges:
                    if reverse:a,b=b,a
                    adj[a].append(b)
                seen={0};st=[0]
                while st:
                    v=st.pop()
                    for w in adj[v]:
                        if w not in seen:seen.add(w);st.append(w)
                return len(seen)==n
            if not reach() or not reach(True):continue
            for lv in itertools.product(range(3),repeat=n):
                changing=[(a,b) for a,b in edges if lv[a]!=lv[b]]
                if changing:
                    alpha=max(lv[a] for a,b in changing)
                    top=[(a,b) for a,b in changing if lv[a]==alpha]
                    assert all(lv[b]<lv[a] for a,b in top)
                total+=1
    return total

def one_active_audit():
    C=[x for x in itertools.product(range(3),repeat=3) if sum(x)<=2]
    no2=0;with2=0
    for s in C:
        for t in C:
            if s==t:continue
            d=s[0];k=t[0]-s[0]
            if d==2:
                assert s==(2,0,0) and k<0
            with2+=1
            if s!=(2,0,0) and t!=(2,0,0):
                if d==1:assert k<=0
                if d==0:assert k<=1
                no2+=1
    return with2,no2

def main():
    pair=[]
    for n in (100,1000,10000,100000):
        a=activation_pair(n);h=honest(n)
        assert a>0 and h<0
        pair.append((n,a,h,a/math.log(n)))
    graph=graph_audit();with2,no2=one_active_audit()
    cp=subprocess.run([sys.executable,str(ROOT/'inherited_cleanroom_atlas'/'cleanroom_atlas_check.py')],text=True,capture_output=True,check=True)
    report={
        'status':'partial_pass_T3_2_not_certified',
        'activation_pair_regression':[[n,format(a,'.15g'),format(h,'.15g'),format(r,'.15g')] for n,a,h,r in pair],
        'first_changing_graph_cases':graph,
        'one_active_channels_with_2A_audited':with2,
        'one_active_channels_without_2A_audited':no2,
        'cleanroom_atlas_stdout_sha256':hashlib.sha256(cp.stdout.encode()).hexdigest(),
        'certified':[
            'actual-current-target residual identity interface',
            'conditional and activation-pair counterexamples',
            'first-changing-source finite graph sign',
            'one-active elementary polynomial/source signs',
            'three-way finite atlas replay',
        ],
        'not_certified':[
            'rate-weighted current-target trace theorem',
            'T3-2 positive recurrence',
        ],
    }
    text=json.dumps(report,sort_keys=True,separators=(',',':'))+'\n'
    (ROOT/'certificates'/'independent_verification.json').write_text(text)
    print(text,end='')
if __name__=='__main__':main()
