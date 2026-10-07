#!/usr/bin/env python3
"""Independent literal reconstructions from USER_REQUEST and Dell Fig. 3 (2010).
No project implementation or manuscript was read. Exact small-instance evidence only.
"""
from functools import lru_cache
import json
from pathlib import Path

def user_dag(w):
    source=("s",0); sink=("t",0); vertices={source,sink}; arcs={(source,sink)}
    bits=bin(w)[3:]
    for i,b in enumerate(bits,1):
        a=("a",i); z=("t",i); vertices.update((a,z))
        arcs.update(((sink,z),(sink,a),(a,z)))
        if b=="1": arcs.add((source,z))
        sink=z
    return source,sink,vertices,arcs

def dell_dag(w):
    # Remove the internal self-loops of Dell's cycle-cover simulator;
    # they become the split identity edges below. Unroll weight 2 as Fig. 3 left.
    k=w.bit_length()-1; source=("z",0); sink=("v",0)
    vertices={source,sink}; arcs=set()
    if w&1: arcs.add((source,sink))
    for j in range(1,k+1):
        z=("z",j); a=("h",j); prev=("z",j-1); vertices.update((z,a))
        arcs.update(((prev,z),(prev,a),(a,z)))
        if (w>>j)&1: arcs.add((z,sink))
    return source,sink,vertices,arcs

def reversal_isomorphism(w):
    s,t,V,E=user_dag(w); k=w.bit_length()-1
    def relabel(x):
        typ,i=x
        return ("v",0) if typ=="s" else (("z",k-i) if typ=="t" else ("h",k-i+1))
    ds,dt,dV,dE=dell_dag(w)
    return relabel(t)==ds and relabel(s)==dt and {relabel(x) for x in V}==dV and {(relabel(y),relabel(x)) for x,y in E}==dE

def split(dag):
    s,t,V,E=dag; internal=V-{s,t}; verts={(s,"L"),(t,"R")}
    verts.update((v,side) for v in internal for side in ("L","R"))
    edges={frozenset(((x,"L"),(y,"R"))) for x,y in E}
    edges.update(frozenset(((v,"L"),(v,"R"))) for v in internal)
    return verts,edges,(s,"L"),(t,"R")

def pm_count(vertices,edges):
    vertices=sorted(vertices,key=str); indices={v:i for i,v in enumerate(vertices)}
    neighbors=[0]*len(vertices)
    for e in edges:
        if not e<=indices.keys(): continue
        x,y=e; i,j=indices[x],indices[y]; neighbors[i]|=1<<j; neighbors[j]|=1<<i
    @lru_cache(None)
    def count(mask):
        if not mask: return 1
        if mask.bit_count()%2: return 0
        active=[i for i in range(len(vertices)) if mask>>i&1]
        i=min(active,key=lambda i:(neighbors[i]&mask).bit_count())
        js=neighbors[i]&mask; total=0
        while js:
            b=js&-js; js-=b
            total+=count(mask^(1<<i)^b)
        return total
    return count((1<<len(vertices))-1)

def signature(w):
    V,E,s,t=split(dell_dag(w))
    return [pm_count(V,E),pm_count(V-{s,t},E),pm_count(V-{s},E),pm_count(V-{t},E)]

if __name__=="__main__":
    rows=[]
    for w in range(1,257):
        sig=signature(w); iso=reversal_isomorphism(w)
        assert sig==[w,1,0,0],(w,sig)
        assert iso,w
        V,E,_,_=split(dell_dag(w))
        rows.append({"W":w,"signature":sig,"exact_reversal_isomorphism":iso,"vertices":len(V),"edges":len(E)})
    out={"source":"Dell–Husfeldt–Wahlén TR10-078 Fig. 3 / USER_REQUEST construction", "tested_W":[1,256],"all_passed":True,"rows":rows}
    Path(__file__).with_name("reconstruction_results.json").write_text(json.dumps(out,indent=2)+"\n")
    print(json.dumps({"tested_W":[1,256],"all_signatures_exact":True,"all_reversal_isomorphisms_exact":True}))
