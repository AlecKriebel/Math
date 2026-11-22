#!/usr/bin/env python3
"""Independent audit checks. No assert statements; identical semantics under -O."""
from itertools import combinations, permutations
from collections import Counter
from pathlib import Path
import ast,json,hashlib
ROOT=Path(__file__).resolve().parent
SRC=ROOT.parent/'domino_1890_analysis'
def need(b,msg):
    if not b: raise RuntimeError(msg)
def std(p):return tuple(1+sum(y<x for y in p) for x in p)
def hits(p,b):
    return [tuple(i+1 for i in ix) for ix in combinations(range(len(p)),len(b)) if std(tuple(p[i] for i in ix))==tuple(b)]
def avoid(p,b):return not hits(p,b)
def cuts(p):
    return [c for c in range(len(p)+1) if avoid(p[:c],(1,3,2)) and avoid(p[c:],(2,3,1))]
def literal(p):return avoid(p,(1,3,2,4)) and bool(cuts(p))
def inv(p):return sum(x>y for i,x in enumerate(p) for y in p[i+1:])
def components(p):
    out=[];last=0
    for i in range(1,len(p)+1):
        if set(p[:i])==set(range(1,i+1)):
            out.append(std(p[last:i]));last=i
    return out
def functions_from(path):
    tree=ast.parse(path.read_text()); tree.body=[x for x in tree.body if isinstance(x,(ast.Import,ast.ImportFrom,ast.FunctionDef))]
    g={};exec(compile(tree,str(path),'exec'),g);return g
B=((1,3,2,4),(1,5,3,4,2),(2,5,3,4,1),(3,6,5,2,4,1),(4,6,5,2,3,1))
cert=json.loads((SRC/'basis_certificate.json').read_text())
expected={p for n in (5,6) for p in permutations(range(1,n+1)) if std(p[:3])==(1,3,2) and std(p[-3:])==(2,3,1)}
need(len(expected)==24,'witness coverage cardinality')
need({tuple(row['witness']) for row in cert}==expected,'witness list equality')
for row in cert:
    w=tuple(row['witness']);b=tuple(row['forbidden_pattern']);ix=tuple(row['positions'])
    need(b in B and ix in hits(w,b),('bad certificate',row))
for b in B:
    need(not literal(b),('basis member',b))
    for i in range(len(b)):need(literal(std(b[:i]+b[i+1:])),('basis minimality',b,i))
original=json.loads((SRC/'counts_extended.json').read_text())
independent=json.loads((ROOT/'independent_counts.json').read_text())
need(len(original)==len(independent)==12,'n scope')
for a,b in zip(original,independent):
    for key in ['n','total','counts','both_end_extensions_fail']:
        need(a[key]==b[key],('independent counts',a['n'],key))
    for p0 in a['example']:
        p=tuple(x+1 for x in p0)
        need(literal(p) and not literal(p+(len(p)+1,)) and not literal((1,)+tuple(x+1 for x in p)),('bad sample',p))
for fname in ['counts.json','counts_extended.json']:
    data=json.loads((SRC/fname).read_text())
    for row in data:need(row==original[row['n']],('count file mismatch',fname,row['n']))
for fname in ['counts.log','counts_extended.log']:
    data=[ast.literal_eval(line) for line in (SRC/fname).read_text().splitlines()]
    for row in data:
        row['example']=[list(p) for p in row['example']]
        need(row==original[row['n']],('count log mismatch',fname,row['n']))
for n in range(1,len(original)):
    old=original[n-1]['counts'];new=original[n]['counts']
    for k,v in enumerate(old):
        need(v<=new[k],('finite monotonicity',n,k))
        if n-1>=k+2:need(v==new[k],('finite stable range',n,k))
# Exhaustively rule out ANY one-point pattern extension preserving inversions.
p=(2,4,1,3);extensions=[]
for pos in range(5):
    for val in range(1,6):
        a=tuple(x+(x>=val) for x in p);q=a[:pos]+(val,)+a[pos:]
        if inv(q)==inv(p):extensions.append(q);need(not literal(q),('insertion survived',q))
need(set(extensions)=={(1,3,5,2,4),(2,4,1,3,5)},'zero-inversion insertions')
need(literal((4,2,3,1)) and not literal((1,5,3,4,2)) and avoid((1,5,3,4,2),(1,3,2,4)),'prepend grid-only obstruction')
explicit=functions_from(SRC/'transfer.py');recursive=functions_from(SRC/'independent_f_test.py')
# Interpret the paper independently via inverse and reverse-complement operations.
def tilde(p):
    c=len(components(p)[0]);return p[:c]+(c+1,)+tuple(x+1 for x in p[c:])
def inverse(p):return tuple(p.index(i)+1 for i in range(1,len(p)+1))
def rc(p):return tuple(len(p)+1-x for x in p[::-1])
def f(p):
    if len(components(p))>=2:return tilde(p)
    if len(components(std(p[1:])))>=2:
        q=tilde(std(p[1:]));v=p[0];return (v,)+tuple(x+(x>=v) for x in q)
    if len(components(std(tuple(x for x in p if x!=1))))>=2:return inverse(f(inverse(p)))
    if len(components(std(p[:-1])))>=2 or len(components(std(tuple(x for x in p if x!=len(p)))))>=2:return rc(f(rc(p)))
    return None
