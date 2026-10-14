#!/usr/bin/env python3
"""Independent rational NVB/geometry controls; explicit checks survive python -O.

No external modules; no imports or execution of the author's checker.
Finite controls supplement the universal derivations in REVIEW.md.
"""
from fractions import Fraction as F
from collections import defaultdict
from bisect import bisect_right
from pathlib import Path
from datetime import datetime, timezone
from hashlib import sha256
import argparse
import json
import random
import sys

checks = 0
negatives = []

def require(condition, message):
    global checks
    checks += 1
    if not condition:
        raise ValueError(message)

def negative(name, fn):
    try:
        fn()
    except ValueError as exc:
        negatives.append({'name':name, 'detected':True, 'reason':str(exc)})
    else:
        raise ValueError('Negative control escaped: '+name)

def pt(x,y): return (F(x), F(y))
def edge(a,b): return tuple(sorted((a,b)))
def mid(a,b): return ((a[0]+b[0])/2,(a[1]+b[1])/2)
def sub(a,b): return (a[0]-b[0],a[1]-b[1])
def dot(a,b): return a[0]*b[0]+a[1]*b[1]
def cross(a,b): return a[0]*b[1]-a[1]*b[0]
def area(v): return abs(cross(sub(v[1],v[0]),sub(v[2],v[0])))/2

class Forest:
    def __init__(self):
        self.nodes = {}
        corners=[pt(0,0),pt(1,0),pt(1,1),pt(0,1)]
        c=pt(F(1,2),F(1,2))
        for r in range(4):
            a,b=corners[r],corners[(r+1)%4]
            self.nodes[(r,'')] = ((a,b,c),{edge(a,b):0,edge(a,c):1,edge(b,c):1})
        self.roots=set(self.nodes)

    def split(self,k):
        v,l=self.nodes[k]
        vals=sorted(l.values())
        require(vals==[vals[0],vals[0]+1,vals[0]+1], 'Invalid newest-vertex label pattern')
        reference=min(l,key=l.get); a,b=reference; c=next(p for p in v if p not in reference)
        m=mid(a,b); i=l[reference]
        childkeys=((k[0],k[1]+'0'),(k[0],k[1]+'1'))
        kids=[((c,a,m),{edge(c,a):i+1,edge(a,m):i+2,edge(c,m):i+2}),
              ((c,m,b),{edge(c,b):i+1,edge(m,b):i+2,edge(c,m):i+2})]
        require(sum(area(w) for w,ll in kids)==area(v), 'Bisection area not conserved')
        for key,kid in zip(childkeys,kids):
            if key in self.nodes:
                require(self.nodes[key]==kid,'Same master-forest address has inconsistent geometry')
            else: self.nodes[key]=kid
        return childkeys

    def refine(self,leaves,keys):
        out=set(leaves)
        for key in sorted(keys):
            require(key in out,'Refining a nonleaf')
            out.remove(key); out.update(self.split(key))
        return out

def square_patterns(box):
    x,y,h=box; corners=[(x,y),(x+h,y),(x+h,y+h),(x,y+h)]
    c=(x+h/2,y+h/2)
    return {frozenset((corners[r],corners[(r+1)%4],c)) for r in range(4)}

def quadrants(box):
    x,y,h=box; hh=h/2
    return [(x,y,hh),(x+hh,y,hh),(x+hh,y+hh,hh),(x,y+hh,hh)]

def inspect_square(forest,keys,box,depth):
    require({frozenset(forest.nodes[k][0]) for k in keys}==square_patterns(box),'Square base pattern mismatch')
    x,y,h=box; c=(x+h/2,y+h/2)
    for k in keys:
        v,l=forest.nodes[k]
        for e,i in l.items():
            require(i==2*depth+(1 if c in e else 0),'Square labels are not the shifted initial labels')

def split_square(forest,leaves,keys,box,depth):
    inspect_square(forest,keys,box,depth)
    first={child for k in keys for child in forest.split(k)}
    second={child for k in first for child in forest.split(k)}
    leaves=(leaves-set(keys))|second
    q=[]
    for b in quadrants(box):
        geometry=square_patterns(b)
        ks={k for k in second if frozenset(forest.nodes[k][0]) in geometry}
        inspect_square(forest,ks,b,depth+1)
        q.append((ks,b,depth+1))
    require(len(second)==16 and len(first)==8, 'Two-generation cycle must use twelve bisections')
    return leaves,q

