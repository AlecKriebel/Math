#!/usr/bin/env python3
"""Independent exact audit: tuple-word tree, pairwise common-neighbor square.
Does not import or execute deposited graph/flow verification functions.
Standard-library only, Python 3.10+. Outputs JSON to stdout.
"""
from pathlib import Path
from itertools import combinations
from fractions import Fraction
from math import isqrt
from datetime import datetime, timezone
import gzip, hashlib, json

SOURCE=Path(__file__).resolve().parents[2]/'sources'/'published-release'
PIN='6573c55f2998f4576a050a0757ca74f1cae9cadfa96ec61c69b181c530f79c4f'

def demand(condition, why):
    if not condition:
        raise RuntimeError(why)

def outward_children(word):
    return tuple(word+(letter,) for letter in (range(3) if not word else range(2)))

def tree_neighbours(word):
    return set(outward_children(word)) | ({word[:-1]} if word else set())

def end_parent(word):
    # The distinguished end is the infinite all-zero word.
    return word+(0,) if all(letter == 0 for letter in word) else word[:-1]

def children(word):
    return tree_neighbours(word)-{end_parent(word)}

def g_neighbours(word):
    p=end_parent(word)
    return tree_neighbours(word)|{end_parent(p)}|set().union(*(children(v) for v in children(word)))

def descendants(word,depth):
    generation={word}
    for _ in range(depth):
        generation=set().union(*(children(x) for x in generation))
    return generation

def build():
    levels=[((),)]
    for _ in range(10):
        levels.append(tuple(child for word in levels[-1] for child in outward_children(word)))
    words=tuple(word for level in levels for word in level)
    index={word:i for i,word in enumerate(words)}
    all_words=set(words)
    # Infinite neighbor lists are built before endpoint restriction.
    infinite_g={word:g_neighbours(word) for word in words}
    k={word:infinite_g[word]&all_words for word in words}
    demand(len(words)==3070,'tree-ball vertex count')
    demand(all(len(nei)==8 and v not in nei for v,nei in infinite_g.items()),'G degree and no loops')
    demand(all(v in g_neighbours(u) for v in words for u in infinite_g[v]),'infinite G reciprocity')
    demand(all(len(children(v))==2 for v in words),'exactly two end-oriented children')
    # Materially distinct square construction: test every unordered endpoint pair.
    edges=tuple((i,j) for i,j in combinations(range(len(words)),2)
                if words[j] in k[words[i]] or not k[words[i]].isdisjoint(k[words[j]]))
    demand(len(edges)==19931,'J edge count')
    root=()
    root_nei=g_neighbours(root)|set().union(*(g_neighbours(x) for x in g_neighbours(root)))
    root_nei.discard(root)
    ancestors=[]
    x=root
    for _ in range(4):
        x=end_parent(x); ancestors.append(x)
    sibling=next(iter(children(end_parent(root))-{root}))
    uncle=next(iter(children(end_parent(end_parent(root)))-{end_parent(root)}))
    classes={'ancestors_1_to_4':set(ancestors),
             **{f'descendants_depth_{d}':descendants(root,d) for d in range(1,5)},
             'sibling':{sibling},'uncle':{uncle},
             'siblings_children':children(sibling),'uncles_children':children(uncle)}
    demand(sum(map(len,classes.values()))==40,'classified count')
    demand(set().union(*classes.values())==root_nei,'classified full H neighborhood')
    root_targets=tuple(sorted(index[w] for w in root_nei))
    demand(tuple(j for i,j in edges if i==0)==root_targets,'complete root neighborhood in J')
    # Every listed J edge has an actual infinite G witness, including boundary.
    demand(all(words[j] in infinite_g[words[i]] or
               not infinite_g[words[i]].isdisjoint(infinite_g[words[j]]) for i,j in edges),'J subset H')
    # Independently count H[W], with intermediate vertices allowed outside W.
    induced_h_edges=set()
    for v in words:
        ns=infinite_g[v]|set().union(*(g_neighbours(z) for z in infinite_g[v]))
        ns.discard(v)
        demand(len(ns)==40,'infinite H degree at word '+repr(v))
        induced_h_edges.update((index[v],index[u]) for u in ns&all_words if index[v]<index[u])
    boundary_extra=sorted(induced_h_edges-set(edges))
    # This equality is additional finite evidence; only subset is needed for transfer.
    triangles={index[w]:len(g_neighbours(root)&g_neighbours(w)) for w in g_neighbours(root)}
    demand(sorted(triangles.values())==[1]*5+[3]*3,'intrinsic tree edge triangle signatures')
    return words,edges,root_targets,classes,boundary_extra,triangles

def boundary_diagnostics():
    cases=[]
    words=[()]
    frontier=[()]
    complete=g_neighbours(())|set().union(*(g_neighbours(v) for v in g_neighbours(())))
    complete.discard(())
    for radius in range(6):
        wset=set(words)
        adjacency={v:g_neighbours(v)&wset for v in words}
        near=adjacency[()]|set().union(*(adjacency[v] for v in adjacency[()]))
        near.discard(())
        demand(near<=complete,'small-ball square adds no false root neighbor')
        if radius>=4:
            demand(near==complete,'radius four contains complete neighborhood')
        cases.append({'radius':radius,'vertices':len(words),'root_degree_square':len(near),
                      'missing_infinite_root_neighbors':len(complete-near)})
        frontier=[child for w in frontier for child in outward_children(w)]
        words.extend(frontier)
    return cases