examples=[]
for p in [(4,n,2,3,5,1)+tuple(range(6,n)) for n in range(7,21)]:
    q=f(p);p0=tuple(x-1 for x in p)
    need(q==tuple(x+1 for x in explicit['f'](p0))==tuple(x+1 for x in recursive['f'](p0)),'f implementations witness')
    need(literal(p) and not literal(q) and avoid(q,(1,3,2,4)) and inv(p)==inv(q),'f witness validity')
    need((2,3,4,5,6) in hits(q,(2,5,3,4,1)),'f witness basis positions')
    examples.append({'input':p,'output':q,'inversions':inv(p),'input_cuts':cuts(p),'output_cuts':cuts(q),'low_range_k_le_2n_minus_7':inv(p)<=2*len(p)-7})
# Compare map implementations on ALL 1324-avoiders through n=8, checking the
# stronger theorem's component and graph observations independently.
def graph_components(p):
    parent=list(range(len(p)))
    def root(i):
        while parent[i]!=i:i=parent[i]
        return i
    for i in range(len(p)):
        for j in range(i+1,len(p)):
            if p[i]>p[j]:parent[root(i)]=root(j)
    return sorted(tuple(i for i in range(len(p)) if root(i)==r) for r in set(root(i) for i in range(len(p))))
rows=[];comparisons=0;graph_checks=0;subclass_checks=0;image_component_checks=0
for n in range(1,9):
    seen={};bad=[];decomposable=0;source_count=0
    for p in permutations(range(1,n+1)):
        if not avoid(p,(1,3,2,4)):continue
        member=bool(cuts(p));comp=components(p)
        need(not avoid(p,(4,2,3,1)) or member,('subclass inclusion',p));subclass_checks+=1
        if len(comp)>=2:need(member==avoid(comp[-1],(4,2,3,1)),('decomposable characterization',p))
        gc=graph_components(p);need(len(gc)==len(comp),('graph components',p));graph_checks+=1
        start=0
        for c in gc:
            need(c==tuple(range(start,start+len(c))),('graph interval',p));start+=len(c)
        rank=inv(p)-n+len(comp)
        need(rank>=0 and (rank>1 or avoid(p,(4,2,3,1))),('cycle rank',p))
        source_count+=member
        q=f(p);p0=tuple(x-1 for x in p);production=explicit['f'](p0)
        need(q==(None if production is None else tuple(x+1 for x in production)),('f explicit disagreement',p))
        if q is None:continue
        if n>=3:need(q==tuple(x+1 for x in recursive['f'](p0)),('f recursive disagreement',p))
        need(inv(q)==inv(p) and avoid(q,(1,3,2,4)),('map basic theorem check',p,q))
        need(q not in seen,('f collision',p,seen.get(q)));seen[q]=p;comparisons+=1
        if len(comp)==1:
            need(len(components(q))<=2,('image component observation',p,q));image_component_checks+=1
        if member and n>=7 and inv(p)<=n:need(literal(q),('low-inversion theorem check',p,q))
        if member and not literal(q):bad.append((p,q,inv(p)))
        if member and len(comp)>=2:decomposable+=1
    rows.append({'n':n,'D_total':source_count,'Av1324_f_domain':len(seen),'D_f_failures':len(bad),'D_decomposable':decomposable})
transfer_lines=(SRC/'transfer.log').read_text().splitlines()
for i,row in enumerate(rows):
    n,c=map(int,transfer_lines[i].split());need(n==row['n'] and c==row['D_f_failures'],('transfer counts',n))
for item in ast.literal_eval(transfer_lines[-1]):
    p=tuple(item['p']);q=tuple(item['f']);need(literal(p) and f(p)==q and not literal(q) and item['k']==inv(p),'transfer log witness')
small=json.loads((SRC/'independent_smallcase_results.json').read_text())
for row in small['rows']:
    need(all(row[key]==original[row['n']][key] for key in ['n','total','counts']),'smallcase counts')
need(len(small['checks'])==28,'smallcase complete set')
for row in small['checks']:
    n,k=row['n'],row['k'];need(0<=n<=6 and 0<=k<=n,'smallcase scope')
    a=original[n]['counts'];b=original[n+1]['counts']
    need(row['count_n']==(a[k] if k<len(a) else 0) and row['count_n_plus_1']==(b[k] if k<len(b) else 0),'smallcase check values')
validation=json.loads((SRC/'VALIDATION.json').read_text())
need(validation['count_file_sha256']==hashlib.sha256((SRC/'counts_extended.json').read_bytes()).hexdigest(),'validation hash')
need(validation==json.loads((SRC/'verify.log').read_text()),'verify log equals validation')
need((ROOT/'verify_normal.log').read_bytes()==(ROOT/'verify_optimized.log').read_bytes(),'normal and -O output')
result={'status':'PASS_PARTIAL_ONLY','counts_independently_regenerated_through_n':11,'last_total':original[-1]['total'],'T_checks_through_n11':sum(row['T_checks'] for row in independent),'certificate_witnesses':24,'map_implementation_comparisons':comparisons,'graph_checks':graph_checks,'subclass_inclusion_checks':subclass_checks,'image_component_checks':image_component_checks,'map_exhaustive_rows':rows,'witnesses':examples,'all_point_insertions_for_2413':25,'zero_inversion_insertions_for_2413':len(extensions),'full_conjecture':'UNRESOLVED'}
print(json.dumps(result,indent=2,sort_keys=True))
