#!/usr/bin/env python3
from __future__ import annotations
from itertools import product, combinations, permutations
from collections import defaultdict
import json, time
from pathlib import Path

HERE=Path(__file__).resolve().parent

# ---------------- theta combinatorics ----------------
def compositions(n):
    for a in range(n+1):
      for b in range(n-a+1):
        c=n-a-b
        if sum(x==0 for x in (a,b,c))<=1:
          yield (a,b,c)

def theta_structure(lengths):
    # vertices 0=U,1=V; port vertices 2... in path order
    vertices=[{'pole':True,'path':None,'pos':None},{'pole':True,'path':None,'pos':None}]
    paths=[]; port_ids=[]
    for i,l in enumerate(lengths):
        ids=[]
        for j in range(l):
            vid=len(vertices); vertices.append({'pole':False,'path':i,'pos':j}); ids.append(vid); port_ids.append(vid)
        paths.append([0]+ids+[1])
    edges=[]
    for i,path in enumerate(paths):
        for j,(u,v) in enumerate(zip(path,path[1:])):
            edges.append((u,v,i,j))
    return vertices,paths,edges,port_ids

def enumerate_orientations(vertices,edges,port_ids,entry,retics):
    n=len(vertices); m=len(edges)
    req=[]
    for v in range(n):
        if vertices[v]['pole']:
            boundary_out=0
        else:
            boundary_out=0 if v==entry else 1
        req.append((1 if v in retics else 2)-boundary_out)
    deg=[0]*n
    inc=[[] for _ in range(n)]
    for ei,(u,v,*_) in enumerate(edges):
        deg[u]+=1;deg[v]+=1;inc[u].append(ei);inc[v].append(ei)
    # impossible req
    if any(r<0 or r>d for r,d in zip(req,deg)): return
    out=[0]*n; undec=deg[:]; bits=[None]*m
    def rec(ei):
        if ei==m:
            if out!=req:return
            # directed adjacency and acyclicity
            adj=[[] for _ in range(n)]; indeg=[0]*n
            for bit,(u,v,*_) in zip(bits,edges):
                a,b=(u,v) if bit==0 else (v,u);adj[a].append(b);indeg[b]+=1
            # boundary: outside->entry, other vertices->outside cannot form internal cycle
            q=[v for v in range(n) if indeg[v]==0];seen=0
            while q:
                x=q.pop();seen+=1
                for y in adj[x]:
                    indeg[y]-=1
                    if indeg[y]==0:q.append(y)
            if seen<n:return
            # rooted TC and no retic child
            for v in range(n):
                internal_children=adj[v]
                has_boundary_child=(not vertices[v]['pole'] and v!=entry)
                if v in retics and any(c in retics for c in internal_children):return
                if not has_boundary_child and not any(c not in retics for c in internal_children):return
            # S criterion for internal tails: no tree vertex tails two retic edges; more literally other two incidences U.
            # Construct mixed status for every internal/boundary incidence.
            directed_into=set()
            for bit,(u,v,*_) in zip(bits,edges):
                a,b=(u,v) if bit==0 else (v,u)
                if b in retics:directed_into.add((a,b))
            if entry in retics: directed_into.add(('IN',entry))
            # For each internal tail into retic, count undirected incidences among its degree-3 full incidences.
            for a,b in directed_into:
                if a=='IN':continue
                und=0
                for eidx in inc[a]:
                    u,v,*_=edges[eidx]; other=v if u==a else u
                    bit=bits[eidx]; tail,head=(u,v) if bit==0 else (v,u)
                    if head not in retics: und+=1
                # boundary edge is undirected unless entry is retic; at tail a it is present only if a is a port vertex.
                if not vertices[a]['pole']:
                    if not (a==entry and a in retics): und+=1
                if und<2:return
            yield tuple(bits)
            return
        u,v,*_=edges[ei]
        # bit0 u->v
        for bit in (0,1):
            tail=u if bit==0 else v
            bits[ei]=bit;out[tail]+=1;undec[u]-=1;undec[v]-=1
            ok=True
            for x in (u,v):
                if out[x]>req[x] or out[x]+undec[x]<req[x]:ok=False
            if ok:yield from rec(ei+1)
            out[tail]-=1;undec[u]+=1;undec[v]+=1
        bits[ei]=None
    yield from rec(0)

