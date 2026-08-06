#!/usr/bin/env python3
"""Independent adversarial replay of the seven-port closure certificate.

This file imports neither the primary verifier nor its core enumerator.  It uses
an alternative recursive completion generator, a separate displayed-tree
implementation, direct exact polynomial expansion, and direct finite-field
minor evaluation.
"""
from __future__ import annotations

from collections import Counter, defaultdict
from hashlib import sha256
from itertools import combinations, permutations, product
from pathlib import Path
import json
import sys

import sympy as sp

ROOT = Path(__file__).resolve().parents[1]
CERT = ROOT / "certificates" / "seven_port_closure.json"
CENSUS = ROOT / "certificates" / "cycle_theta_support_completion_corrected.json"
P = 1_000_003
SEGMENTS = (("U","V"),("S","U"),("S","V"),("U","X0"),("V","X0"))
PATTERNS = {
    629: ((), (0,0,1,1,2)), 644: ((), (0,1,1,2,0)),
    649: ((), (0,2,0,1,1)), 650: ((), (0,2,0,2,0)),
    685: ((), (2,1,0,1,0)), 700: ((0,), (0,0,2,0,1)),
    705: ((0,), (0,1,0,2,0)), 706: ((0,), (0,1,1,0,1)),
}


def digest(obj): return sha256(repr(obj).encode()).hexdigest()

def inv(x): return pow(x % P, P-2, P)


def retics(vertices): return tuple(sorted(v for v,c in vertices.items() if c in {"R","X"}))


def displayed_trees(vertices, edges, leaf_index):
    rs = retics(vertices); result=[]
    for bits in product((0,1), repeat=len(rs)):
        excluded=set()
        for r,b in zip(rs,bits):
            inc=[i for i,e in enumerate(edges) if e[1]==r]
            assert len(inc)==2; excluded.add(inc[1-b])
        active=[i for i in range(len(edges)) if i not in excluded]
        child=defaultdict(list)
        for i in active: child[edges[i][0]].append(edges[i][1])
        memo={}
        def descendants(v):
            if v in memo:return memo[v]
            if v in leaf_index: ans=frozenset((leaf_index[v],))
            else:
                ans=frozenset()
                for w in child.get(v,()):ans |= descendants(w)
            memo[v]=ans;return ans
        result.append((bits,tuple(active),{i:descendants(edges[i][1]) for i in active}))
    return rs,tuple(result)


def lift(vertices,edges,leaves):
    vv={("IN" if x=="S" else x):("T" if x=="S" else c) for x,c in vertices.items()}
    ee=[(("IN" if a=="S" else a),("IN" if b=="S" else b)) for a,b in edges]
    vv["ROOT"]="S";vv["LIN"]="L";ee += [("ROOT","IN"),("ROOT","LIN")]
    return {"vertices":vv,"edges":tuple(ee),"leaves":tuple(("IN" if x=="S" else x) for x in leaves)+("LIN",)}


def core3(words,sink):
    v={"S":"S","U":"T","V":"R","X0":"X"};e=[];parents={}
    for (a,b),word in zip(SEGMENTS,words):
        chain=[a]
        for lab in word:
            q=f"P{lab}";v[q]="T";parents[lab]=q;chain.append(q)
        chain.append(b);e.extend(zip(chain,chain[1:]))
    parents[sink]="X0";leaves=[];labels={}
    for lab in sorted(parents):
        q=f"L{lab}";v[q]="L";e.append((parents[lab],q));leaves.append(q);labels[q]=lab
    net=lift(v,e,leaves);labels["LIN"]=8
    return net,labels


def cycle(counts):
    v={"S":"S","X":"X"};e=[];parents=[]
    for side,count in enumerate(counts):
        chain=["S"]
        for j in range(count):
            q=f"P{side}_{j}";v[q]="T";parents.append(q);chain.append(q)
        chain.append("X");e.extend(zip(chain,chain[1:]))
    parents.append("X");leaves=[]
    for j,p in enumerate(parents):
        q=f"L{j}";v[q]="L";e.append((p,q));leaves.append(q)
    return lift(v,e,leaves)


