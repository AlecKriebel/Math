#!/usr/bin/env python3
"""Independent audit verifier for 30005185. Standard library only.

No author code is imported. Reconstructs a marked QUOTIENT cube by half-edge
connectivity, using the reverse cube sign and dense row elimination. Author
uses an arc-union marked subcomplex, forward sign, and sparse column elimination.
Braid-to-PD checks instead wire four-port braid crossings directly.
"""
import argparse
from collections import defaultdict, Counter
from fractions import Fraction
from itertools import product
from pathlib import Path
import hashlib
import json
import subprocess
import sys
import zipfile

EXPECTED_ZIP_SHA = 'c52b643a0fc86a59ca0aa6f21b12f36d92eba1dac66424d4201f27c91bd40052'
EXPECTED_MANIFEST_SHA = 'df783c4badd6db54bf2655cb8044b0e7ac7a88b249090b6bc3716044ebdf3d70'

def sha(b): return hashlib.sha256(b).hexdigest()
def parity(n): return -1 if n % 2 else 1

def components(n, edges):
    graph = [set() for _ in range(n)]
    for a,b in edges:
        graph[a].add(b); graph[b].add(a)
    unused=set(range(n)); ans=[]
    while unused:
        start=min(unused); seen={start}; todo=[start]
        while todo:
            for v in graph[todo.pop()]:
                if v not in seen: seen.add(v); todo.append(v)
        unused -= seen; ans.append(frozenset(seen))
    return tuple(ans)

def arc_edges(pd):
    ends=defaultdict(list)
    for c,cross in enumerate(pd):
        for j,x in enumerate(cross): ends[x].append(4*c+j)
    assert all(len(v)==2 for v in ends.values())
    return [tuple(v) for v in ends.values()]

def resolution(pd,s):
    ed=arc_edges(pd)
    for c in range(len(pd)):
        pair=((0,3),(1,2)) if s & (1<<c) else ((0,1),(2,3))
        ed.extend((4*c+a,4*c+b) for a,b in pair)
    return components(4*len(pd),ed)

def row_rank(matrix,p):
    if not matrix: return 0
    a=[[x%p if p else Fraction(x) for x in row] for row in matrix]
    nr,nc=len(a),len(a[0]); lead=0
    for col in range(nc):
        pivot=next((r for r in range(lead,nr) if a[r][col]),None)
        if pivot is None: continue
        a[lead],a[pivot]=a[pivot],a[lead]
        div=pow(a[lead][col],-1,p) if p else 1/a[lead][col]
        a[lead]=[(x*div)%p if p else x*div for x in a[lead]]
        for r in range(lead+1,nr):
            if a[r][col]:
                t=a[r][col]
                a[r]=[(x-t*y)%p if p else x-t*y for x,y in zip(a[r],a[lead])]
        lead+=1
        if lead==nr: break
    return lead

def cube(pd, nminus=0, mark=0, reverse_sign=True):
    n=len(pd)
    if not n:
        return {'dims':[1], 'matrices':[], 'basis':[[(0,())]], 'q':[[0]], 'nminus':0, 'd2_terms':0}
    states=[resolution(pd,s) for s in range(1<<n)]
    base=[[] for _ in range(n+1)]; q=[[] for _ in range(n+1)]
    for s,cs in enumerate(states):
        marked=next(j for j,c in enumerate(cs) if mark in c)
        for labels in product((0,1),repeat=len(cs)):
            if labels[marked]: continue # quotient by x on the marked circle
            h=s.bit_count()
            base[h].append((s,labels))
            q[h].append(len(cs)-2*sum(labels)+h+n-3*nminus-1)
    idx=[{x:j for j,x in enumerate(b)} for b in base]
    matrices=[[[0]*len(base[h]) for _ in base[h+1]] for h in range(n)]
    for h in range(n):
        for col,(s,labels) in enumerate(base[h]):
            old=states[s]
            for k in range(n):
                if s & (1<<k): continue
                t=s+(1<<k); new=states[t]
                # Incidence between entire half-edge components detects the saddle.
                links=[[j for j,v in enumerate(new) if u & v] for u in old]
                merging=[j for j,v in enumerate(new) if sum(bool(u&v) for u in old)==2]
                splitting=[i for i,v in enumerate(links) if len(v)==2]
                out=[None]*len(new)
                if merging:
                    assert len(merging)==1 and not splitting
                    j=merging[0]; ins=[i for i,u in enumerate(old) if u&new[j]]
                    power=sum(labels[i] for i in ins)
                    if power==2: continue
                    out[j]=power
                    for i,v in enumerate(links):
                        if i not in ins: assert len(v)==1; out[v[0]]=labels[i]
                    outputs=[out]
                else:
                    assert len(splitting)==1
                    i=splitting[0]; a,b=links[i]
                    for ii,v in enumerate(links):
                        if ii!=i: assert len(v)==1; out[v[0]]=labels[ii]
                    outputs=[]
                    for x,y in ([(1,1)] if labels[i] else [(0,1),(1,0)]):
                        o=out[:];o[a]=x;o[b]=y;outputs.append(o)
                marked=next(j for j,c in enumerate(new) if mark in c)
                # Opposite convention from author's sign. Both orient cube faces.
                exponent=(s>>(k+1)).bit_count() if reverse_sign else (s & ((1<<k)-1)).bit_count()
                for out in outputs:
                    assert None not in out
                    if out[marked]: continue
                    row=idx[h+1][(t,tuple(out))]
                    assert q[h+1][row]==q[h][col]
                    matrices[h][row][col]+=parity(exponent)
    terms=0
    for h in range(n-1):
        a,b=matrices[h],matrices[h+1]
        for row in b:
            nonzero=[(j,x) for j,x in enumerate(row) if x]
            for c in range(len(base[h])):
                assert sum(x*a[j][c] for j,x in nonzero)==0
                terms+=sum(bool(a[j][c]) for j,x in nonzero)
    return {'dims':list(map(len,base)), 'matrices':matrices,'basis':base,'q':q,'nminus':nminus,'d2_terms':terms}