def theta_code(vertices,paths,edges,entry,retics,bits,labels=None,tquot=False):
    # labels maps port vertex to outgoing label; entry gets label 0/IN.
    # Determine triangle nodes if any and tquot requested.
    edge_by_pair={frozenset((u,v)):(idx,u,v) for idx,(u,v,*_) in enumerate(edges)}
    triangles=[]
    # a theta triangle arises from two paths whose edge lengths sum 3
    for i,j in combinations(range(3),2):
        nodes=set(paths[i]+paths[j])
        if len(nodes)==3:triangles.append(nodes)
    tri=triangles[0] if len(triangles)==1 else set()
    def vrole(v):
        if tquot and v in tri:return ('TRI',)
        rt='R' if v in retics else 'T'
        if vertices[v]['pole']:return (rt,'P')
        if v==entry:return (rt,'IN')
        return (rt,labels[v] if labels else 'OUT')
    def estatus(u,v):
        idx,a,b=edge_by_pair[frozenset((u,v))];bit=bits[idx]
        tail,head=(a,b) if bit==0 else (b,a)
        if tquot and u in tri and v in tri:return 0
        if head in retics:
            return 1 if (tail==u and head==v) else -1
        return 0
    def encode(swapped=False):
        pu,pv=(vrole(1),vrole(0)) if swapped else (vrole(0),vrole(1))
        pcs=[]
        for path in paths:
            seq=list(reversed(path)) if swapped else path
            items=[]
            for a,b in zip(seq,seq[1:]):
                items.append(estatus(a,b))
                if b not in (0,1):items.append(vrole(b))
            pcs.append(tuple(items))
        return (pu,pv,tuple(sorted(pcs,key=repr)))
    return min(encode(False),encode(True),key=repr)

def enumerate_theta_role(p):
    codes={}; presentations=0
    for lens in compositions(p):
      vertices,paths,edges,ports=theta_structure(lens)
      for entry in ports:
       for ret in combinations(range(len(vertices)),2):
        ret=set(ret)
        for bits in enumerate_orientations(vertices,edges,ports,entry,ret):
            presentations+=1
            code=theta_code(vertices,paths,edges,entry,ret,bits)
            codes.setdefault(repr(code),(vertices,paths,edges,entry,ret,bits,lens))
    return presentations,codes

def labelled_theta_codes(p):
    pres,roles=enumerate_theta_role(p)
    exact=set();tq=set();raw=0
    for data in roles.values():
        vertices,paths,edges,entry,ret,bits,lens=data
        outs=[v for v in range(len(vertices)) if not vertices[v]['pole'] and v!=entry]
        for perm in permutations(range(1,p)):
            labels=dict(zip(outs,perm));raw+=1
            exact.add(repr(theta_code(vertices,paths,edges,entry,ret,bits,labels,False)))
            tq.add(repr(theta_code(vertices,paths,edges,entry,ret,bits,labels,True)))
    return pres,len(roles),raw,len(exact),len(tq)

