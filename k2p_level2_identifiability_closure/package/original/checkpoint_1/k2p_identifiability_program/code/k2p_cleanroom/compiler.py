"""Independent graph-to-K2P Fourier compiler.

This module intentionally does not import any supplied graph canonicalizer,
switching engine, descendant-mask code, Fourier compiler, or rank routine.
"""
from __future__ import annotations
from dataclasses import dataclass
from itertools import product
from typing import Any, Dict, Iterable, List, Mapping, Sequence, Tuple
import sympy as sp

GroupElt=int  # 0..3, represented by two bits; addition is XOR.

def gadd(*xs:GroupElt)->GroupElt:
    z=0
    for x in xs:z^=int(x)
    return z

def char(h:GroupElt,x:GroupElt)->int:
    hb=(h&1,(h>>1)&1);xb=(x&1,(x>>1)&1)
    return -1 if ((hb[0]*xb[0]+hb[1]*xb[1])&1) else 1

def edge_eigenvalue(s:Any,g:Any,h:GroupElt)->Any:
    # Convention (1,s,g,s): singleton character 2 carries g.
    return (1,s,g,s)[h]

@dataclass(frozen=True)
class Edge:
    id:str
    tail:str
    head:str
    s:Any
    g:Any

@dataclass
class Network:
    root:str
    leaves:Mapping[str,str]  # taxon -> node
    edges:Sequence[Edge]
    # reticulation node -> list of (incoming edge id, inheritance weight)
    reticulations:Mapping[str,Sequence[Tuple[str,Any]]]

    def validate(self)->None:
        ids=[e.id for e in self.edges]
        if len(ids)!=len(set(ids)):raise ValueError('duplicate edge id')
        byid={e.id:e for e in self.edges}
        incoming:Dict[str,List[str]]={}
        for e in self.edges:incoming.setdefault(e.head,[]).append(e.id)
        for r,opts in self.reticulations.items():
            if len(opts)<2:raise ValueError(f'reticulation {r} has fewer than two parents')
            optids=[x for x,_ in opts]
            if set(optids)!=set(incoming.get(r,[])):raise ValueError(f'reticulation options mismatch at {r}')
            if sp.simplify(sum(w for _,w in opts)-1)!=0:raise ValueError(f'inheritance weights at {r} do not sum to one')
            if any(byid[x].head!=r for x in optids):raise ValueError('wrong reticulation head')
        nodes={self.root,*self.leaves.values()}
        for e in self.edges:nodes|={e.tail,e.head}
        if self.root in {e.head for e in self.edges}:raise ValueError('root has an incoming edge')
        if len(set(self.leaves.values()))!=len(self.leaves):raise ValueError('leaf-node collision')

    @property
    def edge_by_id(self)->Dict[str,Edge]:return {e.id:e for e in self.edges}

    def switchings(self)->Iterable[Tuple[Tuple[str,...],Any]]:
        """Yield selected incoming reticulation edge ids and exact weights."""
        rs=sorted(self.reticulations)
        option_lists=[self.reticulations[r] for r in rs]
        for choices in product(*option_lists):
            selected=tuple(edge_id for edge_id,_ in choices)
            wt=sp.prod(w for _,w in choices)
            yield selected,sp.expand(wt)

    def active_edges(self,selected:Sequence[str])->List[Edge]:
        retic_in={eid for opts in self.reticulations.values() for eid,_ in opts}
        sel=set(selected)
        return [e for e in self.edges if e.id not in retic_in or e.id in sel]

    def descendant_taxa(self,active:Sequence[Edge])->Dict[str,Tuple[str,...]]:
        children:Dict[str,List[Tuple[str,str]]]={}
        indeg:Dict[str,int]={}
        nodes={self.root,*self.leaves.values()}
        for e in active:
            children.setdefault(e.tail,[]).append((e.id,e.head));indeg[e.head]=indeg.get(e.head,0)+1;nodes|={e.tail,e.head}
        if any(v>1 for v in indeg.values()):raise ValueError('switching is not a rooted arborescence')
        # detect cycles and reachability with DFS
        state:Dict[str,int]={};desc_node:Dict[str,set[str]]={}
        leaf_by_node={v:k for k,v in self.leaves.items()}
        def dfs(v:str)->set[str]:
            if state.get(v)==1:raise ValueError('directed cycle')
            if state.get(v)==2:return desc_node[v]
            state[v]=1
            d={leaf_by_node[v]} if v in leaf_by_node else set()
            for _,w in children.get(v,[]):d|=dfs(w)
            state[v]=2;desc_node[v]=d;return d
        reached=dfs(self.root)
        if reached!=set(self.leaves):raise ValueError(f'switching does not reach all leaves: {reached}')
        ans={}
        for e in active:
            ans[e.id]=tuple(sorted(desc_node[e.head]))
        return ans

    def fourier_coordinate(self,assignment:Mapping[str,GroupElt])->Any:
        self.validate()
        taxa=sorted(self.leaves)
        if set(assignment)!=set(taxa):raise ValueError('assignment taxa mismatch')
        if gadd(*(assignment[t] for t in taxa))!=0:return sp.Integer(0)
        total=0
        for selected,wt in self.switchings():
            active=self.active_edges(selected);desc=self.descendant_taxa(active)
            mon=wt
            for e in active:
                h=gadd(*(assignment[t] for t in desc[e.id]))
                mon*=edge_eigenvalue(e.s,e.g,h)
            total+=mon
        return sp.factor(total)

    def fourier_tensor(self)->Dict[Tuple[GroupElt,...],Any]:
        taxa=sorted(self.leaves)
        return {a:self.fourier_coordinate(dict(zip(taxa,a))) for a in product(range(4),repeat=len(taxa))}

    def pattern_tensor(self)->Dict[Tuple[GroupElt,...],Any]:
        taxa=sorted(self.leaves);q=self.fourier_tensor();n=len(taxa)
        out={}
        for x in product(range(4),repeat=n):
            val=0
            for h,qh in q.items():
                c=1
                for hi,xi in zip(h,x):c*=char(hi,xi)
                val+=c*qh
            out[x]=sp.factor(val/(4**n))
        return out

def exact_jacobian_minor(expressions:Sequence[Any],parameters:Sequence[sp.Symbol],rows:Sequence[int],cols:Sequence[int],subs:Mapping[Any,Any])->Any:
    J=sp.Matrix(expressions).jacobian(parameters)
    M=J.extract(list(rows),list(cols)).subs(subs)
    return sp.factor(M.det())
