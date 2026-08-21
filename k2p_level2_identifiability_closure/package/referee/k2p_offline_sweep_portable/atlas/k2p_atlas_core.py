#!/usr/bin/env python3
from __future__ import annotations
from dataclasses import dataclass
from itertools import product, permutations
from collections import Counter, defaultdict
from functools import lru_cache
import networkx as nx

# Exact directed core templates in the order certified by the JC primitive theorem.
CORES = {
    'cycle': {
        'arcs': (('S','X'),('S','X')),
        'retics': ('X',),
        'sinks': ('X',),
        'repairs': ((0,), (1,)),
    },
    'theta0': {
        'arcs': (('S','U'),('S','V'),('U','X'),('V','X'),('U','V')),
        'retics': ('V','X'),
        'sinks': ('X',),
        'repairs': ((2,3),(3,4)),
    },
    'theta1': {
        'arcs': (('S','U'),('S','X'),('V','X'),('U','V'),('U','V')),
        'retics': ('V','X'),
        'sinks': ('X',),
        'repairs': ((2,3),(2,4)),
    },
    'theta2': {
        'arcs': (('S','U'),('S','V'),('U','X0'),('V','X0'),('U','X1'),('V','X1')),
        'retics': ('X0','X1'),
        'sinks': ('X0','X1'),
        'repairs': ((2,3),(2,5),(3,4),(4,5)),
    },
    'theta3': {
        'arcs': (('S','U'),('S','X0'),('V','X0'),('U','X1'),('V','X1'),('U','V')),
        'retics': ('X0','X1'),
        'sinks': ('X0','X1'),
        'repairs': ((2,),(4,)),
    },
}


def weak_compositions(total:int,bins:int):
    if bins==1:
        yield (total,); return
    for first in range(total+1):
        for rest in weak_compositions(total-first,bins-1):
            yield (first,)+rest

@dataclass(frozen=True)
class ModelRecord:
    core_id: str
    incoming_selected: bool
    repair_index: int|None
    selected_sink_mask: int
    words: tuple[tuple[object,...],...]
    graph: nx.DiGraph
    selected_labels: tuple[int,...]
    dummy_labels: tuple[str,...]
    source_support: bool=False
    extra_count: int=0


def build_graph(core_id:str, words:tuple[tuple[object,...],...], sink_labels:dict[str,object], incoming_label:object):
    spec=CORES[core_id]; arcs=spec['arcs']
    G=nx.DiGraph(core_id=core_id)
    # Distinct node for each repeated segment subdivision; core nodes shared.
    for n in {x for e in arcs for x in e}:
        G.add_node(('core',n), role=('retic' if n in spec['retics'] else 'tree'), label=None, dummy=False)
    root=('root',); lin=('leaf','INCOMING')
    G.add_node(root,role='root',label=None,dummy=False)
    G.add_node(lin,role='leaf',label=incoming_label if isinstance(incoming_label,int) else None,dummy=not isinstance(incoming_label,int),dummy_name=None if isinstance(incoming_label,int) else str(incoming_label))
    G.add_edge(root,('core','S'),edge_role='incoming_core')
    G.add_edge(root,lin,edge_role='incoming_arm')
    for i,((tail,head),word) in enumerate(zip(arcs,words)):
        prev=('core',tail)
        for j,label in enumerate(word):
            p=('sub',i,j); leaf=('leaf','seg',i,j)
            G.add_node(p,role='tree',label=None,dummy=False)
            sel=isinstance(label,int)
            G.add_node(leaf,role='leaf',label=label if sel else None,dummy=not sel,dummy_name=None if sel else str(label))
            G.add_edge(prev,p,edge_role=f'seg{i}')
            G.add_edge(p,leaf,edge_role='arm')
            prev=p
        G.add_edge(prev,('core',head),edge_role=f'seg{i}')
    for j,sink in enumerate(spec['sinks']):
        label=sink_labels[sink]; leaf=('leaf','sink',j)
        sel=isinstance(label,int)
        G.add_node(leaf,role='leaf',label=label if sel else None,dummy=not sel,dummy_name=None if sel else str(label))
        G.add_edge(('core',sink),leaf,edge_role='sink_arm')
    validate_graph(G)
    return G


def validate_graph(G):
    assert nx.is_directed_acyclic_graph(G)
    labels=[]
    for n,d in G.nodes(data=True):
        deg=(G.in_degree(n),G.out_degree(n)); role=d['role']
        if role=='root': assert deg==(0,2),(n,deg)
        elif role=='tree': assert deg==(1,2),(n,deg)
        elif role=='retic': assert deg==(2,1),(n,deg)
        elif role=='leaf': assert deg==(1,0),(n,deg)
        if isinstance(d.get('label'),int): labels.append(d['label'])
    assert len(labels)==len(set(labels))
    # chosen rooted completion tree-child
    for n,d in G.nodes(data=True):
        if d['role']!='leaf':
            assert any(G.nodes[c]['role'] in ('tree','leaf') for c in G.successors(n)),(n,list(G.successors(n)))


def source_supports(core_ids=('theta0','theta1','theta3'), extras=0):
    records=[]
    for core_id in core_ids:
        spec=CORES[core_id]
        for ri,repair in enumerate(spec['repairs']):
            # One selected repair label on each repair segment; all sink children selected.
            base={i:[] for i in range(len(spec['arcs']))}
            labels=[]; nextlab=1 # incoming is label 0
            for pos,arc_idx in enumerate(repair):
                base[arc_idx].append(nextlab); labels.append(nextlab); nextlab+=1
            for extra_assign in product(range(len(spec['arcs'])), repeat=extras):
                words={i:list(v) for i,v in base.items()}
                for arc_idx in extra_assign:
                    words[arc_idx].append(nextlab); labels.append(nextlab); nextlab+=1
                # all within-segment orders for extras and repair roles
                order_choices=[tuple(permutations(words[i])) if words[i] else ((),) for i in range(len(spec['arcs']))]
                for ordered in product(*order_choices):
                    sink_labels={}
                    curr=max([0,*[x for row in ordered for x in row]])+1
                    for sink in spec['sinks']:
                        sink_labels[sink]=curr; labels.append(curr); curr+=1
                    G=build_graph(core_id,tuple(tuple(x) for x in ordered),sink_labels,0)
                    sl=tuple(sorted(d['label'] for _,d in G.nodes(data=True) if isinstance(d.get('label'),int)))
                    records.append(ModelRecord(core_id,True,ri,(1<<len(spec['sinks']))-1,tuple(tuple(x) for x in ordered),G,sl,(),True,extras))
    return records


