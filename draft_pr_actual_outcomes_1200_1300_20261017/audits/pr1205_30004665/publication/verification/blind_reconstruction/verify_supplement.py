#!/usr/bin/env python3
"""Exact edge/route/facet checks; never change the historical freeze."""
import collections, hashlib, itertools, json
import sympy as s
import verify_blind as v

def chamber_edge(w,u,move,C):
    """Compare x^e (x_t*x_(t+2)+x_(t+1))^q signatures.
    Positive string braid lift: (u,v,w) ->
    (v*w/(u*w+v), u*w, (u*w+v)/w), tropicalizing to KS2022 Def2.
    """
    n=len(w); b,_,_=v.seed(w); old=v.chamber(w,C); new=v.chamber(u,C)
    p=v.transport(w,u,move); kind,t=move
    for i in range(n):
        left=list(new.row(i)); lq=0
        if kind=='commute': left[t],left[t+1]=left[t+1],left[t]
        else:
            a,bb,c=left[t:t+3]
            left[t:t+3]=[bb,a,a+bb-c]; lq=c-a
        j=p[i]; right=list(old.row(j)); rq=0
        if kind=='braid':
            r=b[j][t]
            if j==t: right=[-e for e in right]
            elif r>0: right[t+1]+=r; rq=-r
            elif r<0: right[t]+=r; right[t+2]+=r; rq=-r
        assert left==right and lq==rq,(w,u,move,i,left,right,lq,rq)

def other_routes(w):
    """Ordinary BFS, reversed neighbors, different optimized target words."""
    q=collections.deque([w]); parent={w:None}
    while q:
        u=q.popleft()
        for target,m in reversed(list(v.moves(u))):
            if target not in parent: parent[target]=(u,m); q.append(target)
    routes={}
    for a in sorted(set(w)):
        target=max(u for u in parent if u[-1]==a)
        rev=[]; u=target
        while parent[u] is not None:
            p,m=parent[u]; rev.append((p,u,m)); u=p
        routes[a]=list(reversed(rev))
    return routes,parent

def main():
    raw=(v.BASE/'blind_frozen.json').read_bytes(); d=json.loads(raw)
    assert hashlib.sha256(raw).hexdigest()=='7881d1d0ef80ff7ca036f16a06d2d7f23cb666bab223500226d6cded3f66a30d'
    C,_,_=v.roots(v.WORD)
    routes,vertices=other_routes(v.WORD); edge_count=0
    for w in vertices:
        for u,m in v.moves(w): chamber_edge(w,u,m,C); edge_count+=1
    print('All',edge_count,'directed chamber-ansatz/braid edges agree.',flush=True)
    alternate=[]
    for a,route in routes.items():
        p,z=v.pullback(route)
        assert v.laurent_terms(p,z)==d['summands'][str(a)]['canonical_X_support']
        alternate.append({'a':a,'target_word':list(route[-1][1]) if route else list(v.WORD),
            'moves':[{'kind':m[0],'start_position':m[1]+1} for _,_,m in route],
            'mutations':sum(m[0]=='braid' for _,_,m in route)})
        print('Alternate route',a,'agrees exactly.',flush=True)
    labels=[]; rows=[]; witnesses={}
    frozen={k-1 for k in d['seed']['frozen_positions']}
    mutable=[j for j in range(12) if j not in frozen]
    for a,entry in d['summands'].items():
        group=[t['exponents'] for t in entry['canonical_X_support']]
        fixed=next(k for k in frozen if all(r[k]==-1 for r in group))
        assert all(all(r[k]==0 for k in frozen if k!=fixed) for r in group)
        found={}
        for direction in itertools.product((-1,0,1),repeat=len(mutable)):
            values=[sum(r[k]*q for k,q in zip(mutable,direction)) for r in group]
            low=min(values); indices=[j for j,q in enumerate(values) if q==low]
            if len(indices)==1 and indices[0] not in found:
                i=indices[0]
                other=min((q for j,q in enumerate(values) if j!=i),default=low+1)
                w=[-1000 if j in frozen else 0 for j in range(12)]
                for k,q in zip(mutable,direction): w[k]=2*q
                w[fixed]=low+other; found[i]=w
            if len(found)==len(group): break
        assert len(found)==len(group),(a,'direction search failed')
        for term_index,term in enumerate(entry['canonical_X_support']):
            label=(int(a),term_index)
            labels.append(label); rows.append(term['exponents']); witnesses[label]=found[term_index]
    interior=[-1]*12
    assert all(sum(e*x for e,x in zip(row,interior))>0 for row in rows)
    certificates=[]
    for i,row in enumerate(rows):
        witness=witnesses[labels[i]]
        pairings=[sum(e*x for e,x in zip(r,witness)) for r in rows]
        assert pairings[i]<0 and all(x>0 for j,x in enumerate(pairings) if j!=i)
        depth=-pairings[i]; height=sum(e*x for e,x in zip(row,interior))
        boundary=[height*x+depth*y for x,y in zip(witness,interior)]
        boundary_pairings=[sum(e*x for e,x in zip(r,boundary)) for r in rows]
        assert boundary_pairings[i]==0 and all(x>0 for j,x in enumerate(boundary_pairings) if i!=j)
        certificates.append({'label':labels[i],'exclusive_violation_witness':witness,
             'all_pairings':pairings,'facet_relative_interior_point':boundary,
             'boundary_pairings':boundary_pairings})
    output={'frozen_sha256':hashlib.sha256(raw).hexdigest(),'chamber_edge_checks':edge_count,
       'alternate_routes':alternate,'strict_interior_point':interior,'facets':certificates,
       'claim':'All 22 canonical-X inequalities are facets of a full-dimensional cone; the unimodular chamber pullback also has 22 facets.'}
    path=v.BASE/'supplement_exact.json'; encoded=(json.dumps(output,indent=2,sort_keys=True)+'\n').encode()
    if path.exists(): assert path.read_bytes()==encoded
    else: path.write_bytes(encoded)
    print(json.dumps({'facets':len(certificates),'supplement_sha256':hashlib.sha256(encoded).hexdigest()},indent=2))

if __name__=='__main__': main()
