#!/usr/bin/env python3
"""Independent exact diagnostics; no import from the author's checker.

Requires SymPy. This does not claim to prove the all-ranks theorem by testing.
"""
import itertools as it
import json
import sympy as s


def analyze(rows):
    n=len(rows); width=len(rows[0]); zero=s.zeros(0,width)
    mats=[s.Matrix([rows[i] for i in range(n) if mask>>i&1]) if mask else zero for mask in range(1<<n)]
    ranks=[m.rank() for m in mats]
    full=(1<<n)-1
    closures=[sum(1<<i for i in range(n) if ranks[mask|1<<i]==ranks[mask]) for mask in range(1<<n)]
    flats=[mask for mask in range(1<<n) if closures[mask]==mask]
    lines=[mask for mask in flats if ranks[mask]==2]
    long=[mask for mask in lines if mask.bit_count()>2]
    rels=[]
    for mask in long:
        ids=[i for i in range(n) if mask>>i&1]
        for v in mats[mask].T.nullspace():
            row=[0]*n
            for j,i in enumerate(ids):row[i]=v[j]
            rels.append(row)
    relrank=s.Matrix(rels).rank() if rels else 0
    modular=[mask for mask in flats if all(ranks[mask]+ranks[t]==ranks[mask|t]+ranks[mask&t] for t in flats)]
    chains={0:[]}
    for k in range(1,ranks[full]+1):
        for mask in modular:
            if ranks[mask]!=k:continue
            for prev in list(chains):
                if ranks[prev]==k-1 and prev&mask==prev:
                    chains[mask]=chains[prev]+[mask];break
    return {'n':n,'rank':int(ranks[full]),'relation_rank':int(relrank),
            'formal':relrank==n-ranks[full],
            'long_lines':[[i for i in range(n) if mask>>i&1] for mask in long],
            'supersolvable':full in chains,'flat_count':len(flats),
            'modular_chain_masks':chains.get(full)},ranks,modular


def homogeneous_certificate(forms, variables, degree):
    mons=[]
    for powers in it.product(range(degree),repeat=len(variables)):
        if sum(powers)==degree-1:mons.append(s.prod(v**e for v,e in zip(variables,powers)))
    cs=s.symbols('c:'+str(len(variables)*len(mons)))
    coeff=[v*sum(cs[i*len(mons)+j]*m for j,m in enumerate(mons)) for i,v in enumerate(variables)]
    equations=[]
    for f in forms:
        v=next(v for v in variables if s.diff(f,v))
        image=sum(s.diff(f,vv)*a for vv,a in zip(variables,coeff))
        rem=s.expand(image.subs(v,s.solve(f,v)[0]))
        equations.extend(s.Poly(rem,*variables).coeffs())
    matrix,_=s.linear_eq_to_matrix(equations,cs)
    space=matrix.nullspace()
    basis=[s.Matrix([s.expand(a.subs(dict(zip(cs,b)))) for a in coeff]) for b in space]
    Q=s.prod(forms); euler=s.Matrix(variables)
    for left,right in it.combinations(basis,2):
        det=s.factor(s.Matrix.hstack(euler,left,right).det())
        if det:
            factor=s.cancel(det/Q)
            assert not factor.free_symbols and factor!=0
            for theta in (euler,left,right):
                for f in forms:
                    v=next(v for v in variables if s.diff(f,v))
                    rem=s.expand(sum(s.diff(f,vv)*a for vv,a in zip(variables,theta)).subs(v,s.solve(f,v)[0]))
                    assert s.expand(rem)==0
            return {'basis':[list(map(str,t)) for t in (euler,left,right)],'degrees':[1,degree,degree],
                    'determinant_over_Q':str(factor),'logarithmic_checks':3*len(forms)}
    raise AssertionError('No Saito certificate found')


def main():
    r=s.symbols('r',integer=True,positive=True)
    arithmetic=[]
    for n,total_sq,b2,defect in [(2*r-1,4*r-3,2*(r-1)**2,r-1),(2*r,4*r+2,2*r*r-2*r-1,r+1)]:
        assert s.expand((n*n-total_sq)/2-b2)==0
        assert s.expand(n*(n-1)/2-b2-defect)==0
        arithmetic.append({'n':str(n),'b2':str(b2),'defect':str(defect)})
    t=s.symbols('t',nonzero=True)
    normal=s.Matrix([[1,0,0],[0,1,0],[1,1,0],[0,0,1],[1,0,t],[0,1,-t]])
    relations=s.Matrix([[1,1,-1,0,0,0],[1,0,0,t,-1,0],[0,1,0,-t,0,-1],[0,0,1,0,-1,-1]])
    assert relations*normal==s.zeros(4,3)
    assert relations.rank()==3
    assert all(relations[list(ids),:].rank()==3 for ids in it.combinations(range(4),3))
    assert s.Matrix([[1,1,0],[1,0,t],[0,1,-t]]).det()==0
    fixtures={
      'k4_alternate_normalization':[[1,0,0],[0,1,0],[1,1,0],[0,0,1],[1,0,2],[0,1,-2]],
      'four_pencil_with_nonunit_attachment':[[1,0,0],[0,1,0],[1,1,0],[2,3,0],[0,0,1],[2,3,5]],
      'k4_with_nonunit_attachment':[[1,0,0,0],[0,1,0,0],[1,1,0,0],[0,0,1,0],[1,0,2,0],[0,1,-2,0],[0,0,0,1],[2,0,4,3]],
      'nonformal_false_pruning_control':[[1,0,0],[0,1,0],[1,2,3],[2,5,11],[0,0,1],[1,0,1]],
      'nonfano_boundary':[[1,0,0],[0,1,0],[0,0,1],[1,-1,0],[1,0,-1],[0,1,-1],[1,1,-1]],
    }
    outputs={}
    for name,rows in fixtures.items():
        out,ranks,modular=analyze(rows);outputs[name]=out
        if name=='nonformal_false_pruning_control':
            assert not out['formal'] and out['long_lines']==[[0,4,5]]
            assert ranks[(1<<4)-1]==3
            out['retained_rank_after_terminal_triple_removal']=3
            out['warning']='Without formality, terminal-pencil pruning need not lower rank.'
        else:
            assert out['formal']
            assert out['supersolvable']==(name!='nonfano_boundary')
        if name.endswith('attachment'):
            old=(1<<(len(rows)-2))-1
            assert old in modular and ranks[old]==out['rank']-1
            out['retained_flat_is_modular_coatom']=True
    x,y,z=s.symbols('x y z')
    nf=homogeneous_certificate([x,y,z,x-y,x-z,y-z,x+y-z],(x,y,z),3)
    print(json.dumps({'symbolic_arithmetic':arithmetic,'symbolic_k4_minimal_dependency':True,
      'independent_fixtures':outputs,'nonfano_saito_certificate':nf,
      'interpretation':'Independent finite diagnostics and symbolic identities; universal proof assessed separately.'},indent=2))

if __name__=='__main__':main()