def target_completions(selected_total:int, incoming_selected:bool):
    """selected_total includes all real tensor boundaries.
    If incoming_selected, one label sits at incoming and selected_total-1 outgoing.
    Otherwise all selected_total sit on outgoing and incoming is a zero-character dummy.
    Generate every sink subset, weak composition, and minimum repair completion.
    Selected positions initially receive labels 0..k-1 deterministically; caller applies permutations.
    """
    records=[]
    for core_id,spec in CORES.items():
        nout=selected_total-1 if incoming_selected else selected_total
        ns=len(spec['sinks'])
        for mask in range(1<<ns):
            selected_sinks=[s for j,s in enumerate(spec['sinks']) if mask>>j&1]
            ordinary=nout-len(selected_sinks)
            if ordinary<0: continue
            for counts in weak_compositions(ordinary,len(spec['arcs'])):
                labs=iter(range(1 if incoming_selected else 0, selected_total))
                selected_words=tuple(tuple(next(labs) for _ in range(c)) for c in counts)
                repairs=((None,()),) if core_id=='cycle' else tuple(enumerate(spec['repairs']))
                for ri,repair in repairs:
                    full=[list(w) for w in selected_words]; dummies=[]
                    for ai in repair:
                        if not full[ai]:
                            dum=f'D_REPAIR_{ri}_{ai}'; full[ai].append(dum); dummies.append(dum)
                    sink_labels={}
                    # sink selected labels continue after ordinary labels according to deterministic iterator
                    # Need reconstruct next available labels.
                    used=[x for row in selected_words for x in row]
                    next_label=(max(used)+1) if used else (1 if incoming_selected else 0)
                    for j,sink in enumerate(spec['sinks']):
                        if mask>>j&1:
                            sink_labels[sink]=next_label; next_label+=1
                        else:
                            dum=f'D_SINK_{j}'; sink_labels[sink]=dum; dummies.append(dum)
                    incoming=0 if incoming_selected else 'INCOMING'
                    if not incoming_selected: dummies.append('INCOMING')
                    G=build_graph(core_id,tuple(tuple(x) for x in full),sink_labels,incoming)
                    sl=tuple(sorted(d['label'] for _,d in G.nodes(data=True) if isinstance(d.get('label'),int)))
                    if sl!=tuple(range(selected_total)):
                        raise AssertionError((core_id,selected_total,incoming_selected,counts,mask,sl))
                    records.append(ModelRecord(core_id,incoming_selected,ri,mask,tuple(tuple(x) for x in full),G,sl,tuple(sorted(dummies))))
    return records


def relabel_record(record:ModelRecord, perm:tuple[int,...]):
    G=record.graph.copy()
    for n,d in G.nodes(data=True):
        if isinstance(d.get('label'),int): d['label']=perm[d['label']]
    return ModelRecord(record.core_id,record.incoming_selected,record.repair_index,record.selected_sink_mask,record.words,G,tuple(sorted(perm)),record.dummy_labels,record.source_support,record.extra_count)


def reticulation_nodes(G):
    return tuple(sorted((n for n,d in G.nodes(data=True) if d['role']=='retic'),key=repr))


def selected_arm_edges(G):
    return { (u,v) for u,v in G.edges() if G.nodes[v]['role']=='leaf' and isinstance(G.nodes[v].get('label'),int) }


def zero_sum_assignments(k:int):
    for prefix in product(range(4),repeat=k-1):
        x=0
        for v in prefix:x^=v
        yield prefix+(x,)


def ct_orbit_rep(chars):
    # swap C=1 and T=3 globally; G=2 fixed
    sw=tuple(3 if x==1 else (1 if x==3 else x) for x in chars)
    return min(tuple(chars),sw)

@lru_cache(maxsize=None)
def orbit_assignments(k:int):
    return tuple(sorted({ct_orbit_rep(c) for c in zero_sum_assignments(k)}))


def descendant_masks_for_switch(G, kept_edges):
    children={n:[] for n in G.nodes()}
    for u,v in kept_edges: children[u].append(v)
    topo=list(nx.topological_sort(nx.edge_subgraph(G,kept_edges).copy()))
    mask={}
    for n in reversed(topo):
        lab=G.nodes[n].get('label')
        m=(1<<lab) if isinstance(lab,int) else 0
        for c in children[n]: m|=mask[c]
        mask[n]=m
    return {(u,v):mask[v] for u,v in kept_edges}


def retic_variants(G):
    ret=reticulation_nodes(G)
    if not ret:
        yield (),(); return
    for order in permutations(ret):
        pls=[tuple(sorted(G.predecessors(r),key=repr)) for r in order]
        for flips in product((0,1),repeat=len(order)):
            yield order,tuple((p[f],p[1-f]) for p,f in zip(pls,flips))


def weight_polynomial(bits):
    # mask of lambda variables -> integer coefficient
    poly={0:1}
    for j,b in enumerate(bits):
        new=defaultdict(int)
        for m,c in poly.items():
            if b:new[m|1<<j]+=c
            else:
                new[m]+=c;new[m|1<<j]-=c
        poly={m:c for m,c in new.items() if c}
    return tuple(sorted(poly.items()))


def sector_for_mask(mask:int,chars):
    x=0;i=0
    while mask:
        if mask&1:x^=chars[i]
        i+=1;mask>>=1
    return 0 if x==0 else (2 if x==2 else 1)

@dataclass(frozen=True)
class MapDescriptor:
    k:int
    retic_count:int
    edge_class_count:int
    outputs:tuple # each output tuple of (monomial, lambda polynomial)
    edge_signatures:tuple