def weak_pattern(pattern):
    selected_sinks, counts = pattern
    # Independent deterministic completion uses repair (0,4).
    v={"S":"S","U":"T","V":"R","X0":"X"};e=[];selected=[];dummy=[]
    occupied={i for i,c in enumerate(counts) if c}
    for i,((a,b),count) in enumerate(zip(SEGMENTS,counts)):
        chain=[a]
        for j in range(count):
            q=f"P{i}_{j}";v[q]="T";selected.append(q);chain.append(q)
        if i in {0,4} and i not in occupied:
            q=f"D{i}";v[q]="T";dummy.append(q);chain.append(q)
        chain.append(b);e.extend(zip(chain,chain[1:]))
    (selected if selected_sinks else dummy).append("X0")
    selected_leaves=[];dummy_leaves=[];leaves=[]
    for j,p in enumerate(selected):
        q=f"L{j}";v[q]="L";e.append((p,q));selected_leaves.append(q);leaves.append(q)
    for j,p in enumerate(dummy):
        q=f"Z{j}";v[q]="L";e.append((p,q));dummy_leaves.append(q);leaves.append(q)
    return lift(v,e,leaves),tuple(selected_leaves),tuple(dummy_leaves)


def insert_labels(base_words, labels):
    states={tuple(tuple(w) for w in base_words)}
    for label in labels:
        new=set()
        for words in states:
            for segment in range(5):
                for position in range(len(words[segment])+1):
                    local=[list(w) for w in words]
                    local[segment].insert(position,label)
                    new.add(tuple(tuple(w) for w in local))
        states=new
    return states


def completion_set(pattern):
    selected_sinks,counts=pattern;next_label=1;base=[]
    for c in counts:base.append(tuple(range(next_label,next_label+c)));next_label+=c
    old_sink=next_label if selected_sinks else None
    if old_sink is not None:next_label+=1
    assert next_label==5
    extras={5,6,7};ans=set()
    if old_sink is None:
        for sink in extras:
            for words in insert_labels(base,sorted(extras-{sink})):
                occ=tuple(bool(w) for w in words)
                if occ[4] and (occ[0] or occ[3]):ans.add((words,sink))
    else:
        for words in insert_labels(base,sorted(extras)):
            occ=tuple(bool(w) for w in words)
            if occ[4] and (occ[0] or occ[3]):ans.add((words,old_sink))
    return ans


def standard_stc(net,labels):
    vertices=net["vertices"]
    root_children=[];mixed=[]
    for a,b in net["edges"]:
        if a=="ROOT":root_children.append(b);continue
        mixed.append(("D" if vertices[b] in {"R","X"} else "U",a,b))
    a,b=root_children
    if vertices[a] in {"R","X"}:mixed.append(("D",b,a))
    elif vertices[b] in {"R","X"}:mixed.append(("D",a,b))
    else:mixed.append(("U",a,b))
    undeg=Counter()
    for kind,a,b in mixed:
        if kind=="U":undeg[a]+=1;undeg[b]+=1
    return all(undeg[a]==2 for kind,a,b in mixed if kind=="D")


def full_schema(net,labels):
    leaf_index={leaf:label-1 for leaf,label in labels.items()}
    rs,trees=displayed_trees(net["vertices"],net["edges"],leaf_index)
    out=[]
    for bits,active,desc in trees:
        rows=[]
        for i in active:
            mask=sum(1<<q for q in desc[i]);rows.append((i,mask))
        out.append((tuple(bits),tuple(rows)))
    return tuple(net["edges"]),tuple(rs),tuple(out)


def independent_mixed_graph_code(net, labels):
    """Canonical coloured mixed-graph code, independently of the primary code."""
    vertices=net["vertices"];colors={};root_children=[];edges=[]
    for v,c in vertices.items():
        if c=="S":continue
        if c=="L":
            label=labels.get(v)
            colors[v]="LIN" if label==8 else (f"L{label}" if label is not None else "Z")
        elif c in {"R","X"}:colors[v]="R"
        else:colors[v]="T"
    for u,v in net["edges"]:
        if u=="ROOT":root_children.append(v);continue
        if vertices[v] in {"R","X"}:edges.append(("D",u,v))
        else:edges.append(("U",)+tuple(sorted((u,v))))
    assert len(root_children)==2
    a,b=root_children
    if vertices[a] in {"R","X"}:edges.append(("D",b,a))
    elif vertices[b] in {"R","X"}:edges.append(("D",a,b))
    else:edges.append(("U",)+tuple(sorted((a,b))))
    edges=tuple(sorted(edges));adj={v:[] for v in colors}
    for kind,a,b in edges:
        if kind=="U":adj[a].append(("U",b));adj[b].append(("U",a))
        else:adj[a].append(("OUT",b));adj[b].append(("IN",a))
    groups=defaultdict(list)
    for v,c in colors.items():groups[c].append(v)
    initial=tuple(tuple(sorted(groups[c])) for c in sorted(groups))
    def refine(cells):
        while True:
            cell_of={v:i for i,cell in enumerate(cells) for v in cell};out=[];changed=False
            for cell in cells:
                blocks=defaultdict(list)
                for v in cell:
                    counts=Counter((rel,cell_of[w]) for rel,w in adj[v])
                    sig=tuple(counts[(rel,j)] for j in range(len(cells)) for rel in ("U","OUT","IN"))
                    blocks[sig].append(v)
                changed |= len(blocks)>1
                out.extend(tuple(sorted(blocks[key])) for key in sorted(blocks))
            cells=tuple(out)
            if not changed:return cells
    def code(cells):
        order=tuple(cell[0] for cell in cells);pos={v:i for i,v in enumerate(order)};image=[]
        for kind,a,b in edges:
            a,b=pos[a],pos[b]
            if kind=="U" and a>b:a,b=b,a
            image.append((kind,a,b))
        return tuple(colors[v] for v in order),tuple(sorted(image))
    def search(cells):
        cells=refine(cells)
        if all(len(cell)==1 for cell in cells):return code(cells)
        j=next(i for i,cell in enumerate(cells) if len(cell)>1);best=None
        for v in cells[j]:
            remainder=tuple(x for x in cells[j] if x!=v)
            candidate=search(cells[:j]+((v,),remainder)+cells[j+1:])
            if best is None or candidate<best:best=candidate
        return best
    return search(initial)