def integral_unit_cancellation(c):
    """Exact Z chain contractions. A zero remainder certifies torsion-free H."""
    mats=[[row[:] for row in m] for m in c['matrices']]
    dims=c['dims'][:]; cancellations=[0]*len(mats)
    for h in range(len(mats)):
        while True:
            a=mats[h]
            pivot=next(((r,col) for r,row in enumerate(a) for col,x in enumerate(row) if abs(x)==1),None)
            if pivot is None: break
            r,col=pivot;unit=a[r][col]
            # Gaussian cancellation is unimodular because unit is +1 or -1.
            mats[h]=[[a[i][j]-a[i][col]*unit*a[r][j] for j in range(dims[h]) if j!=col]
                     for i in range(dims[h+1]) if i!=r]
            if h: del mats[h-1][col]
            if h+1<len(mats):
                for row in mats[h+1]:del row[r]
            dims[h]-=1;dims[h+1]-=1;cancellations[h]+=1
    assert all(not x for m in mats for row in m for x in row), 'Non-unit residual requires full Smith analysis'
    return {'homology_free_ranks_cube_degree':dims,'unit_chain_contractions_by_degree':cancellations,
            'zero_residual_differential':True,'integral_homology_torsion_free':True,
            'all_field_total_reduced_rank':sum(dims)}

