#!/usr/bin/env python3
"""Fresh exact finite-state and nonreachability-certificate checks; no inherited code.
All pass/fail guards remain active under Python -O. Finite checks are not a proof.
"""
from collections import deque
from itertools import product
from math import gcd
from pathlib import Path
import json, sys


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def degree(A):
    return tuple(map(sum, A))


def step(A, x, v):
    d=degree(A)
    require(x[v]>=d[v], 'illegal requested firing')
    return tuple(x[j]+A[v][j]-(d[v] if j==v else 0) for j in range(len(A)))


def count_state(A, x, f):
    d=degree(A)
    return tuple(x[j]+sum(A[v][j]*f[v] for v in range(len(A)))-d[j]*f[j] for j in range(len(A)))


def strong(A):
    n=len(A)
    for s in range(n):
        seen={s};q=[s]
        for u in q:
            for v in range(n):
                if A[u][v] and v not in seen:seen.add(v);q.append(v)
        if len(seen)!=n:return False
    return True


def explore(A, x, cap=200000):
    """Exhaust the whole reachable state graph, then test for directed cycles."""
    x=tuple(x);d=degree(A);seen={x};q=deque([x]);edges={};parent={x:None}
    low=tuple(min(0,c) for c in x)
    while q:
        z=q.popleft();out=[]
        for v in range(len(A)):
            if z[v]>=d[v]:
                w=step(A,z,v);require(sum(w)==sum(x),'mass conservation')
                require(all(w[j]>=low[j] for j in range(len(A))),'signed lower bound')
                out.append(w)
                if w not in seen:
                    require(len(seen)<cap,'state cap reached; no result accepted')
                    seen.add(w);q.append(w);parent[w]=(z,v)
        edges[z]=out
    indeg={z:0 for z in seen}
    for out in edges.values():
        for w in out:indeg[w]+=1
    q=deque(z for z in seen if not indeg[z]);acyclic=0
    while q:
        z=q.popleft();acyclic+=1
        for w in edges[z]:
            indeg[w]-=1
            if not indeg[w]:q.append(w)
    cycle=acyclic<len(seen);stable=any(not out for out in edges.values())
    require(cycle!=stable,'abelian dichotomy violated in finite control')
    return seen,cycle,edges,parent


def reduction(A,x,M_override=None,deficit_offset=0,marker_initial=0):
    n=len(A);N=(sum(x)+1)**n;M=N+1 if M_override is None else M_override
    B=N*(M*max(degree(A))+1);H=[[0]*(n+2) for _ in range(n+2)]
    for u in range(n):
        for v in range(n):H[u][v]=M*A[u][v]
        H[u][n]=1;H[n][u]=B
    H[n][n+1]=H[n+1][n]=1
    X=tuple([M*c+N for c in x]+[n*B+1-N+deficit_offset,marker_initial])
    f=tuple([N]*n+[1,0]);Y=count_state(H,X,f)
    return tuple(map(tuple,H)),X,Y,N,M,B,f