def reduced_witness_type(net, labels, triple):
    """Displayed-choice descendant-mask tensor after marginalizing to a triple."""
    local={label:index for index,label in enumerate(triple)}
    leaf_index={leaf:local[label] for leaf,label in labels.items() if label in local}
    _rs,trees=displayed_trees(net["vertices"],net["edges"],leaf_index)
    signatures=[]
    for edge_index in range(len(net["edges"])):
        row=[]
        for _bits,active,descendants in trees:
            if edge_index not in active:row.append(0);continue
            mask=0
            for position in descendants[edge_index]:mask |= 1<<position
            row.append(mask)
        if any(row):signatures.append(tuple(row))
    return tuple(sorted(set(signatures)))


def F_polynomial(net, observed, triple, prefix):
    leaf_index={leaf:i for i,leaf in enumerate(tuple(observed)+("LIN",))}
    rs,trees=displayed_trees(net["vertices"],net["edges"],leaf_index)
    xs=sp.symbols(f"{prefix}x0:{len(net['edges'])}");ls=sp.symbols(f"{prefix}l0:{len(rs)}")
    vals=[]
    for local in ((1,1,0),(1,0,1),(0,1,1),(1,2,3)):
        ass=[0]*(len(observed)+1)
        for p,z in zip(triple,local):ass[p]=z
        total=0
        for bits,active,desc in trees:
            term=1
            for j,b in enumerate(bits):term*=ls[j] if b==0 else 1-ls[j]
            for i in active:
                ch=0
                for q in desc[i]:ch ^= ass[q]
                if ch:term*=xs[i]
            total+=term
        vals.append(sp.expand(total))
    return sp.factor(vals[0]*vals[1]*vals[2]-vals[3]**2)


def monomial_positive(q):
    coeff,rest=sp.factor(q).as_coeff_Mul()
    if coeff<=0:return False
    for term in sp.Mul.make_args(rest):
        if term.is_Symbol:continue
        if term.is_Pow and term.base.is_Symbol and term.exp.is_Integer and term.exp>0:continue
        return False
    return True


def positive_factorization(expr):
    coeff,factors=sp.factor_list(expr);sign=1 if coeff>0 else -1
    for f,power in factors:
        f=sp.factor(f);s=None
        if f.is_Symbol:s=1
        elif len(f.free_symbols)==1:
            x=next(iter(f.free_symbols))
            if sp.expand(f-(x-1))==0:s=-1
            elif sp.expand(f-(x+1))==0:s=1
        if s is None:
            plus=sp.expand(f+1)
            if plus.is_Mul and all(a.is_Symbol or (a.is_Pow and a.base.is_Symbol and a.exp>0) for a in sp.Mul.make_args(plus)):s=-1
        if s is None:
            lambdas=[x for x in f.free_symbols if str(x).endswith("l0") or str(x).endswith("l1")]
            for l0 in lambdas:
                for l1 in lambdas:
                    if l0==l1:continue
                    A=sp.factor(sp.diff(sp.diff(f,l0),l1));C=sp.factor(-f.subs(l0,0)/l1)
                    if sp.expand(f+l0*(1-l1)*A+l1*C)==0 and monomial_positive(A) and monomial_positive(C):s=-1;break
                if s is not None:break
        if s is None and power%2==0:s=1
        assert s is not None,(f,power)
        if power%2==0:s=1
        sign*=s
    assert sign==1