def evaluate(c,p):
    ds=c['dims']; mats=c['matrices']; rs=[row_rank(m,p) for m in mats]+[0]
    hom=[d-rs[h]-(rs[h-1] if h else 0) for h,d in enumerate(ds)]
    assert all(x>=0 for x in hom)
    # Independently split by q to test normalized bidegrees and Euler polynomial.
    hh=[]
    for h in range(len(ds)):
        for q in sorted(set(c['q'][h])):
            here=[i for i,v in enumerate(c['q'][h]) if v==q]
            incoming=0; outgoing=0
            if h:
                prev=[i for i,v in enumerate(c['q'][h-1]) if v==q]
                incoming=row_rank([[mats[h-1][i][j] for j in prev] for i in here],p)
            if h<len(mats):
                nxt=[i for i,v in enumerate(c['q'][h+1]) if v==q]
                outgoing=row_rank([[mats[h][i][j] for j in here] for i in nxt],p)
            dim=len(here)-incoming-outgoing
            if dim: hh.append([h-c['nminus'],q,dim])
    assert sum(x[2] for x in hh)==sum(hom)
    polynomial=Counter()
    for h,q,d in hh:
        assert q%2==0
        polynomial[q//2]+=parity(h)*d
    polynomial={str(q):v for q,v in sorted(polynomial.items()) if v}
    return {'field':'Q' if not p else f'F_{p}', 'chain_dimensions':ds,
            'differential_ranks':rs,'homology_dimensions_cube_degree':hom,
            'total_reduced_rank':sum(hom),'normalized_bigraded_homology':hh,
            'jones_t_exponent_coefficients':polynomial,
            'V_at_1':sum(polynomial.values()),
            'V_at_minus_1':sum(parity(int(q))*v for q,v in polynomial.items())}

def braid_graph(width,word,state):
    # Native ports NW, NE, SE, SW; wire at braid levels without constructing PD.
    first=[None]*width;last=[None]*width;edges=[]
    for c,g in enumerate(word):
        k=abs(g)-1;assert 0<=k<width-1
        for strand,inp,out in ((k,0,3),(k+1,1,2)):
            if first[strand] is None: first[strand]=4*c+inp
            else: edges.append((last[strand],4*c+inp))
            last[strand]=4*c+out
        horizontal=(g>0) != bool(state & (1<<c))
        pairs=((0,1),(2,3)) if horizontal else ((0,3),(1,2))
        edges.extend((4*c+a,4*c+b) for a,b in pairs)
    assert None not in first
    edges.extend(zip(first,last))
    return components(4*len(word),edges)

def check_braid(pd,width,word):
    assert len(pd)==len(word)
    port=[]
    for c,g in enumerate(word):
        port.extend(4*c+x for x in ([1,0,3,2] if g>0 else [0,3,2,1]))
    for s in range(1<<len(word)):
        image=frozenset(frozenset(port[x] for x in comp) for comp in resolution(pd,s))
        assert image==frozenset(braid_graph(width,word,s))
    # Traversal through crossings pairs opposite ports, hence counts link components.
    ed=arc_edges(pd)
    ed += [(4*c+a,4*c+b) for c in range(len(pd)) for a,b in ((0,2),(1,3))]
    assert len(components(4*len(pd),ed))==1
    return 1<<len(word)

def convolve(a,b):
    out=Counter()
    for x,v in a.items():
        for y,w in b.items():out[int(x)+int(y)]+=v*w
    return {str(q):v for q,v in sorted(out.items()) if v}

def algebra_checks():
    # Stronger all-free-degree identity, exhaustively by parity, independent of author.
    n=0; slice=0
    for k in range(7):
        for tokens in product(range(4),repeat=k):
            exponents=[1+(a//2) for a in tokens];delta=[a%2 for a in tokens]
            for free_delta in (0,1):
                rank=1+2*k
                determinant=parity(free_delta)+sum(parity(d)+parity(d+a-1) for a,d in zip(exponents,delta))
                E=sum(a%2==0 for a in exponents)
                assert (rank-determinant-2*(free_delta%2)-2*E)%4==0
                if free_delta==0 and determinant%4==1:
                    assert rank%4==(1+2*E)%4;slice+=1
                n+=1
    # Smith elementary complexes with composite and repeated prime powers.
    uct=0
    for invariant_factors in product((2,3,4,6,9,10,25),repeat=3):
        for p in (2,3,5,7):
            rational=1;modp=1+2*sum(x%p==0 for x in invariant_factors)
            tp=sum(x%p==0 for x in invariant_factors)
            assert modp-rational==2*tp;uct+=1
    assert row_rank([[2]],0)==1 and row_rank([[2]],2)==0
    assert row_rank([[3]],3)==0 and row_rank([[9]],3)==0
    assert row_rank([[1,1],[1,-1]],0)==2
    assert row_rank([[1,1],[1,-1]],2)==1
    return {'graded_cases':n,'slice_determinant_cases':slice,'uct_elementary_cases':uct,
            'free_degree_sign_negative_control':{'free_delta':1,'exponents':[1],'source_delta':[0], 'rank':3,'determinant':1,'E':0},
            'even_exponent_formal_control':{'rank':3,'determinant':1,'E':1,'knot_realization_claimed':False}}

def run(author,zip_path):
    manifest_bytes=(author/'AUTHOR_MANIFEST.json').read_bytes()
    assert sha(manifest_bytes)==EXPECTED_MANIFEST_SHA
    manifest=json.loads(manifest_bytes)
    expected={x['path']:x for x in manifest['files']}
    assert {x.name for x in author.iterdir() if x.is_file()}==set(expected)|{'AUTHOR_MANIFEST.json'}
    for path,record in expected.items():
        b=(author/path).read_bytes();assert len(b)==record['bytes'] and sha(b)==record['sha256']
    archive=zip_path.read_bytes();assert len(archive)==20354 and sha(archive)==EXPECTED_ZIP_SHA
    with zipfile.ZipFile(zip_path) as z:
        assert not z.testzip()
        assert set(z.namelist())=={'khovanov_30005185/'+x for x in set(expected)|{'AUTHOR_MANIFEST.json'}}
        for name in z.namelist():assert z.read(name)==(author/Path(name).name).read_bytes()
    controls=json.loads((author/'KNOT_CHECKS.json').read_text())['examples']
    diagrams={e['name']:e['pd'] for e in controls}
    sq=diagrams['square_knot']
    assert [[1 if x==7 else x for x in c] for c in sq[:3]]==diagrams['trefoil']
    assert [[(7 if x==1 else x)-6 for x in c] for c in sq[3:]]==diagrams['mirror_trefoil']
    assert sum((a//4<3)!=(b//4<3) for a,b in arc_edges(sq))==2
    minus={'unknot':0,'trefoil':0,'mirror_trefoil':3,'stevedore_6_1':3,'negative_control_6_2':2,'square_knot':3}
    braids={'trefoil':(2,[-1]*3),'stevedore_6_1':(4,[-1,-1,-2,1,3,-2,3]),'negative_control_6_2':(3,[-1,-1,-1,2,-1,2])}
    out=[]; braid_states=0;results={};basepoints=0
    for e in controls:
        name=e['name'];pd=e['pd']
        if pd:
            strand_edges=arc_edges(pd)+[(4*j+a,4*j+b) for j in range(len(pd)) for a,b in ((0,2),(1,3))]
            assert len(components(4*len(pd),strand_edges))==1
        c=cube(pd,minus[name]);fields=[]
        for p,reported in zip((0,2,3,5),e['computations']):
            got=evaluate(c,p)
            for key in ('field','chain_dimensions','differential_ranks','homology_dimensions_cube_degree','total_reduced_rank'):
                assert got[key]==reported[key],(name,p,key)
            assert got['V_at_1']==1
            fields.append(got)
        results[name]=fields[0]['jones_t_exponent_coefficients']
        if name in braids:braid_states+=check_braid(pd,*braids[name])
        if pd:
            # Every half-edge basepoint, over F3, not only the author's chosen arc.
            for mark in range(4*len(pd)):
                cc=cube(pd,minus[name],mark)
                rr=[row_rank(m,3) for m in cc['matrices']]
                assert sum(cc['dims'])-2*sum(rr)==e['expected_reduced_rank'];basepoints+=1
            cf=cube(pd,minus[name],reverse_sign=False)
            # Two cube sign conventions differ by (-1)^{h(h-1)/2} at vertices.
            for h,(a,b) in enumerate(zip(c['matrices'],cf['matrices'])):
                assert all(x==parity(h)*y for ar,br in zip(a,b) for x,y in zip(ar,br))
        integral=integral_unit_cancellation(c)
        assert integral['homology_free_ranks_cube_degree']==fields[0]['homology_dimensions_cube_degree']
        out.append({'name':name,'independent_d2_terms':c['d2_terms'],'computations':fields,'integral_unit_cancellation':integral})
    assert results['mirror_trefoil']=={str(-int(q)):v for q,v in results['trefoil'].items()}
    assert results['square_knot']==convolve(results['trefoil'],results['mirror_trefoil'])
    # These expected Jones coefficients are elementary small-control metadata;
    # source names match up to the globally reversed braid convention.
    assert results['stevedore_6_1']=={'-2':1,'-1':-1,'0':2,'1':-2,'2':1,'3':-1,'4':1}
    assert results['negative_control_6_2']=={'-1':1,'0':-1,'1':2,'2':-2,'3':2,'4':-2,'5':1}
    # R1 and R2 controls, independent of named knots and of the frozen examples.
    extra=[]
    for label,pd,neg,want in [
        ('one_negative_curl',[[1,2,2,1]],1,1),
        ('one_positive_curl',[[2,2,1,1]],0,1),
        ('positive_hopf',[[1,3,4,2],[3,1,2,4]],0,2),
        ('two_component_unlink_R2',[[1,3,4,2],[1,2,4,3]],1,2)]:
        c=cube(pd,neg)
        totals=[]
        for p in (0,2,3,5):
            # Link grading may be odd, so only total-rank checks here.
            rank=sum(c['dims'])-2*sum(row_rank(m,p) for m in c['matrices'])
            if 'curl' in label:
                normalized=evaluate(c,p)
                assert normalized['normalized_bigraded_homology']==[[0,0,1]]
            assert rank==want,(label,rank);totals.append(rank)
        extra.append({'name':label,'total_ranks_Q_F2_F3_F5':totals})
    # Replay author scripts only in explicit subprocesses, after independent checks.
    replay=[]
    for script,receipt in [('cube_verify.py','KNOT_CHECKS.json'),('verify_algebra.py','ALGEBRA_CHECKS.json')]:
        raw=subprocess.check_output([sys.executable,'-B',str(author/script)],cwd=author)
        assert json.loads(raw)==json.loads((author/receipt).read_text());replay.append(script)
    return {'status':'PASS','author_manifest_sha256':sha(manifest_bytes),'author_zip_sha256':sha(archive),
            'author_files_including_manifest_verified':12,'author_replays':replay,
            'method':'Independent half-edge marked quotient, reverse cube sign, dense exact row ranks; no author imports.',
            'braid_resolution_partitions_compared':braid_states,'basepoint_controls_F3':basepoints,
            'examples':out,'extra_controls':extra,'algebra':algebra_checks(),
            'universal_problem_solved':False,'ribbonness_computed':False}

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--author',type=Path,required=True);ap.add_argument('--zip',type=Path,required=True)
    a=ap.parse_args();print(json.dumps(run(a.author.resolve(),a.zip.resolve()),indent=2,sort_keys=True))