def inspect(data,words,edges,targets):
    demand(type(data) is dict,'object')
    for key,val in [('q',2),('radius',10),('vertices',len(words)),('denominator',10**9),
                    ('total_energy_denominator',10**18)]:
        demand(type(data[key]) is int and data[key]==val,'integer parameter '+key)
    demand(data['edge_order']==[list(e) for e in edges],'all edges and ordering')
    demand(all(type(v) is int for e in data['edge_order'] for v in e),'edge label integer types')
    demand(data['root_neighbors']==list(targets),'all targets and ordering')
    demand(all(type(v) is int for v in data['root_neighbors']),'target integer types')
    demand(type(data['flows']) is list and len(data['flows'])==40,'flow count')
    energies=[]
    divergences=[]
    maximum_abs_current=0
    zero_count=0
    for target,row in zip(targets,data['flows']):
        demand(type(row) is list and len(row)==len(edges),'row length')
        demand(all(type(a) is int for a in row),'current exact integer types')
        # Oriented current contribution lists; divergence is summed per vertex.
        incidence=[[] for _ in words]
        for (i,j),a in zip(edges,row):
            incidence[i].append(a)
            incidence[j].append(-a)
            maximum_abs_current=max(maximum_abs_current,abs(a))
            zero_count+=a==0
        div=tuple(map(sum,incidence))
        demand(div==tuple(-10**9 if i==0 else 10**9 if i==target else 0 for i in range(len(words))),
               'exact full divergence row for target '+str(target))
        divergences.append({'target':target,'nonzero_divergence':[[i,a] for i,a in enumerate(div) if a]})
        energies.append(sum(a*a for a in row))
    demand(type(data['energy_numerators']) is list and all(type(e) is int for e in data['energy_numerators']),
           'energy integer types')
    demand(energies==data['energy_numerators'],'every per-flow energy')
    total=sum(energies)
    demand(type(data['total_energy_numerator']) is int and data['total_energy_numerator']==total,'total energy data')
    demand(total==3208526010913748780,'total energy theorem')
    demand(100*total<321*10**18,'strict 3.21 inequality')
    demand(Fraction(73,50)**2>2,'rational radical upper bound')
    demand((24-Fraction(73,50))/7==Fraction(161,50),'strict 3.22 G lower bound')
    demand((Fraction(161,50)-Fraction(321,100))/2==Fraction(1,200),'stated bF gap')
    scale=10**60
    sqrt_lower=isqrt(2*scale*scale)
    demand(sqrt_lower**2<2*scale*scale<(sqrt_lower+1)**2,'certified sqrt interval')
    degree_lo=(24-Fraction(sqrt_lower+1,scale))/7
    degree_hi=(24-Fraction(sqrt_lower,scale))/7
    return {'currents_verified':len(edges)*len(energies),'divergences_verified':len(words)*len(energies),
            'energy_numerators':energies,'exact_total_numerator':total,'exact_total_denominator':10**18,
            'reduced_total_energy':str(Fraction(total,10**18)),
            'strict_upper_margin':str(Fraction(321,100)-Fraction(total,10**18)),
            'strict_expected_degree_gap_lower_rational':str(degree_lo-Fraction(total,10**18)),
            'strict_bF_gap_lower_rational':str((degree_lo-Fraction(total,10**18))/2),
            'G_degree_enclosure':[str(degree_lo),str(degree_hi)],'all_divergence_supports':divergences,
            'maximum_abs_current_numerator':maximum_abs_current,'zero_current_entries':zero_count}

def main():
    raw=(SOURCE/'square_flow_certificate.json.gz').read_bytes()
    demand(hashlib.sha256(raw).hexdigest()==PIN,'certificate identity')
    decoded=gzip.decompress(raw)
    data=json.loads(decoded)
    words,edges,targets,classes,extra,triangles=build()
    result=inspect(data,words,edges,targets)
    manifest=json.loads((SOURCE/'source-manifest.json').read_text())
    for row in manifest['files']:
        value=(SOURCE/row['path']).read_bytes()
        demand(len(value)==row['bytes'],'manifest byte size '+row['path'])
        demand(hashlib.sha256(value).hexdigest()==row['sha256'],'manifest SHA256 '+row['path'])
    index={w:i for i,w in enumerate(words)}
    result.update({'status':'PASS','timestamp_utc':datetime.now(timezone.utc).isoformat(),
                   'method':'Tree word coordinates, pairwise square common-neighbor test, per-vertex signed contribution sums; no deposited functions imported.',
                   'vertices':len(words),'edges':len(edges),'root_neighbors':list(targets),
                   'root_neighbor_classes':{name:sorted(index[w] for w in group) for name,group in classes.items()},
                   'J_edges_subset_H':True,'H_induced_W_edges_absent_from_J':extra,
                   'infinite_H_degrees_checked':len(words),'small_radius_boundary_diagnostics':boundary_diagnostics(),
                   'root_G_edge_triangle_counts':triangles,'manifest_members_verified':len(manifest['files']),
                   'certificate_sha256':PIN,'compressed_bytes':len(raw),'json_bytes':len(decoded),
                   'limits':'Exact finite feasibility and constants; infinite transfer separately reviewed mathematically. No novelty certification, exact H expectation, optimality, or human peer-review claim.'})
    return result

if __name__=='__main__':
    print(json.dumps(main(),indent=2,sort_keys=True))