def determinant_mod(matrix):
    A=[row[:] for row in matrix];n=len(A);det=1
    for c in range(n):
        r=next(i for i in range(c,n) if A[i][c]%P)
        if r!=c:A[c],A[r]=A[r],A[c];det=-det%P
        pivot=A[c][c]%P;det=det*pivot%P;ip=inv(pivot)
        for i in range(c+1,n):
            if A[i][c]%P:
                factor=A[i][c]*ip%P
                for j in range(c,n):A[i][j]=(A[i][j]-factor*A[c][j])%P
    return det


def jacobian_at(net,assignments,edge_values,inheritance_values):
    leaf_index={v:i for i,v in enumerate(net["leaves"])}
    rs,trees=displayed_trees(net["vertices"],net["edges"],leaf_index)
    E=len(net["edges"]);rows=[]
    for ass in assignments:
        row=[0]*(E+len(rs))
        for bits,active,desc in trees:
            active_nonzero=[];prodv=1
            for i in active:
                ch=0
                for q in desc[i]:ch ^= ass[q]
                if ch:active_nonzero.append(i);prodv=prodv*edge_values[i]%P
            weight=1
            for j,b in enumerate(bits):weight=weight*(inheritance_values[j] if b==0 else 1-inheritance_values[j])%P
            term=weight*prodv%P
            for i in active_nonzero:row[i]=(row[i]+term*inv(edge_values[i]))%P
            for j,b in enumerate(bits):
                lam=inheritance_values[j]
                dw=weight*inv(lam if b==0 else 1-lam)%P
                if b:dw=-dw%P
                row[E+j]=(row[E+j]+dw*prodv)%P
        rows.append(row)
    return rows


def verify_minor(net,record):
    m=record["minor"]
    rows=jacobian_at(net,[tuple(a) for a in m["row_assignments"]],m["edge_values_mod_prime"],m["inheritance_values_mod_prime"])
    matrix=[[row[j] for j in m["columns"]] for row in rows]
    assert determinant_mod(matrix)==m["determinant_mod_prime"]!=0


def verify_gauge_upper(net,expected):
    n=len(net["leaves"]);rs=retics(net["vertices"]);E=len(net["edges"])
    assert E==2*n+3*len(rs)-2
    root_out=[i for i,e in enumerate(net["edges"]) if e[0]=="ROOT"]
    assert len(root_out)==2
    used=set(root_out)
    for r in rs:
        inc=[i for i,e in enumerate(net["edges"]) if e[1]==r]
        out=[i for i,e in enumerate(net["edges"]) if e[0]==r]
        assert len(inc)==2 and len(out)==1 and not(set(inc+out)&used)
        used.update(inc+out)
    assert E+len(rs)-(1+2*len(rs))==expected