def prefix_check(A,x):
    H,X,Y,N,M,B,f=reduction(A,x);n=len(A);d=degree(A);dh=degree(H)
    require(strong(H) and all(H[v][v]==0 for v in range(n+2)), 'output graph class')
    require(min(X)>=0 and min(Y)>=0 and sum(X)==sum(Y) and X!=Y,'configuration output class')
    require(Y==tuple([M*x[v]+M*N*(sum(A[u][v] for u in range(n))-d[v])+B for v in range(n)]+[(n-1)*N,1]),'explicit target formula')
    counts={tuple([0]*n)};q=deque(counts);transitions=0;endpoints=[]
    while q:
        t=q.popleft();k=sum(t);z=count_state(A,x,t);h=count_state(H,X,t+(0,0))
        require(h[-1]==0 and h[-2]==n*B+1-N+k,'gate/marker prefix invariant')
        require(all(h[v]==M*z[v]+N-t[v] for v in range(n)),'scaling invariant')
        if k==N:endpoints.append(t);continue
        require(h[-2]<dh[-2],'gate unlocked early')
        for v in range(n):
            require((z[v]>=d[v])==(h[v]>=dh[v]),'source/target legality mismatch')
            if z[v]>=d[v]:
                nt=list(t);nt[v]+=1;nt=tuple(nt);transitions+=1
                if nt not in counts:counts.add(nt);q.append(nt)
    source_states,nonhalting,_,_=explore(A,x)
    require(bool(endpoints)==nonhalting,'finite cutoff mismatch with exhaustive source cycle test')
    cleanup=0
    if endpoints:
        t=endpoints[len(endpoints)//2];h=count_state(H,X,t+(0,0));h=step(H,h,n)
        require(min(h[:n])>=B,'post-gate budget')
        start=t;pending={start};q=deque([start]);last=None
        while q:
            u=q.popleft();z=count_state(H,X,u+(1,0))
            if u==tuple([N]*n):last=z;continue
            for v in range(n):
                if u[v]<N:
                    require(z[v]>=dh[v],'illegal cleanup order')
                    nu=list(u);nu[v]+=1;nu=tuple(nu);cleanup+=1
                    if nu not in pending:pending.add(nu);q.append(nu)
        require(last==Y,'cleanup misses target')
    return {'n':n,'C':sum(x),'N':N,'prefix_count_states':len(counts),'prefix_transitions':transitions,'cleanup_transitions':cleanup,'source_states':len(source_states),'nonhalting':nonhalting}


def relay(A,x):
    n=len(A);loops=[v for v in range(n) if A[v][v]];m=n+len(loops);H=[[0]*m for _ in range(m)]
    for u in range(n):
        for v in range(n):
            if u!=v:H[u][v]=A[u][v]
    for k,v in enumerate(loops):H[v][n+k]=H[n+k][v]=A[v][v]
    return tuple(map(tuple,H)),tuple(x)+tuple([0]*len(loops))


def normalize(A,x):
    H=[list(r) for r in A];k=tuple(max(0,-c) for c in x)
    for v in range(len(A)):H[v][v]+=k[v]
    return tuple(map(tuple,H)),tuple(x[v]+k[v] for v in range(len(A))),k


def egcd(a,b):
    if not b:return (a,1,0)
    g,u,v=egcd(b,a%b);return g,v,u-(a//b)*v


def reduced_two(A,x,y):
    a=A[0][1];b=A[1][0];d=gcd(a,b);delta=y[0]-x[0]
    if sum(x)!=sum(y) or delta%d:return None
    _,u,v=egcd(a,b);f0=-u*(delta//d);f1=v*(delta//d);p=(b//d,a//d)
    k=min(f0//p[0],f1//p[1]);f=(f0-k*p[0],f1-k*p[1])
    require(min(f)>=0 and not all(f[j]>=p[j] for j in range(2)),'reduced solution')
    require(count_state(A,x,f)==y and count_state(A,(0,0),p)==(0,0),'integer linear algebra')
    return f,p


def cert(A,x,f,u,proper=True,strict=True):
    if min(u)<0 or any(u[j]>f[j] for j in range(len(A))) or (proper and u==f):return False
    z=count_state(A,x,u);d=degree(A)
    return all(u[v]==f[v] or (z[v]<d[v] if strict else z[v]<=d[v]) for v in range(len(A)))


def main():
    rows=[]
    for a,b in product(range(1,4),repeat=2):
        A=((0,a),(b,0))
        for x in product(range(3),repeat=2):rows.append(prefix_check(A,x))
    graphs3=[]
    for bits in product(range(2),repeat=6):
        A=[[0]*3 for _ in range(3)];k=0
        for u in range(3):
            for v in range(3):
                if u!=v:A[u][v]=bits[k];k+=1
        A=tuple(map(tuple,A))
        if strong(A):graphs3.append(A)
    require(len(graphs3)==18,'three-vertex graph enumeration')
    for A in graphs3:
        for x in [(0,0,0),(1,0,0),(0,1,0),(0,0,1)]:rows.append(prefix_check(A,x))
    target=[]
    for a,b in product(range(1,3),repeat=2):
        A=((0,a),(b,0))
        for x in [(0,0),(1,0),(0,1)]:
            H,X,Y,N,M,B,f=reduction(A,x);s,cyc,e,p=explore(H,X)
            _,nonhalt,_,_=explore(A,x)
            require((Y in s)==nonhalt,'unrestricted target reachability counterexample')
            count=None
            if Y in s:
                count=[0]*4;z=Y
                while p[z] is not None:z,v=p[z];count[v]+=1
            target.append({'A':A,'x':x,'source_nonhalting':nonhalt,'target_states_exhausted':len(s),'target_reachable':Y in s,'found_count':count,'designated_count':f})
    # A real target-returning period supplies alternative target-reaching counts.
    A=((0,1),(1,0));x=(1,0);H,X,Y,N,M,B,f=reduction(A,x);period=(B,B,1,1)
    require(count_state(H,(0,0,0,0),period)==(0,0,0,0), 'output period')
    u=[0]*4;z=Y;word=[]
    while tuple(u)!=period:
        options=[v for v in range(4) if u[v]<period[v] and z[v]>=degree(H)[v]]
        require(bool(options), 'actual target-return period not legal')
        v=options[0];z=step(H,z,v);u[v]+=1;word.append(v)
    require(z==Y, 'period misses original target')
    alternative={'A':A,'x':x,'designated_count':f,'period':period,'alternative_target_count':tuple(f[j]+period[j] for j in range(4)),'actual_legal_target_return_word':word,'marker_fired_after_gate':True}
    normalization=[];num_transitions=0
    for ell0,ell1,a,b in product(range(2),range(2),range(1,3),range(1,3)):
        A=((ell0,a),(b,ell1))
        for x in product(range(-1,3),repeat=2):
            s,cyc,e,_=explore(A,x);H,z,k=normalize(A,x);s2,cyc2,e2,_=explore(H,z)
            shifted={tuple(t[j]+k[j] for j in range(2)) for t in s}
            require(s2==shifted and cyc==cyc2,'signed normalization state conjugacy')
            for t,out in e.items():
                t2=tuple(t[j]+k[j] for j in range(2));require(e2[t2]==[tuple(w[j]+k[j] for j in range(2)) for w in out],'legal-word conjugacy');num_transitions+=len(out)
            K,w=relay(H,z);s3,cyc3,e3,_=explore(K,w)
            require(strong(K) and all(K[j][j]==0 for j in range(len(K))),'relay graph class')
            require(cyc==cyc3,'relay changes nonhalting')
            normalization.append({'A':A,'x':x,'old_states':len(s),'normalized_states':len(s2),'relay_states':len(s3),'nonhalting':cyc})
    one=[]
    for ell in range(4):
        for c in range(5):
            A=((ell,),);s,cyc,_,_=explore(A,(c,));require(cyc==(c>=ell),'one-vertex classification')
            replacement=((0,1),(1,0));rx=(1,0) if c>=ell else (0,0)
            _,r,_,_=explore(replacement,rx);require(r==cyc,'one-vertex replacement')
            one.append({'ell':ell,'c':c,'nonhalting':cyc})
    cases=0;uchecks=0;certificates=0;nonimage=0;maxbits=0
    certificate_rows=[]
    for a,b in product(range(1,5),repeat=2):
        A=((0,a),(b,0))
        for C in range(6):
            for x0 in range(C+1):
                x=(x0,C-x0);reachable,_,_,_=explore(A,x)
                for y0 in range(C+1):
                    y=(y0,C-y0);cases+=1;sol=reduced_two(A,x,y)
                    if sol is None:require(y not in reachable,'nonimage reachable');nonimage+=1;continue
                    f,p=sol;maxbits=max(maxbits,*[v.bit_length() for v in f]);found=[]
                    for u in product(range(f[0]+1),range(f[1]+1)):
                        okay=cert(A,x,f,u);uchecks+=1
                        if okay:found.append(u)
                    require(bool(found)==(y not in reachable),'coNP count certificate mismatch')
                    certificates+=len(found)
                    if found and len(certificate_rows)<10:certificate_rows.append({'A':A,'x':x,'y':y,'f':f,'p':p,'u':found[0],'z':count_state(A,x,found[0])})
    negatives=[]
    A=((0,1),(1,0));x=(0,0);y=(0,0);f=(0,0)
    require(not cert(A,x,f,(0,0)) and cert(A,x,f,(0,0),proper=False),'missing properness control')
    negatives.append({'variant':'omit u != f','false_nonreachability':True,'x':x,'y':y,'f':f,'u':(0,0)})
    require(cert(A,x,(1,1),(0,0)),'unreduced firing-vector control')
    negatives.append({'variant':'omit reducedness','false_nonreachability':True,'x':x,'y':y,'f':(1,1),'u':(0,0)})
    x=(1,0);y=(0,1);f=(1,0)
    require(not cert(A,x,f,(0,0)) and cert(A,x,f,(0,0),strict=False),'nonstrict threshold control')
    negatives.append({'variant':'replace obstruction < degree by <= degree','false_nonreachability':True,'x':x,'y':y,'f':f,'u':(0,0)})
    # Intentionally bad reduction parameters, exhaust unrestricted target graphs.
    for variant,kw in [('M=1',{'M_override':1}),('gate deficit lowered by one',{'deficit_offset':1})]:
        found=None
        for a,b in product(range(1,4),repeat=2):
            for x in product(range(2),repeat=2):
                A=((0,a),(b,0));_,nonhalt,_,_=explore(A,x)
                if nonhalt:continue
                H,X,Y,_,_,_,_=reduction(A,x,**kw);states,_,_,_=explore(H,X)
                if Y in states:found={'variant':variant,'A':A,'x':x,'target_states':len(states),'false_positive':True};break
            if found:break
        require(found is not None,'invalid reduction not falsified');negatives.append(found)
    # Naively deleting loops preserves net L, but can change activity.
    A=((1,1),(1,1));x=(1,0);_,old,_,_=explore(A,x);K=((0,1),(1,0));_,new,_,_=explore(K,x)
    require(not old and new,'naive loop deletion control');negatives.append({'variant':'delete loops without relay','A':A,'x':x,'old_nonhalting':old,'new_nonhalting':new})
    A=((0,1),(1,0));x=(-1,2);H,z,k=normalize(A,x);wrong=((0,1),(1,0));
    require(degree(H)!=(1,1) and (z[0]>=degree(H)[0])==(x[0]>=1),'normalization thresholds')
    # A direct local witness where merely adding chips changes a legal move.
    x=(-1,2);H,z,k=normalize(A,x);x_after=step(A,x,1);z_after=step(H,z,1)
    require((x_after[0]>=1)==(z_after[0]>=degree(H)[0]) and (x_after[0]>=1)!=(z_after[0]>=1),'chips-only fault')
    negatives.append({'variant':'add compensating chips but omit compensating loops','word_prefix_counts':(0,1),'old_state':x_after,'wrong_state':z_after,'false_legal_move_at':0,'note':'actual legal one-firing prefix in both correct games'})
    one_signed=0
    for ell in range(1,4):
        for c in range(-2,4):
            A=((ell,),);x=(c,);old,cyc,_,_=explore(A,x);H,z,k=normalize(A,x);K,w=relay(H,z);new,cyc2,_,_=explore(K,w)
            require(cyc==cyc2 and strong(K) and all(K[j][j]==0 for j in range(len(K))), 'signed one-vertex relay')
            one_signed+=1
    binary=[]
    for bits in [1,8,64,512,4096]:
        a=(1<<bits)+1;A=((0,a),(a+2,0));x=(1<<bits,3)
        H,X,Y,N,M,B,f=reduction(A,x)
        require(strong(H) and min(X)>=0 and min(Y)>=0 and sum(X)==sum(Y),'large-binary output')
        upper=12*bits+40;actual=max(v.bit_length() for row in H for v in row);actual=max(actual,*[v.bit_length() for v in X+Y])
        require(actual<=upper,'large-binary blowup control')
        binary.append({'input_parameter_bits':bits,'N_bits':N.bit_length(),'M_bits':M.bit_length(),'B_bits':B.bit_length(),'largest_output_integer_bits':actual,'explicit_test_bound':upper})
    return {'status':'PASS','optimized_guards_active':True,'source_prefix_cleanup_cases':len(rows),'source_prefix_count_states':sum(r['prefix_count_states'] for r in rows),'source_prefix_transitions':sum(r['prefix_transitions'] for r in rows),'all_cleanup_order_transitions':sum(r['cleanup_transitions'] for r in rows),'source_positive_cases':sum(r['nonhalting'] for r in rows),'unrestricted_target_cases':target,'alternative_firing_count_control':alternative,'signed_normalization_relay_cases':len(normalization),'signed_word_transition_checks':num_transitions,'normalization_relay_total_states':sum(r['relay_states'] for r in normalization),'one_vertex_cases':one,'signed_one_vertex_relay_cases':one_signed,'certificate_source_target_pairs':cases,'certificate_candidate_count_vectors':uchecks,'certificate_count':certificates,'nonimage_pairs':nonimage,'maximum_small_certificate_bits':maxbits,'sample_certificates':certificate_rows,'negative_controls':negatives,'large_binary_controls':binary,'finite_checks_only':True,'historical_omitted_program_replayed':False}

if __name__=='__main__':
    out=main();dest=Path(sys.argv[1]) if len(sys.argv)>1 else None
    data=json.dumps(out,indent=2)+'\n'
    if dest:dest.write_text(data)
    print(json.dumps({k:v for k,v in out.items() if k not in ['one_vertex_cases','sample_certificates','unrestricted_target_cases','negative_controls','large_binary_controls']},sort_keys=True))
