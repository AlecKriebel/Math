#!/usr/bin/env python3
"""New adversarial exact source-state check. No candidate code imports."""
import sys
sys.dont_write_bytecode = True
from fractions import Fraction as Q
from itertools import product
from math import lcm
from pathlib import Path
import json, hashlib, datetime

def require(ok, message):
    if not ok:
        raise RuntimeError(message)

def make(weights, base=True):
    n=len(weights);S=sum(weights);delta=Q(1,120*S)
    arcs=[]
    for sg in (1,-1):
        arcs.append(((sg,'s',0),(sg,'t',0),1,delta if base else Q(0)))
        for level,w in enumerate(weights,1):
            c=sg*Q(w,48*S);cap=2**(level-1);dear=Q(2**level-1,2)-c
            arcs += [((sg,'s',level),(sg,'s',level-1),cap,c),
                     ((sg,'t',level-1),(sg,'t',level),cap,c),
                     ((sg,'s',level),(sg,'t',level-1),cap,dear),
                     ((sg,'s',level-1),(sg,'t',level),cap,dear)]
        arcs += [('S',(sg,'s',n),2**n,Q(0)),((sg,'t',n),'T',2**n,Q(0))]
    arcs.append(((1,'s',0),(-1,'t',0),1,Q(0)))
    return arcs,delta

def every_path(arcs,flow,cost):
    adj={}
    for i,(u,v,cap,_) in enumerate(arcs):
        if flow[i]<cap:adj.setdefault(u,[]).append((v,i,1,cap-flow[i],cost[i]))
        if flow[i]>0:adj.setdefault(v,[]).append((u,i,-1,flow[i],-cost[i]))
    found=[]
    def dfs(u,seen,path,value):
        if u=='T':
            found.append((value,tuple(path)));return
        for v,i,d,cap,c in adj.get(u,[]):
            if v not in seen:dfs(v,seen|{v},path+[(i,d,cap)],value+c)
    dfs('S',{'S'},[],Q(0))
    return found

def move(flow,path,fraction=None):
    amount=min(cap for _,_,cap in path) if fraction is None else fraction
    updated=list(flow)
    for i,d,_ in path:updated[i]+=d*amount
    return tuple(updated),amount

def dual_check(arcs,flow,cost):
    vertices={v for arc in arcs for v in arc[:2]};dist={v:Q(0) for v in vertices}
    residual=[]
    for i,(u,v,cap,_) in enumerate(arcs):
        if flow[i]<cap:residual.append((u,v,cost[i]))
        if flow[i]>0:residual.append((v,u,-cost[i]))
    for _ in range(len(vertices)):
        changed=False
        for u,v,c in residual:
            if dist[v]>dist[u]+c:dist[v]=dist[u]+c;changed=True
        if not changed:break
    require(not changed,'negative residual cycle in fractional optimum')
    require(all(c+dist[u]-dist[v]>=0 for u,v,c in residual),'invalid dual potential')