def construct(n):
    f=Forest(); leaves=set(f.roots)
    squares={'':(set(f.roots),(F(0),F(0),F(1)),0)}
    split_squares=set()
    def split_at(address):
        nonlocal leaves
        ks,box,depth=squares.pop(address)
        leaves,qs=split_square(f,leaves,ks,box,depth)
        split_squares.add(address)
        for suffix,q in zip('0123',qs): squares[address+suffix]=q
    def fill(address,levels):
        if levels:
            split_at(address)
            for suffix in '0123': fill(address+suffix,levels-1)
    for j in range(1,n+1):
        spine='0'*(j-1)
        if spine in squares: split_at(spine)
        address=spine+'1'
        box=squares[address][1]
        require(box==(F(1,2**j),F(0),F(1,2**j)),'Q_j dyadic address mismatch')
        fill(address,j)
    expected=F(16,3)*4**n+8*n-F(4,3)
    require(len(leaves)==expected,'Adaptive exact leaf count mismatch')
    require(len(leaves)<=7*4**n,'Adaptive leaf count exceeded explicit bound')
    require(len(split_squares)==n+sum((4**j-1)//3 for j in range(1,n+1)),'Quadtree split count mismatch')
    return f,leaves

def line_interval(e):
    a,b=e; dx=b[0]-a[0];dy=b[1]-a[1]
    if dx==0: return ('v',a[0]),(a[1],b[1])
    slope=dy/dx
    return ('s',slope,a[1]-slope*a[0]),(a[0],b[0])

def edges_of(f,leaves):
    edges=defaultdict(list)
    for k in leaves:
        for e,i in f.nodes[k][1].items():edges[e].append((k,i))
    return edges

def hanging_owners(f,leaves):
    groups=defaultdict(set); all_edges=edges_of(f,leaves)
    for e in all_edges:
        line,interval=line_interval(e);groups[line].update(interval)
    groups={line:sorted(points) for line,points in groups.items()}
    owners=set()
    for e,occ in all_edges.items():
        line,(a,b)=line_interval(e)
        vertices=groups[line]
        i=bisect_right(vertices,a)
        if i<len(vertices) and vertices[i]<b: owners.update(k for k,label in occ)
    return owners

def complete(f,leaves):
    rounds=0; costs=[]
    while True:
        marked=hanging_owners(f,leaves)
        if not marked: break
        costs.append(len(marked));leaves=f.refine(leaves,marked);rounds+=1
        require(rounds<100,'Closure did not terminate in the control')
    return leaves,costs

def boundary(e):
    a,b=e
    return any(a[i]==b[i]==z for i in (0,1) for z in (0,1))

def conforming_check(f,leaves):
    require(not hanging_owners(f,leaves),'Hanging vertices remain')
    require(sum(area(f.nodes[k][0]) for k in leaves)==1,'Mesh area mismatch')
    es=edges_of(f,leaves)
    for e,occ in es.items():
        require(len(occ)==(1 if boundary(e) else 2),'Interior/boundary edge multiplicity mismatch')
        require(len({i for k,i in occ})==1,'Adjacent exact-edge labels inconsistent')
    for k in leaves:
        v,l=f.nodes[k]
        d=sorted(dot(sub(a,b),sub(a,b)) for a,b in l)
        require(d[0]==d[1] and d[2]==2*d[0],'Loss of right-isosceles shape regularity')
        require(d[2]/area(v)==4,'Dimensionless mesh shape constant mismatch')
    require(len(es)<=3*len(leaves),'Edge counting bound failed')
    return es

def value(p,n):
    x,y=p
    for j in range(1,n+1):
        qx=F(1,2**j);side=qx;h=F(1,4**j)
        if qx<=x<=qx+side and 0<=y<=side:
            tx=(x-qx)%h;ty=y%h
            return h-2*max(abs(tx-h/2),abs(ty-h/2))
    return F(0)

def gradient(v,n):
    a,b,c=v;ab=sub(b,a);ac=sub(c,a)
    d=cross(ab,ac); vb=value(b,n)-value(a,n);vc=value(c,n)-value(a,n)
    return ((vb*ac[1]-vc*ab[1])/d,(ab[0]*vc-ac[0]*vb)/d)

def energy_check(f,leaves,n):
    grads={k:gradient(f.nodes[k][0],n) for k in leaves}
    energy=F(0)
    for k,g in grads.items():
        v,l=f.nodes[k];a=v[0]
        probes=[mid(*e) for e in l]+[(sum(p[0] for p in v)/3,sum(p[1] for p in v)/3)]
        for p in probes:require(value(p,n)==value(a,n)+dot(g,sub(p,a)),'V_n not affine on a mesh triangle')
        energy+=dot(g,g)*area(v)
    require(energy==F(4,3)*(1-F(1,4**n)),'Exact finite energy mismatch')
    require(energy+F(4,3*4**n)==F(4,3),'Infinite tail mismatch')
    return grads,energy

def selected_check(f,leaves,n,omit=False,corrupt=False):
    es=edges_of(f,leaves);grads,energy=energy_check(f,leaves,n)
    groups=defaultdict(list)
    for e,occ in es.items():
        line,interval=line_interval(e)
        if line[0]=='s' and line[1]==1:groups[line[2]].append((interval,e,occ))
    used=set();m_total=0;segments=0;weighted=F(0);edge_square_sum=F(0)
    dropped=False
    for j in range(1,n+1):
        qx=F(1,2**j);h=F(1,4**j)
        for iy in range(2**j):
            for ix in range(2**j):
                a=(qx+ix*h,iy*h);b=(a[0]+h/2,a[1]+h/2)
                chain=[(interval,e,occ) for interval,e,occ in groups[a[1]-a[0]] if a[0]<=interval[0] and interval[1]<=b[0]]
                chain.sort()
                if omit and not dropped:chain=chain[1:];dropped=True
                require(bool(chain),'Selected segment has no fine-edge cover')
                require(chain[0][0][0]==a[0] and chain[-1][0][1]==b[0], 'Selected segment endpoint missing')
                for left,right in zip(chain,chain[1:]):require(left[0][1]==right[0][0],'Gap/overlap in selected fine-edge chain')
                local_sum=F(0)
                for interval,e,occ in chain:
                    require(e not in used,'Selected segments share a fine edge')
                    used.add(e);require(len(occ)==2 and not boundary(e),'Selected segment contains a noninterior edge')
                    jump=sub(grads[occ[0][0]],grads[occ[1][0]])
                    if corrupt:jump=(F(0),F(0))
                    require(dot(jump,sub(e[1],e[0]))==0,'Tangential gradient continuity failed')
                    require(dot(jump,jump)==8,'Selected jump squared is not eight')
                    length2=dot(sub(e[1],e[0]),sub(e[1],e[0]))
                    local_sum+=8*length2
                m=len(chain);require(local_sum>=4*h*h/m,'First segment allocation inequality failed')
                segments+=1;m_total+=m;weighted+=2*h;edge_square_sum+=local_sum
    require(segments==sum(4**j for j in range(1,n+1)),'Selected segment count mismatch')
    require(weighted==2*n,'Weighted jump-length level sum mismatch')
    require(m_total==len(used) and m_total<=3*len(leaves),'Distinct selected fine-edge count failed')
    require(edge_square_sum>=F(4*n*n,m_total),'Second allocation inequality failed')
    return {'segments':segments,'fine_edges':m_total,'weighted_jump_length':str(weighted),'jump_length_square_sum':str(edge_square_sum),'allocation_lower_bound':str(F(4*n*n,m_total))}

def ancestors(leaves):
    return {(r,p[:i]) for r,p in leaves for i in range(len(p))}

def overlay(f,a,b):
    internal=ancestors(a)|ancestors(b);leaves=set();todo=list(f.roots)
    while todo:
        k=todo.pop()
        if k in internal:todo.extend(f.split(k))
        else:leaves.add(k)
    require(len(leaves)==4+len(internal),'Binary-forest leaf identity failed')
    require(len(leaves)<=len(a)+len(b)-4,'Overlay cardinality failed')
    return leaves

def old_owner(k,old):
    r,p=k
    candidates=[(r,p[:i]) for i in range(len(p)+1) if (r,p[:i]) in old]
    require(len(candidates)==1,'Overlay is not a common refinement')
    return candidates[0]

def coefficient_check(f,old,fine,wrong=False):
    sums=defaultdict(lambda:F(0));old_coeff={k:F((-1)**i*(10**30+i+1),i+1) for i,k in enumerate(sorted(old))}
    old_integral=sum(old_coeff[k]*area(f.nodes[k][0]) for k in old)
    fine_integral=F(0)
    for k in fine:
        owner=old_owner(k,old);a=area(f.nodes[k][0]);sums[owner]+=a
        coeff=old_coeff[owner]+(1 if wrong else 0)
        require(coeff==old_coeff[owner],'P_0 coefficient was not transferred unchanged')
        fine_integral+=coeff*a
    require(all(sums[k]==area(f.nodes[k][0]) for k in old),'Overlay descendants do not cover old elements')
    require(old_integral==fine_integral,'Piecewise constant integral changed under overlay')

def disjoint_boxes(boxes):
    for i,(x,y,h) in enumerate(boxes):
        for X,Y,H in boxes[i+1:]:
            require(min(x+h,X+H)<=max(x,X) or min(y+h,Y+H)<=max(y,Y),'Positive-area square overlap')

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',default='exact_mesh_results.json');args=ap.parse_args()
    start=datetime.now(timezone.utc).isoformat();rows=[];overlay_rows=[]
    disjoint_boxes([(F(1,2**j),F(0),F(1,2**j)) for j in range(1,41)])
    negative('nested-square replacement loses orthogonal supports',lambda:disjoint_boxes([(F(0),F(0),F(1,2**j)) for j in range(1,5)]))
    for n in range(1,6):
        f,raw=construct(n);unclosed=len(raw)
        if n==2:negative('omitted conforming completion',lambda:conforming_check(f,raw))
        closed,costs=complete(f,raw);es=conforming_check(f,closed)
        grads,energy=energy_check(f,closed,n);sel=selected_check(f,closed,n)
        rows.append({'n':n,'raw_triangles':unclosed,'conforming_triangles':len(closed),'closure_markings':costs,'triangles_over_4n':str(F(len(closed),4**n)),'exact_energy':str(energy),**sel})
        if n<=3:
            for seed in range(4):
                rng=random.Random(991+n*10+seed);other=set(f.roots)
                for it in range(12+5*seed):other=f.refine(other,{rng.choice(sorted(other))})
                other,c=complete(f,other);conforming_check(f,other)
                both=overlay(f,closed,other);conforming_check(f,both)
                coefficient_check(f,other,both);energy_check(f,both,n);selected_check(f,both,n)
                overlay_rows.append({'n':n,'seed':seed,'first_triangles':len(closed),'second_triangles':len(other),'overlay_triangles':len(both),'upper_bound':len(closed)+len(other)-4})
                if n==1 and seed==0:
                    negative('coarsening masquerades as common refinement',lambda:coefficient_check(f,closed,set(f.roots)))
                    negative('changed arbitrary P_0 coefficients',lambda:coefficient_check(f,other,both,wrong=True))
                    negative('missing selected fine-edge cover',lambda:selected_check(f,both,n,omit=True))
                    negative('zeroed selected jump',lambda:selected_check(f,both,n,corrupt=True))
    broken=Forest();k=sorted(broken.roots)[0];v,l=broken.nodes[k];broken.nodes[k]=(v,{e:0 for e in l})
    negative('incompatible newest-vertex labels',lambda:broken.split(k))
    require(len(negatives)==7,'Negative-control receipt count mismatch')
    result={'status':'PASS','started_at_utc':start,'finished_at_utc':datetime.now(timezone.utc).isoformat(),'python_optimization':sys.flags.optimize,'explicit_checks':checks,'script_sha256':sha256(Path(__file__).read_bytes()).hexdigest(),'construction_rows':rows,'overlay_rows':overlay_rows,'negative_controls':negatives,'limits':'Finite exact controls are not all-mesh enumeration. The universal proof and imported completion theorem are separated in REVIEW.md.'}
    Path(args.output).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))

if __name__=='__main__':main()
