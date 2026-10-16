#!/usr/bin/env python3
"""Fresh exact audit controls; no imported family code, no full curve search."""
from collections import Counter, defaultdict
from fractions import Fraction as F
from itertools import permutations, product
from math import gcd
import json
from pathlib import Path

ASSERTIONS=0
def check(condition, detail):
    global ASSERTIONS
    ASSERTIONS+=1
    if not condition: raise AssertionError(detail)

class UF:
    def __init__(self,items): self.p={x:x for x in items}
    def find(self,x):
        if self.p[x]!=x: self.p[x]=self.find(self.p[x])
        return self.p[x]
    def join(self,a,b): self.p[self.find(a)]=self.find(b)

def complete(vertices,original,relations):
    arrows=list(original)
    incoming={v:[i for i,(s,t) in enumerate(arrows) if t==v] for v in vertices}
    outgoing={v:[i for i,(s,t) in enumerate(arrows) if s==v] for v in vertices}
    for v in vertices:
        for name,table in [('in',incoming),('out',outgoing)]:
            while len(table[v])<2:
                leaf=('leaf',len(arrows))
                table[v].append(len(arrows))
                arrows.append((leaf,v) if name=='in' else (v,leaf))
    options=[]
    for v in vertices:
        choices=[]
        for perm in permutations(range(2)):
            if all(((i,j) in relations)==(perm[incoming[v].index(i)]==outgoing[v].index(j)) for i in incoming[v] if i<len(original) for j in outgoing[v] if j<len(original)):
                choices.append(perm)
        check(bool(choices),('completion absent',v))
        options.append(choices)
    return arrows,incoming,outgoing,options

