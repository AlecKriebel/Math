#!/usr/bin/env python3
"""Independent exact audit of the six-edge finite permutation witness.

Uses only Python's standard library. No author programs, LP code or Flint
modules are imported. Every interval is checked, including possible crossings
of coordinate blocks in the middle of a segment.
"""
from bisect import bisect_right
from collections import Counter
from datetime import datetime,timezone
from hashlib import sha256
from pathlib import Path
import json

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
AUTHOR=ROOT/'root_orbit'
EXPECTED=((0,-2),(1,3),(1,-5),(6,10),(6,-12))

def integer(x):
    assert type(x) in (int,str),('not an integer',x)
    if type(x)==str: assert x.lstrip('-').isdigit()
    return int(x)

def partition(intervals,n):
    current=0
    for start,end in sorted(intervals):
        assert start==current and end>start,(current,start,end)
        current=end
    assert current==n,(current,n)

def main():
    frozen=json.loads((AUTHOR/'HEIGHT_MANIFEST.json').read_text())
    hashes={}
    for name,row in frozen['files'].items():
        p=AUTHOR/name; body=p.read_bytes()
        h=sha256(body).hexdigest()
        assert h==row['sha256'] and len(body)==row['bytes'],(name,h)
        hashes[str(p.relative_to(ROOT))]=h
    for name in ('positive_hierarchy/HEIGHT_NORM_COUNTERMODEL.md',
                 'priority/sources/merladet_minasyan2505.18054v3.html'):
        hashes[name]=sha256((ROOT/name).read_bytes()).hexdigest()
    certificate=json.loads((AUTHOR/'height_exact_multiset_certificate.json').read_text())
    maps=json.loads((AUTHOR/'height_compressed_permutations.json').read_text())
    assert tuple(map(tuple,certificate['pairs']))==EXPECTED
    assert len(certificate['support'])==certificate['symmetric_pair_count']==82
    expected=Counter()
    for row in certificate['support']:
        v=tuple(map(integer,row['triple'])); m=integer(row['pair_multiplicity'])
        assert len(v)==3 and m>0 and v!=(0,0,0)
        expected[v]+=m; expected[tuple(-c for c in v)]+=m
    n=sum(expected.values())
    assert n==integer(certificate['total_list_size'])==integer(maps['N'])==4370132
    assert len(expected)==164
    blocks=[]; reconstructed=Counter()
    for row in maps['blocks']:
        start=integer(row['start']); length=integer(row['length'])
        v=tuple(map(integer,row['triple']))
        assert len(v)==3 and 0<=start<start+length<=n
        blocks.append((start,start+length,v)); reconstructed[v]+=length
    partition([(a,b) for a,b,v in blocks],n)
    assert reconstructed==expected
    blocks.sort(); starts=[a for a,b,v in blocks]
    def block_at(j):
        assert 0<=j<n
        i=bisect_right(starts,j)-1
        a,b,v=blocks[i]
        assert a<=j<b
        return b,v
    assert any(v[0] for v in expected) and any(v[1] for v in expected)
    out=[]; coordinate_comparisons=0
    assert len(maps['permutations'])==5
    for row,(p,q) in zip(maps['permutations'],EXPECTED):
        assert (integer(row['p']),integer(row['q']))==(p,q)
        left=Counter(); right=Counter()
        for (a,b,t),m in expected.items():
            left[p*a+t]+=m; right[q*b+t]+=m
        assert left==right,(p,q,'full signed projection mismatch')
        segs=[tuple(map(integer,s)) for s in row['segments']]
        assert all(len(s)==4 and s[2]>0 for s in segs)
        partition([(s,s+length) for s,d,length,v in segs],n)
        partition([(d,d+length) for s,d,length,v in segs],n)
        checks=0; wrong_orientation=None
        for src,dst,length,value in segs:
            assert 0<=src<src+length<=n and 0<=dst<dst+length<=n
            pos=0
            while pos<length:
                se,sv=block_at(src+pos); de,dv=block_at(dst+pos)
                take=min(length-pos,se-src-pos,de-dst-pos)
                assert take>0
                # P e_j=e_{Pj}: (P v)_{Pj}=v_j.
                assert p*sv[0]+sv[2]==q*dv[1]+dv[2]==value,(p,q,src,dst,pos)
                # One exact witness that forgetting u -> P^{-1} is unsafe.
                if wrong_orientation is None and p*dv[0]+dv[2]!=q*sv[1]+sv[2]:
                    wrong_orientation={'source_index':src+pos,'destination_index':dst+pos,
                      'pA_at_destination_plus_H':p*dv[0]+dv[2],
                      'qB_at_source_plus_H':q*sv[1]+sv[2]}
                pos+=take; checks+=1
            coordinate_comparisons+=length
        assert wrong_orientation is not None
        out.append({'p':p,'q':q,'segments':len(segs),'signed_projection_values':len(left),
                    'projection_counts':{str(v):left[v] for v in sorted(left)},
                    'source_and_destination_cover_every_index_once':True,
                    'all_coordinate_block_pieces_checked':checks,
                    'wrong_orientation_falsifier':wrong_orientation})
    original=((7,1),(7,-1),(8,4),(8,-4),(13,11),(13,-11))
    assert tuple((x-7,y-1) for x,y in original[1:])==EXPECTED
    assert all(x*x+1==y*y+49 for x,y in original)
    assert all(7+(x-7)==x and 1+(y-1)==y for x,y in original)
    # Appended last coordinate is 1 on T and zero on A,B. These 2x2
    # minors certify rank2 for both vertex lattices without a large matrix.
    arow=next(v for v in expected if v[0])
    brow=next(v for v in expected if v[1])
    lattice={'a_T_minor':[[arow[0],arow[2]],[0,1]],
             'b_T_minor':[[brow[1],brow[2]],[0,1]],
             'a_t_original_minor':[[arow[0],arow[2]-7*arow[0]],[0,1]],
             'b_s_original_minor':[[brow[1],brow[2]-brow[1]],[0,1]],
             'determinants':[arow[0],brow[1],arow[0],brow[1]]}
    assert all(lattice['determinants'])
    result={'utc':datetime.now(timezone.utc).isoformat(),'verdict':'PASS',
      'scope':'Exact positive Euclidean-by-finite witness for the six-edge height-normalization example, not Pell and not all21.124.',
      'input_sha256':hashes,'support_pairs':82,'signed_support_points':len(expected),
      'N':n,'euclidean_dimension_with_height_coordinate':n+1,
      'total_permutation_coordinate_equalities_proved':coordinate_comparisons,
      'permutations':out,'vertex_lattice_rank_certificates':lattice,
      'tree_basis_check':'T=a^7 t=b s; (p,q)=(x-7,y-1); t=T a^-7,s=T b^-1',
      'semidirect_product_orientation':'u_i maps to P_i^-1, so u_i^-1 translation(v) u_i=translation(P_i v)',
      'discreteness':'All translation coordinates integral; both vertex restrictions rank2; Q finite.'}
    (HERE/'independent_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'verdict':'PASS','N':n,'signed_support':len(expected),
                     'segments':[r['segments'] for r in out],
                     'subpieces':[r['all_coordinate_block_pieces_checked'] for r in out],
                     'coordinate_equalities':coordinate_comparisons},indent=2))

if __name__=='__main__': main()
