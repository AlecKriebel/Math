#!/usr/bin/env python3
"""Exact finite terminal-strip and guard regressions, not an asymptotic proof."""
from pathlib import Path
from itertools import permutations,combinations
from collections import Counter
import hashlib,json,sys
P=Path(__file__).resolve().parent

def require(ok,data):
    if not ok:raise RuntimeError(data)
def av1324(p):return not any(p[i]<p[k]<p[j]<p[l] for i,j,k,l in combinations(range(len(p)),4))
def av213(p):return not any(p[j]<p[i]<p[k] for i,j,k in combinations(range(len(p)),3))
def av132(p):return not any(p[i]<p[k]<p[j] for i,j,k in combinations(range(len(p)),3))
def std(p):
    rank={v:i+1 for i,v in enumerate(sorted(p))}
    return tuple(rank[v] for v in p)
def inv(p):
    q=[0]*len(p)
    for i,v in enumerate(p,1):q[v-1]=i
    return tuple(q)
def rc(p):return tuple(len(p)+1-v for v in p[::-1])
def S(p):return rc(inv(p))
def top(p):
    for a in range(1,len(p)+1):
        if not av213(tuple(v for v in p if v>len(p)-a)):return a-1
    return len(p)
def greedy(p):
    out=[]
    while p:
        if len(out)%2==0:
            a=top(p);chosen=std(tuple(v for v in p if v>len(p)-a))
            p=std(tuple(v for v in p if v<=len(p)-a))
        else:
            a=len(p)
            for b in range(1,len(p)+1):
                if not av132(p[:b]):a=b-1;break
            chosen=S(std(p[:a]));p=std(p[a:])
        out.append(chosen)
    return out

def guard(q,a):
    n=len(q);b=n-a
    return (n+2,b+1,n+3)+tuple(v+(v>b) for v in q)
def padded_inverse(A):
    a=len(A)
    return (a+1,a+2)+inv(A)

rows=[];max_fiber=0;example=None
for n in range(1,8):
    images=Counter();count=even=odd=0
    for pi in permutations(range(1,n+1)):
        if not av1324(pi):continue
        count+=1;states=greedy(pi);A=states[-1];a=len(A);parity=len(states)%2
        even+=parity==0;odd+=parity==1
        q=inv(pi) if parity else rc(pi)
        require(av1324(q),('symmetry class',pi))
        require(std(tuple(v for v in q if v>n-a))==inv(A),('terminal state transformation',pi,states,q))
        require(top(q)>=a,('terminal size',pi,states,q))
        out=guard(q,a)
        require(av1324(out),('guard avoidance',pi,states,out))
        first=greedy(out)[0]
        require(first==padded_inverse(A),('exact first state',pi,A,out,first))
        q_back=std(out[3:]);back=inv(q_back) if parity else rc(q_back)
        require(back==pi,('tagged inverse',pi,out,parity,back))
        images[out]+=1
        if images[out]>max_fiber:max_fiber=images[out];example={'n':n,'output':out,'fiber':max_fiber}
    require(all(v<=2 for v in images.values()),('fiber bound',n,max(images.values())))
    rows.append({'n':n,'avoidance_count':count,'even_terminal_indices':even,'odd_terminal_indices':odd,'distinct_guard_images':len(images),'max_image_fiber':max(images.values())})

files=['TERMINAL_MARK_AND_POINTWISE_LIFT.md',Path(__file__).name]
result={'status':'passed','scope':'Finite exact regression only; no radius or uniform-limit inference','max_input_n':7,'max_output_n':10,'rows':rows,'maximum_fiber':max_fiber,'fiber_example':example,
        'pins':{name:{'sha256':hashlib.sha256((P/name).read_bytes()).hexdigest(),'bytes':(P/name).stat().st_size} for name in files}}
out=P/(sys.argv[1] if len(sys.argv)>1 else 'CHECK_NORMAL.json')
out.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