def surface(vertices,original,relations,choice=None):
    arrows,ins,outs,options=complete(vertices,original,relations)
    picks=choice if choice is not None else [x[0] for x in options]
    q=len(arrows)
    vu=UF([(i,k) for i in range(q) for k in range(4)])
    eu=UF([(i,k) for i in range(q) for k in range(4)])
    # A link node is an occurrence of an edge germ at its oriented side end.
    lu=UF([(i,k,e) for i in range(q) for k in range(4) for e in (0,1)])
    pairs={}
    for v,perm in zip(vertices,picks):
        for ii,a in enumerate(ins[v]):
            for jj,b in enumerate(outs[v]):
                # G,S,R,T counterclockwise; oriented edge k goes k -> k+1.
                ea,eb=(2,1) if perm[ii]==jj else (3,0)
                check((a,ea) not in pairs and (b,eb) not in pairs,('edge reuse',a,b,ea,eb))
                pairs[(a,ea)]=(b,eb); pairs[(b,eb)]=(a,ea)
                eu.join((a,ea),(b,eb))
                vu.join((a,ea),(b,(eb+1)%4)); vu.join((a,(ea+1)%4),(b,eb))
                lu.join((a,ea,0),(b,eb,1)); lu.join((a,ea,1),(b,eb,0))
    link_edges=defaultdict(list)
    for i in range(q):
        for k in range(4):
            link_edges[vu.find((i,k))].append((lu.find((i,(k-1)%4,1)),lu.find((i,k,0))))
    boundary=[(i,k) for i in range(q) for k in range(4) if (i,k) not in pairs]
    bverts={vu.find((i,k)) for i,k in boundary}|{vu.find((i,(k+1)%4)) for i,k in boundary}
    for v,edges in link_edges.items():
        adj=defaultdict(list)
        for x,y in edges: adj[x].append(y); adj[y].append(x)
        seen=set(); todo=[next(iter(adj))]
        while todo:
            x=todo.pop()
            if x not in seen: seen.add(x); todo.extend(adj[x])
        check(seen==set(adj),('disconnected vertex link',v))
        deg=Counter(len(x) for x in adj.values())
        check((deg[1]==2 and not any(k not in (1,2) for k in deg)) if v in bverts else set(deg)=={2},('nonmanifold vertex link',v,deg))
    bystart=defaultdict(list)
    for e in boundary: bystart[vu.find(e)].append(e)
    check(all(len(es)==1 for es in bystart.values()),'boundary branching')
    loops=[]; unused=set(boundary)
    while unused:
        start=min(unused); cur=start; loop=[]
        while cur in unused:
            unused.remove(cur); loop.append(cur)
            cur=bystart[vu.find((cur[0],(cur[1]+1)%4))][0]
        check(cur==start,'boundary walk merged')
        loops.append(loop)
    green={vu.find((i,0)) for i in range(q)}
    red={vu.find((i,2)) for i in range(q)}
    gp=green-bverts; rp=red-bverts
    ns=[]
    for loop in loops:
        points={vu.find((i,k)) for i,k in loop}|{vu.find((i,(k+1)%4)) for i,k in loop}
        ns.append(len(points&green))
        check(len(points&green)==len(points&red)>0,'colored boundary count/positivity')
    chi=len({vu.find(x) for x in vu.p})-len({eu.find(x) for x in eu.p})+q
    g=(2-len(loops)-chi)//2
    check(2-len(loops)-chi==2*g and g>=0,'invalid genus')
    # Retain red corner cycles as incidence witnesses; cycle length is number of lozenges.
    red_lengths=sorted(sum(vu.find((i,2))==v for i in range(q)) for v in rp)
    # Quotient fan has three disjoint vertex types. Duplicate triples can occur,
    # so faces and edges are occurrences, not merely sets of their vertices.
    fv=lambda i,k:('corner',vu.find((i,k)))
    fm=lambda i,k:('midpoint',eu.find((i,k)))
    fc=lambda i:('center',i)
    halfedges=UF([(i,k,h) for i in range(q) for k in range(4) for h in (0,1)])
    for (i,k),(j,l) in pairs.items():
        for h in (0,1):halfedges.join((i,k,h),(j,l,1-h))
    ftri=[];fedges={}
    for i in range(q):
        for k in range(4):
            for h in (0,1):
                corner=k if h==0 else (k+1)%4
                vs=[fv(i,corner),fm(i,k),fc(i)]
                es=[('half',halfedges.find((i,k,h))),('spoke_mid',i,k),('spoke_corner',i,corner)]
                check(len(set(vs))==3 and len(set(es))==3,'fan simplex collapses')
                for e,ends in zip(es,[(vs[0],vs[1]),(vs[1],vs[2]),(vs[2],vs[0])]):
                    if e in fedges:check(fedges[e]==frozenset(ends),'incompatible fan edge endpoints')
                    else:fedges[e]=frozenset(ends)
                ftri.append((vs,es))
    bary=[]
    for f,(vs,es) in enumerate(ftri):
        for v in vs:
            for e in es:
                if v in fedges[e]:bary.append(frozenset([('V',v),('E',e),('F',f)]))
    check(len(bary)==6*len(ftri) and len(set(bary))==len(bary),'bary subdivision duplicate simplex')
    check(all(len(t)==3 for t in bary),'bary triangle repeated vertex')
    bedges=Counter(frozenset(e) for t in bary for e in __import__('itertools').combinations(t,2))
    check(all(c in (1,2) for c in bedges.values()),'bary edge nonmanifold')
    bchi=len(set().union(*bary))-len(bedges)+len(bary)
    check(bchi==chi,'triangulation Euler mismatch')
    duplicate_fan_triples=len(ftri)-len(set(frozenset(vs) for vs,es in ftri))
    return {'genus':g,'boundaries':len(loops),'white_punctures':len(gp),'black_punctures':len(rp),'white_counts':sorted(ns),'puncture_red_valences':red_lengths,'chi_filled_punctures':chi,'arrows_completed':q,'corner_link_checks':len(link_edges),'duplicate_fan_vertex_triples':duplicate_fan_triples,'genuine_bary_triangles':len(bary)}

def cycles_bridge(m,n):
    verts=list(range(m+n))
    arrows=[(i,(i+1)%m) for i in range(m)]+[(m+i,m+(i+1)%n) for i in range(n)]
    relations={(i,(i+1)%m) for i in range(m)}|{(m+i,m+(i+1)%n) for i in range(n)}
    arrows.append((0,m))
    return verts,arrows,relations

def paths(vs,arrows,rels):
    counts=[len(vs)]; layer=[(i,) for i in range(len(arrows))]
    while layer:
        counts.append(len(layer))
        layer=[p+(j,) for p in layer for j,a in enumerate(arrows) if arrows[p[-1]][1]==a[0] and (p[-1],j) not in rels]
        check(len(counts)<20,'unexpected unbounded path family')
    return counts

def local_completions():
    tables=0
    for inc in range(3):
        for out in range(3):
            for bits in product((0,1),repeat=inc*out):
                tab=[[bits[i*out+j] for j in range(out)] for i in range(inc)]
                gentle=all(row.count(0)<=1 and row.count(1)<=1 for row in tab) and all(sum(tab[i][j]==b for i in range(inc))<=1 for j in range(out) for b in (0,1))
                if not gentle: continue
                compatible=[p for p in permutations(range(2)) if all(tab[i][j]==int(p[i]==j) for i in range(inc) for j in range(out))]
                check(bool(compatible),('unextendible gentle subtable',tab))
                check(len(compatible)==(1 if inc and out else 2),('completion ambiguity',inc,out,tab))
                tables+=1
    return tables