def descriptor_variant(G,ret_order,parent_orders):
    k=len([1 for _,d in G.nodes(data=True) if isinstance(d.get('label'),int)])
    chars_list=orbit_assignments(k)
    all_edges=tuple(G.edges()); arms=selected_arm_edges(G)
    switches=[]
    for bits in product((0,1),repeat=len(ret_order)):
        removed=set()
        for j,r in enumerate(ret_order):
            kp=parent_orders[j][bits[j]]
            for p in G.predecessors(r):
                if p!=kp:removed.add((p,r))
        kept=tuple(e for e in all_edges if e not in removed)
        emask=descendant_masks_for_switch(G,kept)
        switches.append((bits,kept,emask))
    # group only non-arm, tensor-visible edge classes by full switching/character sector signature
    edge_sigs=[]; internal_edges=[]
    for e in all_edges:
        if e in arms: continue
        sig=[]
        for bits,kept,emask in switches:
            if e not in emask: sig.extend((0,)*len(chars_list))
            else: sig.extend(sector_for_mask(emask[e],c) for c in chars_list)
        if any(sig): internal_edges.append(e);edge_sigs.append(tuple(sig))
    active=tuple(sorted(set(edge_sigs)))
    class_of={sig:i for i,sig in enumerate(active)}
    edge_class={e:class_of[s] for e,s in zip(internal_edges,edge_sigs)}
    outputs=[]
    wpol={bits:weight_polynomial(bits) for bits,_,_ in switches}
    for chars in chars_list:
        grouped=defaultdict(lambda:defaultdict(int))
        for bits,kept,emask in switches:
            fac=Counter()
            for e in kept:
                ci=edge_class.get(e)
                if ci is None: continue
                sec=sector_for_mask(emask[e],chars)
                if sec:fac[(ci,sec)]+=1
            mon=tuple(sorted((ci,sec,exp) for (ci,sec),exp in fac.items()))
            for mask,coef in wpol[bits]:grouped[mon][mask]+=coef
        expr=[]
        for mon,poly in grouped.items():
            p=tuple(sorted((m,c) for m,c in poly.items() if c))
            if p:expr.append((mon,p))
        outputs.append(tuple(sorted(expr)))
    return MapDescriptor(k,len(ret_order),len(active),tuple(outputs),active)


def model_descriptor(G):
    variants=[descriptor_variant(G,*v) for v in retic_variants(G)]
    return min(variants,key=lambda d:(d.retic_count,d.edge_class_count,d.outputs,d.edge_signatures))


def eval_descriptor(desc:MapDescriptor, edge_pairs, lambdas):
    from fractions import Fraction
    ans=[]
    for expr in desc.outputs:
        val=Fraction(0)
        for mon,poly in expr:
            mval=Fraction(1)
            for ci,sec,exp in mon:mval*=edge_pairs[ci][sec-1]**exp
            pval=Fraction(0)
            for mask,coef in poly:
                t=Fraction(coef)
                for j,lam in enumerate(lambdas):
                    if mask>>j&1:t*=lam
                pval+=t
            val+=mval*pval
        ans.append(val)
    return tuple(ans)

if __name__=='__main__':
    for k in (4,5):
        ts=target_completions(k,True); tm=target_completions(k,False)
        print(k,len(ts),len(tm))
    for ids in (('theta0','theta1','theta3'),('theta2',)):
        s=source_supports(ids)
        print(ids,len(s),[(r.core_id,r.repair_index,len(r.selected_labels)) for r in s])

# ---------- selected restrictions and published immediate filters ----------
def restrict_rooted(G, keep_labels:set[int]):
    H=G.copy()
    # delete all unselected/dummy leaves
    for n,d in list(H.nodes(data=True)):
        if d['role']=='leaf' and d.get('label') not in keep_labels:
            H.remove_node(n)
    changed=True
    while changed:
        changed=False
        # remove unlabeled dead ends
        for n,d in list(H.nodes(data=True)):
            if H.out_degree(n)==0 and not (d['role']=='leaf' and d.get('label') in keep_labels):
                H.remove_node(n);changed=True;break
        if changed:continue
        # suppress ordinary indegree1/outdegree1
        for n,d in list(H.nodes(data=True)):
            if d['role']!='leaf' and H.in_degree(n)==1 and H.out_degree(n)==1:
                u=next(H.predecessors(n));v=next(H.successors(n));H.remove_node(n)
                if u!=v and not H.has_edge(u,v):H.add_edge(u,v,edge_role='suppressed')
                changed=True;break
        if changed:continue
        # if root unary, delete it and promote child
        roots=[n for n in H if H.in_degree(n)==0]
        if len(roots)==1 and H.nodes[roots[0]]['role']!='leaf' and H.out_degree(roots[0])==1:
            r=roots[0];c=next(H.successors(r));H.remove_node(r);changed=True
    # recompute roles from degrees
    for n,d in H.nodes(data=True):
        if d.get('label') in keep_labels:d['role']='leaf'
        elif H.in_degree(n)==0:d['role']='root'
        elif H.in_degree(n)==2:d['role']='retic'
        else:d['role']='tree'
    return H


def switch_graphs(G):
    ret=[n for n,d in G.nodes(data=True) if d['role']=='retic' and G.in_degree(n)==2]
    ins=[tuple(G.in_edges(r)) for r in ret]
    for choices in product(*ins):
        H=G.copy();keep=set(choices)
        for rows in ins:
            for e in rows:
                if e not in keep:H.remove_edge(*e)
        yield H


def unrooted_restricted_tree(G,keep_labels:set[int]):
    H=restrict_rooted(G,keep_labels)
    U=nx.Graph()
    U.add_nodes_from((n,d.copy()) for n,d in H.nodes(data=True));U.add_edges_from(H.edges())
    changed=True
    while changed:
        changed=False
        for n,d in list(U.nodes(data=True)):
            lab=d.get('label')
            if lab not in keep_labels and U.degree(n)<=1:
                U.remove_node(n);changed=True;break
            if lab not in keep_labels and U.degree(n)==2:
                a,b=list(U.neighbors(n));U.remove_node(n)
                if a!=b:U.add_edge(a,b)
                changed=True;break
    return U


def quartet_splits(G,quad:tuple[int,int,int,int]):
    keep=set(quad);out=set()
    for sw in switch_graphs(G):
        U=unrooted_restricted_tree(sw,keep)
        split=None
        for u,v in list(U.edges()):
            U.remove_edge(u,v);comps=list(nx.connected_components(U));U.add_edge(u,v)
            if len(comps)!=2:continue
            labs=[]
            for C in comps:
                labs.append(frozenset(U.nodes[n].get('label') for n in C if U.nodes[n].get('label') in keep))
            if sorted(map(len,labs))==[2,2]:
                split=tuple(sorted((tuple(sorted(labs[0])),tuple(sorted(labs[1])))))
                break
        out.add(split if split is not None else ('star',))
    return frozenset(out)


def triple_type(G,triple:tuple[int,int,int]):
    H=restrict_rooted(G,set(triple))
    r=sum(1 for n,d in H.nodes(data=True) if d['role']=='retic' and H.in_degree(n)==2)
    if r==0:return 'tree'
    if r==1:return 'sunlet'
    return f'r{r}'


def topology_signature(G):
    labels=tuple(sorted(d['label'] for _,d in G.nodes(data=True) if isinstance(d.get('label'),int)))
    qs=tuple((q,quartet_splits(G,q)) for q in __import__('itertools').combinations(labels,4))
    ts=tuple((t,triple_type(G,t)) for t in __import__('itertools').combinations(labels,3))
    return labels,qs,ts


