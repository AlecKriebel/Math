#!/usr/bin/env python3
"""Independent pure-Python quotient-Koszul audit of the frozen samples.
Reads public JSON, writes only beside this file. No author code imported.
"""
from itertools import combinations, combinations_with_replacement, product
from pathlib import Path
import json, math, hashlib
ROOT=Path(__file__).resolve().parent
PUBLIC=ROOT.parent/'public'

def echelon(vectors,p):
    basis={}
    for vector in vectors:
        row=[x%p for x in vector]
        for j,b in sorted(basis.items()):
            if row[j]:
                c=row[j];row=[(x-c*y)%p for x,y in zip(row,b)]
        pivot=next((j for j,x in enumerate(row) if x),None)
        if pivot is None:continue
        c=pow(row[pivot],-1,p);row=[c*x%p for x in row]
        # Maintain reduced pivots, so quotient reduction is direct.
        for j,b in list(basis.items()):
            if b[pivot]:
                c=b[pivot];basis[j]=[(x-c*y)%p for x,y in zip(b,row)]
        basis[pivot]=row
    return basis

def exponents(n,d):
    # Deliberately different generator order from the author script.
    if n==1:
        yield (d,);return
    for a in range(d,-1,-1):
        for b in exponents(n-1,d-a):yield (a,)+b

def quotient_spaces(M,p):
    sqfree={r:list(combinations(range(4),r)) for r in range(5)}
    cross=list(reversed(list(combinations(range(4),2))))
    # Author's ascending lexicographic exponent order corresponds to this order:
    cross=[tuple(i for i,a in enumerate(v) if a) for v in sorted(exponents(4,2)) if max(v)<2]
    bases={}; free={}
    for r in range(5):
        idx={a:i for i,a in enumerate(sqfree[r])};relations=[]
        if r>=2:
            for row in M:
                for b in sqfree[r-2]:
                    v=[0]*len(idx)
                    for a,c in zip(cross,row):
                        if not set(a)&set(b):v[idx[tuple(sorted(a+b))]]+=c
                    relations.append(v)
        bases[r]=echelon(relations,p)
        free[r]=[j for j in range(len(idx)) if j not in bases[r]]
    def multiply(r,basis_index,var):
        if not 0<=r<4:return []
        a=sqfree[r][free[r][basis_index]]
        v=[0]*len(sqfree[r+1])
        if var not in a:v[sqfree[r+1].index(tuple(sorted(a+(var,))))]=1
        for j,row in sorted(bases[r+1].items()):
            if v[j]:
                c=v[j];v=[(x-c*y)%p for x,y in zip(v,row)]
        return [v[j] for j in free[r+1]]
    return [len(free[r]) for r in range(5)],multiply

def koszul_rank(h,e,dims,multiply,p):
    a=e-h
    if a<0 or a>4:return 0
    source=list(combinations(range(4),h));target=list(combinations(range(4),h-1))
    targetdim=dims[a+1] if 0<=a+1<=4 else 0
    columns=[]
    for wedge in source:
        for b in range(dims[a]):
            v=[0]*(len(target)*targetdim)
            for j,var in enumerate(wedge):
                tw=wedge[:j]+wedge[j+1:];offset=target.index(tw)*targetdim
                for k,c in enumerate(multiply(a,b,var)):
                    v[offset+k]=(v[offset+k]+(-1)**j*c)%p
            columns.append(v)
    return len(echelon(columns,p))

def multiply_polys(a,b,p):
    c={}
    for u,x in a.items():
        for v,y in b.items():
            w=tuple(i+j for i,j in zip(u,v));c[w]=(c.get(w,0)+x*y)%p
    return {w:x for w,x in c.items() if x}

def cube_rank(M,p):
    mon=list(exponents(4,2));cross=[v for v in sorted(mon) if max(v)<2]
    gs=[{v:1} for v in mon if max(v)==2]
    gs += [{v:c for v,c in zip(cross,row) if c} for row in M]
    target=list(exponents(4,6));vectors=[]
    for ids in combinations_with_replacement(range(len(gs)),3):
        f={(0,0,0,0):1}
        for i in ids:f=multiply_polys(f,gs[i],p)
        vectors.append([f.get(v,0) for v in target])
    return len(echelon(vectors,p))

def main():
    data=json.loads((PUBLIC/'control-results.json').read_text());records=[]
    for old in data['finite_field_samples']:
        p=old['field'];M=old['cross_matrix'];dims,mul=quotient_spaces(M,p)
        betti={}
        for e in range(3,7):
            k2=math.comb(4,2)*(dims[e-2] if 0<=e-2<=4 else 0)
            betti[e]=k2-koszul_rank(2,e,dims,mul,p)-koszul_rank(3,e,dims,mul,p)
            assert betti[e]>=0
        linear=all(betti[e]==0 for e in range(4,7));rank=cube_rank(M,p)
        assert linear==old['linearly_presented']
        assert betti[3]==old['linear_syzygies']
        assert rank==old['cube_rank']
        records.append({'p':p,'cross_dim':old['cross_dim'],'trial':old['trial'],'quotient_hilbert_function':dims,'betti_2_graded':betti,'linearly_presented':linear,'cube_rank':rank})
    # Degree-2 example: verify cubic annihilation and target square over many p.
    gs=[{(2,0,0):1,(0,0,2):-1},{(0,2,0):1,(0,0,2):-1},{(1,1,0):1},{(1,0,1):1},{(0,1,1):1}]
    explicit=[]
    for p in (2,3,5,7,11,101):
        m4=list(exponents(3,4));vs=[]
        for i,j in combinations_with_replacement(range(5),2):
            f=multiply_polys(gs[i],gs[j],p);vs.append([f.get(m,0) for m in m4])
        rank=len(echelon(vs,p));assert rank==15
        explicit.append({'p':p,'square_rank':rank,'target_dimension':15})
    out={'method':'independent pure-Python quotient Koszul homology and polynomial products; no author code imported','sample_count':len(records),'certified_linear':sum(v['linearly_presented'] for v in records),'all_recorded_linearity_and_cube_ranks_match':True,'records':records,'explicit_example_square_checks':explicit}
    (ROOT/'INDEPENDENT_CONTROL_RESULTS.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k not in ('records','explicit_example_square_checks')},indent=2))
if __name__=='__main__':main()