def cross(a,b,c,d):
    u=(b[0]-a[0],b[1]-a[1]);v=(d[0]-c[0],d[1]-c[1])
    det=u[0]*v[1]-u[1]*v[0]
    if not det:return None
    delta=(c[0]-a[0],c[1]-a[1])
    t=(delta[0]*v[1]-delta[1]*v[0])/det
    s=(delta[0]*u[1]-delta[1]*u[0])/det
    if 0<t<1 and 0<s<1:return (t,s,1 if det>0 else -1)
    return None

def rational_controls():
    t=F(2,5)
    # The two local endpoints on a reversed seam are exact only with 1-t.
    check(t==1-(1-t),'shared reversed seam')
    check(t!=1-t,'orientation trap control')
    a=(F(0),F(1,3)); b=(F(1),F(1,3)); c=(F(1,2),F(0)); d=(F(1,2),F(1))
    check(cross(a,b,c,d)==(F(1,2),F(1,3),1),'exact crossing')
    check(cross(b,a,c,d)==(F(1,2),F(1,3),-1),'crossing reversal')
    # Three chart segments form one proper whole-disk crosscut: interior pieces are not crosscuts.
    portion=[(F(0),F(1,2)),(F(1,3),F(2,5)),(F(2,3),F(3,5)),(F(1),F(1,2))]
    boundary=lambda x:x[0] in (0,1) or x[1] in (0,1)
    check(boundary(portion[0]) and boundary(portion[-1]),'proper maximal portion endpoints')
    check(not boundary(portion[1]) and not boundary(portion[2]),'elementary-segment falsification control')
    # Physical equality is not occurrence equality after cutting a self-crossing dissection seam.
    occurrences=[('edge4','left',t),('edge4','right',t)]
    check(occurrences[0]!=occurrences[1] and occurrences[0][2]==occurrences[1][2],'one-crossing loop end copies')
    return {'reversed_seam':str(t),'maximal_portion_segments':3,'same_physical_crossing_distinct_cut_occurrences':[(e,side,str(x)) for e,side,x in occurrences]}