def permute_signature(sig,perm):
    labels,qs,ts=sig
    def pset(t):return tuple(sorted(perm[x] for x in t))
    newq=[]
    for q,sets in qs:
        mapped=[]
        for s in sets:
            if s==('star',):mapped.append(s)
            else:mapped.append(tuple(sorted((pset(s[0]),pset(s[1])))))
        newq.append((pset(q),frozenset(mapped)))
    newt=[(pset(t),typ) for t,typ in ts]
    return tuple(sorted(newq)),tuple(sorted(newt))


def immediate_compatible(source_sig,target_sig_perm):
    _,sqs,sts=source_sig
    tq,tt=target_sig_perm
    if tuple(sqs)!=tuple(tq):return False,'quartet'
    sm=dict(sts);tm=dict(tt)
    for tr in sm:
        if {sm[tr],tm[tr]}=={'tree','sunlet'}:return False,'tree_sunlet'
    return True,None

def model_descriptor_fast2(G):
    """Same canonical polynomial-map descriptor, but traverses the graph once.
    Canonicalizes the reticulation-variable hyperoctahedral action afterward.
    """
    k=len([1 for _,d in G.nodes(data=True) if isinstance(d.get('label'),int)])
    chars_list=orbit_assignments(k)
    ret=reticulation_nodes(G); r=len(ret)
    parents=tuple(tuple(sorted(G.predecessors(x),key=repr)) for x in ret)
    all_edges=tuple(G.edges());arms=selected_arm_edges(G)
    base_switch=[]
    for bits in product((0,1),repeat=r):
        removed=set()
        for j,node in enumerate(ret):
            kp=parents[j][bits[j]]
            for p in parents[j]:
                if p!=kp:removed.add((p,node))
        kept=tuple(e for e in all_edges if e not in removed)
        emask=descendant_masks_for_switch(G,kept)
        # edge sector rows by output index
        esec={e:tuple(sector_for_mask(emask[e],c) for c in chars_list) for e in kept if e not in arms}
        base_switch.append((bits,kept,esec))
    # group action: new variable j refers to old variable perm[j], with optional complement flip.
    actions=[(p,f) for p in permutations(range(r)) for f in product((0,1),repeat=r)] if r else [((),())]
    variants=[]
    for p,f in actions:
        # For each new bits, determine old bits and retrieve original switch.
        ordered=[]
        for nb in product((0,1),repeat=r):
            ob=[0]*r
            for j in range(r):ob[p[j]]=nb[j]^f[j]
            oi=0
            for bit in ob:oi=(oi<<1)|bit
            ordered.append((nb,base_switch[oi]))
        # edge signatures under this switch order
        sigs=[];iedges=[]
        for e in all_edges:
            if e in arms:continue
            sig=[]
            for nb,(ob,kept,esec) in ordered:
                sig.extend(esec.get(e,(0,)*len(chars_list)))
            if any(sig):iedges.append(e);sigs.append(tuple(sig))
        active=tuple(sorted(set(sigs)));cl={s:i for i,s in enumerate(active)}
        ecl={e:cl[s] for e,s in zip(iedges,sigs)}
        outputs=[]
        for ci in range(len(chars_list)):
            grouped=defaultdict(lambda:defaultdict(int))
            for nb,(ob,kept,esec) in ordered:
                fac=Counter()
                for e in kept:
                    c=ecl.get(e)
                    if c is None:continue
                    sec=esec.get(e,(0,)*len(chars_list))[ci]
                    if sec:fac[(c,sec)]+=1
                mon=tuple(sorted((c,sec,x) for (c,sec),x in fac.items()))
                for mask,coef in weight_polynomial(nb):grouped[mon][mask]+=coef
            expr=[]
            for mon,poly in grouped.items():
                pp=tuple(sorted((m,c) for m,c in poly.items() if c))
                if pp:expr.append((mon,pp))
            outputs.append(tuple(sorted(expr)))
        variants.append(MapDescriptor(k,r,len(active),tuple(outputs),active))
    return min(variants,key=lambda d:(d.retic_count,d.edge_class_count,d.outputs,d.edge_signatures))

# ---------- exact rational Jacobian evaluation and rank certificates ---------
def default_exact_point(desc:MapDescriptor, salt:int=0):
    from fractions import Fraction as F
    edges=[]
    for i in range(desc.edge_class_count):
        # All s<1/2, so g>2s-1 automatically; strictly positive and distinct.
        s=F(2*i+3+salt, 8*i+16+4*salt)
        g=F(3*i+5+salt, 10*i+21+3*salt)
        assert 0<s<1 and 0<g<1 and g>2*s-1
        edges.append((s,g))
    lams=[]
    for j in range(desc.retic_count):
        l=F(j+2+salt, j+5+2*salt)
        assert 0<l<1;lams.append(l)
    return tuple(edges),tuple(lams)


def descriptor_jacobian(desc:MapDescriptor, edge_pairs=None,lambdas=None):
    from fractions import Fraction as F
    if edge_pairs is None:edge_pairs,lambdas=default_exact_point(desc)
    assert lambdas is not None
    p=2*desc.edge_class_count+desc.retic_count
    rows=[]
    for expr in desc.outputs:
        grad=[F(0) for _ in range(p)]
        for mon,poly in expr:
            # edge monomial
            mval=F(1)
            powers={}
            for ci,sec,exp in mon:
                var=2*ci+(sec-1);powers[var]=exp;mval*=edge_pairs[ci][sec-1]**exp
            # lambda polynomial and derivatives
            pval=F(0);pd=[F(0) for _ in lambdas]
            for mask,coef in poly:
                term=F(coef)
                for j,l in enumerate(lambdas):
                    if mask>>j&1:term*=l
                pval+=term
                for j,l in enumerate(lambdas):
                    if mask>>j&1:
                        # l nonzero at chosen point
                        pd[j]+=term/l
            for var,exp in powers.items():
                ci=var//2;sec=var%2
                grad[var]+=mval*pval*exp/edge_pairs[ci][sec]
            for j,x in enumerate(pd):grad[2*desc.edge_class_count+j]+=mval*x
        rows.append(grad)
    return rows