def main():
    cert=json.loads(CERT.read_text())
    assert cert["status"]=="PROVED"
    # The eight role tuples have a trivial core automorphism: S,U,V,X0 have
    # distinct directed/vertex roles.  Thus S4 acts freely and different word
    # occupancies cannot collide.
    assert len(cert["graph_symmetry_orbits_under_S4"])==8
    assert all(o["orbit_size"]==24 and len(set(o["member_graph_sha256"]))==24 for o in cert["graph_symmetry_orbits_under_S4"])
    assert len({h for o in cert["graph_symmetry_orbits_under_S4"] for h in o["member_graph_sha256"]})==192
    expected_meta={(r["presentation_id"],r["permutation_index"],tuple(r["outgoing_relabelling"])) for r in cert["residual_records"]}
    regenerated={(pid,i,p) for pid in PATTERNS for i,p in enumerate(permutations((1,2,3,4)))}
    assert expected_meta==regenerated
    census=json.loads(CENSUS.read_text())
    residual={(r["presentation_index"],r["permutation_index"]) for r in census["records"] if r["missing_rigid_support_ports"]==3}
    assert residual=={(pid,i) for pid in PATTERNS for i in range(24)}
    assert sha256(CENSUS.read_bytes()).hexdigest()==cert["residual_census_dependency"]["sha256"]

    # Alternative recursive completion generator.
    expected={(r["presentation_id"],tuple(tuple(w) for w in r["segment_words"]),r["sink_label"]):r for r in cert["completion_records"]}
    regenerated_completions={}
    for pid,pattern in PATTERNS.items():
        for words,sink in completion_set(pattern):
            net,labels=core3(words,sink);assert standard_stc(net,labels)
            key=(pid,words,sink);assert key not in regenerated_completions
            regenerated_completions[key]=(net,labels)
    assert set(expected)==set(regenerated_completions)
    assert len(regenerated_completions)==1686
    completion_graph_codes=set()
    for key,(net,labels) in regenerated_completions.items():
        assert digest(full_schema(net,labels))==expected[key]["full_parameterization_sha256"]
        graph_code=independent_mixed_graph_code(net,labels)
        assert digest(graph_code)==expected[key]["canonical_graph_sha256"]
        assert graph_code not in completion_graph_codes
        completion_graph_codes.add(graph_code)
    assert len(completion_graph_codes)==1686

    # Independent exact F replay on base representatives.
    zero_table={k:{tuple(t) for t in v} for k,v in cert["base_F_zero_patterns"].items()}
    positive={(r["presentation_id"],tuple(r["triple"])):r for r in cert["base_positive_F_certificates"]}
    for pid,pattern in PATTERNS.items():
        net,selected,_dummy=weak_pattern(pattern)
        for triple in combinations(range(5),3):
            f=F_polynomial(net,selected,triple,f"p{pid}t{''.join(map(str,triple))}_")
            assert (f==0)==(triple in zero_table[str(pid)])
            if (pid,triple) in positive:
                assert sp.expand(f-sp.sympify(positive[(pid,triple)]["factorization"]))==0
                positive_factorization(f)

    # Independent exact cycle positivity.
    for record in cert["cycle_positive_F_certificates"]:
        net=cycle(tuple(record["side_counts"]));obs=tuple(net["leaves"][:-1])
        prefix=f"cycle{record['side_counts'][0]}{record['side_counts'][1]}_"
        f=F_polynomial(net,obs,(0,1,2),prefix)
        assert sp.expand(f-sp.sympify(record["factorization"]))==0;positive_factorization(f)

    # Universal completed-orbit factors.
    A,la=core3(((),(1,2),(),(3,),(4,)),5)
    B,lb=core3(((),(1,),(),(2,3),(5,)),4)
    for net,record in zip((A,B),cert["seven_port_universal_F_certificates"]):
        f=F_polynomial(net,("L1","L2","L5"),(0,1,2),"caseA_" if record["orbit"]==649 else "caseB_")
        assert sp.expand(f-sp.sympify(record["factorization"]))==0;positive_factorization(f)

    # Every 649/705 completion has the certified structural witness and the
    # same reduced displayed-tree tensor type as the symbolic universal case.
    caseA_type=reduced_witness_type(A,la,(1,2,5))
    caseB_type=reduced_witness_type(B,lb,(1,2,5))
    universal_type_checks=Counter()
    for key,(net,labels) in regenerated_completions.items():
        pid,words,sink=key
        if pid==649:witness=(1,2,sink);reference=caseA_type
        elif pid==705:
            e=min(x for x in (5,6,7) if x in words[4]);witness=(1,2,e);reference=caseB_type
        else:continue
        assert tuple(expected[key]["separator_triple"])==witness and 4 not in witness
        assert reduced_witness_type(net,labels,witness)==reference
        universal_type_checks[pid]+=1
    assert universal_type_checks==Counter({649:270,705:216})

    # Recompute every stored exact generic-rank minor and the structural upper bound.
    for r in cert["generic_dimensions"]["cycle_sources"]:
        net=cycle(tuple(r["counts"]));verify_gauge_upper(net,15);verify_minor(net,r)
    for r in cert["generic_dimensions"]["core3_theta_targets"]:
        counts=tuple(r["counts"]);words=[];lab=1
        for c in counts:words.append(tuple(range(lab,lab+c)));lab+=c
        net,_=core3(tuple(words),7);verify_gauge_upper(net,17);verify_minor(net,r)

    assert cert["classification"]["stochastic_disjointness"]==192
    result={
        "status":"VERIFIED",
        "residual_records":192,
        "S4_orbits":8,
        "completed_standard_S_TC_graphs":1686,
        "completed_graph_codes_independently_unique":len(completion_graph_codes),
        "universal_reduced_tensor_checks":dict(universal_type_checks),
        "cycle_dimensions_replayed":len(cert["generic_dimensions"]["cycle_sources"]),
        "theta_dimensions_replayed":len(cert["generic_dimensions"]["core3_theta_targets"]),
        "all_pairs_stochastically_disjoint":True,
    }
    (ROOT/"certificates"/"seven_port_adversarial_review.json").write_text(
        json.dumps(result,indent=2,sort_keys=True)+"\n"
    )
    print(json.dumps(result,indent=2,sort_keys=True))

if __name__=="__main__":main()
