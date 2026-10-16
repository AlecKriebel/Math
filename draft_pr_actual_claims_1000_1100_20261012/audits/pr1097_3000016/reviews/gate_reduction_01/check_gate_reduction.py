#!/usr/bin/env python3
"""Fresh exact finite falsification controls. No historical-code replay; no asserts."""
from collections import deque
from itertools import product
import json,sys,datetime,hashlib
from pathlib import Path

def need(q,msg):
    if not q: raise ValueError(msg)

def degree(a):return tuple(map(sum,a))
def legal(a,x):return tuple(v for v,d in enumerate(degree(a)) if x[v]>=d)
def fire(a,x,v):
    need(v in legal(a,x),'illegal firing')
    y=list(x);y[v]-=sum(a[v])
    for w,k in enumerate(a[v]):y[w]+=k
    need(sum(y)==sum(x),'conservation');return tuple(y)
def strong(a):
    n=len(a)
    for start in range(n):
        seen={start};stack=[start]
        while stack:
            u=stack.pop()
            for v in range(n):
                if a[u][v] and v not in seen:seen.add(v);stack.append(v)
        if len(seen)!=n:return False
    return True

def graph_space(a,x,cap=300000):
    x=tuple(x);todo=deque([x]);edges={};pred={x:None}
    while todo:
        z=todo.popleft();rows=[]
        for v in legal(a,z):
            y=fire(a,z,v);rows.append((y,v))
            if y not in pred:
                pred[y]=(z,v);todo.append(y)
                if len(pred)>cap:raise ValueError('explicit state-space cap exceeded; no completion claim')
        edges[z]=rows
    # A reachable directed cycle is equivalent to an infinite word. Kahn removal
    # detects all cycles without importing any chip-firing dichotomy.
    indeg={z:0 for z in edges}
    for rows in edges.values():
        for y,_ in rows:indeg[y]+=1
    todo=deque(z for z,d in indeg.items() if not d);removed=0
    while todo:
        z=todo.popleft();removed+=1
        for y,_ in edges[z]:
            indeg[y]-=1
            if not indeg[y]:todo.append(y)
    return edges,pred,removed<len(edges)
def path(pred,y):
    out=[]
    while pred[y] is not None:
        y,v=pred[y];out.append(v)
    return tuple(reversed(out))

def construct(a,x,variant=None):
    n=len(a);C=sum(x);N=(C+1)**n
    if variant=='short_cutoff':N=1
    M=N+1
    if variant=='bad_scale':M=max(0,N-1)
    D=max(degree(a));B=N*(M*D+1)
    h=[[0]*(n+2) for _ in range(n+2)]
    for u in range(n):
        for v in range(n):h[u][v]=M*a[u][v]
        h[u][n]=1;h[n][u]=B
    h[n][n+1]=h[n+1][n]=1
    X=tuple(M*x[v]+N for v in range(n))+(n*B+1-N,0)
    if variant=='early_gate':X=X[:n]+(X[n]+1,0)
    f=(N,)*n+(1,0)
    Y=list(X)
    for v,k in enumerate(f):
        Y[v]-=sum(h[v])*k
        for w,m in enumerate(h[v]):Y[w]+=m*k
    return tuple(map(tuple,h)),X,tuple(Y),N,M,B,f

def prefix_all_orders(a,x,h,X,N,M):
    n=len(a);layers={(0,)*n:(tuple(x),X,())};states=0;transitions=0;last=[]
    for t in range(N+1):
        next_layer={}
        for counts,(z,w,word) in layers.items():
            states+=1
            need(all(w[v]==M*z[v]+N-counts[v] for v in range(n)),'simulation identity')
            need(w[n]==sum(h[n])-N+t and w[n+1]==0,'gate/marker identity')
            need((n in legal(h,w))==(t>=N),'gate threshold off by one')
            need(n+1 not in legal(h,w),'pre-gate marker')
            if t==N:last.append((counts,z,w,word));continue
            lh=tuple(v for v in legal(h,w) if v<n)
            need(lh==legal(a,z),'legal-old equivalence')
            for v in lh:
                c=list(counts);c[v]+=1;c=tuple(c)
                y=fire(a,z,v);u=fire(h,w,v);transitions+=1
                if c in next_layer:need(next_layer[c][:2]==(y,u),'odometer configuration dependence')
                else:next_layer[c]=(y,u,word+(v,))
        layers=next_layer
        if not layers and t<N:break
    return last,states,transitions