def exact_rank_pivots(matrix):
    from fractions import Fraction as F
    if not matrix:return 0,(),()
    A=[list(map(F,row)) for row in matrix];m=len(A);n=len(A[0]);r=0;pivcols=[];pivrows=[];row_ids=list(range(m))
    for c in range(n):
        q=next((i for i in range(r,m) if A[i][c]),None)
        if q is None:continue
        A[r],A[q]=A[q],A[r];row_ids[r],row_ids[q]=row_ids[q],row_ids[r]
        pv=A[r][c];A[r]=[x/pv for x in A[r]]
        for i in range(m):
            if i!=r and A[i][c]:
                x=A[i][c];A[i]=[a-x*b for a,b in zip(A[i],A[r])]
        pivcols.append(c);pivrows.append(row_ids[r]);r+=1
        if r==m:break
    return r,tuple(pivrows),tuple(pivcols)


def determinant_square(A):
    from fractions import Fraction as F
    A=[list(map(F,row)) for row in A];n=len(A);det=F(1)
    for c in range(n):
        q=next((i for i in range(c,n) if A[i][c]),None)
        if q is None:return F(0)
        if q!=c:A[c],A[q]=A[q],A[c];det=-det
        pv=A[c][c];det*=pv
        for i in range(c+1,n):
            if A[i][c]:
                f=A[i][c]/pv
                for j in range(c+1,n):A[i][j]-=f*A[c][j]
    return det


def rank_certificate(desc:MapDescriptor,salt=0):
    edges,lams=default_exact_point(desc,salt)
    J=descriptor_jacobian(desc,edges,lams)
    rank,rows,cols=exact_rank_pivots(J)
    minor=[[J[i][j] for j in cols] for i in rows]
    det=determinant_square(minor)
    assert (rank==0)==(det==0)
    return {'rank':rank,'rows':rows,'columns':cols,'determinant':str(det),'edge_pairs':tuple((str(a),str(b)) for a,b in edges),'lambdas':tuple(map(str,lams))}

# ---------- multihomogeneous quadratic invariant engine --------------------
def output_sparse_polynomials(desc:MapDescriptor):
    """Return q-coordinate pullbacks as integer sparse polynomials.
    Exponent tuple order: s_0,g_0,...,s_E,g_E,lambda_0,... .
    """
    p=2*desc.edge_class_count+desc.retic_count
    out=[]
    for expr in desc.outputs:
        poly=defaultdict(int)
        for mon,lpoly in expr:
            base=[0]*p
            for ci,sec,exp in mon:base[2*ci+sec-1]+=exp
            for mask,coef in lpoly:
                ex=list(base)
                for j in range(desc.retic_count):
                    if mask>>j&1:ex[2*desc.edge_class_count+j]+=1
                poly[tuple(ex)]+=coef
        out.append({m:c for m,c in poly.items() if c})
    return tuple(out)


def sparse_mul(a,b):
    out=defaultdict(int)
    for ea,ca in a.items():
        for eb,cb in b.items():out[tuple(x+y for x,y in zip(ea,eb))]+=ca*cb
    return {e:c for e,c in out.items() if c}


def sparse_lincomb(polys,coeffs):
    from fractions import Fraction as F
    out=defaultdict(F)
    for p,c in zip(polys,coeffs):
        c=F(c)
        if not c:continue
        for e,v in p.items():out[e]+=c*v
    return {e:c for e,c in out.items() if c}

@lru_cache(maxsize=None)
def coordinate_weights(k:int):
    ans=[]
    for chars in orbit_assignments(k):
        row=[]
        for x in chars:row.extend((1 if x in (1,3) else 0,1 if x==2 else 0))
        ans.append(tuple(row))
    return tuple(ans)

@lru_cache(maxsize=None)
def quadratic_blocks(k:int):
    from itertools import combinations_with_replacement
    ws=coordinate_weights(k);blocks=defaultdict(list)
    for i,j in combinations_with_replacement(range(len(ws)),2):
        w=tuple(a+b for a,b in zip(ws[i],ws[j]));blocks[w].append((i,j))
    return tuple((w,tuple(v)) for w,v in sorted(blocks.items()))


def polynomial_columns_for_block(desc,block,cache=None):
    if cache is None:cache={}
    ops=output_sparse_polynomials(desc)
    vals=[]
    for i,j in block:
        key=(i,j)
        if key not in cache:cache[key]=sparse_mul(ops[i],ops[j])
        vals.append(cache[key])
    return vals


def exact_kernel_sparse_columns(columns):
    """Kernel of matrix whose columns are sparse rational vectors; block <=16."""
    import sympy as sp
    if not columns:return ()
    rows=sorted(set().union(*(c.keys() for c in columns)))
    if not rows:
        # every column zero
        return tuple(tuple(sp.Integer(1) if i==j else sp.Integer(0) for i in range(len(columns))) for j in range(len(columns)))
    rid={e:i for i,e in enumerate(rows)}
    M=sp.MutableSparseMatrix(len(rows),len(columns),{})
    for j,col in enumerate(columns):
        for e,c in col.items():M[rid[e],j]=sp.Rational(c)
    ns=M.nullspace()
    return tuple(tuple(v[i,0] for i in range(len(columns))) for v in ns)


