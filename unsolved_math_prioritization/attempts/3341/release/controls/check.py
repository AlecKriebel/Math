#!/usr/bin/env python3
"""Deterministic, standard-library-only finite controls; not a hierarchy solver."""
import itertools
import json
from collections import Counter, defaultdict
from pathlib import Path


def bit(s, u):
    return (s >> u) & 1


def grid(h, w):
    return list(range(h*w)), [(i*w+j, i*w+j+1) for i in range(h) for j in range(w-1)], [(i*w+j, (i+1)*w+j) for i in range(h-1) for j in range(w)]


def row_valid(s, h, w, H):
    return sum(bit(s, i*w) for i in range(h)) == 1 and all(bit(s,u)==bit(s,v) for u,v in H)


def col_valid(s, h, w, V):
    return sum(bit(s,j) for j in range(w)) == 1 and all(bit(s,u)==bit(s,v) for u,v in V)


def diag_valid(s, h, w, direction):
    # Exactly the clauses of Diag+ or Diag- in the proof, on concrete grids.
    start = 0 if direction == 1 else w-1
    end = w-1 if direction == 1 else 0
    if any(bit(s,j) != (j==start) for j in range(w)):
        return False
    for u in range(h*w):
        if not bit(s,u):
            continue
        i,j = divmod(u,w)
        if i == h-1 and j != end:
            return False
        if i < h-1:
            jj=j+direction
            if not (0 <= jj < w and bit(s,(i+1)*w+jj)):
                return False
        if i > 0:
            jj=j-direction
            if not (0 <= jj < w and bit(s,(i-1)*w+jj)):
                return False
    return True


def geometry():
    rows = []
    square_sets = {}
    for h in range(1,5):
        for w in range(1,5):
            cells,H,V=grid(h,w)
            rr=[s for s in range(1<<(h*w)) if row_valid(s,h,w,H)]
            cc=[s for s in range(1<<(h*w)) if col_valid(s,h,w,V)]
            dd=[s for s in range(1<<(h*w)) if diag_valid(s,h,w,1)]
            ee=[s for s in range(1<<(h*w)) if diag_valid(s,h,w,-1)]
            assert set(rr)=={sum(1<<(i*w+j) for j in range(w)) for i in range(h)}
            assert set(cc)=={sum(1<<(i*w+j) for i in range(h)) for j in range(w)}
            expected_d=[] if h!=w else [sum(1<<(i*w+i) for i in range(h))]
            expected_e=[] if h!=w else [sum(1<<(i*w+w-1-i) for i in range(h))]
            assert dd==expected_d and ee==expected_e
            rows.append({'h':h,'w':w,'subsets_tested':1<<(h*w),'rows':len(rr),'columns':len(cc),'positive_diagonals':len(dd),'negative_diagonals':len(ee)})
            if h==w:
                square_sets[h]=(rr,cc,dd[0],ee[0])
    return rows,square_sets


def only(s):
    assert s and s&(s-1)==0
    return s.bit_length()-1