def complete(a,x,h,X,Y,N,last,order):
    counts,z,w,word=last
    w=fire(h,w,len(a));out=list(word)+[len(a)]
    remaining=[N-k for k in counts]
    need(all(w[v]>=N*(sum(h[v])) for v in range(len(a))),'cleanup reserve')
    for v in order:
        for _ in range(remaining[v]):w=fire(h,w,v);out.append(v)
    need(w==Y,'target not reached')
    need(tuple(out.count(v) for v in range(len(h)))==(N,)*len(a)+(1,0),'wrong prescribed counts')
    return len(out)

def test_reduction():
    rows=[];prefix_states=prefix_edges=0;full_halting_states=0;maxN=0
    cases=[]
    for a,b,x,y in product(range(1,4),range(1,4),range(4),range(4)):
        cases.append((((0,a),(b,0)),(x,y)))
    pairs=[(u,v) for u in range(3) for v in range(3) if u!=v]
    for bits in product(range(2),repeat=6):
        a=[[0]*3 for _ in range(3)]
        for (u,v),b in zip(pairs,bits):a[u][v]=b
        a=tuple(map(tuple,a))
        if strong(a):
            for x in product(range(2),repeat=3):cases.append((a,x))
    for a,x in cases:
        edges,_,nonhalt=graph_space(a,x)
        h,X,Y,N,M,B,f=construct(a,x)
        need(strong(h) and all(h[v][v]==0 for v in range(len(h))),'target graph class')
        need(min(X)>=0 and min(Y)>=0 and X!=Y and sum(X)==sum(Y),'target configurations')
        last,ns,ne=prefix_all_orders(a,x,h,X,N,M);prefix_states+=ns;prefix_edges+=ne;maxN=max(maxN,N)
        need(bool(last)==nonhalt,'finite cutoff equivalence')
        if nonhalt:
            # First, last and middle possible odometers, with both extreme cleanup
            # orders, are actual words; all orders are proved separately above.
            picks={0,len(last)//2,len(last)-1}
            for k in sorted(picks):
                complete(a,x,h,X,Y,N,last[k],tuple(range(len(a))))
                complete(a,x,h,X,Y,N,last[k],tuple(reversed(range(len(a)))))
            rows.append({'n':len(a),'nonhalting':True,'source_states':len(edges),'N':N,'prefix_states':ns,'boundary_odometers':len(last)})
        else:
            full,_,hcycle=graph_space(h,X);full_halting_states+=len(full)
            need(Y not in full and not hcycle,'full arbitrary-order halting-target falsifier')
            rows.append({'n':len(a),'nonhalting':False,'source_states':len(edges),'N':N,'prefix_states':ns,'complete_augmented_states':len(full)})
    return {'cases':len(rows),'nonhalting_cases':sum(x['nonhalting'] for x in rows),'halting_cases':sum(not x['nonhalting'] for x in rows),'prefix_states':prefix_states,'prefix_edges':prefix_edges,'complete_halting_augmented_states':full_halting_states,'max_N':maxN,'case_table_sha256':hashlib.sha256(json.dumps(rows,sort_keys=True).encode()).hexdigest()}

def relay(a,x):
    n=len(a);owners=[v for v in range(n) if a[v][v]];e=[[0]*(n+len(owners)) for _ in range(n+len(owners))]
    for u in range(n):
        for v in range(n):
            if u!=v:e[u][v]=a[u][v]
    for j,v in enumerate(owners):e[v][n+j]=e[n+j][v]=a[v][v]
    return tuple(map(tuple,e)),tuple(x)+(0,)*len(owners),owners

def test_relays_and_offsets():
    cases=states=edges_checked=0
    for a,b,l0,l1,x,y in product(range(1,3),range(1,3),range(3),range(3),range(3),range(3)):
        g=((l0,a),(b,l1));z=(x,y);orig,_,c1=graph_space(g,z);e,w,owners=relay(g,z);expanded,_,c2=graph_space(e,w)
        need(c1==c2,'relay changes nonhalting');need(strong(e),'relay connectivity')
        for state,arcs in expanded.items():
            projected=list(state[:2])
            for j,v in enumerate(owners):
                need(state[2+j]%g[v][v]==0,'partial relay packet');projected[v]+=state[2+j]
            projected=tuple(projected);need(projected in orig,'relay projected source state')
            for nxt,v in arcs:
                if v<2:need(v in legal(g,projected),'relay projected firing illegal')
                edges_checked+=1
            states+=1
        cases+=1
    signed_cases=signed_states=0
    for a,b,l0,l1,x,y in product(range(1,3),range(1,3),range(2),range(2),range(-2,3),range(-2,3)):
        g=((l0,a),(b,l1));z=(x,y);off=(max(0,-x),max(0,-y));e=((l0+off[0],a),(b,l1+off[1]));w=tuple(z[i]+off[i] for i in range(2));orig,_,c1=graph_space(g,z);expanded,_,c2=graph_space(e,w)
        need(c1==c2,'signed offset nonhalting');need({tuple(t[i]+off[i] for i in range(2)) for t in orig}==set(expanded),'signed offset state space')
        for t in orig:need(legal(g,t)==legal(e,tuple(t[i]+off[i] for i in range(2))),'signed offset legal word')
        signed_states+=len(orig);signed_cases+=1
    one=[]
    for ell,c in product(range(4),range(5)):
        g=((ell,),);orig,_,cyc=graph_space(g,(c,));need(cyc==(c>=ell),'one-vertex threshold')
        e,w,owners=relay(g,(c,))
        if ell:need(graph_space(e,w)[2]==cyc,'one-vertex relay equivalence')
        fixed=((0,1),(1,0));initial=(1,0) if cyc else (0,0);need(graph_space(fixed,initial)[2]==cyc,'fixed one-vertex replacement')
        one.append({'loops':ell,'chips':c,'nonhalting':cyc})
    return {'relay_cases':cases,'expanded_states':states,'expanded_edges':edges_checked,'signed_offset_cases':signed_cases,'signed_states':signed_states,'one_vertex_cases':len(one)}

def test_late_counts():
    a=((0,1),(1,0));x=(1,1);h,X,Y,N,M,B,f=construct(a,x);last,_,_=prefix_all_orders(a,x,h,X,N,M);counts,z,w,word=last[-1]
    direct=list(word)+[2]
    w=fire(h,w,2)
    for v in [1,0]:
        for _ in range(N-counts[v]):w=fire(h,w,v);direct.append(v)
    need(w==Y,'direct path')
    p=(B,B,1,1);counts=[0]*4;cycle=[]
    for _ in range(sum(p)):
        choices=[v for v in legal(h,w) if counts[v]<p[v]]
        need(bool(choices),'selected positive target not recurrent')
        v=choices[-1];w=fire(h,w,v);counts[v]+=1;cycle.append(v)
    need(tuple(counts)==p and w==Y,'alternate-odometer cycle')
    allword=direct+cycle;total=tuple(allword.count(v) for v in range(4))
    need(total==tuple(f[v]+p[v] for v in range(4)) and total[2]==2 and total[3]==1,'multiple-gate target witness')
    # Deliberately defer the first gate by one old firing, then finish to f.
    before=last[-1]; c,z,w0,word0=before
    choices=[v for v in legal(h,w0) if v<2 and c[v]<N]
    need(bool(choices),'delayed-gate control needs one further old move')
    v=choices[0];delayed=list(word0)+[v];w0=fire(h,w0,v);c=list(c);c[v]+=1
    w0=fire(h,w0,2);delayed.append(2)
    for v in [0,1]:
        for _ in range(N-c[v]):w0=fire(h,w0,v);delayed.append(v)
    need(w0==Y and delayed.index(2)==N+1,'delayed first gate target witness')
    _,pred,cycleflag=graph_space(h,X,cap=300000)
    need(Y in pred,'unrestricted target BFS')
    return {'source':{'adjacency':a,'initial':x},'N':N,'B':B,'direct_counts':f,'alternate_counts':total,'cycle_counts':p,'cycle_word':cycle,'direct_word':direct,'delayed_gate_word':delayed,'first_gate_delay_from_threshold':1,'complete_augmented_states':len(pred),'augmented_reachable_cycle':cycleflag}

def test_faults():
    rows=[]
    for variant,a,x in [('early_gate',((0,1),(1,0)),(0,0)),('short_cutoff',((0,2),(3,0)),(2,0))]:
        need(not graph_space(a,x)[2],'fault source must halt');h,X,Y,N,M,B,f=construct(a,x,variant);space,pred,_=graph_space(h,X)
        need(Y in space,'deliberate invalid variant must create false positive')
        rows.append({'variant':variant,'source':{'adjacency':a,'initial':x},'N':N,'M':M,'B':B,'X':X,'Y':Y,'false_positive_word':path(pred,Y),'complete_augmented_states':len(space)})
    a=((0,2),(2,0));x=(1,0);h,X,Y,N,M,B,f=construct(a,x,'bad_scale')
    need(0 not in legal(a,x) and 0 in legal(h,X),'small-scale fault must permit illegal simulation')
    rows.append({'variant':'bad_scale','N':N,'M':M,'source_illegal_vertex':0,'augmented_initial':X,'threshold':sum(h[0])})
    # Raising the marker's target count without the corresponding gate balance
    # must be caught by the explicit target equation.
    h,X,Y,N,M,B,f=construct(((0,1),(1,0)),(1,0));bad=Y[:-1]+(2,)
    need(sum(bad)!=sum(X),'marker balance fault conservation detector')
    rows.append({'variant':'wrong_marker_target','rejected_by':'total chip conservation'})
    return rows

def test_binary_size():
    rows=[]
    for n in [2,3,5,8]:
        a=[[0]*n for _ in range(n)]
        for v in range(n):a[v][(v+1)%n]=(1<<(128*(v+1)))+1
        a=tuple(map(tuple,a));x=tuple((1<<(256+v))+v for v in range(n))
        h,X,Y,N,M,B,f=construct(a,x)
        need(strong(h) and min(X)>=0 and min(Y)>=0 and sum(X)==sum(Y),'large binary construction')
        bits=sum(max(1,z.bit_length()) for row in a for z in row)+sum(z.bit_length() for z in x)
        out=max(z.bit_length() for row in h for z in row)
        out=max(out,max(z.bit_length() for z in X+Y))
        need(out<=4*n*(bits+1),'conservative polynomial-bit control')
        rows.append({'n':n,'input_integer_bits':bits,'N_bits':N.bit_length(),'B_bits':B.bit_length(),'maximum_output_integer_bits':out,'arc_list_expanded':False,'legal_word_simulated':False})
    return rows

def main():
    if '--self-test-invalid' in sys.argv:
        need(False,'intentional control: unconditional exception survives optimized Python')
    out={'schema':1,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS','scope':'fresh finite falsification controls; universal conclusions rely on authored proofs, no historical-code replay','reduction':test_reduction(),'relay_and_signed':test_relays_and_offsets(),'alternate_target_counts':test_late_counts(),'invalid_variants':test_faults(),'large_binary_construction':test_binary_size()}
    print(json.dumps(out,indent=2))
if __name__=='__main__':main()