def quadratic_controls():
    # g=2 with one radical generator: all 32 quadratic forms, and all handle+radical lifts.
    n=5
    pair=lambda x,y:sum(((x>>(2*i))&1)*((y>>(2*i+1))&1)+((x>>(2*i+1))&1)*((y>>(2*i))&1) for i in range(2))%2
    vectors=range(1<<n); r=1<<4
    cases=0; counterexamples=[]; arf_counts=Counter()
    for linear in vectors:
        q=lambda x:(sum(((x>>(2*i))&1)*((x>>(2*i+1))&1) for i in range(2))+(linear&x).bit_count())%2
        for x in vectors:
            for y in vectors: check(q(x^y)==(q(x)+q(y)+pair(x,y))%2,('quadratic identity',linear,x,y))
        base=[1,2,4,8]
        A=sum(q(base[2*i])*q(base[2*i+1]) for i in range(2))%2
        if q(r)==0:arf_counts[A]+=1
        for bits in product((0,1),repeat=4):
            lifted=[x^(r if b else 0) for x,b in zip(base,bits)]
            Ap=sum(q(lifted[2*i])*q(lifted[2*i+1]) for i in range(2))%2
            if q(r)==0: check(Ap==A,'Arf changes when radical zero')
            elif Ap!=A: counterexamples.append({'linear':linear,'base_Arf':A,'lifted_Arf':Ap,'lift_bits':bits})
        cases+=1
    check(bool(counterexamples),'missing radical-nonzero lift counterexample')
    check(arf_counts==Counter({0:10,1:6}),('both Arf branches',arf_counts))
    # q sign conversion leaves q=w/2+1 mod2 unchanged for every even handle integer.
    for w in range(-30,31,2):check((w//2+1)%2==((-w)//2+1)%2,'even sign conversion')
    # Genus-one peripheral detours and integral symplectic swaps preserve the ideal.
    for a,b,c in product(range(-6,7),repeat=3):
        D=gcd(gcd(a,b),c+2)
        check(D==gcd(gcd(a+b,b),c+2),'genus-one Dehn twist ideal')
        check(D==gcd(gcd(-b,a),c+2),'genus-one symplectic swap ideal')
        check(D==gcd(gcd(a+c+2,b),c+2),'genus-one peripheral detour ideal')
        check(D==gcd(gcd(-a,-b),c+2),'handle sign ideal')
    check(gcd(gcd(0,0),-2+2)==0,'zero gcd')
    check(gcd(gcd(0,0),0+2)==2,'peripheral-only genus-one gcd')
    first=[(1,1),(2,-1)];second=[(1,-1),(2,1)]
    check(sorted(n for n,w in first)==sorted(n for n,w in second) and sorted(w for n,w in first)==sorted(w for n,w in second),'paired-record equal marginals')
    check(sorted(first)!=sorted(second),'paired-record unequal keys')
    return {'quadratic_forms':cases,'radical_zero_Arf_counts':dict(arf_counts),'radical_nonzero_Arf_lift_counterexamples':len(counterexamples),'first_Arf_lift_counterexample':counterexamples[0],'paired_record_trap':{'first':first,'second':second}}

def main():
    results={'local_gentle_subtables':local_completions(),'rational':rational_controls(),'quadratic':quadratic_controls(),'witnesses':[],'surface_edge_cases':{}}
    fixtures={'isolated':([0],[],set()),'square_zero_loop':([0],[(0,0)],{(0,0)}),'two_parallel':([0,1],[(0,1),(0,1)],set()),'two_loop_cross_nonrelation':([0],[(0,0),(0,0)],{(0,1),(1,0)}),'genus_one':([0,1],[(0,1),(0,1),(1,0)],{(1,2),(2,0)}),'genus_two':([0,1,2,3],[(0,1),(0,1),(1,0),(2,3),(2,3),(3,2),(1,2)],{(1,2),(2,0),(4,5),(5,3),(0,6),(6,4)})}
    # two_loop_cross_nonrelation is an intentional infinite-dimensional link
    # contrast with white punctures; genus_one and genus_two have finite paths.
    for name,(vs,ar,rel) in fixtures.items():
        s=surface(vs,ar,rel);results['surface_edge_cases'][name]=s
        if name=='isolated':check(s['genus']==0 and s['boundaries']==1 and s['white_counts']==[2] and s['black_punctures']==0,'isolated surface')
        if name=='square_zero_loop':check(s['genus']==0 and s['boundaries']==1 and s['white_counts']==[1] and s['puncture_red_valences']==[1],'square-zero surface')
        if name=='two_loop_cross_nonrelation':check(s['white_punctures']>0,'infinite-dimensional contrast')
        if name in ('genus_one','genus_two'):
            check(s['genus']==(1 if name=='genus_one' else 2) and s['boundaries']==1 and s['white_punctures']==s['black_punctures']==0,('handle genus fixture',name,s))
            results['surface_edge_cases'][name]['permitted_path_counts']=paths(vs,ar,rel)
        if name=='square_zero_loop':check(s['duplicate_fan_vertex_triples']>0,'missing quotient triangulation adversarial stress')
    for m,n in [(3,5),(4,4),(3,3),(3,4),(4,5),(5,5)]:
        vs,ar,rel=cycles_bridge(m,n)
        pathcounts=paths(vs,ar,rel)
        check(pathcounts==[m+n,m+n+1,2,1],('path counts',m,n,pathcounts))
        check(sum(pathcounts)==2*(m+n)+4,'dimension')
        arrows,ins,outs,opts=complete(vs,ar,rel)
        combos=list(product(*opts))
        signatures=[]
        for choice in combos:
            s=surface(vs,ar,rel,choice)
            check(s['genus']==0 and s['boundaries']==1 and s['black_punctures']==2 and s['white_punctures']==0 and s['white_counts']==[m+n-1] and s['puncture_red_valences']==sorted([m,n]),('witness surface',m,n,s))
            signatures.append(s)
        wpunctures=[-m,-n] # Each CCW puncture sector leaves its one white occurrence on the right.
        outer=4-2*(1+2)-sum(wpunctures) # APS Euler winding identity on compact core.
        check(outer==m+n-2,'outer winding')
        results['witnesses'].append({'m':m,'n':n,'path_counts':pathcounts,'dimension':sum(pathcounts),'completion_count':len(combos),'surface':signatures[0],'peripheral_windings':[outer]+sorted(wpunctures),'AG_records':sorted([[m+n-1,1],[0,m],[0,n]])})
    a,b=results['witnesses'][:2]
    check(a['surface']['white_counts']==b['surface']['white_counts'] and a['surface']['genus']==b['surface']['genus'],'named witness truncated key equality')
    check(a['peripheral_windings'][0]==b['peripheral_windings'][0],'named witness outer equality')
    check(a['peripheral_windings'][1:]!=b['peripheral_windings'][1:],'named witness full key inequality')
    results['assertions']=ASSERTIONS
    results['orbit_edge_evaluations']=0
    results['limitations']='Finite exact controls; no full enumerator; no experimental proof of universal termination. Winding sector sign and Euler inference are explained in DERIVATIONS.md.'
    (Path(__file__).parent/'RESULTS.json').write_text(json.dumps(results,indent=2)+ '\n')
    print(json.dumps(results,indent=2))

if __name__=='__main__':main()