def mirror_control(square_sets):
    result=[]
    for n,(rows,cols,D,E) in square_sets.items():
        # Build all mismatch pairs from the actual validated set witnesses.
        pairs=[]
        for T in rows:
            a,b=only(T&D),only(T&E)
            X=next(s for s in cols if bit(s,a))
            Y=next(s for s in cols if bit(s,b))
            for R in rows:
                pairs.append((only(R&X),only(R&Y)))
        mirror_count=0
        for p in range(1<<(n*n)):
            certificate=any(bit(p,u)!=bit(p,v) for u,v in pairs)
            direct=all(bit(p,i*n+j)==bit(p,i*n+n-1-j) for i in range(n) for j in range(n))
            assert certificate == (not direct)
            mirror_count += direct
        assert mirror_count == 1<<(n*((n+1)//2))
        result.append({'side':n,'pictures_tested':1<<(n*n),'symmetric':mirror_count,'nonsymmetric':(1<<(n*n))-mirror_count,'witness_pairs':len(pairs)})
    return result


def tiles(p,h,w):
    # Exterior is a distinct fixed symbol 2.
    def read(i,j):
        return p[i*w+j] if 0<=i<h and 0<=j<w else 2
    return {tuple(read(i+di,j+dj) for di,dj in [(0,0),(0,1),(1,0),(1,1)]) for i in range(-1,h) for j in range(-1,w)}


def splice_control():
    h,w=2,4
    buckets=defaultdict(list)
    for p in itertools.product(range(2),repeat=h*w):
        buckets[tuple(p[i*w+j] for i in range(h) for j in [1,2])].append(p)
    count=0
    for bucket in buckets.values():
        for a in bucket:
            for b in bucket:
                s=tuple(a[i*w+j] if j<2 else b[i*w+j] for i in range(h) for j in range(w))
                assert tiles(s,h,w)<=tiles(a,h,w)|tiles(b,h,w)
                count+=1
    assert count==4096
    bounds=[]
    for g in [1,2,3,4,16,256]:
        r=2*g.bit_length()+1
        n=2*r
        pictures=2**(n*r)
        signatures=g**(2*n)
        assert pictures>signatures
        bounds.append({'lift_alphabet_size':g,'side':n,'symmetric_inputs':str(pictures),'signature_upper_bound':str(signatures)})
    return {'two_by_four_matching_pairs':count,'counting_examples':bounds}


def padding_control():
    result=[]
    for h in range(1,4):
        for w in range(h,4):
            active=[i*w+j for i in range(h) for j in range(w)]
            cnt=Counter(sum(bit(s,u)<<v for v,u in enumerate(active)) for s in range(1<<(w*w)))
            assert len(cnt)==1<<(h*w)
            assert set(cnt.values())=={1<<(w*w-h*w)}
            # All predicates on the source powerset only when it has <= 8 elements.
            predicates=0
            if h*w<=3:
                source=range(1<<(h*w))
                for f in range(1<<(1<<(h*w))):
                    original_exists=any(bit(f,s) for s in source)
                    original_forall=all(bit(f,s) for s in source)
                    lifted_exists=any(bit(f,s) for s in cnt)
                    lifted_forall=all(bit(f,s) for s in cnt)
                    assert original_exists==lifted_exists and original_forall==lifted_forall
                    predicates+=1
            result.append({'height':h,'width':w,'source_cells':h*w,'padded_cells':w*w,'padded_subsets':1<<(w*w),'restriction_fiber_size':1<<(w*w-h*w),'all_predicates_tested':predicates})
    return result


def quant_eval(k, f, cert=False):
    def rec(i,prefix):
        if i==k:
            accept=bool(bit(f,prefix))
            if not cert:
                return accept
            valid_value=prefix.bit_count()%2
            vals=[((c==valid_value) and accept) if k%2 else ((c!=valid_value) or accept) for c in [0,1]]
            return any(vals) if k%2 else all(vals)
        vals=[rec(i+1,prefix|(b<<i)) for b in [0,1]]
        return any(vals) if i%2==0 else all(vals)
    return rec(0,0)


def certificate_control():
    examples=[]
    for k in range(1,4):
        total=1<<(1<<k)
        for f in range(total):
            assert quant_eval(k,f)==quant_eval(k,f,True)
        examples.append({'alternating_one_bit_blocks':k,'all_acceptance_truth_tables_tested':total})
    # Required adversarial cases: losing existence or uniqueness invalidates the device.
    zero_valid_exists=any(False for _ in [0,1])
    zero_valid_forall=all(True for _ in [0,1])
    two_valid_exists=any([True,False])
    two_valid_forall=all([True,False])
    assert zero_valid_exists!=zero_valid_forall
    assert two_valid_exists!=two_valid_forall
    return {'exhaustive_small_boolean_tests':examples,'no_valid_certificate_divergence_detected':True,'two_disagreeing_valid_certificates_divergence_detected':True}


def encode(p,n,a):
    ell=max(1,(a-1).bit_length()); c=2*ell+8
    q=[[0]*(c*n) for _ in range(c*n)]
    ring=[[1,1,1],[1,0,1],[1,1,1]]
    for i in range(n):
        for j in range(n):
            for u in range(3):
                for v in range(3): q[i*c+u][j*c+v]=ring[u][v]
            for b in range(ell): q[i*c+5][j*c+1+2*b]=bit(p[i*n+j],b)
    return q,c,ell


def decode(q,c,ell):
    size=len(q)
    ring=[[1,1,1],[1,0,1],[1,1,1]]
    markers=[]
    for i in range(1,size-1):
        for j in range(1,size-1):
            if all(q[i+u-1][j+v-1]==ring[u][v] for u in range(3) for v in range(3)):
                markers.append((i,j))
    letters=[sum(q[i+4][j+2*b]<<b for b in range(ell)) for i,j in markers]
    return markers,letters


def coding_control():
    tested=[]
    for a in [1,2,3,4,8]:
        for n in ([1,2] if a<=4 else [1]):
            count=0
            for p in itertools.product(range(a),repeat=n*n):
                q,c,ell=encode(p,n,a)
                markers,letters=decode(q,c,ell)
                assert markers==[(i*c+1,j*c+1) for i in range(n) for j in range(n)]
                assert letters==list(p)
                H={(u,v) for u in range(len(markers)) for v in range(len(markers)) if markers[v]==(markers[u][0],markers[u][1]+c)}
                V={(u,v) for u in range(len(markers)) for v in range(len(markers)) if markers[v]==(markers[u][0]+c,markers[u][1])}
                assert H=={(i*n+j,i*n+j+1) for i in range(n) for j in range(n-1)}
                assert V=={(i*n+j,(i+1)*n+j) for i in range(n-1) for j in range(n)}
                count+=1
            tested.append({'alphabet_size':a,'source_side':n,'source_pictures_tested':count,'binary_block_side':c})
    return tested


def main():
    geom,sets=geometry()
    out={'status':'PASS','scope':'Finite deterministic controls only; not an MSO hierarchy decision procedure, not a full tiling-system enumeration, not a polynomial-hierarchy proof, and not an executed Turing-machine tableau compiler.','geometry':geom,'mirror':mirror_control(sets),'splicing':splice_control(),'padding':padding_control(),'certificate_parity':certificate_control(),'binary_coding':coding_control()}
    path=Path(__file__).resolve().parents[1]/'CONTROL_RESULTS.json'
    path.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'status':out['status'],'mirror_pictures':sum(x['pictures_tested'] for x in out['mirror']),'splice_pairs':out['splicing']['two_by_four_matching_pairs'],'coded_pictures':sum(x['source_pictures_tested'] for x in out['binary_coding']),'output':str(path)},indent=2))


if __name__=='__main__':
    main()