# ---------------- cycle combinatorics ----------------
def cycle_codes(p):
    # p port vertices on cycle; one IN label 0. choose retic outgoing port and cyclic order labels.
    # exact code under dihedral; T quotient erases retic on p=3 only.
    exact=set();tq=set();raw=0
    labels=list(range(1,p))
    for perm in permutations(labels):
      seq=(0,)+perm
      for rpos in range(1,p): # entry cannot be retic
        raw+=1
        def code_for(s,r,rev=False):
            n=len(s)
            arr=[]
            for i,x in enumerate(s):
                role='IN' if x==0 else x
                isr=(i==r)
                if p==3: # triangle quotient handled later
                    pass
                arr.append(('R' if isr else 'T',role))
            return tuple(arr)
        # canonical rotations/reversal preserving labels automatically; brute all dihedral transformations of indexed sequence and retic
        variants=[]; tvars=[]
        for rev in (False,True):
          inds=list(range(p));
          if rev: inds=[0]+list(reversed(range(1,p))) # not all reflections; use all rotations below generic
        # generic dihedral transformations on positions
        for shift in range(p):
          for sign in (1,-1):
            pos=[(shift+sign*i)%p for i in range(p)]
            arr=[];arrt=[]
            for old in pos:
                lab=seq[old];role='IN' if lab==0 else lab
                arr.append((('R' if old==rpos else 'T'),role))
                arrt.append((('TRI' if p==3 else ('R' if old==rpos else 'T')),role))
            variants.append(tuple(arr));tvars.append(tuple(arrt))
        exact.add(repr(min(variants,key=repr)));tq.add(repr(min(tvars,key=repr)))
    return raw,len(exact),len(tq)

if __name__=='__main__':
    out={}
    expected={
      4:(30,21,9),
      5:(612,516,48),
      6:(9420,8520,300),
      7:(135900,127260,2160),
    }
    for p in (4,5,6,7):
        pres,roles=enumerate_theta_role(p)
        lp,lr,raw,ex,tq=labelled_theta_codes(p)
        craw,cex,ctq=cycle_codes(p)
        assert (ex,tq,ctq)==expected[p]
        rec={'theta_strong_presentations':pres,'theta_role_classes':len(roles),
             'theta_label_raw':raw,'theta_label_exact':ex,'theta_label_mod_T':tq,
             'cycle_raw':craw,'cycle_exact':cex,'cycle_mod_T':ctq,'total_mod_T':tq+ctq}
        out[str(p)]=rec;print(p,rec,flush=True)
    target=HERE.parent/'certificates'/'nonroot_topology_counts.json'
    target.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print('ALL PRIMITIVE TOPOLOGY ATLAS CHECKS PASSED')

def theta_event_core_code(vertices,paths,edges,entry,retics,bits):
    # Directed rooted event core: retain poles, reticulations, and the entry split;
    # suppress other ordinary path vertices.
    pair={frozenset((u,v)):(idx,u,v) for idx,(u,v,*_) in enumerate(edges)}
    def edir(a,b):
        idx,u,v=pair[frozenset((a,b))]; bit=bits[idx]; tail,head=(u,v) if bit==0 else (v,u)
        return 1 if (tail==a and head==b) else -1
    def role(v):
        bitsr=[]
        if v in retics:bitsr.append('R')
        else:bitsr.append('T')
        if v==entry:bitsr.append('S')
        if vertices[v]['pole']:bitsr.append('P')
        return ''.join(bitsr)
    def encode(sw=False):
        pu,pv=(role(1),role(0)) if sw else (role(0),role(1))
        pcs=[]
        for path in paths:
            seq=list(reversed(path)) if sw else path
            retained=[seq[0]]+[v for v in seq[1:-1] if v in retics or v==entry]+[seq[-1]]
            items=[]
            for a,b in zip(retained,retained[1:]):
                # find segment in seq and ensure all directed consistently from a to b or reverse
                ia=seq.index(a); ib=seq.index(b); sub=seq[ia:ib+1]
                ds=[edir(x,y) for x,y in zip(sub,sub[1:])]
                assert all(d==ds[0] for d in ds), (seq,retained,ds)
                items.append(ds[0]);
                if b not in (0,1):items.append(role(b))
            pcs.append(tuple(items))
        return (pu,pv,tuple(sorted(pcs,key=repr)))
    return min(encode(False),encode(True),key=repr)