def test(weights):
    arcs,delta=make(weights);p=len(arcs);n=len(weights);S=sum(weights);F=2**(n+1);e=p-1
    require(p==8*n+7,'arc count');cost=[a[3] for a in arcs]
    D=lcm(*(v.denominator for v in cost));pert=[v+Q(1,4*D*3**(i+1)) for i,v in enumerate(cost)]
    start=(Q(0),)*p;front={start};seen=0;branches=0;midpoints=[];states=[]
    for step in range(F):
        nxt=set()
        for flow in front:
            paths=every_path(arcs,flow,cost);best=min(v for v,_ in paths);chosen=[path for v,path in paths if v==best]
            seen+=1;branches+=len(chosen)-1
            if step%2==0:
                j=step//2;z=sum(((-1)**((j>>(i-1))&1))*Q(w,24*S) for i,w in enumerate(weights,1))
                plus=[];minus=[];bridge=[]
                for value,path in paths:
                    if any(i==e and d==1 for i,d,_ in path):bridge.append(value)
                    elif all(arcs[i][0]=='S' or arcs[i][1]=='T' or arcs[i][0][0]==1 for i,_,_ in path):plus.append(value)
                    else:minus.append(value)
                parity=(-1)**j
                require(min(plus)==j+z+parity*delta,'plus table mismatch')
                require(min(minus)==j-z+parity*delta,'minus table mismatch')
                require(min(bridge)==j-(0 if j%2==0 else 2*delta),'bridge table mismatch')
                require(flow[e]==0,'bridge nonzero at synchronized state')
                require(all(any(i==e and d==1 for i,d,_ in path)==(z==0) for path in chosen),'wrong synchronized source event')
                states.append({'j':j,'z':str(z),'minimum':str(best),'shortest_paths':len(chosen)})
            for path in chosen:
                update,amount=move(flow,path);require(amount==1,'nonunit original execution');nxt.add(update)
                uses=any(i==e and d==1 for i,d,_ in path)
                if uses:
                    require(flow[e]==0 and update[e]==1,'incorrect forward bridge change')
                    after=every_path(arcs,update,cost);v=min(x for x,_ in after);companions=[p for x,p in after if x==v]
                    require(all(any(i==e and d==-1 for i,d,_ in p) for p in companions),'permitted shortest companion does not reverse bridge')
                    expected=step//2+(2*delta if (step//2)%2==0 else 0)
                    require(v==expected,'reverse companion table mismatch')
                    midpoints.append(str(Q(step)+Q(1,2)))
        front=nxt
    require(all(not every_path(arcs,f,cost) and f[e]==0 for f in front),'terminal residual failure')
    yes=any(sum((-1)**((mask>>i)&1)*w for i,w in enumerate(weights))==0 for mask in range(2**n))
    require(bool(midpoints)==yes,'PARTITION event failure')
    # A separate perturbed run checks identical-state coupling and quarter fractions.
    f=start;fractions_checked=0
    for step in range(F):
        pp=every_path(arcs,f,pert);minimum=min(v for v,_ in pp);paths=[p for v,p in pp if v==minimum]
        require(len(paths)==1,'perturbation leaves path tie');path=paths[0]
        op=every_path(arcs,f,cost);minimum_original=min(v for v,_ in op)
        require(sum(cost[i]*d for i,d,_ in path)==minimum_original,'wrong original residual comparison')
        for amount in (Q(1,7),Q(1,2),Q(6,7)):
            middle,_=move(f,path,amount);dual_check(arcs,middle,pert);fractions_checked+=1
            if middle[e]==Q(1,2):require(Q(step)+amount<=F-Q(3,2) or any(i==e and d==-1 for i,d,_ in path),'forward midpoint range')
        f,amount=move(f,path);require(amount==1,'nonunit perturbed step')
    return {'weights':weights,'partition_yes':yes,'all_original_states':seen,'tie_branches':branches,'forward_midpoints':sorted(set(midpoints)),'fractional_dual_checks':fractions_checked,'tables':states}

def main():
    cases=[list(t) for n in (1,2,3) for t in product(range(1,5),repeat=n)]
    cases += [[1,1,1,1],[2,3,5,9],[1,2,4,8],[1,2,3,4,8]]
    results=[test(w) for w in cases]
    # Adversarial control: base delta=0 permits avoiding the diagnostic bridge on yes [1,1].
    arcs,_=make([1,1],False);flow=(Q(0),)*len(arcs);e=len(arcs)-1
    for _ in range(8):
        paths=every_path(arcs,flow,[a[3] for a in arcs]);minimum=min(v for v,_ in paths)
        avoiding=[p for v,p in paths if v==minimum and all(i!=e for i,_,_ in p)]
        require(avoiding,'negative control cannot avoid bridge');flow,_=move(flow,avoiding[0])
    result={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'status':'PASS','cases':len(results),'original_states':sum(r['all_original_states'] for r in results),'fractional_dual_checks':sum(r['fractional_dual_checks'] for r in results),'negative_control_delta_zero_yes_can_skip_bridge':True,'limits':'Finite exact all-choice and fractional dual checks; proof and primary source carry all-instance and all-real quantifiers. No candidate checker is imported.','results':results}
    Path(__file__).with_name('INDEPENDENT_SOURCE_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='results'},indent=2))

if __name__=='__main__':main()
