#!/usr/bin/env python3
"""Exact cyclotomic component checks; see ABELIAN_HOLONOMY_DELTA.md."""
from itertools import combinations,product
from pathlib import Path
from datetime import datetime,timezone
import json
COEFF=[-99,812,-714,-714,820,-105]

def roots60():
    # Phi_60(x)=x^16+x^14-x^10-x^8-x^6+x^2+1.
    phi={14:1,10:-1,8:-1,6:-1,2:1,0:1}
    out=[];v=[0]*16;v[0]=1
    for k in range(60):
        out.append(tuple(v));top=v[-1];v=[0]+v[:-1]
        if top:
            for j,c in phi.items():v[j]-=top*c
    assert v==list(out[0])
    return out

def run():
    R=roots60();solutions=[]
    for x,y,z in product(range(60),repeat=3):
        es=[x,y,z,(x+y)%60,(x+z)%60,(y+z)%60]
        val=[sum(c*R[e][j] for c,e in zip(COEFF,es)) for j in range(16)]
        if not any(val):solutions.append([x,y,z])
    abscoeff=list(map(abs,COEFF));triples=[]
    for inds in combinations(range(6),3):
        vals=[abscoeff[i] for i in inds]
        # Minimal three-term rational root-of-unity relations have equal magnitudes
        # or a collinear cancellation in which one magnitude is the sum of the other two.
        # Reducible three-term relations cannot occur with all three coefficients nonzero.
        if len(set(vals))==1 or 2*max(vals)==sum(vals):triples.append(inds)
    pair_equal=[list(ij) for ij in combinations(range(6),2) if abscoeff[ij[0]]==abscoeff[ij[1]]]
    return {'utc':datetime.now(timezone.utc).isoformat(),'result':'PASS_ENUMERATION_ONLY','cyclotomic_polynomial':[1,0,1,0,0,0,-1,0,-1,0,-1,0,0,0,1,0,1],'order60_triples_checked':60**3,'determinant_zero_exponents':solutions,'equal_magnitude_pairs':pair_equal,'possible_vanishing_triples':triples,'scope':'The enumeration is exact in Q(zeta60). Completeness for arbitrary roots of unity requires the separate written minimal-relation/Mann argument; it is not established by this script alone.'}

if __name__=='__main__':
    result=run();Path(__file__).with_name('abelian_holonomy_certificate.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