def primitive_integer_vector(vec):
    import sympy as sp, math
    den=1
    for x in vec:den=sp.ilcm(den,sp.denom(x))
    vals=[int(x*den) for x in vec];g=0
    for x in vals:g=math.gcd(g,abs(x))
    if g:vals=[x//g for x in vals]
    first=next((x for x in vals if x),1)
    if first<0:vals=[-x for x in vals]
    return tuple(vals)


def quadratic_separator(source:MapDescriptor,target:MapDescriptor):
    """Return exact multihomogeneous target invariant nonzero on source, or None."""
    assert source.k==target.k
    sops=output_sparse_polynomials(source);tops=output_sparse_polynomials(target)
    smul={};tmul={}
    for weight,block in quadratic_blocks(source.k):
        if len(block)<2:continue
        tc=[];sc=[]
        for ij in block:
            if ij not in tmul:tmul[ij]=sparse_mul(tops[ij[0]],tops[ij[1]])
            if ij not in smul:smul[ij]=sparse_mul(sops[ij[0]],sops[ij[1]])
            tc.append(tmul[ij]);sc.append(smul[ij])
        for vec in exact_kernel_sparse_columns(tc):
            ivec=primitive_integer_vector(vec)
            spull=sparse_lincomb(sc,ivec)
            if spull:
                # exact recheck target zero
                assert not sparse_lincomb(tc,ivec)
                return {'degree':2,'weight':weight,'coordinate_pairs':block,'coefficients':ivec,'source_nonzero_terms':len(spull),'source_witness_term':(next(iter(spull))[0:] if spull else None),'source_pullback':spull}
    return None

# Faster exact kernel implementation for small multihomogeneous blocks.
def proportional_relation(a,b):
    """Return (u,v) nonzero with u*a+v*b=0, else None."""
    from fractions import Fraction as F
    if not a and not b:return (1,0)
    if not a:return (1,0)
    if not b:return (0,1)
    keys=set(a)|set(b)
    ratio=None
    for e in keys:
        x=F(a.get(e,0));y=F(b.get(e,0))
        if x==0 and y==0:continue
        if x==0 or y==0:return None
        r=x/y
        if ratio is None:ratio=r
        elif r!=ratio:return None
    # a = ratio*b => a - ratio b=0
    return primitive_integer_vector((1,-ratio))


def kernel_sparse_columns_fast(columns):
    from fractions import Fraction as F
    n=len(columns)
    if n==0:return ()
    if n==1:return ((1,),) if not columns[0] else ()
    if n==2:
        if not columns[0] and not columns[1]:return ((1,0),(0,1))
        rel=proportional_relation(columns[0],columns[1])
        return (rel,) if rel else ()
    # Collect coefficient rows in Q^n, then compute their row-space RREF.
    byrow=defaultdict(lambda:[F(0) for _ in range(n)])
    for j,col in enumerate(columns):
        for e,c in col.items():byrow[e][j]=F(c)
    basis=[];piv=[]
    for row in byrow.values():
        row=list(row)
        for b,p in zip(basis,piv):
            if row[p]:
                f=row[p]
                row=[x-f*y for x,y in zip(row,b)]
        p=next((j for j,x in enumerate(row) if x),None)
        if p is None:continue
        pv=row[p];row=[x/pv for x in row]
        # eliminate new pivot from existing rows for RREF
        for i,b in enumerate(basis):
            if b[p]:
                f=b[p];basis[i]=[x-f*y for x,y in zip(b,row)]
        # insert ordered by pivot
        idx=0
        while idx<len(piv) and piv[idx]<p:idx+=1
        piv.insert(idx,p);basis.insert(idx,row)
        if len(basis)==n:break
    free=[j for j in range(n) if j not in piv]
    ans=[]
    for f in free:
        v=[F(0) for _ in range(n)];v[f]=F(1)
        for row,p in reversed(list(zip(basis,piv))):
            v[p]=-sum(row[j]*v[j] for j in free)
        ans.append(primitive_integer_vector(v))
    return tuple(ans)

# override quadratic separator with cached/faster implementation
_OUTPUT_POLY_CACHE={}
_QUADRATIC_SOURCE_PRODUCT_CACHE={}
def output_sparse_polynomials_cached(desc):
    val=_OUTPUT_POLY_CACHE.get(desc)
    if val is None:
        val=output_sparse_polynomials(desc);_OUTPUT_POLY_CACHE[desc]=val
    return val

def quadratic_separator_fast(source:MapDescriptor,target:MapDescriptor,max_block_size=16):
    assert source.k==target.k
    # Source products recur for every target in a source lane; target products
    # are class-local.  Persist the former lazily and release the latter after
    # each class so the full target universe is not retained in memory.
    sops=output_sparse_polynomials_cached(source);tops=output_sparse_polynomials(target)
    smul=_QUADRATIC_SOURCE_PRODUCT_CACHE.setdefault(source,{});tmul={}
    blocks=sorted(quadratic_blocks(source.k),key=lambda wb:(len(wb[1]),wb[0]))
    for weight,block in blocks:
        if len(block)<2 or len(block)>max_block_size:continue
        tc=[];sc=[]
        for ij in block:
            if ij not in tmul:tmul[ij]=sparse_mul(tops[ij[0]],tops[ij[1]])
            if ij not in smul:smul[ij]=sparse_mul(sops[ij[0]],sops[ij[1]])
            tc.append(tmul[ij]);sc.append(smul[ij])
        for ivec in kernel_sparse_columns_fast(tc):
            spull=sparse_lincomb(sc,ivec)
            if spull:
                assert not sparse_lincomb(tc,ivec)
                return {'degree':2,'weight':weight,'coordinate_pairs':block,'coefficients':ivec,'source_nonzero_terms':len(spull),'source_pullback':spull}
    return None

# ---------- selected topology and ordinary-triangle relation ---------------
def selected_graph_from_completion(record:ModelRecord):
    return restrict_rooted(record.graph,set(record.selected_labels))


def sd0_mixed(G):
    """Return undirected skeleton with arrowhead flags at endpoints.
    Edge attr heads is frozenset of endpoint nodes carrying retained arrowheads.
    """
    H=G.copy()
    roots=[n for n,d in H.nodes(data=True) if d['role']=='root' or H.in_degree(n)==0]
    if len(roots)!=1:raise ValueError(('roots',roots))
    root=roots[0];children=list(H.successors(root))
    if len(children)!=2:raise ValueError(('root degree',len(children)))
    # Record all edges except root arcs; retic child gives arrowhead at child.
    M=nx.Graph()
    for n,d in H.nodes(data=True):
        if n==root:continue
        M.add_node(n,role=d.get('role'),label=d.get('label'))
    for u,v in H.edges():
        if u==root:continue
        heads=frozenset({v}) if H.nodes[v].get('role')=='retic' else frozenset()
        if M.has_edge(u,v):raise ValueError('parallel')
        M.add_edge(u,v,heads=heads)
    a,b=children
    heads=set()
    if H.nodes[a].get('role')=='retic':heads.add(a)
    if H.nodes[b].get('role')=='retic':heads.add(b)
    if a==b or M.has_edge(a,b):raise ValueError('root suppression not simple')
    M.add_edge(a,b,heads=frozenset(heads))
    return M


def mixed_isomorphic(A,B,ignore_heads_edges=None):
    def nm(x,y):return x.get('label')==y.get('label')
    def em(x,y):return x.get('heads',frozenset())==y.get('heads',frozenset())
    return nx.algorithms.isomorphism.GraphMatcher(A,B,node_match=nm,edge_match=em).is_isomorphic()


def mixed_relation(source_G,target_G):
    try:A=sd0_mixed(source_G);B=sd0_mixed(target_G)
    except ValueError:return 'none'
    def nm(x,y):return x.get('label')==y.get('label')
    def em(x,y):return x.get('heads',frozenset())==y.get('heads',frozenset())
    GM=nx.algorithms.isomorphism.GraphMatcher(A,B,node_match=nm,edge_match=em)
    if GM.is_isomorphic():return 'isomorphic'
    # Underlying labelled graph maps, then test all arrowhead discrepancies lie inside one triangle
    GM=nx.algorithms.isomorphism.GraphMatcher(A,B,node_match=nm)
    for mp in GM.isomorphisms_iter():
        # mp A->B
        dif=[]
        for u,v,d in A.edges(data=True):
            x,y=mp[u],mp[v]
            hb=B.edges[x,y].get('heads',frozenset())
            mapped=frozenset(mp[z] for z in d.get('heads',frozenset()))
            if mapped!=hb:dif.append((frozenset((x,y)),mapped,hb))
        if not dif:continue
        # Find a B triangle containing every discrepant edge; outside identical already.
        triangles=[]
        for cyc in nx.cycle_basis(B):
            if len(cyc)==3:
                es={frozenset((cyc[i],cyc[(i+1)%3])) for i in range(3)};triangles.append(es)
        for es in triangles:
            if all(e in es for e,_,_ in dif):
                # each orientation has exactly two headed triangle edges into one retic vertex
                def ret_vertex(edge_data):
                    hs=[]
                    for e,ma,hb in edge_data:
                        hs.extend(hb)
                    return Counter(hs).most_common(1)[0][0] if hs else None
                return 'triangle'
    return 'none'

# ---------- exact mixed-graph isomorphism via incidence expansion ----------
def mixed_incidence_graph(M, forget_triangle_edges=None):
    H=nx.Graph()
    forget_triangle_edges = set() if forget_triangle_edges is None else {frozenset(e) for e in forget_triangle_edges}
    for v,d in M.nodes(data=True):
        lab=d.get('label')
        H.add_node(('v',v),kind='vertex',label=lab)
    for idx,(u,v,d) in enumerate(M.edges(data=True)):
        en=('e',idx);H.add_node(en,kind='edge',label=None)
        heads=d.get('heads',frozenset())
        forget=frozenset((u,v)) in forget_triangle_edges
        H.add_edge(en,('v',u),head=False if forget else (u in heads))
        H.add_edge(en,('v',v),head=False if forget else (v in heads))
    return H

def mixed_exact_isomorphic(A,B,forget_all_triangle_heads=False):
    if forget_all_triangle_heads:
        def tris(M):
            U=nx.Graph();U.add_nodes_from(M.nodes());U.add_edges_from(M.edges())
            es=set()
            for cyc in nx.enumerate_all_cliques(U):
                if len(cyc)==3:
                    if all(U.has_edge(cyc[i],cyc[(i+1)%3]) for i in range(3)):
                        es|={frozenset((cyc[i],cyc[(i+1)%3])) for i in range(3)}
                elif len(cyc)>3:break
            return es
        IA=mixed_incidence_graph(A,tris(A));IB=mixed_incidence_graph(B,tris(B))
    else:
        IA=mixed_incidence_graph(A);IB=mixed_incidence_graph(B)
    nm=lambda x,y:x.get('kind')==y.get('kind') and x.get('label')==y.get('label')
    em=lambda x,y:x.get('head')==y.get('head')
    return nx.algorithms.isomorphism.GraphMatcher(IA,IB,node_match=nm,edge_match=em).is_isomorphic()

def mixed_relation_exact(source_G,target_G):
    try:A=sd0_mixed(source_G);B=sd0_mixed(target_G)
    except ValueError:return 'none'
    if mixed_exact_isomorphic(A,B):return 'isomorphic'
    # T quotient: exact underlying labelled graph with all heads on one ordinary triangle forgotten.
    # Enumerate one triangle on each side and compare after forgetting precisely its three edge heads.
    def tri_edges(M):
        U=nx.Graph();U.add_nodes_from(M.nodes());U.add_edges_from(M.edges())
        ans=[]
        for a in U.nodes():
            for b in U.neighbors(a):
                if repr(a)>=repr(b):continue
                for c in set(U.neighbors(a))&set(U.neighbors(b)):
                    if repr(b)>=repr(c):continue
                    ans.append({frozenset((a,b)),frozenset((a,c)),frozenset((b,c))})
        return ans
    for ea in tri_edges(A):
        IA=mixed_incidence_graph(A,ea)
        for eb in tri_edges(B):
            IB=mixed_incidence_graph(B,eb)
            nm=lambda x,y:x.get('kind')==y.get('kind') and x.get('label')==y.get('label')
            em=lambda x,y:x.get('head')==y.get('head')
            if nx.algorithms.isomorphism.GraphMatcher(IA,IB,node_match=nm,edge_match=em).is_isomorphic():
                return 'triangle'
    return 'none'


def _mixed_triangle_edges(M):
    U=nx.Graph();U.add_nodes_from(M.nodes());U.add_edges_from(M.edges())
    ans=[]
    for a in U.nodes():
        for b in U.neighbors(a):
            if repr(a)>=repr(b):continue
            for c in set(U.neighbors(a))&set(U.neighbors(b)):
                if repr(b)>=repr(c):continue
                ans.append({frozenset((a,b)),frozenset((a,c)),frozenset((b,c))})
    return ans


def prepare_mixed_source(source_G):
    """Cache the source side of the exact mixed-graph relation test."""
    try:A=sd0_mixed(source_G)
    except ValueError:return None
    return {
        'plain':mixed_incidence_graph(A),
        'triangles':tuple(mixed_incidence_graph(A,edges) for edges in _mixed_triangle_edges(A)),
    }


def mixed_relation_exact_prepared(prepared_source,target_G):
    """Exact equivalent of mixed_relation_exact with a prepared source graph."""
    if prepared_source is None:return 'none'
    try:B=sd0_mixed(target_G)
    except ValueError:return 'none'
    nm=lambda x,y:x.get('kind')==y.get('kind') and x.get('label')==y.get('label')
    em=lambda x,y:x.get('head')==y.get('head')
    IB=mixed_incidence_graph(B)
    if nx.algorithms.isomorphism.GraphMatcher(
        prepared_source['plain'],IB,node_match=nm,edge_match=em
    ).is_isomorphic():return 'isomorphic'
    target_triangles=tuple(mixed_incidence_graph(B,edges) for edges in _mixed_triangle_edges(B))
    for IA in prepared_source['triangles']:
        for IB in target_triangles:
            if nx.algorithms.isomorphism.GraphMatcher(
                IA,IB,node_match=nm,edge_match=em
            ).is_isomorphic():return 'triangle'
    return 'none'

# ---------- multihomogeneous cubic invariant engine -------------------------
@lru_cache(maxsize=None)
def cubic_blocks(k:int):
    from itertools import combinations_with_replacement
    ws=coordinate_weights(k);blocks=defaultdict(list)
    for inds in combinations_with_replacement(range(len(ws)),3):
        w=tuple(ws[inds[0]][j]+ws[inds[1]][j]+ws[inds[2]][j] for j in range(2*k))
        blocks[w].append(inds)
    return tuple((w,tuple(v)) for w,v in sorted(blocks.items()))

def sparse_mul_many(polys):
    if not polys:return {():1}
    out=polys[0]
    for p in polys[1:]:out=sparse_mul(out,p)
    return out

def cubic_separator_fast(source:MapDescriptor,target:MapDescriptor,max_block_size=40,min_block_size=2):
    assert source.k==target.k
    sops=output_sparse_polynomials_cached(source);tops=output_sparse_polynomials_cached(target)
    scache={};tcache={}
    blocks=sorted(cubic_blocks(source.k),key=lambda wb:(len(wb[1]),wb[0]))
    for weight,block in blocks:
        if len(block)<min_block_size or len(block)>max_block_size:continue
        tc=[];sc=[]
        for inds in block:
            if inds not in tcache:tcache[inds]=sparse_mul_many([tops[i] for i in inds])
            if inds not in scache:scache[inds]=sparse_mul_many([sops[i] for i in inds])
            tc.append(tcache[inds]);sc.append(scache[inds])
        for ivec in kernel_sparse_columns_fast(tc):
            spull=sparse_lincomb(sc,ivec)
            if spull:
                assert not sparse_lincomb(tc,ivec)
                return {'degree':3,'weight':weight,'coordinate_triples':block,'coefficients':ivec,
                        'source_nonzero_terms':len(spull),'source_pullback':spull}
    return None

# ---------- generic multihomogeneous degree-d invariant engine -------------
@lru_cache(maxsize=None)
def homogeneous_blocks(k:int,degree:int):
    from itertools import combinations_with_replacement
    ws=coordinate_weights(k);blocks=defaultdict(list)
    for inds in combinations_with_replacement(range(len(ws)),degree):
        w=tuple(sum(ws[i][j] for i in inds) for j in range(2*k))
        blocks[w].append(inds)
    return tuple((w,tuple(v)) for w,v in sorted(blocks.items()))

def homogeneous_separator_fast(source:MapDescriptor,target:MapDescriptor,degree:int,max_block_size:int,min_block_size:int=2):
    assert source.k==target.k
    sops=output_sparse_polynomials_cached(source);tops=output_sparse_polynomials_cached(target)
    scache={};tcache={}
    blocks=sorted(homogeneous_blocks(source.k,degree),key=lambda wb:(len(wb[1]),wb[0]))
    for weight,block in blocks:
        if len(block)<min_block_size or len(block)>max_block_size:continue
        tc=[];sc=[]
        for inds in block:
            if inds not in tcache:tcache[inds]=sparse_mul_many([tops[i] for i in inds])
            if inds not in scache:scache[inds]=sparse_mul_many([sops[i] for i in inds])
            tc.append(tcache[inds]);sc.append(scache[inds])
        for ivec in kernel_sparse_columns_fast(tc):
            spull=sparse_lincomb(sc,ivec)
            if spull:
                assert not sparse_lincomb(tc,ivec)
                return {'degree':degree,'weight':weight,'coordinate_monomials':block,'coefficients':ivec,
                        'source_nonzero_terms':len(spull),'source_pullback':spull}
    return None

@lru_cache(maxsize=None)
def homogeneous_blocks_subset(k:int,degree:int,subset:tuple[int,...]):
    from itertools import combinations_with_replacement
    ws=coordinate_weights(k);blocks=defaultdict(list)
    for inds in combinations_with_replacement(subset,degree):
        w=tuple(sum(ws[i][j] for i in inds) for j in range(2*k));blocks[w].append(inds)
    return tuple((w,tuple(v)) for w,v in sorted(blocks.items()))

def homogeneous_separator_subset(source:MapDescriptor,target:MapDescriptor,degree:int,subset:tuple[int,...],max_block_size:int=1000):
    sops=output_sparse_polynomials_cached(source);tops=output_sparse_polynomials_cached(target)
    scache={};tcache={}
    blocks=sorted(homogeneous_blocks_subset(source.k,degree,tuple(sorted(subset))),key=lambda wb:(len(wb[1]),wb[0]))
    for weight,block in blocks:
        if len(block)<2 or len(block)>max_block_size:continue
        tc=[];sc=[]
        for inds in block:
            if inds not in tcache:tcache[inds]=sparse_mul_many([tops[i] for i in inds])
            if inds not in scache:scache[inds]=sparse_mul_many([sops[i] for i in inds])
            tc.append(tcache[inds]);sc.append(scache[inds])
        for ivec in kernel_sparse_columns_fast(tc):
            spull=sparse_lincomb(sc,ivec)
            if spull:
                assert not sparse_lincomb(tc,ivec)
                return {'degree':degree,'weight':weight,'subset':tuple(sorted(subset)),
                        'coordinate_monomials':block,'coefficients':ivec,
                        'source_nonzero_terms':len(spull),'source_pullback':spull}
    return None

# ---------- directed semialgebraic source-invariant sign certificates -------
def coefficient_sign(poly):
    vals=[v for v in poly.values() if v]
    if vals and all(v>0 for v in vals):return 1
    if vals and all(v<0 for v in vals):return -1
    return 0

def source_invariant_positive_target(source:MapDescriptor,target:MapDescriptor,degree:int=2,max_block_size:int=200):
    assert source.k==target.k
    sops=output_sparse_polynomials_cached(source);tops=output_sparse_polynomials_cached(target)
    blocks=(quadratic_blocks(source.k) if degree==2 else homogeneous_blocks(source.k,degree))
    blocks=sorted(blocks,key=lambda wb:(len(wb[1]),wb[0]))
    scache={};tcache={}
    for weight,block in blocks:
        if len(block)<2 or len(block)>max_block_size:continue
        sc=[];tc=[]
        for inds0 in block:
            inds=inds0 if isinstance(inds0,tuple) else tuple(inds0)
            if degree==2 and len(inds)==2:pass
            if inds not in scache:scache[inds]=sparse_mul_many([sops[i] for i in inds])
            if inds not in tcache:tcache[inds]=sparse_mul_many([tops[i] for i in inds])
            sc.append(scache[inds]);tc.append(tcache[inds])
        for vec in kernel_sparse_columns_fast(sc):
            tp=sparse_lincomb(tc,vec)
            sg=coefficient_sign(tp)
            if sg:
                assert not sparse_lincomb(sc,vec)
                return {'degree':degree,'weight':weight,'coordinate_monomials':block,
                        'coefficients':vec,'target_sign':sg,'target_pullback':tp}
    return None
